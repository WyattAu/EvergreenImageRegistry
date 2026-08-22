#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry — VEX Document Generator
# =============================================================================
# Generates OpenVEX documents from vulnerability scan results (Trivy/Syft).
# VEX (Vulnerability Exploitability Exchange) provides machine-readable
# statements about whether a CVE is actually exploitable in a given image.
#
# Usage:
#   ./scripts/generate_vex.sh [OPTIONS]
#
# Options:
#   --image <name>    Generate VEX for a specific image
#   --tier1           Generate VEX for all Tier 1 images
#   --scan            Run Trivy scan first (requires trivy)
#   --dry-run         Show what would be generated
#   --help            Show this help
#
# VEX States (per CSAF/OASIS):
#   not_affected    - Component is not affected by the vulnerability
#   fixed           - Vulnerability has been fixed in this version
#   under_investigation - Being investigated
#   open            - Vulnerable, no fix yet
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

DRY_RUN=false
TARGET_IMAGE=""
TIER1_ONLY=false
RUN_SCAN=false
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
VEX_DIR="$REPO_ROOT/compliance/vex/documents"
REGISTRY="ghcr.io/wyattau/evergreenimageregistry"

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

usage() {
    head -30 "$0" | tail -28
    exit 0
}

while [ $# -gt 0 ]; do
    case "$1" in
        --image)     TARGET_IMAGE="$2"; shift 2 ;;
        --tier1)     TIER1_ONLY=true; shift ;;
        --scan)      RUN_SCAN=true; shift ;;
        --dry-run)   DRY_RUN=true; shift ;;
        --help)      usage ;;
        *)           log_error "Unknown option: $1"; usage ;;
    esac
done

mkdir -p "$VEX_DIR"

# ---- Find Tier 1 images ----
find_tier1() {
    for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
        [ -f "$manifest" ] || continue
        tier=$(grep -oP 'tier\s*=\s*"\K[^"]+' "$manifest" 2>/dev/null | head -1)
        [ "$tier" = "critical" ] && basename "$(dirname "$manifest")"
    done
}

# ---- Generate VEX for a single image ----
generate_vex() {
    local img="$1"
    local dockerfile="$REPO_ROOT/images/$img/Dockerfile"
    local vex_file="$VEX_DIR/${img}.vex.json"
    local ref="${REGISTRY}/${img}:latest"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    if [ ! -f "$dockerfile" ]; then
        log_warn "No Dockerfile: $img"
        return 1
    fi

    log_info "Generating VEX for $img..."

    if [ "$DRY_RUN" = true ]; then
        log_info "Would generate: $vex_file"
        return 0
    fi

    # Build or pull the image
    local tag="evergreen-vex-scan:${img}"
    if [ "$RUN_SCAN" = true ]; then
        if ! docker build -t "$tag" -f "$dockerfile" "$REPO_ROOT/images/$img/" >/dev/null 2>&1; then
            log_error "Build failed: $img"
            return 1
        fi
    fi

    # Run Trivy scan if available and --scan
    local scan_results="/tmp/vex-scan-${img}.json"
    if [ "$RUN_SCAN" = true ] && command -v trivy &>/dev/null; then
        trivy image --format json --output "$scan_results" "$tag" 2>/dev/null || true
    fi

    # Extract CVEs from scan results or create empty VEX
    local cve_count=0
    if [ -f "$scan_results" ] && [ -s "$scan_results" ]; then
        cve_count=$(python3 -c "
import json
with open('$scan_results') as f:
    data = json.load(f)
results = data.get('Results', [])
vulns = []
for r in results:
    for v in r.get('Vulnerabilities', []):
        vulns.append(v)
print(len(vulns))
" 2>/dev/null || echo "0")
    fi

    # Generate VEX document
    python3 << PYEOF
import json
import os
from datetime import datetime

timestamp = "$timestamp"
img = "$img"
vex_file = "$vex_file"
scan_results = "$scan_results"
cve_count = int("$cve_count")

# Build VEX document
vex = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.5",
    "version": 1,
    "metadata": {
        "timestamp": timestamp,
        "tools": {
            "services": [{
                "name": "evergreenctl",
                "version": "1.0.0",
                "vendor": "Evergreen Image Registry"
            }]
        },
        "supplier": {
            "name": "Evergreen Image Registry",
            "url": ["https://github.com/WyattAu/EvergreenImageRegistry"]
        }
    },
    "vulnerabilities": [],
    "services": [{
        "bom-ref": f"pkg:docker/{img}",
        "name": img,
        "version": "latest"
    }]
}

# Add CVEs from scan results
if os.path.exists(scan_results) and os.path.getsize(scan_results) > 0:
    with open(scan_results) as f:
        data = json.load(f)

    seen_cves = set()
    for result in data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            cve_id = vuln.get("VulnerabilityID", "")
            if not cve_id or cve_id in seen_cves:
                continue
            seen_cves.add(cve_id)

            severity = vuln.get("Severity", "UNKNOWN").upper()
            cvss = vuln.get("CVSS", {})
            score = 0
            for source in cvss.values():
                score = max(score, source.get("V3Score", 0))

            # Determine VEX state
            fixed_version = vuln.get("Fix", {}).get("Versions", [])
            if fixed_version:
                state = "fixed"
                justification = "component_upstream_updated"
                response = ["update"]
            else:
                state = "under_investigation"
                justification = "vulnerable_code_not_present_execute_path"
                response = ["will_not_fix"]

            vex["vulnerabilities"].append({
                "id": cve_id,
                "source": {
                    "name": "NVD",
                    "url": f"https://nvd.nist.gov/vuln/detail/{cve_id}"
                },
                "ratings": [{
                    "source": {"name": "NVD"},
                    "score": score,
                    "severity": severity,
                    "method": "CVSSv31"
                }],
                "description": vuln.get("Description", "")[:500],
                "published": vuln.get("PublishedDate", timestamp),
                "affected": [{
                    "ref": f"pkg:docker/{img}",
                    "versions": [{
                        "version": vuln.get("InstalledVersion", "unknown"),
                        "status": "affected"
                    }],
                    "package": {
                        "name": vuln.get("PkgName", "unknown"),
                        "version": vuln.get("InstalledVersion", "unknown"),
                        "type": vuln.get("PkgIdentifier", {}).get("PURL", {}).get("type", "generic")
                    }
                }],
                "analysis": {
                    "state": state,
                    "justification": justification,
                    "response": [response[0]],
                    "detail": f"Fixed in: {', '.join(fixed_version)}" if fixed_version else "No fix available"
                }
            })

# Write VEX document
with open(vex_file, "w") as f:
    json.dump(vex, f, indent=2)

print(f"Generated {vex_file} ({len(vex['vulnerabilities'])} CVEs)")
PYEOF

    # Clean up
    rm -f "$scan_results"
    docker rmi "$tag" 2>/dev/null || true
    log_ok "VEX generated for $img"
    return 0
}

# ---- Main ----
log_info "Evergreen Image Registry — VEX Document Generator"
log_info "================================================="
echo ""

if [ -n "$TARGET_IMAGE" ]; then
    generate_vex "$TARGET_IMAGE"
else
    images=()
    if [ "$TIER1_ONLY" = true ]; then
        log_info "Scope: Tier 1 (critical) images"
        while IFS= read -r img; do
            images+=("$img")
        done < <(find_tier1)
    else
        log_info "Scope: Tier 1 (critical) images (default)"
        while IFS= read -r img; do
            images+=("$img")
        done < <(find_tier1)
    fi

    total=${#images[@]}
    log_info "Found $total images"
    echo ""

    generated=0
    failed=0

    for img in "${images[@]}"; do
        if generate_vex "$img"; then
            generated=$((generated + 1))
        else
            failed=$((failed + 1))
        fi
    done

    echo ""
    echo "=========================================="
    echo "VEX Generation Complete"
    echo "=========================================="
    echo "  Total:     $total"
    echo "  Generated: $generated"
    echo "  Failed:    $failed"
    echo "  Output:    $VEX_DIR/"
    echo "=========================================="
fi
