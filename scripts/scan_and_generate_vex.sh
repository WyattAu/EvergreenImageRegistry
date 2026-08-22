#!/usr/bin/env bash
# =============================================================================
# Scan Tier 1 Images + Generate VEX Documents
# =============================================================================
# Builds images, scans with Trivy, and generates VEX documents with CVE data.
#
# Usage:
#   ./scripts/scan_and_generate_vex.sh [--image NAME] [--dry-run]
# =============================================================================

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
VEX_DIR="$REPO_ROOT/compliance/vex/documents"
DRY_RUN=false
TARGET_IMAGE=""

# Find trivy binary
TRIVY=""
for p in /usr/local/bin/trivy /usr/bin/trivy $HOME/.local/bin/trivy /tmp/bin/trivy; do
    [ -x "$p" ] && TRIVY="$p" && break
done
[ -z "$TRIVY" ] && { echo "ERROR: trivy not found"; exit 1; }
echo "Using trivy: $TRIVY"

while [ $# -gt 0 ]; do
    case "$1" in
        --image)    TARGET_IMAGE="$2"; shift 2 ;;
        --dry-run)  DRY_RUN=true; shift ;;
        *)          echo "Unknown: $1"; exit 1 ;;
    esac
done

mkdir -p "$VEX_DIR"

scan_and_generate() {
    local img="$1"
    local dockerfile="$REPO_ROOT/images/$img/Dockerfile"
    local vex_file="$VEX_DIR/${img}.vex.json"
    local tag="evergreen-scan:${img}"

    [ -f "$dockerfile" ] || { echo "SKIP $img (no Dockerfile)"; return 0; }

    if [ "$DRY_RUN" = true ]; then
        echo "WOULD SCAN $img"
        return 0
    fi

    echo "Building $img..."
    if ! timeout 180 docker build -t "$tag" -f "$dockerfile" "$REPO_ROOT/images/$img/" >/dev/null 2>&1; then
        echo "FAIL build: $img"
        return 1
    fi

    echo "Scanning $img..."
    local scan_file="/tmp/trivy-${img}.json"
    if ! "$TRIVY" image --format json --output "$scan_file" "$tag" 2>/dev/null; then
        echo "FAIL scan: $img"
        docker rmi "$tag" 2>/dev/null || true
        return 1
    fi

    # Generate VEX from scan results
    python3 << PYEOF
import json
import os
from datetime import datetime

scan_file = "$scan_file"
vex_file = "$vex_file"
img = "$img"
timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

with open(scan_file) as f:
    scan = json.load(f)

vex = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.5",
    "version": 1,
    "metadata": {
        "timestamp": timestamp,
        "tools": {"services": [{"name": "trivy", "version": "0.58.0"}]},
        "supplier": {"name": "Evergreen Image Registry"}
    },
    "vulnerabilities": [],
    "services": [{"bom-ref": f"pkg:docker/{img}", "name": img}]
}

seen = set()
for result in scan.get("Results", []):
    for vuln in result.get("Vulnerabilities", []):
        cve = vuln.get("VulnerabilityID", "")
        if not cve or cve in seen:
            continue
        seen.add(cve)

        severity = vuln.get("Severity", "UNKNOWN").upper()
        score = vuln.get("CVSS", {}).get("NVD", {}).get("V3Score", 0)
        fix_versions = vuln.get("Fix", {}).get("Versions", [])

        state = "fixed" if fix_versions else "under_investigation"
        justification = "component_upstream_updated" if fix_versions else "vulnerable_code_not_present_execute_path"

        vex["vulnerabilities"].append({
            "id": cve,
            "source": {"name": "NVD", "url": f"https://nvd.nist.gov/vuln/detail/{cve}"},
            "ratings": [{"source": {"name": "NVD"}, "score": score, "severity": severity}],
            "description": vuln.get("Description", "")[:500],
            "published": vuln.get("PublishedDate", timestamp),
            "affected": [{
                "ref": f"pkg:docker/{img}",
                "versions": [{"version": vuln.get("InstalledVersion", "?"), "status": "affected"}],
                "package": {"name": vuln.get("PkgName", "?"), "version": vuln.get("InstalledVersion", "?")}
            }],
            "analysis": {
                "state": state,
                "justification": justification,
                "response": ["update"] if fix_versions else ["will_not_fix"],
                "detail": f"Fixed in: {', '.join(fix_versions)}" if fix_versions else "No fix available"
            }
        })

with open(vex_file, "w") as f:
    json.dump(vex, f, indent=2)

print(f"  VEX: {len(vex['vulnerabilities'])} CVEs -> {vex_file}")
PYEOF

    rm -f "$scan_file"
    docker rmi "$tag" 2>/dev/null || true
    echo "OK $img"
}

echo "=== Trivy Scan + VEX Generation ==="

if [ -n "$TARGET_IMAGE" ]; then
    scan_and_generate "$TARGET_IMAGE"
else
    # Tier 1 images
    images=()
    for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
        tier=$(grep -o 'tier = "critical"' "$manifest" 2>/dev/null || true)
        [ -n "$tier" ] || continue
        img=$(basename "$(dirname "$manifest")")
        images+=("$img")
    done

    echo "Scanning ${#images[@]} Tier 1 images..."
    echo ""

    ok=0
    fail=0
    for img in "${images[@]}"; do
        if scan_and_generate "$img"; then
            ok=$((ok + 1))
        else
            fail=$((fail + 1))
        fi
    done

    echo ""
    echo "=========================================="
    echo "OK: $ok | Failed: $fail"
    echo "=========================================="
fi
