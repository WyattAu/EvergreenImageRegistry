#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC2034
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIER="all"
DEST=""
BUNDLE_DIR=""
BUNDLE_NAME=""
MANIFEST_FILE=""

TIER1_IMAGES=(
    nginx envoy traefik haproxy caddy
    coredns bind unbound
    wireguard strongswan openvpn tailscale netmaker netbird netclient
    vault keycloak zitadel headscale
    prometheus grafana loki thanos node-exporter
    postgresql redis mysql mariadb mongodb
    etcd consul
    minio restic rclone
    trivy grype cosign syft step-cli
)

TIER2_IMAGES=(
    jenkins argocd tekton drone forgejo gitea
    rabbitmq nats activemq
    memcached dragonfly cockroachdb sqlite
    victoriametrics cadvisor
    postgresql-exporter redis-exporter mysql-exporter node-exporter
)

TIER3_IMAGES=(
    python node php ruby openjdk
    gitlab mattermost synapse
    couchdb solr elasticsearch
    kafka zookeeper
)

usage() {
    cat <<'EOF'
Usage: create_bundle.sh --tier <1|2|3|all> --dest <directory>

Create an air-gap transfer bundle with OCI images, SBOMs, signatures, and checksums.

Options:
  --tier    Image tier to include: 1, 2, 3, or all (default: all)
  --dest    Destination directory for the bundle (required)
  --help    Show this help message

Bundle contents:
  - OCI image layouts (docker save format)
  - SBOMs (SPDX JSON)
  - Cosign signatures
  - CHECKSUMS (SHA256)
  - transfer-manifest.json
EOF
    exit 0
}

select_images() {
    case "$TIER" in
        1) echo "${TIER1_IMAGES[*]}" ;;
        2) echo "${TIER2_IMAGES[*]}" ;;
        3) echo "${TIER3_IMAGES[*]}" ;;
        all) echo "${TIER1_IMAGES[*]} ${TIER2_IMAGES[*]} ${TIER3_IMAGES[*]}" ;;
        *) echo "Error: invalid tier '$TIER'" >&2; exit 1 ;;
    esac
}

generate_checksums() {
    local dir="$1"
    local checksum_file="$dir/CHECKSUMS"

    echo "# SHA256 Checksums - Generated $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$checksum_file"
    echo "# Evergreen Air-Gap Bundle" >> "$checksum_file"
    echo "" >> "$checksum_file"

    find "$dir" -type f ! -name "CHECKSUMS" ! -name "transfer-manifest.json" | sort | while read -r file; do
        local relpath
        relpath="${file#"$dir"/}"
        local sha256
        sha256=$(sha256sum "$file" | awk '{print $1}')
        echo "$sha256  $relpath" >> "$checksum_file"
    done
}

verify_checksums() {
    local dir="$1"
    local checksum_file="$dir/CHECKSUMS"

    echo "Verifying checksums..."
    if (cd "$dir" && sha256sum -c CHECKSUMS --quiet 2>&1); then
        echo "  All checksums verified."
    else
        echo "  WARNING: Some checksums did not match."
    fi
}

generate_manifest() {
    local bundle_dir="$1"
    local manifest_file="$2"
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    local total_size
    total_size=$(du -sb "$bundle_dir" | awk '{print $1}')

    local image_count=0
    local sbom_count=0
    local sig_count=0

    [ -d "$bundle_dir/images" ] && image_count=$(find "$bundle_dir/images" -name "*.tar" 2>/dev/null | wc -l)
    [ -d "$bundle_dir/sboms" ] && sbom_count=$(find "$bundle_dir/sboms" -name "*.spdx.json" 2>/dev/null | wc -l)
    [ -d "$bundle_dir/signatures" ] && sig_count=$(find "$bundle_dir/signatures" -name "*.sig" 2>/dev/null | wc -l)

    cat > "$manifest_file" <<MANIFEST
{
  "schema": "evergreen-airgap-bundle-v1",
  "generated": "${timestamp}",
  "tier": "${TIER}",
  "bundle_name": "${BUNDLE_NAME}",
  "total_size_bytes": ${total_size},
  "contents": {
    "images": ${image_count},
    "sboms": ${sbom_count},
    "signatures": ${sig_count},
    "checksums": "CHECKSUMS"
  },
  "images": [
MANIFEST

    local first=true
    if [ -d "$bundle_dir/images" ]; then
        for tar_file in "$bundle_dir/images"/*.tar; do
            [ -f "$tar_file" ] || continue
            local img_name
            img_name=$(basename "$tar_file" .tar)
            local img_size
            img_size=$(stat -c%s "$tar_file" 2>/dev/null || stat -f%z "$tar_file" 2>/dev/null)
            local img_sha256
            img_sha256=$(sha256sum "$tar_file" | awk '{print $1}')

            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> "$manifest_file"
            fi

            cat >> "$manifest_file" <<IMG
    {
      "name": "${img_name}",
      "file": "images/${img_name}.tar",
      "size_bytes": ${img_size},
      "sha256": "${img_sha256}"
    }
IMG
        done
    fi

    cat >> "$manifest_file" <<MANIFEST
  ],
  "integrity": {
    "checksum_algorithm": "sha256",
    "checksum_file": "CHECKSUMS",
    "manifest_signature": null
  },
  "transfer_instructions": {
    "extract": "tar -xzf <bundle>.tar.gz",
    "load_images": "for f in images/*.tar; do docker load -i \"\$f\"; done",
    "verify_checksums": "sha256sum -c CHECKSUMS",
    "verify_signatures": "cosign verify-blob --key cosign.pub signatures/<image>.sig"
  }
}
MANIFEST
}

while [ $# -gt 0 ]; do
    case "$1" in
        --tier) TIER="$2"; shift 2 ;;
        --dest) DEST="$2"; shift 2 ;;
        --help) usage ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

if [ -z "$DEST" ]; then
    echo "Error: --dest is required" >&2
    exit 1
fi

BUNDLE_NAME="evergreen-bundle-${TIER}-$(date +%Y%m%d%H%M%S)"
BUNDLE_DIR="${DEST}/${BUNDLE_NAME}"
MANIFEST_FILE="${BUNDLE_DIR}/transfer-manifest.json"

echo "=========================================="
echo "Evergreen Air-Gap Bundle Creator"
echo "=========================================="
echo "Tier:       $TIER"
echo "Bundle:     $BUNDLE_NAME"
echo "Destination: $BUNDLE_DIR"
echo ""

mkdir -p "$BUNDLE_DIR"/{images,sboms,signatures}

echo "Selecting images for tier $TIER..."
mapfile -t IMAGE_LIST < <(select_images | tr ' ' '\n' | sort -u)
echo "  ${#IMAGE_LIST[@]} images selected"
echo ""

echo "Exporting OCI images..."
for image in "${IMAGE_LIST[@]}"; do
    echo -n "  $image ... "

    if docker image inspect "$image" >/dev/null 2>&1; then
        docker save "$image" -o "$BUNDLE_DIR/images/${image}.tar" 2>/dev/null
        echo "OK ($(du -h "$BUNDLE_DIR/images/${image}.tar" | cut -f1))"
    else
        echo "SKIP (not found locally)"
    fi
done
echo ""

echo "Generating SBOMs..."
if command -v syft >/dev/null 2>&1; then
    for image in "${IMAGE_LIST[@]}"; do
        if docker image inspect "$image" >/dev/null 2>&1; then
            echo -n "  $image ... "
            if syft "$image" -o spdx-json="$BUNDLE_DIR/sboms/${image}.spdx.json" >/dev/null 2>&1; then
                echo "OK"
            else
                echo "FAIL"
            fi
        fi
    done
else
    echo "  SKIP (syft not found - install with: curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh)"
fi
echo ""

echo "Generating cosign signatures..."
if command -v cosign >/dev/null 2>&1; then
    for image in "${IMAGE_LIST[@]}"; do
        if docker image inspect "$image" >/dev/null 2>&1; then
            echo -n "  $image ... "
            if cosign sign --yes --output-signature="$BUNDLE_DIR/signatures/${image}.sig" \
                --output-certificate="$BUNDLE_DIR/signatures/${image}.pem" \
                "$image" >/dev/null 2>&1; then
                echo "OK"
            else
                echo "FAIL (key may not be configured)"
            fi
        fi
    done
else
    echo "  SKIP (cosign not found)"
fi
echo ""

echo "Generating SHA256 checksums..."
generate_checksums "$BUNDLE_DIR"
echo ""

echo "Generating transfer manifest..."
generate_manifest "$BUNDLE_DIR" "$MANIFEST_FILE"
echo "  Manifest: $MANIFEST_FILE"
echo ""

echo "Verifying checksums..."
verify_checksums "$BUNDLE_DIR"
echo ""

echo "=========================================="
echo "Bundle Summary"
echo "=========================================="
echo "  Name:     $BUNDLE_NAME"
echo "  Location: $BUNDLE_DIR"
echo "  Tier:     $TIER"
echo "  Images:   $(find "$BUNDLE_DIR/images" -name '*.tar' 2>/dev/null | wc -l)"
echo "  SBOMs:    $(find "$BUNDLE_DIR/sboms" -name '*.spdx.json' 2>/dev/null | wc -l)"
echo "  Sigs:     $(find "$BUNDLE_DIR/signatures" -name '*.sig' 2>/dev/null | wc -l)"
echo "  Size:     $(du -sh "$BUNDLE_DIR" | cut -f1)"
echo ""
echo "To create transfer archive:"
echo "  tar -czf ${BUNDLE_NAME}.tar.gz -C '$DEST' '$BUNDLE_NAME'"
echo "=========================================="
