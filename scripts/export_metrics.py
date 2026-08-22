#!/usr/bin/env python3
"""
Evergreen Image Registry — Prometheus Metrics Exporter
=====================================================
Exports compliance, SBOM, and validation metrics in Prometheus format.
Can run as a one-shot script or as a long-running HTTP server.

Usage:
  One-shot (write to file):
    python3 scripts/export_metrics.py --output /tmp/metrics.prom

  HTTP server (scrape endpoint):
    python3 scripts/export_metrics.py --serve --port 9120

  With custom images dir:
    python3 scripts/export_metrics.py --images-dir images/ --output /tmp/metrics.prom
"""

import argparse
import json
import re
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
VEX_DIR = REPO_ROOT / "compliance" / "vex" / "documents"
SCRIPTS_DIR = REPO_ROOT / "scripts"


def collect_metrics(images_dir: Path) -> str:
    """Collect all metrics and return Prometheus exposition format."""
    lines = []
    now = time.time()

    # --- Image count by tier ---
    tier_counts = {"critical": 0, "standard": 0}
    total_images = 0
    for manifest in images_dir.glob("*/manifest.toml"):
        try:
            content = manifest.read_text()
            tier_match = re.search(r'tier\s*=\s*"(\w+)"', content)
            tier = tier_match.group(1) if tier_match else "unknown"
            if tier in tier_counts:
                tier_counts[tier] += 1
            total_images += 1
        except Exception:
            continue

    lines.append("# HELP eir_images_total Total number of images in the registry")
    lines.append("# TYPE eir_images_total gauge")
    lines.append(f"eir_images_total {total_images}")
    lines.append("")

    for tier, count in tier_counts.items():
        lines.append(f'eir_images_by_tier{{tier="{tier}"}} {count}')

    lines.append("")

    # --- SBOM coverage ---
    sbom_total = 0
    sbom_fresh = 0
    sbom_sizes = []
    for sbom_file in images_dir.glob("*/sbom.spdx.json"):
        sbom_total += 1
        size = sbom_file.stat().st_size
        sbom_sizes.append(size)
        if size > 1000:
            sbom_fresh += 1

    lines.append("# HELP eir_sboms_total Total SBOM files")
    lines.append("# TYPE eir_sboms_total gauge")
    lines.append(f"eir_sboms_total {sbom_total}")
    lines.append("")

    lines.append("# HELP eir_sboms_with_packages SBOMs containing actual package data")
    lines.append("# TYPE eir_sboms_with_packages gauge")
    lines.append(f"eir_sboms_with_packages {sbom_fresh}")
    lines.append("")

    lines.append("# HELP eir_sbom_coverage_ratio Ratio of images with valid SBOMs")
    lines.append("# TYPE eir_sbom_coverage_ratio gauge")
    coverage = sbom_fresh / total_images if total_images > 0 else 0
    lines.append(f"eir_sbom_coverage_ratio {coverage:.4f}")
    lines.append("")

    if sbom_sizes:
        avg_size = sum(sbom_sizes) / len(sbom_sizes)
        lines.append("# HELP eir_sbom_size_bytes Average SBOM file size")
        lines.append("# TYPE eir_sbom_size_bytes gauge")
        lines.append(f"eir_sbom_size_bytes {avg_size:.0f}")
        lines.append("")

    # --- VEX documents ---
    vex_count = 0
    vex_cves_total = 0
    vex_states = {"fixed": 0, "not_affected": 0, "under_investigation": 0, "open": 0}
    if VEX_DIR.exists():
        for vex_file in VEX_DIR.glob("*.vex.json"):
            vex_count += 1
            try:
                data = json.loads(vex_file.read_text())
                vulns = data.get("vulnerabilities", [])
                vex_cves_total += len(vulns)
                for v in vulns:
                    state = v.get("analysis", {}).get("state", "unknown")
                    if state in vex_states:
                        vex_states[state] += 1
            except Exception:
                continue

    lines.append("# HELP eir_vex_documents_total Total VEX documents")
    lines.append("# TYPE eir_vex_documents_total gauge")
    lines.append(f"eir_vex_documents_total {vex_count}")
    lines.append("")

    lines.append("# HELP eir_vex_cves_total Total CVEs tracked in VEX documents")
    lines.append("# TYPE eir_vex_cves_total gauge")
    lines.append(f"eir_vex_cves_total {vex_cves_total}")
    lines.append("")

    for state, count in vex_states.items():
        if count > 0:
            lines.append(f'eir_vex_cves_by_state{{state="{state}"}} {count}')

    if vex_states:
        lines.append("")

    # --- Constraint violations (from validation baseline) ---
    baseline_file = Path("/tmp/validation_baseline.json")
    if baseline_file.exists():
        try:
            data = json.loads(baseline_file.read_text())
            total_violations = data.get("total_violations", 0)
            images_passed = data.get("images_passed", 0)
            images_failed = data.get("images_failed", 0)
            sev = data.get("violations_by_severity", {})
            by_code = data.get("violations_by_code", {})

            lines.append(
                "# HELP eir_validation_images_passed Images passing all BLOCK constraints"
            )
            lines.append("# TYPE eir_validation_images_passed gauge")
            lines.append(f"eir_validation_images_passed {images_passed}")
            lines.append("")

            lines.append(
                "# HELP eir_validation_images_failed Images with BLOCK violations"
            )
            lines.append("# TYPE eir_validation_images_failed gauge")
            lines.append(f"eir_validation_images_failed {images_failed}")
            lines.append("")

            lines.append(
                "# HELP eir_validation_pass_rate Fraction of images passing validation"
            )
            lines.append("# TYPE eir_validation_pass_rate gauge")
            total = images_passed + images_failed
            rate = images_passed / total if total > 0 else 0
            lines.append(f"eir_validation_pass_rate {rate:.4f}")
            lines.append("")

            lines.append(
                "# HELP eir_validation_violations_total Total constraint violations"
            )
            lines.append("# TYPE eir_validation_violations_total gauge")
            lines.append(f"eir_validation_violations_total {total_violations}")
            lines.append("")

            for severity, count in sev.items():
                lines.append(
                    f'eir_validation_violations_by_severity{{severity="{severity}"}} {count}'
                )

            lines.append("")

            for code, count in by_code.items():
                lines.append(
                    f'eir_validation_violations_by_constraint{{constraint="{code}"}} {count}'
                )

            lines.append("")

            # Pass rate metric
            lines.append(
                "# HELP eir_validation_block_violations BLOCK-severity violations (CI-blocking)"
            )
            lines.append("# TYPE eir_validation_block_violations gauge")
            lines.append(f"eir_validation_block_violations {sev.get('BLOCK', 0)}")
            lines.append("")

            lines.append(
                "# HELP eir_validation_warn_violations WARN-severity violations (non-blocking)"
            )
            lines.append("# TYPE eir_validation_warn_violations gauge")
            lines.append(f"eir_validation_warn_violations {sev.get('WARN', 0)}")
            lines.append("")

        except Exception as e:
            lines.append(f"# WARNING: Failed to load validation baseline: {e}")
            lines.append("")

    # --- Workflow count ---
    workflows_dir = REPO_ROOT / ".github" / "workflows"
    workflow_count = (
        len(list(workflows_dir.glob("*.yml"))) if workflows_dir.exists() else 0
    )
    lines.append("# HELP eir_workflows_total Total CI/CD workflows")
    lines.append("# TYPE eir_workflows_total gauge")
    lines.append(f"eir_workflows_total {workflow_count}")
    lines.append("")

    # --- Dockerfile compliance indicators ---
    dockerfiles_with_healthcheck = 0
    dockerfiles_with_user = 0
    dockerfiles_with_entrypoint = 0
    dockerfiles_with_labels = 0
    dockerfiles_with_stopsignal = 0

    for df in images_dir.glob("*/Dockerfile"):
        try:
            content = df.read_text()
            if "HEALTHCHECK" in content:
                dockerfiles_with_healthcheck += 1
            if re.search(r"^\s*USER\s+", content, re.MULTILINE):
                dockerfiles_with_user += 1
            if "ENTRYPOINT" in content:
                dockerfiles_with_entrypoint += 1
            if "org.opencontainers.image" in content:
                dockerfiles_with_labels += 1
            if "STOPSIGNAL" in content:
                dockerfiles_with_stopsignal += 1
        except Exception:
            continue

    total_dfs = len(list(images_dir.glob("*/Dockerfile"))) or 1

    lines.append("# HELP eir_dockerfiles_healthcheck Dockerfiles with HEALTHCHECK")
    lines.append("# TYPE eir_dockerfiles_healthcheck gauge")
    lines.append(f"eir_dockerfiles_healthcheck {dockerfiles_with_healthcheck}")
    lines.append("")

    lines.append("# HELP eir_dockerfiles_nonroot Dockerfiles with USER directive")
    lines.append("# TYPE eir_dockerfiles_nonroot gauge")
    lines.append(f"eir_dockerfiles_nonroot {dockerfiles_with_user}")
    lines.append("")

    lines.append("# HELP eir_dockerfiles_entrypoint Dockerfiles with ENTRYPOINT")
    lines.append("# TYPE eir_dockerfiles_entrypoint gauge")
    lines.append(f"eir_dockerfiles_entrypoint {dockerfiles_with_entrypoint}")
    lines.append("")

    lines.append("# HELP eir_dockerfiles_oci_labels Dockerfiles with OCI labels")
    lines.append("# TYPE eir_dockerfiles_oci_labels gauge")
    lines.append(f"eir_dockerfiles_oci_labels {dockerfiles_with_labels}")
    lines.append("")

    # --- CIS compliance ratio ---
    lines.append("# HELP eir_cis_healthcheck_ratio Fraction of images with HEALTHCHECK")
    lines.append("# TYPE eir_cis_healthcheck_ratio gauge")
    lines.append(
        f"eir_cis_healthcheck_ratio {dockerfiles_with_healthcheck / total_dfs:.4f}"
    )
    lines.append("")

    lines.append("# HELP eir_cis_nonroot_ratio Fraction of images with USER directive")
    lines.append("# TYPE eir_cis_nonroot_ratio gauge")
    lines.append(f"eir_cis_nonroot_ratio {dockerfiles_with_user / total_dfs:.4f}")
    lines.append("")

    # --- Scrape timestamp ---
    lines.append("# HELP eir_metrics_scrape_timestamp Timestamp of metrics collection")
    lines.append("# TYPE eir_metrics_scrape_timestamp gauge")
    lines.append(f"eir_metrics_scrape_timestamp {now:.0f}")
    lines.append("")

    return "\n".join(lines)


class MetricsHandler(BaseHTTPRequestHandler):
    """HTTP handler for Prometheus /metrics endpoint."""

    def do_GET(self):
        if self.path == "/metrics":
            metrics = collect_metrics(IMAGES_DIR)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
            self.end_headers()
            self.wfile.write(metrics.encode())
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress default logging


def main():
    global IMAGES_DIR
    parser = argparse.ArgumentParser(description="Export EIR compliance metrics")
    parser.add_argument(
        "--images-dir", type=Path, default=IMAGES_DIR, help="Images directory"
    )
    parser.add_argument(
        "--output", type=Path, help="Write metrics to file (one-shot mode)"
    )
    parser.add_argument("--serve", action="store_true", help="Run as HTTP server")
    parser.add_argument("--port", type=int, default=9120, help="Port for HTTP server")
    args = parser.parse_args()

    IMAGES_DIR = args.images_dir

    if args.serve:
        server = HTTPServer(("0.0.0.0", args.port), MetricsHandler)
        print(f"Metrics server listening on :{args.port}/metrics")
        server.serve_forever()
    else:
        metrics = collect_metrics(IMAGES_DIR)
        if args.output:
            args.output.write_text(metrics)
            print(f"Metrics written to {args.output}")
        else:
            print(metrics)


if __name__ == "__main__":
    main()
