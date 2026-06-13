#!/usr/bin/env bash
# Drift Detection Monitor for EvergreenImageRegistry
# Checks upstream versions and creates GitHub issues on drift detection
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
GITHUB_REPO="${GITHUB_REPO:-WyattAu/EvergreenImageRegistry}"
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"
DRIFT_REPORT=""

log() { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
warn() { log "${YELLOW}WARN${NC}: $*"; }
err() { log "${RED}ERROR${NC}: $*"; }
ok() { log "${GREEN}OK${NC}: $*"; }

check_image_drift() {
    local image="$1"
    local dockerfile="$REPO_ROOT/images/$image/Dockerfile"
    [ ! -f "$dockerfile" ] && return 0

    local upstream_version=""
    local local_version=""

    # Extract version from Dockerfile ARG
    local_version=$(grep -oP 'ARG VERSION=\K.*' "$dockerfile" 2>/dev/null | head -1 || echo "")

    # Check upstream GitHub releases
    local source_url=$(grep -oP 'github\.com/[^/]+/[^/]+(?=/)' "$dockerfile" 2>/dev/null | head -1 || echo "")
    if [ -n "$source_url" ]; then
        upstream_version=$(gh api "repos/$source_url/releases/latest" --jq '.tag_name' 2>/dev/null || echo "")
    fi

    if [ -n "$local_version" ] && [ -n "$upstream_version" ] && [ "$local_version" != "$upstream_version" ]; then
        warn "$image: local=$local_version, upstream=$upstream_version"
        DRIFT_REPORT="${DRIFT_REPORT}**${image}**: ${local_version} → ${upstream_version}\n"
        return 1
    fi
    ok "$image: up to date (${local_version:-unknown})"
    return 0
}

create_github_issue() {
    local title="$1"
    local body="$2"
    gh issue create \
        --repo "$GITHUB_REPO" \
        --title "$title" \
        --body "$body" \
        --label "drift,automated" 2>/dev/null || warn "Failed to create GitHub issue"
}

send_notification() {
    local message="$1"
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -s -X POST "$SLACK_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"text\": \"$message\"}" >/dev/null 2>&1 || true
    fi
    if [ -n "$DISCORD_WEBHOOK" ]; then
        curl -s -X POST "$DISCORD_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"content\": \"$message\"}" >/dev/null 2>&1 || true
    fi
}

main() {
    log "Starting drift detection for $GITHUB_REPO"

    local drift_count=0
    local total=0

    for dockerfile in "$REPO_ROOT"/images/*/Dockerfile; do
        local image=$(basename $(dirname "$dockerfile"))
        [[ "$image" == _* ]] && continue
        [ "$image" = "tests" ] || [ "$image" = "health-shim" ] && continue
        total=$((total + 1))
        check_image_drift "$image" || drift_count=$((drift_count + 1))
    done

    log "Checked $total images, found $drift_count with drift"

    if [ $drift_count -gt 0 ]; then
        local issue_body="## Drift Detection Report\n\n$(date -u '+%Y-%m-%d %H:%M:%S UTC')\n\n$drift_count image(s) have upstream version changes:\n\n${DRIFT_REPORT}\n\n### Action Required\n- Review upstream changes\n- Update Dockerfile ARG VERSION\n- Rebuild and test\n- Update SBOM"
        create_github_issue "Drift detected: $drift_count images need updating" "$issue_body"
        send_notification "⚠️ EIR Drift: $drift_count images have upstream updates available"
        exit 1
    else
        ok "All images up to date"
        exit 0
    fi
}

main "$@"
