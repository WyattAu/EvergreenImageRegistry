#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DOCKERFILE_CI="${PROJECT_ROOT}/Dockerfile.ci"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

declare -A TOOLS=(
    ["docker"]="https://download.docker.com/linux/static/stable/x86_64/"
    ["buildx"]="https://github.com/docker/buildx/releases/latest/download/"
    ["trivy"]="https://github.com/aquasecurity/trivy/releases/latest/download/"
    ["grype"]="https://github.com/anchore/grype/releases/latest/download/"
    ["cosign"]="https://github.com/sigstore/cosign/releases/latest/download/"
    ["syft"]="https://github.com/anchore/syft/releases/latest/download/"
    ["hadolint"]="https://github.com/hadolint/hadolint/releases/latest/download/"
    ["helm"]="https://get.helm.sh/"
    ["kubectl"]="https://dl.k8s.io/release/stable.txt"
    ["crane"]="https://github.com/google/go-containerregistry/releases/latest/download/"
    ["yq"]="https://github.com/mikefarah/yq/releases/latest/download/"
    ["trufflehog"]="https://github.com/trufflesecurity/trufflehog/releases/latest/download/"
)

declare -A CURRENT_VERSIONS

extract_current_versions() {
    local line tool _version

    while IFS= read -r line; do
        if [[ "$line" =~ docker-([0-9]+\.[0-9]+\.[0-9]+)\.tgz ]]; then
            CURRENT_VERSIONS["docker"]="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ buildx-v([0-9]+\.[0-9]+\.[0-9]+)\.linux ]]; then
            CURRENT_VERSIONS["buildx"]="v${BASH_REMATCH[1]}"
        elif [[ "$line" =~ trivy_([0-9]+\.[0-9]+\.[0-9]+)_Linux ]]; then
            CURRENT_VERSIONS["trivy"]="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ grype_([0-9]+\.[0-9]+\.[0-9]+)_linux ]]; then
            CURRENT_VERSIONS["grype"]="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ cosign_([0-9]+\.[0-9]+\.[0-9]+)_linux ]]; then
            CURRENT_VERSIONS["cosign"]="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ syft_([0-9]+\.[0-9]+\.[0-9]+)_linux ]]; then
            CURRENT_VERSIONS["syft"]="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ hadolint-Linux-x86_64.*v([0-9]+\.[0-9]+\.[0-9]+) ]]; then
            CURRENT_VERSIONS["hadolint"]="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ helm-v([0-9]+\.[0-9]+\.[0-9]+)-linux ]]; then
            CURRENT_VERSIONS["helm"]="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ k8s.io/release/v([0-9]+\.[0-9]+\.[0-9]+)/bin ]]; then
            CURRENT_VERSIONS["kubectl"]="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ yq_linux_amd64.*v([0-9]+\.[0-9]+\.[0-9]+) ]]; then
            CURRENT_VERSIONS["yq"]="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ trufflehog_([0-9]+\.[0-9]+\.[0-9]+)_linux ]]; then
            CURRENT_VERSIONS["trufflehog"]="${BASH_REMATCH[1]}"
        fi
    done < "$DOCKERFILE_CI"

    CURRENT_VERSIONS["crane"]="latest"
}

check_latest_versions() {
    declare -A _LATEST
    local tool

    printf "${CYAN}Checking latest versions...${NC}\n\n"

    for tool in "${!TOOLS[@]}"; do
        local url="${TOOLS[$tool]}"
        local latest=""

        case "$tool" in
            docker)
                local listing
                listing=$(curl -fsSL "$url" 2>/dev/null || echo "")
                if [[ "$listing" =~ docker-([0-9]+\.[0-9]+\.[0-9]+)\.tgz ]]; then
                    latest="${BASH_REMATCH[1]}"
                    while [[ "$listing" =~ docker-([0-9]+\.[0-9]+\.[0-9]+)\.tgz ]]; do
                        latest="${BASH_REMATCH[1]}"
                        listing="${listing#*${BASH_REMATCH[0]}}"
                    done
                fi
                ;;
            buildx)
                local redirect_url
                redirect_url=$(curl -fsSL -o /dev/null -w '%{url_effective}' \
                    "https://github.com/docker/buildx/releases/latest" 2>/dev/null || echo "")
                if [[ "$redirect_url" =~ /v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
                    latest="v${BASH_REMATCH[1]}"
                fi
                ;;
            trivy)
                local redirect_url
                redirect_url=$(curl -fsSL -o /dev/null -w '%{url_effective}' \
                    "https://github.com/aquasecurity/trivy/releases/latest" 2>/dev/null || echo "")
                if [[ "$redirect_url" =~ /v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
                    latest="${BASH_REMATCH[1]}"
                fi
                ;;
            grype)
                local redirect_url
                redirect_url=$(curl -fsSL -o /dev/null -w '%{url_effective}' \
                    "https://github.com/anchore/grype/releases/latest" 2>/dev/null || echo "")
                if [[ "$redirect_url" =~ /v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
                    latest="${BASH_REMATCH[1]}"
                fi
                ;;
            cosign)
                local redirect_url
                redirect_url=$(curl -fsSL -o /dev/null -w '%{url_effective}' \
                    "https://github.com/sigstore/cosign/releases/latest" 2>/dev/null || echo "")
                if [[ "$redirect_url" =~ /v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
                    latest="${BASH_REMATCH[1]}"
                fi
                ;;
            syft)
                local redirect_url
                redirect_url=$(curl -fsSL -o /dev/null -w '%{url_effective}' \
                    "https://github.com/anchore/syft/releases/latest" 2>/dev/null || echo "")
                if [[ "$redirect_url" =~ /v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
                    latest="${BASH_REMATCH[1]}"
                fi
                ;;
            hadolint)
                local redirect_url
                redirect_url=$(curl -fsSL -o /dev/null -w '%{url_effective}' \
                    "https://github.com/hadolint/hadolint/releases/latest" 2>/dev/null || echo "")
                if [[ "$redirect_url" =~ /v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
                    latest="${BASH_REMATCH[1]}"
                fi
                ;;
            helm)
                local listing
                listing=$(curl -fsSL "https://get.helm.sh/" 2>/dev/null || echo "")
                if [[ "$listing" =~ helm-v([0-9]+\.[0-9]+\.[0-9]+)-linux-amd64\.tar\.gz ]]; then
                    latest="${BASH_REMATCH[1]}"
                    while [[ "$listing" =~ helm-v([0-9]+\.[0-9]+\.[0-9]+)-linux-amd64\.tar\.gz ]]; do
                        latest="${BASH_REMATCH[1]}"
                        listing="${listing#*${BASH_REMATCH[0]}}"
                    done
                fi
                ;;
            kubectl)
                latest=$(curl -fsSL "https://dl.k8s.io/release/stable.txt" 2>/dev/null | sed 's/^v//' || echo "")
                ;;
            crane)
                latest="latest"
                ;;
            yq)
                local redirect_url
                redirect_url=$(curl -fsSL -o /dev/null -w '%{url_effective}' \
                    "https://github.com/mikefarah/yq/releases/latest" 2>/dev/null || echo "")
                if [[ "$redirect_url" =~ /v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
                    latest="${BASH_REMATCH[1]}"
                fi
                ;;
            trufflehog)
                local redirect_url
                redirect_url=$(curl -fsSL -o /dev/null -w '%{url_effective}' \
                    "https://github.com/trufflesecurity/trufflehog/releases/latest" 2>/dev/null || echo "")
                if [[ "$redirect_url" =~ /v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
                    latest="${BASH_REMATCH[1]}"
                fi
                ;;
        esac

        local current="${CURRENT_VERSIONS[$tool]:-unknown}"
        local status=""

        if [[ -z "$latest" ]]; then
            printf "  ${YELLOW}%-12s${NC} current: %-15s latest: ${YELLOW}check failed${NC}\n" "$tool" "$current"
        elif [[ "$current" == "$latest" ]]; then
            printf "  ${GREEN}%-12s${NC} current: %-15s latest: ${GREEN}%s${NC}\n" "$tool" "$current" "$latest"
        else
            printf "  ${RED}%-12s${NC} current: %-15s latest: ${RED}%s${NC}  ${YELLOW}UPDATE AVAILABLE${NC}\n" "$tool" "$current" "$latest"
            status="$tool:$current->$latest"
        fi

        if [[ -n "$status" ]]; then
            UPDATES+=("$status")
        fi
    done

    printf "\n"
}

print_diff() {
    if [[ ${#UPDATES[@]} -eq 0 ]]; then
        printf "${GREEN}All tools are up to date.${NC}\n"
        return 0
    fi

    printf "${YELLOW}Version changes detected:${NC}\n\n"
    printf "  %-12s  %-18s  %-18s\n" "TOOL" "CURRENT" "LATEST"
    printf "  %-12s  %-18s  %-18s\n" "----" "-------" "------"
    for entry in "${UPDATES[@]}"; do
        local tool="${entry%%:*}"
        local rest="${entry#*:}"
        local current="${rest%%->*}"
        local latest="${rest#*->}"
        printf "  ${RED}%-12s${NC}  %-18s  ${GREEN}%-18s${NC}\n" "$tool" "$current" "$latest"
    done
    printf "\n"
}

apply_updates() {
    if [[ ${#UPDATES[@]} -eq 0 ]]; then
        printf "${GREEN}Nothing to update.${NC}\n"
        return 0
    fi

    printf "${YELLOW}Applying updates to %s...${NC}\n\n" "$DOCKERFILE_CI"

    local tmp_file
    tmp_file=$(mktemp)
    cp "$DOCKERFILE_CI" "$tmp_file"

    for entry in "${UPDATES[@]}"; do
        local tool="${entry%%:*}"
        local rest="${entry#*:}"
        local current="${rest%%->*}"
        local latest="${rest#*->}"

        case "$tool" in
            docker)
                sed -i "s/docker-${current}\.tgz/docker-${latest}.tgz/g" "$tmp_file"
                ;;
            buildx)
                sed -i "s/buildx-${current}/buildx-${latest}/g" "$tmp_file"
                ;;
            trivy)
                sed -i "s/trivy_${current}_Linux/trivy_${latest}_Linux/g" "$tmp_file"
                ;;
            grype)
                sed -i "s/grype_${current}_linux/grype_${latest}_linux/g" "$tmp_file"
                ;;
            cosign)
                sed -i "s/cosign_${current}_linux/cosign_${latest}_linux/g" "$tmp_file"
                ;;
            syft)
                sed -i "s/syft_${current}_linux/syft_${latest}_linux/g" "$tmp_file"
                ;;
            hadolint)
                sed -i "s|hadolint-Linux-x86_64|hadolint-Linux-x86_64|g" "$tmp_file"
                sed -i "s|releases/download/v${current}/hadolint|releases/download/v${latest}/hadolint|g" "$tmp_file"
                ;;
            helm)
                sed -i "s/helm-v${current}-linux/helm-v${latest}-linux/g" "$tmp_file"
                ;;
            kubectl)
                sed -i "s|release/v${current}/bin|release/v${latest}/bin|g" "$tmp_file"
                ;;
            crane)
                printf "  ${CYAN}crane${NC}: pinned to latest (no version change needed)\n"
                ;;
            yq)
                sed -i "s/yq_linux_amd64.*v${current}/yq_linux_amd64\" # v${latest}/g" "$tmp_file"
                sed -i "s|releases/download/v${current}/yq|releases/download/v${latest}/yq|g" "$tmp_file"
                ;;
            trufflehog)
                sed -i "s/trufflehog_${current}_linux/trufflehog_${latest}_linux/g" "$tmp_file"
                ;;
        esac

        printf "  ${GREEN}%s${NC}: %s -> %s\n" "$tool" "$current" "$latest"
    done

    cp "$tmp_file" "$DOCKERFILE_CI"
    rm -f "$tmp_file"

    printf "\n${GREEN}Updated %s with %d version change(s).${NC}\n" "$DOCKERFILE_CI" "${#UPDATES[@]}"
    printf "${YELLOW}Review changes and commit.${NC}\n"
}

UPDATES=()

main() {
    if [[ ! -f "$DOCKERFILE_CI" ]]; then
        printf "${RED}Error: %s not found.${NC}\n" "$DOCKERFILE_CI"
        exit 1
    fi

    local apply=false
    if [[ "${1:-}" == "--apply" ]]; then
        apply=true
    fi

    printf "${CYAN}=== Evergreen CI Environment Version Check ===${NC}\n"
    printf "Dockerfile.ci: %s\n\n" "$DOCKERFILE_CI"

    extract_current_versions

    printf "${CYAN}Current pinned versions in Dockerfile.ci:${NC}\n"
    for tool in docker buildx trivy grype cosign syft hadolint helm kubectl crane yq trufflehog; do
        printf "  %-12s %s\n" "$tool" "${CURRENT_VERSIONS[$tool]:-not found}"
    done
    printf "\n"

    check_latest_versions
    print_diff

    if $apply; then
        apply_updates
    else
        printf "Run with ${CYAN}--apply${NC} to update Dockerfile.ci\n"
    fi
}

main "$@"
