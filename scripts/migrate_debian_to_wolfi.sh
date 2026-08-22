#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry - Debian-slim to Wolfi Migration Tool
# =============================================================================
# Migrates images from debian-slim to wolfi-base per ADR-007.
#
# Usage:
#   ./scripts/migrate_debian_to_wolfi.sh [OPTIONS]
#
# Options:
#   --scan              Scan and report only (no changes)
#   --image <name>      Migrate a specific image
#   --all               Migrate all eligible images
#   --dry-run           Show what would change without writing
#   --tier <1|2|3>      Filter by tier
#   --output-dir <dir>  Save migration plan to directory
#   --help              Show this help
#
# Migration Strategy:
#   1. Replace FROM debian:bookworm-slim with FROM cgr.dev/chainguard/wolfi-base
#   2. Replace 'apt-get update && apt-get install -y' with 'apk add'
#   3. Remove apt cleanup commands (rm -rf /var/lib/apt/lists/*)
#   4. Update package names (apt → apk equivalents)
#   5. Preserve USER, HEALTHCHECK, EXPOSE, ENTRYPOINT, CMD, ARG, LABEL
#   6. Keep multi-stage builder stages (they use debian legitimately)
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

MODE="scan"
TARGET_IMAGE=""
TIERS=""
DRY_RUN=false
OUTPUT_DIR=""
REPO_ROOT="$(git rev-parse --show-root 2>/dev/null || pwd)"

# ---- Package name mapping (apt → apk) ----
declare -A PKG_MAP=(
    # Core utilities
    [curl]="curl"
    [wget]="wget"
    [git]="git"
    [ca-certificates]="ca-certificates-bundle"
    [openssl]="libssl3 openssl"
    [ca-certificates]="ca-certificates-bundle"
    [gnupg]="gnupg gpg"
    [gpg]="gnupg gpg"
    [dirmngr]="gnupg gpg"
    [software-properties-common]=""

    # Build essentials
    [build-essential]="build-base"
    [gcc]="gcc"
    [g++]="g++"
    [make]="make"
    [cmake]="cmake"
    [autoconf]="autoconf"
    [automake]="automake"
    [libtool]="libtool"
    [pkg-config]="pkgconf"
    [libc6-dev]="libc-dev"
    [libssl-dev]="openssl-dev"
    [libffi-dev]="libffi-dev"
    [zlib1g-dev]="zlib-dev"
    [libcurl4-openssl-dev]="curl-dev"
    [libxml2-dev]="libxml2-dev"
    [libxslt1-dev]="libxslt-dev"
    [libpq-dev]="libpq-dev"
    [libsqlite3-dev]="sqlite-dev"
    [libreadline-dev]="readline-dev"
    [libncurses5-dev]="ncurses-dev"
    [liblzma-dev]="xz-dev"

    # Languages
    [python3]="python3 py3-pip"
    [python3-pip]="py3-pip"
    [python3-dev]="python3-dev"
    [python3-venv]="python3"
    [nodejs]="nodejs npm"
    [npm]="npm"
    [openjdk-17-jdk-headless]="openjdk-17"
    [openjdk-17-jre-headless]="openjdk-17-jre"
    [openjdk-21-jdk-headless]="openjdk-21"
    [openjdk-21-jre-headless]="openjdk-21-jre"

    # Runtime libraries
    [libgomp1]="libgomp"
    [libgomp-dev]="libgomp-dev"
    [libstdc++6]="libstdc++"
    [libgcc-s1]="gcc-libs"

    # Networking
    [iputils-ping]="iputils"
    [net-tools]="net-tools"
    [bind9-host]="bind-tools"
    [dnsutils]="bind-tools"
    [traceroute]="traceroute"
    [tcpdump]="tcpdump"
    [nmap]="nmap"
    [ socat]="socat"

    # System
    [procps]="procps"
    [syslog-ng]="syslog-ng"
    [logrotate]="logrotate"
    [cron]="busybox"
    [rsync]="rsync"
    [jq]="jq"
    [unzip]="unzip"
    [zip]="zip"
    [bzip2]="bzip2"
    [xz-utils]="xz"
    [tar]="tar"
    [gzip]="gzip"

    # Database clients
    [postgresql-client]="postgresql16-client"
    [mysql-client]="mariadb-client"
    [redis-tools]="redis"

    # Misc
    [locales]="glibc-locale"
    [fontconfig]="fontconfig"
    [libfontconfig1]="fontconfig"
    [tini]="tini"
)

usage() {
    head -30 "$0" | tail -28
    exit 0
}

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ---- Parse arguments ----
while [ $# -gt 0 ]; do
    case "$1" in
        --scan)       MODE="scan"; shift ;;
        --image)      MODE="single"; TARGET_IMAGE="$2"; shift 2 ;;
        --all)        MODE="all"; shift ;;
        --dry-run)    DRY_RUN=true; shift ;;
        --tier)       TIERS="$2"; shift 2 ;;
        --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
        --help)       usage ;;
        *)            log_error "Unknown option: $1"; usage ;;
    esac
done

# ---- Scan all images for debian-slim usage ----
scan_debian_images() {
    local count=0
    local eligible=0
    local results=()

    log_info "Scanning images for debian-slim usage..."
    echo ""

    for img_dir in images/*/; do
        [ -f "${img_dir}/Dockerfile" ] || continue
        local img_name
        img_name=$(basename "$img_dir")
        local df="${img_dir}/Dockerfile"

        # Check if final stage uses debian-slim
        local last_from_line
        last_from_line=$(grep -n '^FROM ' "$df" | tail -1 | cut -d: -f1)
        [ -z "$last_from_line" ] && continue

        local final_stage
        final_stage=$(tail -n +"$last_from_line" "$df")

        if echo "$final_stage" | head -1 | grep -qiP 'debian:(bookworm|bullseye|buster|stretch)-slim|debian:latest'; then
            count=$((count + 1))

            # Check tier
            local tier=""
            if [ -f "${img_dir}/manifest.toml" ]; then
                tier=$(grep -oP 'tier\s*=\s*\K[0-9]+' "${img_dir}/manifest.toml" 2>/dev/null || echo "3")
            else
                tier="3"
            fi

            # Filter by tier if specified
            if [ -n "$TIERS" ] && [[ ! ",$TIERS," =~ ",$tier," ]]; then
                continue
            fi

            # Check if eligible for migration (no complex C deps)
            local is_eligible=true
            local reason=""
            local complexity="low"

            # High complexity: C/C++ compilation, kernel modules, etc.
            if echo "$final_stage" | grep -qP '(apt-get install|apt install).*\b(gcc|g\+\+|build-essential|linux-headers|kernel|dpkg-dev)\b'; then
                is_eligible=false
                reason="requires C compilation toolchain"
                complexity="high"
            fi

            # Medium complexity: many packages, custom repos
            local pkg_count
            pkg_count=$(echo "$final_stage" | grep -cP '(apt-get install|apt install)' || true)
            if [ "$pkg_count" -gt 3 ]; then
                complexity="high"
                reason="${reason:+$reason; }many apt-get install steps ($pkg_count)"
            fi

            # Check for custom apt repos
            if echo "$final_stage" | grep -qP '(add-apt-repository|apt-key|sources\.list)'; then
                complexity="high"
                reason="${reason:+$reason; }custom apt repositories"
            fi

            # Check for debian-specific paths
            if echo "$final_stage" | grep -qP '/etc/(debian|dpkg|apt)'; then
                complexity="medium"
                reason="${reason:+$reason; }debian-specific paths"
            fi

            if [ "$is_eligible" = true ]; then
                eligible=$((eligible + 1))
            fi

            results+=("${img_name}|${tier}|${complexity}|${is_eligible}|${reason}")
        fi
    done

    # Print results
    echo "=========================================="
    echo "DEBIAN-SLIM MIGRATION SCAN RESULTS"
    echo "=========================================="
    echo ""
    printf "%-30s %-6s %-10s %-10s %s\n" "IMAGE" "TIER" "COMPLEXITY" "ELIGIBLE" "REASON"
    printf "%-30s %-6s %-10s %-10s %s\n" "-----" "----" "----------" "--------" "------"

    for result in "${results[@]}"; do
        IFS='|' read -r name tier complexity is_elig reason <<< "$result"
        local elig_icon
        if [ "$is_elig" = "true" ]; then
            elig_icon="${GREEN}YES${NC}"
        else
            elig_icon="${RED}NO${NC}"
        fi
        printf "%-30s %-6s %-10s " "$name" "$tier" "$complexity"
        echo -e "$elig_icon    ${reason:-—}"
    done

    echo ""
    echo "=========================================="
    echo "TOTAL: $count images with debian-slim"
    echo "ELIGIBLE: ${eligible} images for migration"
    echo "BLOCKED: $((count - eligible)) images (complex C deps, custom repos)"
    echo "=========================================="

    # Save plan if output dir specified
    if [ -n "$OUTPUT_DIR" ]; then
        mkdir -p "$OUTPUT_DIR"
        local plan_file="${OUTPUT_DIR}/migration-plan.md"
        {
            echo "# Debian-slim → Wolfi Migration Plan"
            echo ""
            echo "**Generated:** $(date -u +%Y-%m-%dT%H:%M:%SZ)"
            echo "**Total debian-slim images:** $count"
            echo "**Eligible for migration:** $eligible"
            echo ""
            echo "## Migration Priority"
            echo ""
            echo "| Priority | Tier | Complexity | Rationale |"
            echo "|----------|------|------------|-----------|"
            echo "| P0 | 1 | low | Critical infra, easy migration |"
            echo "| P1 | 1 | medium | Critical infra, moderate effort |"
            echo "| P2 | 2 | low | Standard, easy migration |"
            echo "| P3 | 2-3 | medium | Standard/Community, moderate effort |"
            echo "| P4 | 3 | low | Community, easy migration |"
            echo ""
            echo "## Image Details"
            echo ""
            for result in "${results[@]}"; do
                IFS='|' read -r name tier complexity is_elig reason <<< "$result"
                if [ "$is_elig" = "true" ]; then
                    echo "### ${name}"
                    echo "- **Tier:** ${tier}"
                    echo "- **Complexity:** ${complexity}"
                    echo "- **Changes:** Replace FROM + apt-get → apk"
                    echo ""
                fi
            done
        } > "$plan_file"
        log_ok "Migration plan saved to: $plan_file"
    fi
}

# ---- Translate a single Dockerfile ----
translate_dockerfile() {
    local df="$1"
    local output="$2"
    local img_name
    img_name=$(basename "$(dirname "$df")")

    cp "$df" "$output"

    # Find the last FROM line number (final stage start)
    local last_from_num
    last_from_num=$(grep -n '^FROM ' "$output" | tail -1 | cut -d: -f1)
    if [ -z "$last_from_num" ]; then
        return 0
    fi

    # 1. Replace debian-slim in final stage FROM (only the last FROM line)
    local last_from_line
    last_from_line=$(sed -n "${last_from_num}p" "$output")
    local new_from
    new_from=$(echo "$last_from_line" | sed 's/FROM debian:[a-z0-9.-]*/FROM cgr.dev\/chainguard\/wolfi-base/')
    sed -i "${last_from_num}s|.*|${new_from}|" "$output"

    # 2. Only transform the final stage (lines from last_from_num onward)
    #    Extract final stage, apply transforms, reassemble
    local total_lines
    total_lines=$(wc -l < "$output")
    local builder_lines=$((last_from_num - 1))

    if [ "$builder_lines" -gt 0 ]; then
        # Split: builder stages (untouched) + final stage (transformed)
        local builder_file
        builder_file=$(mktemp)
        local final_file
        final_file=$(mktemp)

        head -n "$builder_lines" "$output" > "$builder_file"
        tail -n +"$last_from_num" "$output" > "$final_file"

        # Apply transforms to final stage only
        sed -i 's|apt-get update && apt-get install -y --no-install-recommends|apk add --no-cache|g' "$final_file"
        sed -i 's|apt-get update && apt-get install -y|apk add --no-cache|g' "$final_file"
        sed -i 's|apt install -y --no-install-recommends|apk add --no-cache|g' "$final_file"
        sed -i 's|apt-get install -y --no-install-recommends|apk add --no-cache|g' "$final_file"
        sed -i 's|apt install -y|apk add --no-cache|g' "$final_file"
        sed -i 's|apt-get install -y|apk add --no-cache|g' "$final_file"

        # Remove apt cleanup in final stage
        sed -i '/rm -rf \/var\/lib\/apt\/lists\//d' "$final_file"
        sed -i '/rm -rf \/var\/cache\/apt/d' "$final_file"
        sed -i '/apt-get clean/d' "$final_file"
        sed -i '/^apt-get update$/d' "$final_file"

        # Translate package names in final stage
        for apt_pkg in "${!PKG_MAP[@]}"; do
            local apk_pkg="${PKG_MAP[$apt_pkg]}"
            [ -z "$apk_pkg" ] && continue
            sed -i "s|\b${apt_pkg}\b|${apk_pkg}|g" "$final_file"
        done

        # Reassemble
        cat "$builder_file" "$final_file" > "$output"
        rm -f "$builder_file" "$final_file"
    else
        # No builder stages — transform the entire file
        sed -i 's|apt-get update && apt-get install -y --no-install-recommends|apk add --no-cache|g' "$output"
        sed -i 's|apt-get update && apt-get install -y|apk add --no-cache|g' "$output"
        sed -i 's|apt install -y --no-install-recommends|apk add --no-cache|g' "$output"
        sed -i 's|apt-get install -y --no-install-recommends|apk add --no-cache|g' "$output"
        sed -i 's|apt install -y|apk add --no-cache|g' "$output"
        sed -i 's|apt-get install -y|apk add --no-cache|g' "$output"
        sed -i '/rm -rf \/var\/lib\/apt\/lists\//d' "$output"
        sed -i '/rm -rf \/var\/cache\/apt/d' "$output"
        sed -i '/apt-get clean/d' "$output"
        sed -i '/^apt-get update$/d' "$output"
        for apt_pkg in "${!PKG_MAP[@]}"; do
            local apk_pkg="${PKG_MAP[$apt_pkg]}"
            [ -z "$apk_pkg" ] && continue
            sed -i "s|\b${apt_pkg}\b|${apk_pkg}|g" "$output"
        done
    fi

    # 3. Add OCI labels if missing
    if ! grep -q 'org.opencontainers.image' "$output"; then
        local last_line
        last_line=$(wc -l < "$output")
        sed -i "${last_line}a\\
LABEL org.opencontainers.image.source=\"https://github.com/WyattAu/EvergreenImageRegistry\"\\
LABEL org.opencontainers.image.description=\"Migrated from debian-slim to wolfi-base per ADR-007\"" "$output"
    fi

    # 7. Add fallback reason label
    local last_line
    last_line=$(wc -l < "$output")
    sed -i "${last_line}a\\
LABEL evergreen.base.image=\"wolfi-base\"\\
LABEL evergreen.base.fallback_reason=\"Migrated from debian-slim per ADR-007\"" "$output"
}

# ---- Migrate a single image ----
migrate_image() {
    local img_name="$1"
    local img_dir="images/${img_name}"
    local df="${img_dir}/Dockerfile"

    if [ ! -f "$df" ]; then
        log_error "No Dockerfile found for ${img_name}"
        return 1
    fi

    log_info "Migrating ${img_name}..."

    # Create backup
    local backup="${df}.debian-backup"
    if [ ! -f "$backup" ]; then
        cp "$df" "$backup"
        log_info "Backup created: ${backup}"
    fi

    if [ "$DRY_RUN" = true ]; then
        local tmp_df
        tmp_df=$(mktemp)
        translate_dockerfile "$df" "$tmp_df"
        log_info "Dry run diff for ${img_name}:"
        diff -u "$df" "$tmp_df" || true
        rm -f "$tmp_df"
    else
        local tmp_df
        tmp_df=$(mktemp)
        translate_dockerfile "$df" "$tmp_df"
        mv "$tmp_df" "$df"
        log_ok "Migrated ${img_name} from debian-slim to wolfi-base"
    fi
}

# ---- Main ----
case "$MODE" in
    scan)
        scan_debian_images
        ;;
    single)
        if [ -z "$TARGET_IMAGE" ]; then
            log_error "Must specify --image <name>"
            exit 1
        fi
        migrate_image "$TARGET_IMAGE"
        ;;
    all)
        log_info "Migrating all eligible debian-slim images..."
        migrated=0
        failed=0
        for img_dir in images/*/; do
            [ -f "${img_dir}/Dockerfile" ] || continue
            img_name=$(basename "$img_dir")
            df="${img_dir}/Dockerfile"

            # Check if final stage uses debian
            last_from_line=$(grep -n '^FROM ' "$df" | tail -1 | cut -d: -f1)
            [ -z "$last_from_line" ] && continue

            if tail -n +"$last_from_line" "$df" | head -1 | grep -qiP 'debian:(bookworm|bullseye|buster|stretch)-slim|debian:latest'; then
                if migrate_image "$img_name" 2>/dev/null; then
                    migrated=$((migrated + 1))
                else
                    failed=$((failed + 1))
                    log_error "Failed to migrate ${img_name}"
                fi
            fi
        done
        echo ""
        log_ok "Migration complete: ${migrated} migrated, ${failed} failed"
        ;;
esac
