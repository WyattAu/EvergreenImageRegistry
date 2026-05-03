#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
IMAGE_DIR="${REPO_ROOT}/images"
GENERATOR="${SCRIPT_DIR}/generate_sbom.sh"

SKIP_UNCHANGED="${SKIP_UNCHANGED:-true}"

total=0
success=0
skipped=0
cached=0
failed=0
failed_list=""

for image_dir in "${IMAGE_DIR}"/*/; do
  image_name="$(basename "${image_dir}")"

  has_dockerfile=false
  has_manifest=false

  [[ -f "${image_dir}/Dockerfile" ]] && has_dockerfile=true
  [[ -f "${image_dir}/manifest.toml" ]] && has_manifest=true

  if ! ${has_dockerfile} && ! ${has_manifest}; then
    ((skipped++)) || true
    continue
  fi

  sbom_file="${image_dir}/sbom.spdx.json"

  if [[ "${SKIP_UNCHANGED}" == "true" && -f "${sbom_file}" ]]; then
    newest_source=""
    [[ "${has_dockerfile}" == "true" ]] && newest_source="${image_dir}/Dockerfile"
    [[ "${has_manifest}" == "true" ]] && {
      if [[ -z "${newest_source}" ]] || [[ "${image_dir}/manifest.toml" -nt "${newest_source}" ]]; then
        newest_source="${image_dir}/manifest.toml"
      fi
    }
    if [[ -n "${newest_source}" ]] && [[ "${sbom_file}" -nt "${newest_source}" ]]; then
      echo "SKIP (cached): ${image_name}"
      ((cached++)) || true
      continue
    fi
  fi

  ((total++)) || true
  echo ""
  echo "=== [$total] Processing: ${image_name} ==="

  if bash "${GENERATOR}" "${image_name}"; then
    ((success++)) || true
  else
    ((failed++)) || true
    failed_list+="  - ${image_name}\n"
    echo "WARN: Failed to generate SBOM for ${image_name}" >&2
  fi
done

echo ""
echo "========================================"
echo "SBOM Generation Summary"
echo "========================================"
echo "  Processed: ${total}"
echo "  Cached:    ${cached}"
echo "  Skipped:   ${skipped}"
echo "  Succeeded: ${success}"
echo "  Failed:    ${failed}"

if [[ ${failed} -gt 0 ]]; then
  echo ""
  echo "Failed images:"
  echo -e "${failed_list}"
  exit 1
fi

echo ""
echo "All SBOMs generated successfully."
