#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry — SBOM Attestation Signer
# =============================================================================
# Upgrades SBOMs from file-only to signed attestation using:
# - in-toto attestation format (supply chain provenance)
# - cosign sign-blob for cryptographic signing
#
# This bridges the gap with Chainguard/Wolfi's supply chain model.
#
# Usage:
#   ./scripts/generate_sbom_attestation.sh [OPTIONS]
#
# Options:
#   --image <name>    Attest a specific image
#   --tier1           Attest all Tier 1 images only
#   --sign            Sign attestation with cosign key
#   --dry-run         Show what would be generated
#   --help            Show this help
#
# Prerequisites:
#   - cosign (for signing)
#   - syft (for SBOM generation)
#   - python3 (for in-toto format)
# =============================================================================

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
NC='\033[0m'

DRY_RUN=false
TARGET_IMAGE=""
TIER1_ONLY=false
SIGN=false
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
REGISTRY="ghcr.io/wyattau/evergreenimageregistry"
ATTEST_DIR="$REPO_ROOT/compliance/vex/attestations"

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

while [ $# -gt 0 ]; do
    case "$1" in
        --image)   TARGET_IMAGE="$2"; shift 2 ;;
        --tier1)   TIER1_ONLY=true; shift ;;
        --sign)    SIGN=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        --help)    head -25 "$0" | tail -23; exit 0 ;;
        *)         log_error "Unknown: $1"; exit 1 ;;
    esac
done

mkdir -p "$ATTEST_DIR"

# ---- Generate in-toto attestation from SBOM ----
generate_attestation() {
    local img="$1"
    local sbom_path="$REPO_ROOT/images/$img/sbom.spdx.json"
    local attestation_path="$ATTEST_DIR/${img}.attestation.json"
    local ref="${REGISTRY}/${img}:latest"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    if [ ! -f "$sbom_path" ]; then
        log_warn "No SBOM: $img — generating first..."
        if ! syft scan "$ref" -o spdx-json > "$sbom_path" 2>/dev/null; then
            log_error "Cannot generate SBOM: $img"
            return 1
        fi
    fi

    if [ "$DRY_RUN" = true ]; then
        log_info "Would attest: $img"
        return 0
    fi

    # Generate in-toto attestation bundle
    python3 << PYEOF
import json
import hashlib
import subprocess
import os

sbom_path = "$sbom_path"
attestation_path = "$attestation_path"
img = "$img"
ref = "$ref"
timestamp = "$timestamp"

# Read SBOM and compute hash
with open(sbom_path, "rb") as f:
    sbom_content = f.read()
sbom_hash = hashlib.sha256(sbom_content).hexdigest()

# Get image digest if available
image_digest = "unknown"
try:
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{index .RepoDigests 0}}", ref],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        image_digest = result.stdout.strip().split("@")[-1]
except Exception:
    pass

# Build in-toto link
link = {
    "_type": "https://in-toto.io/Link/v0.9",
    "meta": {
        "sbom": {
            "hashes": {"sha256": sbom_hash},
            "length": len(sbom_content),
            "name": f"images/{img}/sbom.spdx.json",
            "uri": f"https://github.com/WyattAu/EvergreenImageRegistry/blob/main/images/{img}/sbom.spdx.json"
        }
    },
    "name": f"sbom-generation-{img}",
    "byProducts": {
        "sbom_format": "SPDX 2.3",
        "sbom_tool": "Syft",
        "sbom_packages": json.loads(sbom_content).get("packages", [])
    },
    "byproducts": {
        "image_reference": ref,
        "image_digest": image_digest,
        "generated_at": timestamp
    },
    "command": ["syft", "scan", ref, "-o", "spdx-json"],
    "environment": {
        "registry": "$REGISTRY",
        "image": img
    }
}

# Build attestation bundle
attestation = {
    "_type": "https://in-toto.io/attestation/v1.0",
    "statementType": "https://in-toto.io/Statement/v0.1",
    "subject": [{
        "name": ref,
        "digest": {"sha256": image_digest} if image_digest != "unknown" else {}
    }],
    "predicateType": "https://in-toto.io/attestation/sbom/v0.1",
    "predicate": {
        "generator": {
            "uri": "https://github.com/WyattAu/EvergreenImageRegistry",
            "version": "1.0.0"
        },
        "sbom": {
            "format": "SPDX 2.3",
            "hash": sbom_hash,
            "location": f"images/{img}/sbom.spdx.json",
            "packages": len(json.loads(sbom_content).get("packages", []))
        },
        "timestamp": timestamp,
        "link": link
    }
}

with open(attestation_path, "w") as f:
    json.dump(attestation, f, indent=2)

print(f"Generated attestation: {attestation_path}")
PYEOF

    log_ok "Attestation generated: $img"

    # Sign with cosign if requested
    if [ "$SIGN" = true ] && command -v cosign &>/dev/null; then
        log_info "Signing attestation for $img..."
        if cosign sign-blob --yes \
            --output-signature "$ATTEST_DIR/${img}.attestation.sig" \
            "$attestation_path" 2>/dev/null; then
            log_ok "Signed: $img"
        else
            log_warn "Cosign signing failed: $img (non-fatal)"
        fi
    fi

    return 0
}

# ---- Main ----
log_info "SBOM Attestation Generator (in-toto + cosign)"
log_info "==============================================="
echo ""

if [ -n "$TARGET_IMAGE" ]; then
    generate_attestation "$TARGET_IMAGE"
else
    # Find images with SBOMs
    images=()
    for sbom in "$REPO_ROOT"/images/*/sbom.spdx.json; do
        [ -f "$sbom" ] || continue
        local_img=$(basename "$(dirname "$sbom")")
        if [ "$TIER1_ONLY" = true ]; then
            tier=$(grep -oP 'tier\s*=\s*"\K[^"]+' "$REPO_ROOT/images/$local_img/manifest.toml" 2>/dev/null | head -1)
            [ "$tier" = "critical" ] && images+=("$local_img")
        else
            images+=("$local_img")
        fi
    done

    total=${#images[@]}
    log_info "Found $total images with SBOMs to attest"
    echo ""

    generated=0
    failed=0

    for img in "${images[@]}"; do
        if generate_attestation "$img"; then
            generated=$((generated + 1))
        else
            failed=$((failed + 1))
        fi
    done

    echo ""
    echo "=========================================="
    echo "Attestation Generation Complete"
    echo "=========================================="
    echo "  Total:     $total"
    echo "  Generated: $generated"
    echo "  Failed:    $failed"
    echo "  Output:    $ATTEST_DIR/"
    echo "=========================================="
fi
