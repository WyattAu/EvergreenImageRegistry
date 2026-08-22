#!/usr/bin/env python3
"""
Evergreen Image Registry — CVE SLA Alerting
============================================
Monitors CVE age against defined SLA thresholds and generates alerts.

SLA Thresholds (from compliance/cve-patch-sla.md):
  Tier 1 Critical: 24h acknowledgment, 24h fix
  Tier 1 High:     8h acknowledgment, 72h fix
  Tier 2 Critical: 8h acknowledgment, 48h fix
  Tier 2 High:     24h acknowledgment, 7 days fix

Usage:
  python3 scripts/vuln_sla_alert.py --check
  python3 scripts/vuln_sla_alert.py --report /tmp/sla-report.json
  python3 scripts/vuln_sla_alert.py --slack webhook-url
  python3 scripts/vuln_sla_alert.py --prometheus /tmp/sla-metrics.prom
"""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
VEX_DIR = REPO_ROOT / "compliance" / "vex" / "documents"

# SLA thresholds in hours
SLA_THRESHOLDS = {
    "critical": {
        "critical": {"acknowledge": 4, "fix": 24},
        "high": {"acknowledge": 8, "fix": 72},
        "medium": {"acknowledge": 24, "fix": 168},
        "low": {"acknowledge": 48, "fix": 720},
    },
    "standard": {
        "critical": {"acknowledge": 8, "fix": 48},
        "high": {"acknowledge": 24, "fix": 168},
        "medium": {"acknowledge": 48, "fix": 336},
        "low": {"acknowledge": 168, "fix": 720},
    },
}


def get_image_tier(image_name: str) -> str:
    """Get tier from manifest."""
    manifest = IMAGES_DIR / image_name / "manifest.toml"
    if manifest.exists():
        content = manifest.read_text()
        match = re.search(r'tier\s*=\s*"(\w+)"', content)
        if match:
            return match.group(1)
    return "standard"


def scan_vulnerabilities(image_name: str) -> list:
    """Scan image for vulnerabilities using Trivy."""
    ref = f"ghcr.io/wyattau/evergreenimageregistry/{image_name}:latest"

    try:
        result = subprocess.run(
            ["trivy", "image", "--format", "json", "--quiet", ref],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            vulns = []
            for result_entry in data.get("Results", []):
                for v in result_entry.get("Vulnerabilities", []):
                    vulns.append(
                        {
                            "id": v.get("VulnerabilityID", ""),
                            "severity": v.get("Severity", "UNKNOWN").upper(),
                            "pkg_name": v.get("PkgName", ""),
                            "installed_version": v.get("InstalledVersion", ""),
                            "fixed_version": v.get("Fix", {}).get("Versions", []),
                            "published": v.get("PublishedDate", ""),
                            "title": v.get("Title", ""),
                        }
                    )
            return vulns
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass

    return []


def check_sla_breaches(image_name: str, tier: str) -> list:
    """Check if any CVEs breach SLA thresholds."""
    vulns = scan_vulnerabilities(image_name)
    now = datetime.now(timezone.utc)
    breaches = []

    for vuln in vulns:
        severity = vuln["severity"].lower()
        if severity not in SLA_THRESHOLDS.get(tier, {}):
            continue

        thresholds = SLA_THRESHOLDS[tier][severity]

        # Parse published date
        published_str = vuln.get("published", "")
        if not published_str:
            continue

        try:
            published = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
        except ValueError:
            continue

        age_hours = (now - published).total_seconds() / 3600

        # Check if fix is available
        has_fix = bool(vuln.get("fixed_version"))

        if has_fix:
            fix_threshold = thresholds["fix"]
            if age_hours > fix_threshold:
                breaches.append(
                    {
                        "image": image_name,
                        "tier": tier,
                        "cve": vuln["id"],
                        "severity": vuln["severity"],
                        "age_hours": round(age_hours, 1),
                        "threshold_hours": fix_threshold,
                        "breach_type": "fix_overdue",
                        "pkg": vuln["pkg_name"],
                        "installed": vuln["installed_version"],
                        "fixed": vuln["fixed_version"],
                        "title": vuln.get("title", ""),
                    }
                )
        else:
            ack_threshold = thresholds["acknowledge"]
            if age_hours > ack_threshold:
                breaches.append(
                    {
                        "image": image_name,
                        "tier": tier,
                        "cve": vuln["id"],
                        "severity": vuln["severity"],
                        "age_hours": round(age_hours, 1),
                        "threshold_hours": ack_threshold,
                        "breach_type": "no_fix_available",
                        "pkg": vuln["pkg_name"],
                        "installed": vuln["installed_version"],
                        "fixed": [],
                        "title": vuln.get("title", ""),
                    }
                )

    return breaches


def generate_slack_message(breaches: list) -> str:
    """Generate Slack-formatted alert message."""
    if not breaches:
        return "✅ No CVE SLA breaches detected."

    critical = [b for b in breaches if b["severity"] == "CRITICAL"]
    high = [b for b in breaches if b["severity"] == "HIGH"]

    msg = "🚨 *CVE SLA Breach Alert*\n"
    msg += f"Found {len(breaches)} SLA breach(es):\n"
    msg += f"  • Critical: {len(critical)}\n"
    msg += f"  • High: {len(high)}\n\n"

    for b in breaches[:10]:
        emoji = "🔴" if b["severity"] == "CRITICAL" else "🟠"
        msg += f"{emoji} *{b['cve']}* ({b['severity']})\n"
        msg += f"   Image: `{b['image']}` (Tier {b['tier']})\n"
        msg += f"   Age: {b['age_hours']}h (threshold: {b['threshold_hours']}h)\n"
        msg += f"   Package: {b['pkg']} {b['installed']}\n"
        if b["fixed"]:
            msg += f"   Fix available: {', '.join(b['fixed'])}\n"
        msg += "\n"

    if len(breaches) > 10:
        msg += f"... and {len(breaches) - 10} more breaches\n"

    return msg


def generate_prometheus(breaches: list, all_vulns: dict) -> str:
    """Generate Prometheus metrics for SLA tracking."""
    lines = []

    # Breach counts
    lines.append("# HELP eir_sla_breach_total Total SLA breaches by severity")
    lines.append("# TYPE eir_sla_breach_total gauge")
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = len([b for b in breaches if b["severity"] == severity])
        lines.append(f'eir_sla_breach_total{{severity="{severity}"}} {count}')
    lines.append("")

    # Breach by tier
    lines.append("# HELP eir_sla_breach_by_tier SLA breaches by tier")
    lines.append("# TYPE eir_sla_breach_by_tier gauge")
    for tier in ["critical", "standard"]:
        count = len([b for b in breaches if b["tier"] == tier])
        lines.append(f'eir_sla_breach_by_tier{{tier="{tier}"}} {count}')
    lines.append("")

    # Total open vulnerabilities
    lines.append("# HELP eir_vuln_open_total Total open vulnerabilities")
    lines.append("# TYPE eir_vuln_open_total gauge")
    total_vulns = sum(len(v) for v in all_vulns.values())
    lines.append(f"eir_vuln_open_total {total_vulns}")
    lines.append("")

    # Vulnerabilities by image
    lines.append("# HELP eir_vuln_by_image Vulnerabilities per image")
    lines.append("# TYPE eir_vuln_by_image gauge")
    for img, vulns in sorted(all_vulns.items()):
        lines.append(f'eir_vuln_by_image{{image="{img}"}} {len(vulns)}')
    lines.append("")

    # SLA compliance ratio
    lines.append("# HELP eir_sla_compliance_ratio Fraction of CVEs within SLA")
    lines.append("# TYPE eir_sla_compliance_ratio gauge")
    if total_vulns > 0:
        compliant = total_vulns - len(breaches)
        lines.append(f"eir_sla_compliance_ratio {compliant / total_vulns:.4f}")
    else:
        lines.append("eir_sla_compliance_ratio 1.0")
    lines.append("")

    lines.append("# HELP eir_sla_check_timestamp Timestamp of SLA check")
    lines.append("# TYPE eir_sla_check_timestamp gauge")
    lines.append(f"eir_sla_check_timestamp {datetime.utcnow().timestamp():.0f}")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CVE SLA alerting")
    parser.add_argument(
        "--check", action="store_true", help="Check all images for SLA breaches"
    )
    parser.add_argument("--image", type=str, help="Check specific image")
    parser.add_argument("--report", type=Path, help="Write JSON report")
    parser.add_argument("--slack", type=str, help="Slack webhook URL")
    parser.add_argument("--prometheus", type=Path, help="Prometheus metrics output")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually scan")
    args = parser.parse_args()

    # Find images to check
    if args.image:
        images = [args.image]
    elif args.check:
        images = []
        for manifest in sorted(IMAGES_DIR.glob("*/manifest.toml")):
            images.append(manifest.parent.name)
    else:
        print("Usage: vuln_sla_alert.py --check | --image <name>")
        sys.exit(1)

    print(f"Checking {len(images)} images for SLA breaches...")

    all_breaches = []
    all_vulns = {}

    for i, img in enumerate(images):
        tier = get_image_tier(img)
        print(f"  [{i + 1}/{len(images)}] {img} (tier={tier})... ", end="", flush=True)

        if args.dry_run:
            print("skipped (dry-run)")
            continue

        vulns = scan_vulnerabilities(img)
        all_vulns[img] = vulns

        breaches = check_sla_breaches(img, tier)
        all_breaches.extend(breaches)

        if breaches:
            print(f"⚠️ {len(breaches)} breach(es)")
        else:
            print(f"✅ ({len(vulns)} vulns, within SLA)")

    # Generate outputs
    print(f"\n{'=' * 50}")
    print("SLA Check Complete")
    print(f"  Images checked: {len(images)}")
    print(f"  Total breaches: {len(all_breaches)}")
    print(
        f"  Critical breaches: {len([b for b in all_breaches if b['severity'] == 'CRITICAL'])}"
    )
    print(f"{'=' * 50}")

    if args.report:
        report = {
            "checked_at": datetime.utcnow().isoformat() + "Z",
            "images_checked": len(images),
            "total_breaches": len(all_breaches),
            "breaches": all_breaches,
            "summary": {
                "by_severity": defaultdict(int),
                "by_tier": defaultdict(int),
            },
        }
        for b in all_breaches:
            report["summary"]["by_severity"][b["severity"]] += 1
            report["summary"]["by_tier"][b["tier"]] += 1
        report["summary"]["by_severity"] = dict(report["summary"]["by_severity"])
        report["summary"]["by_tier"] = dict(report["summary"]["by_tier"])

        args.report.write_text(json.dumps(report, indent=2))
        print(f"\nReport: {args.report}")

    if args.prometheus:
        prom = generate_prometheus(all_breaches, all_vulns)
        args.prometheus.write_text(prom)
        print(f"Prometheus: {args.prometheus}")

    if args.slack:
        msg = generate_slack_message(all_breaches)
        try:
            import urllib.request

            payload = json.dumps({"text": msg}).encode()
            req = urllib.request.Request(
                args.slack,
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            urllib.request.urlopen(req, timeout=10)
            print("\nSlack alert sent")
        except Exception as e:
            print(f"\nSlack alert failed: {e}")

    # Exit with error if critical breaches
    critical_breaches = [b for b in all_breaches if b["severity"] == "CRITICAL"]
    if critical_breaches:
        sys.exit(1)


if __name__ == "__main__":
    main()
