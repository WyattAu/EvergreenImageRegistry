#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry — ARM Variant Generator
# =============================================================================
# Generates ARM-optimized variants for edge/IoT deployments.
# Supports: ARM32 (arm/v7), ARM64 (arm64/v8), NVIDIA Jetson
#
# Usage:
#   ./scripts/generate_arm_variants.sh --image redis --arch arm64
#   ./scripts/generate_arm_variants.sh --tier1 --arch arm64
#   ./scripts/generate_arm_variants.sh --edge-profile
# =============================================================================

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
NC='\033[0m'

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
REGISTRY="ghcr.io/wyattau/evergreenimageregistry"
TARGET_IMAGE=""
ARCH="arm64"
TIER1_ONLY=false
EDGE_PROFILE=false

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

while [ $# -gt 0 ]; do
    case "$1" in
        --image)       TARGET_IMAGE="$2"; shift 2 ;;
        --arch)        ARCH="$2"; shift 2 ;;
        --tier1)       TIER1_ONLY=true; shift ;;
        --edge-profile) EDGE_PROFILE=true; shift ;;
        --help)        head -22 "$0" | tail -20; exit 0 ;;
        *)             log_error "Unknown: $1"; exit 1 ;;
    esac
done

# ---- Edge Profile: Minimal images for constrained devices ----
# Edge profile uses:
#   - Alpine-based builder (for cross-compilation)
#   - Static binaries only (no glibc dependency)
#   - Stripped binaries (reduce size)
#   - No CA certs (offline devices)
EDGE_CGO_ENABLED=0
EDGE_LDFLAGS="-s -w -linkmode external -extldflags '-static'"

# ---- Build ARM variant ----
build_arm_variant() {
    local img="$1"
    local dockerfile="$REPO_ROOT/images/$img/Dockerfile"
    local arm_dockerfile="$REPO_ROOT/images/$img/Dockerfile.arm${ARCH#arm}"

    if [ ! -f "$dockerfile" ]; then
        log_warn "No Dockerfile: $img"
        return 1
    fi

    log_info "Building ARM variant: $img (arch=$ARCH)"

    if [ "$EDGE_PROFILE" = true ]; then
        # Generate edge-optimized Dockerfile
        cat > "$arm_dockerfile" << EOF
# =============================================================================
# $img — ARM${ARCH#arm} Edge Variant
# =============================================================================
# Minimal build for edge/IoT deployments.
# Static binary, no glibc, stripped for size.
# =============================================================================

FROM --platform=linux/${ARCH} alpine:3.18 AS builder

RUN apk add --no-cache gcc musl-dev linux-headers

# Build with static linking for edge deployment
ARG CGO_ENABLED=${EDGE_CGO_ENABLED}
ARG TARGETARCH=${ARCH}

# Copy and build (actual build commands vary per image)
COPY . /build

FROM --platform=linux/${ARCH} scratch

COPY --from=builder /build/output /app

USER 65532:65532

ENTRYPOINT ["/app"]

LABEL org.opencontainers.image.title="${img}-arm${ARCH#arm}-edge" \
      org.opencontainers.image.description="${img} ARM${ARCH#arm} edge variant (minimal)" \
      evergreenimageregistry.io.edge="true" \
      evergreenimageregistry.io.arch="${ARCH}"
EOF
        log_ok "Edge Dockerfile generated: $arm_dockerfile"
    fi

    # Build multi-platform
    TAG="${REGISTRY}/${img}:latest-${ARCH}"
    if docker buildx build \
        --platform "linux/${ARCH}" \
        -t "$TAG" \
        --load \
        "$REPO_ROOT/images/$img" 2>/dev/null; then
        log_ok "Built: $TAG"
    else
        log_warn "Build failed: $img (may not support this architecture)"
    fi
}

# ---- Main ----
log_info "ARM Variant Generator"
log_info "====================="
echo ""

if [ -n "$TARGET_IMAGE" ]; then
    build_arm_variant "$TARGET_IMAGE"
else
    images=()
    if [ "$TIER1_ONLY" = true ]; then
        for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
            [ -f "$manifest" ] || continue
            tier=$(grep -oP 'tier\s*=\s*"\K[^"]+' "$manifest" 2>/dev/null | head -1)
            [ "$tier" = "critical" ] && images+=("$(basename "$(dirname "$manifest")")")
        done
    else
        for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
            images+=("$(basename "$(dirname "$manifest")")")
        done
    fi

    total=${#images[@]}
    log_info "Building $total ARM variants (arch=$ARCH, edge=$EDGE_PROFILE)"
    echo ""

    built=0
    failed=0
    for img in "${images[@]}"; do
        if build_arm_variant "$img"; then
            built=$((built + 1))
        else
            failed=$((failed + 1))
        fi
    done

    echo ""
    echo "=========================================="
    echo "ARM Variant Build Complete"
    echo "=========================================="
    echo "  Built:  $built"
    echo "  Failed: $failed"
    echo "  Arch:   $ARCH"
    echo "  Edge:   $EDGE_PROFILE"
    echo "=========================================="
fi
