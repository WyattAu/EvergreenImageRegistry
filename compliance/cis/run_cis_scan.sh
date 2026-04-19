#!/usr/bin/env bash
set -euo pipefail

IMAGE=""
TIER=""
OUTPUT_DIR=""
BENCH_SECURITY=""
SCORE=0
TOTAL=0
PASS_COUNT=0
FAIL_COUNT=0
NA_COUNT=0
RESULTS=()

usage() {
    cat <<'EOF'
Usage: run_cis_scan.sh --image <image> --tier <1|2|3> [--output-dir <dir>]

Scan a container image against CIS Docker Benchmark sections 4-5.

Options:
  --image       Container image reference (required)
  --tier        Image tier: 1, 2, or 3 (required)
  --output-dir  Directory for report output (default: stdout)
  --help        Show this help message
EOF
    exit 0
}

log_pass() { RESULTS+=("PASS|$1|$2"); }
log_fail() { RESULTS+=("FAIL|$1|$2"); }
log_na()   { RESULTS+=("NA|$1|$2"); }

check_4_4_1() {
    local id="4.4.1"
    local title="Ensure a user for the container has been created"
    local uid
    uid=$(docker run --rm --entrypoint id "$IMAGE" -u 2>/dev/null | tr -d '[:space:]' || echo "0")
    if [ "$uid" != "0" ]; then
        log_pass "$id" "$title"
    else
        log_fail "$id" "$title (container runs as root)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_4_4_2() {
    local id="4.4.2"
    local title="Ensure that containers use trusted base images"
    if docker inspect --format='{{index .Config.Labels "org.opencontainers.image.source"}}' "$IMAGE" 2>/dev/null | grep -q .; then
        log_pass "$id" "$title"
    elif docker inspect --format='{{index .RepoDigests 0}}' "$IMAGE" 2>/dev/null | grep -q '@sha256:'; then
        log_pass "$id" "$title"
    else
        log_na "$id" "$title (cannot verify source - requires cosign or digest pin)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_4_4_3() {
    local id="4.4.3"
    local title="Ensure unnecessary packages are not installed"
    local has_shell=false
    local has_pkgmgr=false

    if docker run --rm --entrypoint /bin/sh "$IMAGE" -c "echo ok" 2>/dev/null; then
        has_shell=true
    fi

    for pm in apt apt-get apk dnf yum; do
        if docker run --rm --entrypoint "$pm" "$IMAGE" --version 2>/dev/null; then
            has_pkgmgr=true
        fi
    done

    if [ "$has_shell" = false ] && [ "$has_pkgmgr" = false ]; then
        log_pass "$id" "$title"
    elif [ "$TIER" = "3" ]; then
        log_na "$id" "$title (Tier 3 images may have shell/pkgmgr - documented exception)"
    else
        log_fail "$id" "$title (shell=$has_shell, pkgmgr=$has_pkgmgr)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_4_4_4() {
    local id="4.4.4"
    local title="Ensure images are scanned and rebuilt to include security patches"
    log_na "$id" "$title (requires external vulnerability database - verify with trivy scan)"
    TOTAL=$((TOTAL + 1))
}

check_4_5_1() {
    local id="4.5.1"
    local title="Ensure the container is restricted from acquiring additional privileges"
    local secopt
    secopt=$(docker inspect --format='{{.HostConfig.SecurityOpt}}' "$IMAGE" 2>/dev/null || echo "")
    if echo "$secopt" | grep -q "no-new-privileges"; then
        log_pass "$id" "$title"
    else
        log_na "$id" "$title (runtime enforcement - set --security-opt no-new-privileges:true)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_4_5_2() {
    local id="4.5.2"
    local title="Ensure containers are restricted from acquiring additional privileges via su/sudo"
    local has_sudo=false
    local has_su=false

    if docker run --rm --entrypoint sudo "$IMAGE" --version 2>/dev/null; then
        has_sudo=true
    fi
    if docker run --rm --entrypoint su "$IMAGE" --help 2>/dev/null; then
        has_su=true
    fi

    if [ "$has_sudo" = false ] && [ "$has_su" = false ]; then
        log_pass "$id" "$title"
    else
        log_fail "$id" "$title (sudo=$has_sudo, su=$has_su)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_4_5_3() {
    local id="4.5.3"
    local title="Ensure containers are restricted from acquiring additional capabilities"
    local caps
    caps=$(docker inspect --format='{{.HostConfig.CapAdd}}' "$IMAGE" 2>/dev/null || echo "[]")
    if [ "$caps" = "[]" ] || [ "$caps" = "<no value>" ]; then
        log_na "$id" "$title (image-level - verify runtime uses --cap-drop ALL)"
    else
        log_fail "$id" "$title (capabilities added: $caps)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_4_5_4() {
    local id="4.5.4"
    local title="Ensure privileged containers are not used"
    local privileged
    privileged=$(docker inspect --format='{{.HostConfig.Privileged}}' "$IMAGE" 2>/dev/null || echo "false")
    if [ "$privileged" = "false" ]; then
        log_na "$id" "$title (image-level - verify runtime does not use --privileged)"
    else
        log_fail "$id" "$title (container is privileged)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_4_5_5() {
    local id="4.5.5"
    local title="Ensure health checks are configured for the container"
    local health
    health=$(docker inspect --format='{{.Config.Healthcheck}}' "$IMAGE" 2>/dev/null || echo "<no value>")
    if [ "$health" != "<no value>" ] && [ -n "$health" ] && [ "$health" != "[]" ]; then
        log_pass "$id" "$title"
    else
        log_fail "$id" "$title (no HEALTHCHECK instruction)"
    fi
    TOTAL=$((TOTAL + 1))
}

while [ $# -gt 0 ]; do
    case "$1" in
        --image)     IMAGE="$2"; shift 2 ;;
        --tier)      TIER="$2"; shift 2 ;;
        --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
        --help)      usage ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

if [ -z "$IMAGE" ]; then
    echo "Error: --image is required" >&2
    exit 1
fi

if [ -z "$TIER" ]; then
    echo "Error: --tier is required" >&2
    exit 1
fi

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
    echo "Error: image '$IMAGE' not found locally" >&2
    exit 1
fi

if command -v docker-bench-security >/dev/null 2>&1; then
    BENCH_SECURITY="available"
fi

echo "=========================================="
echo "CIS Docker Benchmark Scan"
echo "Image: $IMAGE"
echo "Tier: $TIER"
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "=========================================="
echo ""

check_4_4_1
check_4_4_2
check_4_4_3
check_4_4_4
check_4_5_1
check_4_5_2
check_4_5_3
check_4_5_4
check_4_5_5

for result in "${RESULTS[@]}"; do
    IFS='|' read -r status id title <<< "$result"
    case "$status" in
        PASS) PASS_COUNT=$((PASS_COUNT + 1)); printf "  [PASS]  %s: %s\n" "$id" "$title" ;;
        FAIL) FAIL_COUNT=$((FAIL_COUNT + 1)); printf "  [FAIL]  %s: %s\n" "$id" "$title" ;;
        NA)   NA_COUNT=$((NA_COUNT + 1));   printf "  [NA]    %s: %s\n" "$id" "$title" ;;
    esac
done

if [ "$NA_COUNT" -gt 0 ]; then
    SCORE=$(( (PASS_COUNT * 100) / (TOTAL - NA_COUNT) ))
else
    SCORE=$(( (PASS_COUNT * 100) / TOTAL ))
fi

echo ""
echo "=========================================="
echo "RESULTS"
echo "=========================================="
echo "  Total:  $TOTAL"
echo "  Pass:   $PASS_COUNT"
echo "  Fail:   $FAIL_COUNT"
echo "  NA:     $NA_COUNT"
echo "  Score:  ${SCORE}%"
echo "=========================================="

if [ -n "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    REPORT_FILE="${OUTPUT_DIR}/cis-$(echo "$IMAGE" | tr '/:' '_')-$(date +%Y%m%d%H%M%S).txt"
    {
        echo "CIS Docker Benchmark Scan Report"
        echo "Image: $IMAGE"
        echo "Tier: $TIER"
        echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo ""
        for result in "${RESULTS[@]}"; do
            IFS='|' read -r status id title <<< "$result"
            echo "[$status] $id: $title"
        done
        echo ""
        echo "Score: ${SCORE}%"
    } > "$REPORT_FILE"
    echo "Report written to: $REPORT_FILE"
fi

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
fi

exit 0
