#!/bin/bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    echo "Installing jq via apt-get..."
    apt-get update -qq && apt-get install -y -qq jq >/dev/null 2>&1
  elif command -v apk >/dev/null 2>&1; then
    echo "Installing jq via apk..."
    apk add --quiet jq >/dev/null 2>&1
  elif command -v python3 >/dev/null 2>&1; then
    echo "jq not available; will use python3 fallback"
  else
    echo "ERROR: jq is required. Install jq or provide python3." >&2
    exit 1
  fi
fi

IMAGE="${1:?Usage: generate_sbom.sh <image-name>}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
IMAGE_DIR="${REPO_ROOT}/images/${IMAGE}"
OUTPUT="${IMAGE_DIR}/sbom.spdx.json"

if [[ ! -d "${IMAGE_DIR}" ]]; then
  echo "ERROR: Image directory not found: ${IMAGE_DIR}" >&2
  exit 1
fi

NAMESPACE="https://github.com/WyattAu/EvergreenImageRegistry/images/${IMAGE}"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
SPDX_VERSION="SPDX-2.3"
DATA_LICENSE="CC0-1.0"

declare -a PACKAGES=()
declare -a BASE_IMAGES=()
declare -a DOWNLOADED_BINARIES=()
declare -a GO_MODULES=()
version=""
vendor=""

json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\r'/\\r}"
  s="${s//$'\t'/\\t}"
  printf '%s' "${s}"
}

is_valid_package_name() {
  local name="$1"
  [[ -n "${name}" ]] || return 1
  [[ "${name}" == "\\" ]] && return 1
  [[ "${name}" =~ ^[[:space:]]*$ ]] && return 1
  [[ "${name}" =~ ^[[:space:]\-]+$ ]] && return 1
  return 0
}

extract_version() {
  local dockerfile="$1"
  grep -oP 'ARG VERSION=\K[^\s]+' "${dockerfile}" 2>/dev/null || echo "unknown"
}

extract_vendor() {
  local dockerfile="$1"
  grep -oP 'org\.opencontainers\.image\.vendor="[^"]*"' "${dockerfile}" 2>/dev/null | sed 's/.*vendor="//;s/"//' || echo "unknown"
}

parse_apt_packages() {
  local dockerfile="$1"
  sed ':a;N;$!ba;s/\\\n/ /g' "${dockerfile}" | grep -oP 'apt-get install[^|&;]*' | sed 's/apt-get install\s*//' | sed 's/--no-install-recommends//g' | sed 's/-y//g' | tr ' ' '\n' | grep -vP '^(apt-get|install|&&|--no-install-recommends|-y|-q|--|rm|-rf|\\\\)$' | sort -u | while IFS= read -r pkg; do
    is_valid_package_name "${pkg}" && printf '%s\n' "${pkg}"
  done || true
}

parse_apk_packages() {
  local dockerfile="$1"
  sed ':a;N;$!ba;s/\\\n/ /g' "${dockerfile}" | grep -oP 'apk add[^|&;]*' | sed 's/apk add\s*//' | sed 's/--no-cache//g' | tr ' ' '\n' | grep -vP '^(apk|add|--no-cache|--|&&|\\\\)$' | sort -u | while IFS= read -r pkg; do
    is_valid_package_name "${pkg}" && printf '%s\n' "${pkg}"
  done || true
}

parse_base_images() {
  local dockerfile="$1"
  grep -oP '^FROM \K[^\s]+' "${dockerfile}" | sort -u || true
}

parse_curl_downloads() {
  local dockerfile="$1"
  grep -oP 'curl\b[^|&;]*-o\s+\K/\S+' "${dockerfile}" | sort -u || true
}

parse_go_modules() {
  local gomod="$1"
  if [[ -f "${gomod}" ]]; then
    grep -vP '^\s*(module|go|require\s*\(|\)|replace\s)' "${gomod}" | grep -vP '^\s*$' | grep -vP '^\s*//' | awk '{print $1}' | sort -u || true
  fi
}

parse_manifest() {
  local manifest="$1"
  if [[ ! -f "${manifest}" ]]; then
    return
  fi
  grep -oP '^\s+builder_packages\s*=\s*\[([^\]]*)\]' "${manifest}" | grep -oP '"[^"]*"' | tr -d '"' | sort -u || true
  grep -oP '^\s+runtime_packages\s*=\s*\[([^\]]*)\]' "${manifest}" | grep -oP '"[^"]*"' | tr -d '"' | sort -u || true
}

if [[ -f "${IMAGE_DIR}/manifest.toml" ]]; then
  echo "Parsing manifest.toml for ${IMAGE}..."
  while IFS= read -r pkg; do
    [[ -n "${pkg}" ]] && PACKAGES+=("${pkg}")
  done < <(parse_manifest "${IMAGE_DIR}/manifest.toml")

  base_img=$(grep -oP '^\s+image\s*=\s*"\K[^"]+' "${IMAGE_DIR}/manifest.toml" 2>/dev/null || true)
  [[ -n "${base_img}" ]] && BASE_IMAGES+=("${base_img}")

  vendor=$(grep -oP '^\s*vendor\s*=\s*"\K[^"]+' "${IMAGE_DIR}/manifest.toml" 2>/dev/null || echo "unknown")
  version=$(grep -oP '^\s*version\s*=\s*"\K[^"]+' "${IMAGE_DIR}/manifest.toml" 2>/dev/null || echo "unknown")

  source_url=$(grep -oP '^\s*url\s*=\s*"\K[^"]+' "${IMAGE_DIR}/manifest.toml" 2>/dev/null || true)
  if [[ -n "${source_url}" ]]; then
    binary_name=$(basename "${source_url}" | sed 's/\.tar\.\(gz\|xz\|bz2\)$//' | sed 's/\.zip$//')
    DOWNLOADED_BINARIES+=("${binary_name}|${source_url}")
  fi
fi

if [[ -f "${IMAGE_DIR}/Dockerfile" ]]; then
  echo "Parsing Dockerfile for ${IMAGE}..."
  if [[ ${#PACKAGES[@]} -eq 0 ]]; then
    while IFS= read -r pkg; do
      [[ -n "${pkg}" ]] && PACKAGES+=("apt:${pkg}")
    done < <(parse_apt_packages "${IMAGE_DIR}/Dockerfile")
    while IFS= read -r pkg; do
      [[ -n "${pkg}" ]] && PACKAGES+=("apk:${pkg}")
    done < <(parse_apk_packages "${IMAGE_DIR}/Dockerfile")
  fi

  if [[ ${#BASE_IMAGES[@]} -eq 0 ]]; then
    while IFS= read -r img; do
      [[ -n "${img}" ]] && BASE_IMAGES+=("${img}")
    done < <(parse_base_images "${IMAGE_DIR}/Dockerfile")
  fi

  if [[ ${#DOWNLOADED_BINARIES[@]} -eq 0 ]]; then
    while IFS= read -r bin; do
      [[ -n "${bin}" ]] && DOWNLOADED_BINARIES+=("$(basename "${bin}")|curl-download")
    done < <(parse_curl_downloads "${IMAGE_DIR}/Dockerfile")
  fi

  [[ -z "${version}" ]] && version=$(extract_version "${IMAGE_DIR}/Dockerfile")
  [[ -z "${vendor}" || "${vendor}" == "unknown" ]] && vendor=$(extract_vendor "${IMAGE_DIR}/Dockerfile")
fi

if [[ -f "${IMAGE_DIR}/go.mod" ]]; then
  echo "Parsing go.mod for ${IMAGE}..."
  while IFS= read -r mod; do
    [[ -n "${mod}" ]] && GO_MODULES+=("${mod}")
  done < <(parse_go_modules "${IMAGE_DIR}/go.mod")
fi

echo "Generating SPDX 2.3 SBOM..."
echo "  Version: ${version:-unknown}"
echo "  Vendor:  ${vendor:-unknown}"
echo "  Base images: ${#BASE_IMAGES[@]}"
echo "  Packages: ${#PACKAGES[@]}"
echo "  Downloaded binaries: ${#DOWNLOADED_BINARIES[@]}"
echo "  Go modules: ${#GO_MODULES[@]}"

declare -a ALL_PACKAGE_JSON=()

if [[ ${#BASE_IMAGES[@]} -gt 0 ]]; then
  for img in "${BASE_IMAGES[@]}"; do
    local_img="$(json_escape "${img}")"
    base_ref="SPDXRef-Package-$(echo "${img}" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9-.' '-')"
    ALL_PACKAGE_JSON+=("{\"SPDXID\":\"${base_ref}\",\"name\":\"${local_img}\",\"downloadLocation\":\"NOASSERTION\",\"filesAnalyzed\":false,\"primaryPackagePurpose\":\"CONTAINER\",\"originator\":\"NOASSERTION\"}")
  done
fi

if [[ ${#PACKAGES[@]} -gt 0 ]]; then
  for pkg in "${PACKAGES[@]}"; do
    pkg_type="generic"
    pkg_name="${pkg}"
    if [[ "${pkg}" == apt:* ]]; then
      pkg_name="${pkg#apt:}"
      pkg_type="debian"
    elif [[ "${pkg}" == apk:* ]]; then
      pkg_name="${pkg#apk:}"
      pkg_type="alpine"
    fi
    is_valid_package_name "${pkg_name}" || continue
    local_pkg_name="$(json_escape "${pkg_name}")"
    local_pkg_type="$(json_escape "${pkg_type}")"
    pkg_ref="SPDXRef-Package-${IMAGE}-$(echo "${pkg_name}" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '-')"
    ALL_PACKAGE_JSON+=("{\"SPDXID\":\"${pkg_ref}\",\"name\":\"${local_pkg_name}\",\"downloadLocation\":\"NOASSERTION\",\"filesAnalyzed\":false,\"primaryPackagePurpose\":\"INSTALLATION\",\"originator\":\"NOASSERTION\",\"externalRefs\":[{\"referenceCategory\":\"PACKAGE-MANAGER\",\"referenceType\":\"purl\",\"referenceLocator\":\"pkg:${local_pkg_type}/${local_pkg_name}\"}]}")
  done
fi

if [[ ${#DOWNLOADED_BINARIES[@]} -gt 0 ]]; then
  for entry in "${DOWNLOADED_BINARIES[@]}"; do
    bin_name="${entry%%|*}"
    bin_url="${entry##*|}"
    local_bin_name="$(json_escape "${bin_name}")"
    local_bin_url="$(json_escape "${bin_url}")"
    local_vendor="$(json_escape "${vendor:-NOASSERTION}")"
    bin_ref="SPDXRef-Package-${IMAGE}-$(echo "${bin_name}" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9-.' '-')"
    ALL_PACKAGE_JSON+=("{\"SPDXID\":\"${bin_ref}\",\"name\":\"${local_bin_name}\",\"downloadLocation\":\"${local_bin_url}\",\"filesAnalyzed\":false,\"primaryPackagePurpose\":\"APPLICATION\",\"originator\":\"${local_vendor}\"}")
  done
fi

if [[ ${#GO_MODULES[@]} -gt 0 ]]; then
  for mod in "${GO_MODULES[@]}"; do
    local_mod="$(json_escape "${mod}")"
    mod_ref="SPDXRef-Package-${IMAGE}-$(echo "${mod}" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9-.' '-')"
    ALL_PACKAGE_JSON+=("{\"SPDXID\":\"${mod_ref}\",\"name\":\"${local_mod}\",\"downloadLocation\":\"NOASSERTION\",\"filesAnalyzed\":false,\"primaryPackagePurpose\":\"LIBRARY\",\"originator\":\"NOASSERTION\",\"externalRefs\":[{\"referenceCategory\":\"PACKAGE-MANAGER\",\"referenceType\":\"purl\",\"referenceLocator\":\"pkg:golang/${local_mod}\"}]}")
  done
fi

pkgs_array="["
first=true
for p in "${ALL_PACKAGE_JSON[@]}"; do
  ${first} && first=false || pkgs_array+=","
  pkgs_array+="${p}"
done
pkgs_array+="]"

if command -v jq >/dev/null 2>&1; then
  jq -n \
    --arg spdx "${SPDX_VERSION}" \
    --arg license "${DATA_LICENSE}" \
    --arg docid "SPDXRef-DOCUMENT-${IMAGE}" \
    --arg name "evergreen-${IMAGE}" \
    --arg ns "${NAMESPACE}" \
    --arg ts "${TIMESTAMP}" \
    --argjson pkgs "${pkgs_array}" \
    '{
      spdxVersion: $spdx,
      dataLicense: $license,
      SPDXID: $docid,
      name: $name,
      documentNamespace: $ns,
      creationInfo: {
        created: $ts,
        creators: ["Tool: evergreen-sbom-generator"]
      },
      packages: $pkgs,
      relationships: [
        {
          spdxElementId: $docid,
          relationshipType: "DESCRIBES",
          relatedSpdxElement: ("SPDXRef-Package-" + ($name | split("-") | .[1]))
        }
      ]
    }' > "${OUTPUT}"
else
  python3 -c "
import json, sys
doc = {
    'spdxVersion': '${SPDX_VERSION}',
    'dataLicense': '${DATA_LICENSE}',
    'SPDXID': 'SPDXRef-DOCUMENT-${IMAGE}',
    'name': 'evergreen-${IMAGE}',
    'documentNamespace': '${NAMESPACE}',
    'creationInfo': {
        'created': '${TIMESTAMP}',
        'creators': ['Tool: evergreen-sbom-generator']
    },
    'packages': json.loads('${pkgs_array}'),
    'relationships': [
        {
            'spdxElementId': 'SPDXRef-DOCUMENT-${IMAGE}',
            'relationshipType': 'DESCRIBES',
            'relatedSpdxElement': 'SPDXRef-Package-${IMAGE}'
        }
    ]
}
json.dump(doc, sys.stdout, indent=2)
print()
" > "${OUTPUT}"
fi

echo "SBOM written to ${OUTPUT}"
