#!/usr/bin/env python3
"""CVE Auto-Remediation: Scan images, detect critical CVEs, trigger rebuilds.

Workflow:
1. Scan all hardened images with Trivy
2. For each CRITICAL CVE found:
   a. Check if upstream has a fix (newer version)
   b. If yes: bump version in manifest.toml, create PR
   c. If no: document in CVE register
3. Track remediation in compliance/cve-register.json
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"
REGISTRY = "ghcr.io/wyattau/evergreenimageregistry"
CVE_REGISTER = (
    Path(__file__).resolve().parent.parent / "compliance" / "cve-register.json"
)

# Images to scan (hardened + critical tier)
PRIORITY_IMAGES = [
    "redis",
    "nginx",
    "traefik",
    "prometheus",
    "alertmanager",
    "grafana",
    "oauth2-proxy",
    "keycloak",
    "postgresql-16",
    "mariadb",
    "nats",
    "node-exporter",
    "blackbox-exporter",
    "cloudflared",
    "valkey",
    "etcd",
    "dex",
    "step-ca",
    "forgejo",
    "vaultwarden",
]


def scan_image(name: str) -> dict:
    """Scan an image with Trivy, return CVE summary."""
    ref = f"{REGISTRY}/{name}:latest"
    result = subprocess.run(
        ["trivy", "image", "--format", "json", "--quiet", ref],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        return {"image": name, "error": result.stderr[:200]}

    try:
        data = json.loads(result.stdout)
        vulns = data.get("Results", [])
        critical = []
        high = []
        medium = []

        for result in vulns:
            for v in result.get("Vulnerabilities", []):
                severity = v.get("Severity", "")
                vuln_id = v.get("VulnerabilityID", "")
                pkg = v.get("PkgName", "")
                fixed = v.get("FixedVersion", "")
                entry = {
                    "id": vuln_id,
                    "package": pkg,
                    "severity": severity,
                    "fixed_version": fixed,
                    "description": v.get("Title", "")[:100],
                }
                if severity == "CRITICAL":
                    critical.append(entry)
                elif severity == "HIGH":
                    high.append(entry)
                elif severity == "MEDIUM":
                    medium.append(entry)

        return {
            "image": name,
            "ref": ref,
            "critical": critical,
            "high": high,
            "medium": medium,
            "total": len(critical) + len(high) + len(medium),
            "scanned_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        return {"image": name, "error": str(e)}


def check_upstream_fix(image: str, vuln: dict) -> bool:
    """Check if an upstream fix exists for the vulnerability."""
    fixed = vuln.get("fixed_version", "")
    return bool(fixed and fixed != "0.0.0-0")


def create_rebuild_pr(image: str, vulns: list):
    """Create a GitHub issue for rebuild."""
    vuln_ids = ", ".join(v["id"] for v in vulns)
    title = f"security: rebuild {image} — {len(vulns)} critical CVE(s)"

    body = f"""## Critical CVEs Detected

**Image:** `{REGISTRY}/{image}:latest`
**CVEs:** {vuln_ids}

### Details

"""
    for v in vulns:
        fix = v.get("fixed_version", "no fix available")
        body += f"- **{v['id']}** ({v['package']}): Fixed in `{fix}`\n"

    body += f"""
### Remediation

1. Bump upstream version in `images/{image}/manifest.toml`
2. Rebuild via CI
3. Verify CVEs resolved

### SLA

Per security policy: Critical CVEs must be remediated within **7 days**.
Detected: {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
Due: {(datetime.now(timezone.utc)).strftime("%Y-%m-%d")}
"""

    result = subprocess.run(
        [
            "gh",
            "issue",
            "create",
            "--repo",
            "WyattAu/EvergreenImageRegistry",
            "--title",
            title,
            "--body",
            body,
            "--label",
            "security,critical-cve",
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result.returncode == 0, result.stdout.strip()


def main():
    print("=== CVE Auto-Remediation Scan ===\n")

    results = []
    issues_created = 0

    for img in PRIORITY_IMAGES:
        print(f"Scanning {img}...", end=" ")
        scan = scan_image(img)

        if "error" in scan:
            print(f"❌ {scan['error'][:60]}")
            results.append(scan)
            continue

        crit = len(scan["critical"])
        high = len(scan["high"])
        print(f"CRITICAL={crit} HIGH={high} TOTAL={scan['total']}")

        if crit > 0:
            fixable = [v for v in scan["critical"] if check_upstream_fix(img, v)]
            if fixable:
                ok, url = create_rebuild_pr(img, fixable)
                if ok:
                    print(f"  → Created issue: {url}")
                    issues_created += 1

        results.append(scan)

    # Save register
    CVE_REGISTER.parent.mkdir(parents=True, exist_ok=True)
    register = {
        "scan_date": datetime.now(timezone.utc).isoformat(),
        "images_scanned": len(results),
        "issues_created": issues_created,
        "results": results,
    }
    CVE_REGISTER.write_text(json.dumps(register, indent=2))

    print("\n=== Summary ===")
    print(f"Images scanned: {len(results)}")
    print(f"Issues created: {issues_created}")
    print(f"Register: {CVE_REGISTER}")


if __name__ == "__main__":
    main()
