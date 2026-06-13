#!/usr/bin/env bash
# =============================================================================
# DRIFT DETECTION - EIR IMAGES vs UPSTREAM
# =============================================================================
# For each critical EIR image, pulls the latest GHCR image, extracts the
# binary hash, compares it against the version pinned in the Dockerfile,
# and detects if the upstream source has changed.
#
# Usage:
#   ./scripts/drift-detect.sh [--image NAME] [--report PATH]
#
# Detects:
#   1. Binary version drift (Dockerfile ARG vs pulled image)
#   2. Base image digest drift (pinned digest vs latest)
#   3. Shim version drift
#   4. Source URL changes
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGES_DIR="${REPO_ROOT}/images"
REPORT_DIR="${REPORT_DIR:-${REPO_ROOT}/.reports}"
TIMESTAMP=$(date -u '+%Y%m%dT%H%M%SZ')
REPORT_FILE="${REPORT_DIR}/drift-detect-${TIMESTAMP}.md"
REGISTRY="ghcr.io/wyattau/evergreenimageregistry"
SINGLE_IMAGE=""

# Critical images to check for drift
CRITICAL_IMAGES=(traefik postgres redis-7 grafana keycloak forgejo cloudflared)

# --- State ---
DRIFT_COUNT=0
CLEAN_COUNT=0
ERROR_COUNT=0
RESULTS=()

# --- Helpers ---
log()  { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" >&2; }
pass() { ((CLEAN_COUNT++)); RESULTS+=("CLEAN|$1|$2"); log "CLEAN $1: $2"; }
drift() { ((DRIFT_COUNT++)); RESULTS+=("DRIFT|$1|$2"); log "DRIFT $1: $2"; }
err() { ((ERROR_COUNT++)); RESULTS+=("ERROR|$1|$2"); log "ERROR $1: $2"; }

# Extract a Dockerfile ARG value
extract_arg() {
    local dockerfile="$1" arg_name="$2"
    grep -E "^ARG\s+${arg_name}=" "${dockerfile}" 2>/dev/null | head -1 | sed "s/^ARG\s*${arg_name}=//" | tr -d '[:space:]'
}

# Extract a LABEL value
extract_label() {
    local dockerfile="$1" label_key="$2"
    grep -E "${label_key}=" "${dockerfile}" 2>/dev/null | head -1 | sed "s/.*${label_key}=//" | sed 's/\s*\\$//' | tr -d '"[:space:]'
}

# Extract base image FROM line (final stage)
extract_base_image() {
    local dockerfile="$1"
    # Get the last FROM line (final stage)
    grep -E '^FROM\s+' "${dockerfile}" | tail -1 | awk '{print $2}'
}

# Extract pinned digest from FROM line
extract_digest() {
    local dockerfile="$1"
    grep -E '^FROM\s+.*@sha256:' "${dockerfile}" | tail -1 | grep -oP '@sha256:[a-f0-9]+' | head -1
}

# Get the binary version from a running container or image
get_image_version() {
    local image="$1" service="$2"
    local version=""

    case "${service}" in
        traefik)
            version=$(docker run --rm --entrypoint="" "${image}" /traefik version 2>/dev/null | grep -oP 'v[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
            ;;
        postgres)
            version=$(docker run --rm --entrypoint="" "${image}" postgres --version 2>/dev/null | grep -oP '[0-9]+\.[0-9]+' | head -1 || true)
            ;;
        redis-7)
            version=$(docker run --rm --entrypoint="" "${image}" redis-server --version 2>/dev/null | grep -oP 'v=[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
            ;;
        grafana)
            version=$(docker run --rm --entrypoint="" "${image}" /grafana-bin/grafana-server --version 2>/dev/null | grep -oP '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
            ;;
        keycloak)
            version=$(docker run --rm --entrypoint="" "${image}" /opt/keycloak/bin/kc.sh --version 2>/dev/null | grep -oP '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
            ;;
        forgejo)
            version=$(docker run --rm --entrypoint="" "${image}" forgejo --version 2>/dev/null | grep -oP '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
            ;;
        cloudflared)
            version=$(docker run --rm --entrypoint="" "${image}" /cloudflared --version 2>/dev/null | grep -oP '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
            ;;
    esac
    echo "${version}"
}

# Get image digest from GHCR
get_ghcr_digest() {
    local image="$1"
    docker manifest inspect "${image}" 2>/dev/null | grep -oP '"digest":\s*"sha256:[a-f0-9]+"' | head -1 | grep -oP 'sha256:[a-f0-9]+' || true
}

# --- Drift Checks ---
check_version_drift() {
    local service="$1" dockerfile="$2" image="$3"
    local df_version
    df_version=$(extract_arg "${dockerfile}" "VERSION")

    if [[ -z "${df_version}" ]]; then
        err "${service}" "no VERSION ARG in Dockerfile"
        return
    fi

    local img_version
    img_version=$(get_image_version "${image}" "${service}")

    if [[ -z "${img_version}" ]]; then
        err "${service}" "could not extract version from image"
        return
    fi

    # Strip leading v for comparison
    local df_clean="${df_version#v}"
    local img_clean="${img_version#v}"

    if [[ "${df_clean}" == "${img_clean}" ]]; then
        pass "${service}" "binary version matches (${df_version})"
    else
        drift "${service}" "binary version drift: Dockerfile=${df_version} image=${img_version}"
    fi
}

check_base_image_drift() {
    local service="$1" dockerfile="$2"
    local base_image
    base_image=$(extract_base_image "${dockerfile}")
    local digest
    digest=$(extract_digest "${dockerfile}")

    if [[ -n "${digest}" ]]; then
        # Check if the pinned digest is still the latest
        local base_without_digest="${base_image%%@*}"
        local latest_digest
        latest_digest=$(docker manifest inspect "${base_without_digest}" 2>/dev/null | grep -oP '"digest":\s*"sha256:[a-f0-9]+"' | head -1 | grep -oP 'sha256:[a-f0-9]+' || true)

        if [[ -z "${latest_digest}" ]]; then
            err "${service}" "could not fetch latest digest for ${base_without_digest}"
            return
        fi

        local pinned_short="${digest#sha256:}"
        local latest_short="${latest_digest#sha256:}"

        if [[ "${pinned_short:0:16}" == "${latest_short:0:16}" ]]; then
            pass "${service}" "base image digest current (${digest:0:20}...)"
        else
            drift "${service}" "base image digest drift: pinned=${digest:0:20}... latest=${latest_digest:0:20}..."
        fi
    else
        pass "${service}" "base image unpinned (${base_image})"
    fi
}

check_shim_drift() {
    local service="$1" dockerfile="$2"
    local shim_version
    shim_version=$(extract_arg "${dockerfile}" "SHIM_VERSION")

    if [[ -z "${shim_version}" ]]; then
        pass "${service}" "no shim version (not using health-shim)"
        return
    fi

    # Check if the shim image tag exists
    local shim_image="ghcr.io/wyattau/evergreenshim/health-shim:${shim_version}"
    if docker manifest inspect "${shim_image}" >/dev/null 2>&1; then
        pass "${service}" "shim version ${shim_version} exists"
    else
        drift "${service}" "shim version ${shim_version} not found in registry"
    fi
}

check_source_drift() {
    local service="$1" dockerfile="$2"
    local source_url
    source_url=$(extract_label "${dockerfile}" "org.opencontainers.image.source")

    if [[ -z "${source_url}" ]]; then
        warn "${service}" "no source URL in labels"
        return
    fi

    # Check if the source repo is accessible
    local http_code
    http_code=$(curl -sf -o /dev/null -w '%{http_code}' "${source_url}" 2>/dev/null || echo "000")
    if [[ "${http_code}" == "200" ]]; then
        pass "${service}" "source URL accessible (${source_url})"
    else
        drift "${service}" "source URL returned HTTP ${http_code}: ${source_url}"
    fi
}

# --- Report ---
generate_report() {
    mkdir -p "${REPORT_DIR}"
    {
        echo "# Drift Detection Report"
        echo ""
        echo "- **Generated**: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
        echo "- **Registry**: ${REGISTRY}"
        echo "- **Images checked**: $((CLEAN_COUNT + DRIFT_COUNT + ERROR_COUNT))"
        echo "- **Clean**: ${CLEAN_COUNT} | **Drift**: ${DRIFT_COUNT} | **Error**: ${ERROR_COUNT}"
        echo ""
        echo "## Results"
        echo ""
        echo "| Status | Service | Detail |"
        echo "|--------|---------|--------|"
        for r in "${RESULTS[@]}"; do
            IFS='|' read -r status service detail <<< "${r}"
            echo "| ${status} | ${service} | ${detail} |"
        done
        echo ""
        if (( DRIFT_COUNT > 0 )); then
            echo "## Drift Summary"
            echo ""
            for r in "${RESULTS[@]}"; do
                IFS='|' read -r status service detail <<< "${r}"
                if [[ "${status}" == "DRIFT" ]]; then
                    echo "- **${service}**: ${detail}"
                fi
            done
            echo ""
            echo "### Recommended Actions"
            echo ""
            echo "1. Review upstream changelogs for affected images"
            echo "2. Update Dockerfile VERSION ARGs where appropriate"
            echo "3. Run \`evergreenctl drift images/<name>/\` for detailed comparison"
            echo "4. Rebuild and push updated images"
        fi
        echo ""
        echo "---"
        echo "*Report generated by scripts/drift-detect.sh*"
    } > "${REPORT_FILE}"
    log "Report written to ${REPORT_FILE}"
}

# --- Main ---
main() {
    log "=== EIR Drift Detection ==="
    log ""

    local images_to_check=("${CRITICAL_IMAGES[@]}")
    if [[ -n "${SINGLE_IMAGE}" ]]; then
        images_to_check=("${SINGLE_IMAGE}")
    fi

    for service in "${images_to_check[@]}"; do
        local dockerfile="${IMAGES_DIR}/${service}/Dockerfile"
        if [[ ! -f "${dockerfile}" ]]; then
            err "${service}" "Dockerfile not found at ${dockerfile}"
            continue
        fi

        log "--- ${service} ---"

        local image="${REGISTRY}/${service}:latest"

        check_version_drift "${service}" "${dockerfile}" "${image}"
        check_base_image_drift "${service}" "${dockerfile}"
        check_shim_drift "${service}" "${dockerfile}"
        check_source_drift "${service}" "${dockerfile}"

        log ""
    done

    log "========================================"
    log "  SUMMARY: Clean=${CLEAN_COUNT} Drift=${DRIFT_COUNT} Error=${ERROR_COUNT}"
    log "========================================"

    generate_report

    if (( DRIFT_COUNT > 0 )); then
        exit 1
    fi
}

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --image)
            SINGLE_IMAGE="$2"
            shift 2
            ;;
        --report)
            REPORT_FILE="$2"
            shift 2
            ;;
        *)
            log "Unknown option: $1"
            exit 1
            ;;
    esac
done

main "$@"
