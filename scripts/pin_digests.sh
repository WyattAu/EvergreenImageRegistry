#!/bin/bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_FILE="${1:-/dev/stdout}"
UPDATE=false
VERBOSE=false

usage() {
    cat <<'EOF'
Usage: pin_digests.sh [OPTIONS] [REPORT_FILE]

Resolve mutable image tags in Dockerfiles to SHA256 digests.

Options:
  --update    Modify Dockerfiles in-place to pin digests
  --verbose   Show resolution details for each image
  -h, --help  Show this help message

Report:
  Outputs CSV: image_name,from_line,current_ref,pinned_digest,status

Examples:
  pin_digests.sh                      # Print report to stdout
  pin_digests.sh report.csv           # Save report to file
  pin_digests.sh --update             # Pin digests in-place
  pin_digests.sh --update --verbose   # Pin and show details
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --update) UPDATE=true; shift ;;
        --verbose) VERBOSE=true; shift ;;
        -h|--help) usage; exit 0 ;;
        -*) echo "Unknown option: $1" >&2; usage; exit 1 ;;
        *) REPORT_FILE="$1"; shift ;;
    esac
done

resolve_digest() {
    local image_ref="$1"
    if command -v docker &>/dev/null; then
        local digest
        digest=$(docker manifest inspect "$image_ref" 2>/dev/null \
            | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'manifest' in data:
        print(data['manifest']['digest'])
    elif 'digest' in data:
        print(data['digest'])
    else:
        print('')
except Exception:
    print('')
" 2>/dev/null)
        if [[ -n "$digest" ]]; then
            echo "$digest"
            return 0
        fi
    fi

    if command -v skopeo &>/dev/null; then
        local digest
        digest=$(skopeo inspect "docker://$image_ref" 2>/dev/null \
            | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('Digest', ''))
except Exception:
    print('')
" 2>/dev/null)
        if [[ -n "$digest" ]]; then
            echo "$digest"
            return 0
        fi
    fi

    local registry image_name tag
    registry=$(echo "$image_ref" | sed -E 's|^([^/]+)/.+$|\1|')
    image_name=$(echo "$image_ref" | sed -E 's|^[^/]*/(.+):.+$|\1|')
    tag=$(echo "$image_ref" | sed -E 's|^.+:([^@]+)$|\1|')

    if [[ "$image_ref" == */* ]]; then
        local api_url="https://${registry}/v2/${image_name}/manifests/${tag}"
    else
        local api_url="https://registry-1.docker.io/v2/${image_name}/manifests/${tag}"
    fi

    local token=""
    local auth_url
    if [[ "$image_ref" == */* ]]; then
        auth_url="https://${registry}/v2/"
    else
        auth_url="https://auth.docker.io/token?service=registry.docker.io&scope=repository:${image_name}:pull"
    fi

    if [[ "$image_ref" != */* ]]; then
        token=$(curl -sf "${auth_url}" 2>/dev/null | python3 -c "
import sys, json
try:
    print(json.load(sys.stdin)['token'])
except Exception:
    print('')
" 2>/dev/null)
    fi

    local digest=""
    if [[ -n "$token" ]]; then
        digest=$(curl -sf -H "Authorization: Bearer ${token}" \
            -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
            "$api_url" -D /tmp/headers.txt 2>/dev/null \
            | head -1)
        digest=$(grep -i 'docker-content-digest' /tmp/headers.txt 2>/dev/null \
            | tr -d '\r' | awk '{print $2}')
    fi

    if [[ -n "$digest" ]]; then
        echo "$digest"
        return 0
    fi

    return 1
}

has_digest() {
    echo "$1" | grep -q '@sha256:'
}

is_pinnable() {
    local ref="$1"
    [[ "$ref" != "scratch" ]] && ! has_digest "$ref"
}

echo "image_name,from_line,current_ref,pinned_digest,status" > "$REPORT_FILE"

dockerfile_count=0
total_from=0
pinned_count=0
mutable_count=0
failed_count=0
updated_count=0

while IFS= read -r -d '' dockerfile; do
    image_dir=$(dirname "${dockerfile#${REPO_ROOT}/images/}")
    dockerfile_count=$((dockerfile_count + 1))

    while IFS= read -r line; do
        line_num="${line%%:*}"
        content="${line#*: }"

        [[ "$content" =~ ^FROM[[:space:]] ]] || continue

        local_from="${content#FROM }"
        local_from="${local_from%%#*}"
        local_from="${local_from%% *}"
        local_from="${local_from%%	*}"
        local_from="${local_from%%as*}"
        local_from="${local_from%%AS*}"
        local_from=$(echo "$local_from" | xargs)

        [[ -z "$local_from" ]] && continue
        [[ "$local_from" == '$'* ]] && {
            echo "${image_dir},${line_num},${local_from},SKIPPED,arg-variable" >> "$REPORT_FILE"
            total_from=$((total_from + 1))
            continue
        }

        total_from=$((total_from + 1))

        if has_digest "$local_from"; then
            pinned_count=$((pinned_count + 1))
            echo "${image_dir},${line_num},${local_from},ALREADY_PINNED,pinned" >> "$REPORT_FILE"
            $VERBOSE && echo "[PINNED]  ${image_dir}:${line_num} ${local_from}"
        elif ! is_pinnable "$local_from"; then
            echo "${image_dir},${line_num},${local_from},N/A,scratch" >> "$REPORT_FILE"
            $VERBOSE && echo "[SKIP]    ${image_dir}:${line_num} ${local_from}"
        else
            mutable_count=$((mutable_count + 1))
            $VERBOSE && echo -n "[RESOLVE] ${image_dir}:${line_num} ${local_from} -> "

            digest=""
            if digest=$(resolve_digest "$local_from" 2>/dev/null) && [[ -n "$digest" ]]; then
                pinned_ref="${local_from%%:*}@${digest}"
                echo "${image_dir},${line_num},${local_from},${pinned_ref},mutable-resolved" >> "$REPORT_FILE"
                $VERBOSE && echo "$digest"

                if $UPDATE; then
                    sed -i "s|${local_from}|${pinned_ref}|" "$dockerfile"
                    updated_count=$((updated_count + 1))
                    $VERBOSE && echo "[UPDATED] ${dockerfile}:${line_num}"
                fi
            else
                failed_count=$((failed_count + 1))
                echo "${image_dir},${line_num},${local_from},RESOLUTION_FAILED,mutable-unresolved" >> "$REPORT_FILE"
                $VERBOSE && echo "FAILED"
            fi
        fi
    done < <(grep -n '^FROM' "$dockerfile" 2>/dev/null)
done < <(find "${REPO_ROOT}/images" -name Dockerfile -print0 | sort -z)

echo ""
echo "=== Digest Pinning Report ==="
echo "Dockerfiles scanned:  ${dockerfile_count}"
echo "FROM lines found:     ${total_from}"
echo "Already pinned:       ${pinned_count}"
echo "Mutable (resolved):   ${mutable_count}"
echo "Mutable (failed):     ${failed_count}"
if $UPDATE; then
    echo "Files updated:        ${updated_count}"
fi
echo "Report saved to:      ${REPORT_FILE}"
