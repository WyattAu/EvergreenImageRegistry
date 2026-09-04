#!/usr/bin/env python3
"""
Evergreen Image Registry - Image Size Tracker

Tracks Docker image sizes and detects regressions against baselines.
Stores baselines in .reports/image_sizes/baselines.json.

Usage:
    python3 scripts/track_image_sizes.py [--check] [--update] [--threshold 20]
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASELINE_FILE = Path(".reports/image_sizes/baselines.json")
DEFAULT_THRESHOLD = 20  # Alert if size increases by > 20%


def get_image_size(image_name: str) -> dict | None:
    """Get the size of a Docker image."""
    try:
        result = subprocess.run(
            [
                "docker",
                "images",
                "--format",
                "{{.Size}}",
                f"ghcr.io/wyattau/evergreenimageregistry/{image_name}:latest",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None

        size_str = result.stdout.strip()

        # Parse size string (e.g., "12.3MB", "1.2GB", "456kB")
        size_bytes = 0
        if "GB" in size_str:
            size_bytes = int(
                float(size_str.replace("GB", "").strip()) * 1024 * 1024 * 1024
            )
        elif "MB" in size_str:
            size_bytes = int(float(size_str.replace("MB", "").strip()) * 1024 * 1024)
        elif "kB" in size_str:
            size_bytes = int(float(size_str.replace("kB", "").strip()) * 1024)
        else:
            # Assume bytes
            size_bytes = int(float(size_str.replace("B", "").strip()))

        return {
            "size_bytes": size_bytes,
            "size_human": size_str,
            "measured_at": datetime.now(timezone.utc).isoformat(),
        }
    except (subprocess.TimeoutExpired, ValueError):
        return None


def load_baselines() -> dict:
    """Load baseline sizes."""
    if BASELINE_FILE.exists():
        return json.loads(BASELINE_FILE.read_text())
    return {"version": 1, "threshold_percent": DEFAULT_THRESHOLD, "images": {}}


def save_baselines(data: dict):
    """Save baseline sizes."""
    BASELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_FILE.write_text(json.dumps(data, indent=2))


def check_regressions(threshold: int):
    """Check all images for size regressions."""
    baselines = load_baselines()
    images_dir = Path("images")
    exclude_dirs = {"_wip", "_archive", "tests"}

    image_dirs = sorted(
        [d for d in images_dir.iterdir() if d.is_dir() and d.name not in exclude_dirs]
    )

    total = len(image_dirs)
    checked = 0
    regressions = []
    new_baselines = []

    for d in image_dirs:
        if not (d / "Dockerfile").exists():
            continue

        img_name = d.name
        checked += 1

        # Get current size
        size_info = get_image_size(img_name)
        if not size_info:
            continue

        current_size = size_info["size_bytes"]

        # Check against baseline
        baseline = baselines["images"].get(img_name)
        if baseline:
            baseline_size = baseline.get("size_bytes", 0)
            if baseline_size > 0:
                change_pct = ((current_size - baseline_size) / baseline_size) * 100
                if change_pct > threshold:
                    regressions.append(
                        {
                            "image": img_name,
                            "baseline_bytes": baseline_size,
                            "current_bytes": current_size,
                            "change_pct": round(change_pct, 1),
                            "baseline_human": baseline.get("size_human", "?"),
                            "current_human": size_info["size_human"],
                        }
                    )

        # Update baseline
        baselines["images"][img_name] = size_info
        new_baselines.append(img_name)

        if checked % 50 == 0:
            print(f"  Checked {checked}/{total} images...")

    # Save updated baselines
    baselines["last_updated"] = datetime.now(timezone.utc).isoformat()
    save_baselines(baselines)

    # Report
    print(f"\nChecked {checked} images")
    print(f"Updated {len(new_baselines)} baselines")

    if regressions:
        print(
            f"\n⚠️  {len(regressions)} size regressions detected (>{threshold}% increase):"
        )
        for r in sorted(regressions, key=lambda x: x["change_pct"], reverse=True):
            print(
                f"  {r['image']}: {r['baseline_human']} → {r['current_human']} (+{r['change_pct']}%)"
            )
        return regressions
    else:
        print("\n✅ No size regressions detected")
        return []


def main():
    threshold = DEFAULT_THRESHOLD

    if "--threshold" in sys.argv:
        idx = sys.argv.index("--threshold")
        threshold = int(sys.argv[idx + 1])

    if "--check" in sys.argv or len(sys.argv) == 1:
        regressions = check_regressions(threshold)

        # Output for GitHub Actions
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write(f"regression_count={len(regressions)}\n")
                if regressions:
                    f.write(f"regressions={json.dumps(regressions)}\n")

        sys.exit(1 if regressions else 0)

    elif "--update" in sys.argv:
        print("Updating baselines only...")
        check_regressions(999)  # High threshold = no alerts, just update


if __name__ == "__main__":
    main()
