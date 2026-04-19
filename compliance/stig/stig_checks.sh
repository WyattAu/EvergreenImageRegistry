#!/usr/bin/env bash
set -euo pipefail

IMAGE=""
TIER=""
OUTPUT_DIR=""
RESULTS=()
PASS_COUNT=0
FAIL_COUNT=0
NA_COUNT=0
TOTAL=0

usage() {
    cat <<'EOF'
Usage: stig_checks.sh --image <image> --tier <1|2|3> [--output-dir <dir>]

Check a container image against DISA STIG requirements.

Options:
  --image       Container image reference (required)
  --tier        Image tier: 1, 2, or 3 (required)
  --output-dir  Directory for report output (default: stdout)
  --help        Show this help message
EOF
    exit 0
}

log_pass() { RESULTS+=("PASS|$1|$2|$3"); }
log_fail() { RESULTS+=("FAIL|$1|$2|$3"); }
log_na()   { RESULTS+=("NA|$1|$2|$3"); }

check_non_root() {
    local stig_id="CCI-000366"
    local constraint="C001"
    local title="Container must run as non-root user"
    local uid
    uid=$(docker run --rm --entrypoint id "$IMAGE" -u 2>/dev/null | tr -d '[:space:]' || echo "0")
    if [ "$uid" != "0" ]; then
        log_pass "$stig_id" "$constraint" "$title (uid=$uid)"
    else
        log_fail "$stig_id" "$constraint" "$title (runs as root)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_no_shell() {
    local stig_id="CCI-000770"
    local constraint="C003"
    local title="Container must not have shell access"
    local found_shell=""
    for shell in /bin/sh /bin/bash /bin/dash /bin/ash /bin/zsh; do
        if docker run --rm --entrypoint "$shell" "$IMAGE" -c "echo ok" 2>/dev/null; then
            found_shell="$shell"
            break
        fi
    done
    if [ -z "$found_shell" ]; then
        log_pass "$stig_id" "$constraint" "$title"
    elif [ "$TIER" = "3" ] || [ "$TIER" = "2" ]; then
        log_na "$stig_id" "$constraint" "$title (shell found: $found_shell - documented Tier $TIER exception)"
    else
        log_fail "$stig_id" "$constraint" "$title (shell found: $found_shell)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_no_pkgmgr() {
    local stig_id="CCI-000213"
    local constraint="C004"
    local title="Container must not have package manager"
    local found_pm=""
    for pm in apt apt-get apk dnf yum zypper pip; do
        if docker run --rm --entrypoint "$pm" "$IMAGE" --version 2>/dev/null; then
            found_pm="$pm"
            break
        fi
    done
    if [ -z "$found_pm" ]; then
        log_pass "$stig_id" "$constraint" "$title"
    elif [ "$TIER" = "3" ]; then
        log_na "$stig_id" "$constraint" "$title (package manager found: $found_pm - documented Tier 3 exception)"
    else
        log_fail "$stig_id" "$constraint" "$title (package manager found: $found_pm)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_no_debug_tools() {
    local stig_id="CCI-001758"
    local constraint="C003,C015"
    local title="Container must not have debug tools"
    local found=""
    for tool in strace gdb ltrace tcpdump wireshark ncat netcat nc vim vi nano; do
        if docker run --rm --entrypoint "$tool" "$IMAGE" --version 2>/dev/null; then
            found="$tool"
            break
        fi
    done
    if [ -z "$found" ]; then
        log_pass "$stig_id" "$constraint" "$title"
    else
        log_fail "$stig_id" "$constraint" "$title (debug tool found: $found)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_readonly_fs() {
    local stig_id="CCI-001751"
    local constraint="C002"
    local title="Container root filesystem must be read-only"
    local readonly_fs
    readonly_fs=$(docker inspect --format='{{.HostConfig.ReadonlyRootfs}}' "$IMAGE" 2>/dev/null || echo "false")
    if [ "$readonly_fs" = "true" ]; then
        log_pass "$stig_id" "$constraint" "$title"
    else
        log_na "$stig_id" "$constraint" "$title (runtime enforcement - set --read-only)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_no_sensitive_env() {
    local stig_id="CCI-001753"
    local constraint="C016"
    local title="Container must not contain sensitive data in environment variables"
    local env_vars
    env_vars=$(docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' "$IMAGE" 2>/dev/null || echo "")
    local found_sensitive=""
    for pattern in PASSWORD SECRET KEY TOKEN PRIVATE; do
        if echo "$env_vars" | grep -qi "$pattern="; then
            found_sensitive="$pattern"
            break
        fi
    done
    if [ -z "$found_sensitive" ]; then
        log_pass "$stig_id" "$constraint" "$title"
    else
        log_fail "$stig_id" "$constraint" "$title (sensitive env pattern found: $found_sensitive)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_no_privileged() {
    local stig_id="CCI-001749"
    local constraint="C017"
    local title="Container must not run in privileged mode"
    local privileged
    privileged=$(docker inspect --format='{{.HostConfig.Privileged}}' "$IMAGE" 2>/dev/null || echo "false")
    if [ "$privileged" = "false" ]; then
        log_pass "$stig_id" "$constraint" "$title"
    else
        log_fail "$stig_id" "$constraint" "$title (privileged mode detected)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_no_host_network() {
    local stig_id="CCI-001750"
    local constraint="C017"
    local title="Container must not use host network mode"
    local net_mode
    net_mode=$(docker inspect --format='{{.HostConfig.NetworkMode}}' "$IMAGE" 2>/dev/null || echo "")
    if [ "$net_mode" != "host" ]; then
        log_pass "$stig_id" "$constraint" "$title"
    else
        log_fail "$stig_id" "$constraint" "$title (host network mode detected)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_no_new_privileges() {
    local stig_id="CCI-001754"
    local constraint="Phase 2"
    local title="Container must not allow privilege escalation"
    local secopt
    secopt=$(docker inspect --format='{{.HostConfig.SecurityOpt}}' "$IMAGE" 2>/dev/null || echo "")
    if echo "$secopt" | grep -q "no-new-privileges"; then
        log_pass "$stig_id" "$constraint" "$title"
    else
        log_na "$stig_id" "$constraint" "$title (runtime enforcement - set --security-opt no-new-privileges:true)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_pinned_tags() {
    local stig_id="CCI-001757"
    local constraint="C019"
    local title="Container image must use pinned tags"
    local user
    user=$(docker inspect --format='{{.Config.User}}' "$IMAGE" 2>/dev/null || echo "")
    local repo_tags
    repo_tags=$(docker inspect --format='{{.RepoTags}}' "$IMAGE" 2>/dev/null || echo "[]")
    local digests
    digests=$(docker inspect --format='{{.RepoDigests}}' "$IMAGE" 2>/dev/null || echo "[]")
    if echo "$digests" | grep -q '@sha256:'; then
        log_pass "$stig_id" "$constraint" "$title (image has digest pin)"
    else
        log_na "$stig_id" "$constraint" "$title (no digest pin - verify tag is immutable at registry level)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_healthcheck() {
    local stig_id="CCI-001759"
    local constraint="C010"
    local title="Container must have health check configured"
    local health
    health=$(docker inspect --format='{{.Config.Healthcheck}}' "$IMAGE" 2>/dev/null || echo "")
    if [ -n "$health" ] && [ "$health" != "<no value>" ] && [ "$health" != "[]" ]; then
        log_pass "$stig_id" "$constraint" "$title"
    else
        log_fail "$stig_id" "$constraint" "$title (no HEALTHCHECK instruction)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_no_interactive_shell() {
    local stig_id="CCI-001758"
    local constraint="C003,C015"
    local title="Container must not allow interactive shell access"
    local entrypoint
    entrypoint=$(docker inspect --format='{{json .Config.Entrypoint}}' "$IMAGE" 2>/dev/null || echo "[]")
    local cmd
    cmd=$(docker inspect --format='{{json .Config.Cmd}}' "$IMAGE" 2>/dev/null || echo "[]")
    if echo "$entrypoint $cmd" | grep -qiE '/bin/(sh|bash|dash|ash|zsh)'; then
        log_fail "$stig_id" "$constraint" "$title (entrypoint/cmd references shell)"
    else
        log_pass "$stig_id" "$constraint" "$title"
    fi
    TOTAL=$((TOTAL + 1))
}

check_sbom() {
    local stig_id="CCI-001813"
    local constraint="C009"
    local title="Container must have a Software Bill of Materials (SBOM)"
    log_na "$stig_id" "$constraint" "$title (verify SBOM exists: syft <image> -o spdx-json)"
    TOTAL=$((TOTAL + 1))
}

check_signed() {
    local stig_id="CCI-001812"
    local constraint="C008"
    local title="Container image must be signed"
    log_na "$stig_id" "$constraint" "$title (verify with: cosign verify <image-ref>)"
    TOTAL=$((TOTAL + 1))
}

check_seccomp() {
    local stig_id="CCI-001755"
    local constraint="Phase 2"
    local title="Container must use seccomp profile"
    local secprofile
    secprofile=$(docker inspect --format='{{.HostConfig.SecurityOpt}}' "$IMAGE" 2>/dev/null || echo "")
    if echo "$secprofile" | grep -q "seccomp"; then
        log_pass "$stig_id" "$constraint" "$title"
    else
        log_na "$stig_id" "$constraint" "$title (runtime enforcement - use --security-opt seccomp=profile.json)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_resource_limits() {
    local stig_id="CCI-001763"
    local constraint="Phase 2"
    local title="Container must have resource limits"
    local mem_limit
    mem_limit=$(docker inspect --format='{{.HostConfig.Memory}}' "$IMAGE" 2>/dev/null || echo "0")
    local cpu_quota
    cpu_quota=$(docker inspect --format='{{.HostConfig.CpuQuota}}' "$IMAGE" 2>/dev/null || echo "0")
    if [ "$mem_limit" != "0" ] || [ "$cpu_quota" != "0" ]; then
        log_pass "$stig_id" "$constraint" "$title"
    else
        log_na "$stig_id" "$constraint" "$title (runtime enforcement - set --memory and --cpus)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_no_sudo() {
    local stig_id="CCI-001752"
    local constraint="C018"
    local title="Container must not have sudo installed"
    if docker run --rm --entrypoint sudo "$IMAGE" --version 2>/dev/null; then
        log_fail "$stig_id" "$constraint" "$title (sudo is accessible)"
    else
        log_pass "$stig_id" "$constraint" "$title"
    fi
    TOTAL=$((TOTAL + 1))
}

check_cap_drop_all() {
    local stig_id="CCI-001752"
    local constraint="C018"
    local title="Container capabilities must be dropped"
    local cap_drop
    cap_drop=$(docker inspect --format='{{.HostConfig.CapDrop}}' "$IMAGE" 2>/dev/null || echo "[]")
    local cap_add
    cap_add=$(docker inspect --format='{{.HostConfig.CapAdd}}' "$IMAGE" 2>/dev/null || echo "[]")
    if echo "$cap_drop" | grep -qi "all"; then
        log_pass "$stig_id" "$constraint" "$title (cap-drop ALL applied)"
    elif [ "$cap_add" = "[]" ]; then
        log_na "$stig_id" "$constraint" "$title (runtime enforcement - use --cap-drop ALL)"
    else
        log_fail "$stig_id" "$constraint" "$title (capabilities added: $cap_add)"
    fi
    TOTAL=$((TOTAL + 1))
}

check_vuln_scan() {
    local stig_id="CCI-001814"
    local constraint="trivy"
    local title="Container must be scanned for vulnerabilities"
    log_na "$stig_id" "$constraint" "$title (verify with: trivy image <image>)"
    TOTAL=$((TOTAL + 1))
}

check_logging() {
    local stig_id="CCI-001761"
    local constraint="Phase 3"
    local title="Container logging must be configured"
    local log_driver
    log_driver=$(docker inspect --format='{{.HostConfig.LogConfig.Type}}' "$IMAGE" 2>/dev/null || echo "json-file")
    if [ -n "$log_driver" ]; then
        log_na "$stig_id" "$constraint" "$title (logging driver: $log_driver - verify centralized log aggregation)"
    else
        log_na "$stig_id" "$constraint" "$title (runtime enforcement - configure log driver)"
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

echo "=========================================="
echo "DISA STIG Compliance Check"
echo "Image: $IMAGE"
echo "Tier: $TIER"
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "=========================================="
echo ""

check_non_root
check_no_shell
check_no_pkgmgr
check_no_debug_tools
check_readonly_fs
check_no_sensitive_env
check_no_privileged
check_no_host_network
check_no_new_privileges
check_pinned_tags
check_healthcheck
check_no_interactive_shell
check_sbom
check_signed
check_seccomp
check_resource_limits
check_no_sudo
check_cap_drop_all
check_vuln_scan
check_logging

for result in "${RESULTS[@]}"; do
    IFS='|' read -r status stig_id constraint title <<< "$result"
    case "$status" in
        PASS) PASS_COUNT=$((PASS_COUNT + 1)); printf "  [PASS]  %-12s %-8s %s\n" "$stig_id" "($constraint)" "$title" ;;
        FAIL) FAIL_COUNT=$((FAIL_COUNT + 1)); printf "  [FAIL]  %-12s %-8s %s\n" "$stig_id" "($constraint)" "$title" ;;
        NA)   NA_COUNT=$((NA_COUNT + 1));   printf "  [NA]    %-12s %-8s %s\n" "$stig_id" "($constraint)" "$title" ;;
    esac
done

echo ""
echo "=========================================="
echo "RESULTS"
echo "=========================================="
echo "  Total:  $TOTAL"
echo "  Pass:   $PASS_COUNT"
echo "  Fail:   $FAIL_COUNT"
echo "  NA:     $NA_COUNT"
echo "=========================================="

if [ -n "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    REPORT_FILE="${OUTPUT_DIR}/stig-$(echo "$IMAGE" | tr '/:' '_')-$(date +%Y%m%d%H%M%S).txt"
    {
        echo "DISA STIG Compliance Check Report"
        echo "Image: $IMAGE"
        echo "Tier: $TIER"
        echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo ""
        for result in "${RESULTS[@]}"; do
            IFS='|' read -r status stig_id constraint title <<< "$result"
            echo "[$status] $stig_id ($constraint): $title"
        done
        echo ""
        echo "Pass: $PASS_COUNT / Fail: $FAIL_COUNT / NA: $NA_COUNT / Total: $TOTAL"
    } > "$REPORT_FILE"
    echo "Report written to: $REPORT_FILE"
fi

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
fi

exit 0
