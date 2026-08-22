#!/usr/bin/env python3
"""
Evergreen Image Registry — Performance Baseline Builder
======================================================
Builds all images and records:
  - Build time (ms)
  - Image size (compressed MB)
  - Layer count
  - Package count
  - Startup time (if testable)

Produces baseline database for performance regression detection.

Usage:
  python3 scripts/build_performance_baselines.py --all
  python3 scripts/build_performance_baselines.py --image redis
  python3 scripts/build_performance_baselines.py --report /tmp/baselines.json
  python3 scripts/build_performance_baselines.py --prometheus /tmp/perf-baselines.prom
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
BASELINE_FILE = REPO_ROOT / ".specs" / "06_5_regression" / "build_times.json"
THRESHOLD_PERCENT = 50  # Alert if build time increases by >50%


def build_image(image_name: str, timeout: int = 300) -> dict:
    """Build an image and measure performance metrics."""
    dockerfile = IMAGES_DIR / image_name / "Dockerfile"
    if not dockerfile.exists():
        return {"error": "no_dockerfile"}

    tag = f"evergreen-perf-test:{image_name}"
    context = str(IMAGES_DIR / image_name)

    # Build and time
    start = time.monotonic()
    try:
        result = subprocess.run(
            ["docker", "build", "-t", tag, "-f", str(dockerfile), context],
            capture_output=True, text=True, timeout=timeout
        )
        build_success = result.returncode == 0
    except subprocess.TimeoutExpired:
        build_success = False
    build_time_ms = int((time.monotonic() - start) * 1000)

    if not build_success:
        return {"error": "build_failed", "build_time_ms": build_time_ms}

    # Get image size
    try:
        inspect = subprocess.run(
            ["docker", "inspect", "--format", "{{.Size}}", tag],
            capture_output=True, text=True, timeout=30
        )
        size_bytes = int(inspect.stdout.strip()) if inspect.returncode == 0 else 0
        size_mb = size_bytes / (1024 * 1024)
    except Exception:
        size_mb = 0

    # Get layer count
    try:
        inspect = subprocess.run(
            ["docker", "inspect", "--format", "{{len .RootFS.Layers}}", tag],
            capture_output=True, text=True, timeout=30
        )
        layers = int(inspect.stdout.strip()) if inspect.returncode == 0 else 0
    except Exception:
        layers = 0

    # Get package count from SBOM
    sbom_path = IMAGES_DIR / image_name / "sbom.spdx.json"
    packages = 0
    if sbom_path.exists():
        try:
            with open(sbom_path) as f:
                data = json.load(f)
            packages = len(data.get("packages", []))
        except Exception:
            pass

    # Clean up
    subprocess.run(["docker", "rmi", tag], capture_output=True, timeout=30)

    return {
        "build_time_ms": build_time_ms,
        "size_mb": round(size_mb, 2),
        "layers": layers,
        "packages": packages,
        "success": True,
    }


def load_baselines() -> dict:
    """Load existing baselines."""
    if BASELINE_FILE.exists():
        try:
            with open(BASELINE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"version": 1, "threshold_percent": THRESHOLD_PERCENT, "images": {}}


def save_baselines(data: dict):
    """Save baselines to file."""
    BASELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Performance baseline builder")
    parser.add_argument("--all", action="store_true", help="Build all images")
    parser.add_argument("--image", type=str, help="Build specific image")
    parser.add_argument("--tier1", action="store_true", help="Build Tier 1 images only")
    parser.add_argument("--timeout", type=int, default=300, help="Build timeout per image")
    parser.add_argument("--report", type=Path, help="Write JSON report")
    parser.add_argument("--prometheus", type=Path, help="Write Prometheus metrics")
    parser.add_argument("--compare", action="store_true", help="Compare against baselines")
    args = parser.parse_args()

    baselines = load_baselines()

    # Find images to build
    images = []
    if args.image:
        images = [args.image]
    elif args.all or args.tier1:
        for manifest in sorted(IMAGES_DIR.glob("*/manifest.toml")):
            img = manifest.parent.name
            if args.tier1:
                content = manifest.read_text()
                import re
                tier = re.search(r'tier\s*=\s*"(\w+)"', content)
                if tier and tier.group(1) == "critical":
                    images.append(img)
            else:
                images.append(img)
    else:
        print("Usage: --all | --tier1 | --image <name>")
        sys.exit(1)

    print(f"Building {len(images)} images for performance baselines...")

    results = {}
    regressions = []

    for i, img in enumerate(images):
        print(f"  [{i+1}/{len(images)}] {img}... ", end="", flush=True)

        metrics = build_image(img, args.timeout)

        if "error" in metrics:
            print(f"ERROR: {metrics['error']}")
            results[img] = {
                "error": metrics["error"],
                "updated": datetime.utcnow().isoformat() + "Z",
            }
            continue

        # Check for regression
        old_baseline = baselines.get("images", {}).get(img, {})
        old_time = old_baseline.get("build_time_ms", 0)

        if old_time > 0 and args.compare:
            increase = ((metrics["build_time_ms"] - old_time) * 100) // old_time
            if increase > THRESHOLD_PERCENT:
                regressions.append({
                    "image": img,
                    "old_ms": old_time,
                    "new_ms": metrics["build_time_ms"],
                    "increase_percent": increase,
                })
                print(f"REGRESSION +{increase}%")
            else:
                print(f"OK ({metrics['build_time_ms']}ms, {metrics['size_mb']}MB)")
        else:
            print(f"OK ({metrics['build_time_ms']}ms, {metrics['size_mb']}MB)")

        # Update baselines
        baselines.setdefault("images", {})[img] = {
            "build_time_ms": metrics["build_time_ms"],
            "size_mb": metrics["size_mb"],
            "layers": metrics["layers"],
            "packages": metrics["packages"],
            "updated": datetime.utcnow().isoformat() + "Z",
        }
        results[img] = baselines["images"][img]

    # Save baselines
    baselines["last_updated"] = datetime.utcnow().isoformat() + "Z"
    baselines["total_images"] = len(baselines.get("images", {}))
    save_baselines(baselines)

    # Summary
    print(f"\n{'='*50}")
    print("Performance Baselines Updated")
    print(f"  Total: {len(images)}")
    print(f"  Success: {len([r for r in results.values() if 'error' not in r])}")
    print(f"  Regressions: {len(regressions)}")
    print(f"  Output: {BASELINE_FILE}")
    print(f"{'='*50}")

    if regressions:
        print("\nRegressions detected:")
        for r in regressions:
            print(f"  {r['image']}: {r['old_ms']}ms → {r['new_ms']}ms (+{r['increase_percent']}%)")

    # Prometheus metrics
    if args.prometheus:
        lines = []
        lines.append("# HELP eir_perf_build_time_ms Build time per image")
        lines.append("# TYPE eir_perf_build_time_ms gauge")
        for img, data in results.items():
            if "build_time_ms" in data:
                lines.append(f'eir_perf_build_time_ms{{image="{img}"}} {data["build_time_ms"]}')
        lines.append("")

        lines.append("# HELP eir_perf_size_mb Image size in MB")
        lines.append("# TYPE eir_perf_size_mb gauge")
        for img, data in results.items():
            if "size_mb" in data:
                lines.append(f'eir_perf_size_mb{{image="{img}"}} {data["size_mb"]}')
        lines.append("")

        lines.append("# HELP eir_perf_regressions_total Regressions detected")
        lines.append("# TYPE eir_perf_regressions_total gauge")
        lines.append(f"eir_perf_regressions_total {len(regressions)}")
        lines.append("")

        args.prometheus.parent.mkdir(parents=True, exist_ok=True)
        args.prometheus.write_text("\n".join(lines))
        print(f"Prometheus: {args.prometheus}")

    # JSON report
    if args.report:
        report = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "baselines": results,
            "regressions": regressions,
            "threshold_percent": THRESHOLD_PERCENT,
        }
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2))
        print(f"Report: {args.report}")


if __name__ == "__main__":
    main()
