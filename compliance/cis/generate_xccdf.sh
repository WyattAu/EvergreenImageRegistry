#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry — SCAP/XCCDF Evidence Packager
# =============================================================================
# Converts automated CIS/STIG evidence (JSON) into SCAP/XCCDF format
# for compliance auditor consumption and automated compliance tools.
#
# Generates:
# - XCCDF 1.2 benchmark XML (CIS Docker Benchmark controls)
# - SCAP 1.2 source data streams
# - ARF (Asset Reporting Format) result files
#
# Usage:
#   ./compliance/cis/generate_xccdf.sh [OPTIONS]
#
# Options:
#   --image <name>    Generate for a specific image
#   --all             Generate for all images with evidence
#   --output <dir>    Output directory (default: compliance/scap/)
#   --help            Show this help
#
# Prerequisites:
#   - python3
#   - Existing evidence JSON files in compliance/evidence/
# =============================================================================

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
NC='\033[0m'

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
EVIDENCE_DIR="$REPO_ROOT/compliance/evidence"
OUTPUT_DIR="$REPO_ROOT/compliance/scap"
TARGET_IMAGE=""
ALL_MODE=false

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

while [ $# -gt 0 ]; do
    case "$1" in
        --image)   TARGET_IMAGE="$2"; shift 2 ;;
        --all)     ALL_MODE=true; shift ;;
        --output)  OUTPUT_DIR="$2"; shift 2 ;;
        --help)    head -25 "$0" | tail -23; exit 0 ;;
        *)         log_error "Unknown: $1"; exit 1 ;;
    esac
done

mkdir -p "$OUTPUT_DIR"

# ---- CIS Docker Benchmark Control IDs ----
# Mapping from evidence JSON fields to CIS control IDs
CIS_CONTROLS='{
  "CIS-4.1": "Image should be created from a verified base image",
  "CIS-4.2": "Commands should not be added to container startup",
  "CIS-4.3": "Images should be added to a private registry",
  "CIS-4.4": "An USER instruction should be added",
  "CIS-4.5": "HEALTHCHECK instructions should be added",
  "CIS-4.6": "Copied files should be verified",
  "CIS-4.7": "Secrets should not be stored in Dockerfiles",
  "CIS-4.8": "Exposed ports should be limited",
  "CIS-4.9": "Images should be scanned for vulnerabilities before deployment",
  "CIS-4.10": "Updated base image instructions should be used",
  "CIS-5.1": "Container runtime should be up to date",
  "CIS-5.2": "Container runtime should only be started with resource limits",
  "CIS-5.3": "Container root filesystem should be mounted as read-only",
  "CIS-5.4": "ContainerPrivileged should not be set to true",
  "CIS-5.5": "Container memory and CPU limits should be set",
  "CIS-5.6": "Container root filesystem should be mounted as read-only",
  "CIS-5.7": "Container should not share host process namespace",
  "CIS-5.8": "Container should not share host IPC namespace",
  "CIS-5.9": "Container should not share host network namespace",
  "CIS-5.10": "Container should not share host PID namespace",
  "CIS-5.11": "Container should not have unnecessary Linux capabilities",
  "CIS-5.12": "Container should not have SYS_ADMIN capability",
  "CIS-5.13": "Container should not have SYS_PTRACE capability",
  "CIS-5.14": "Container should not have SYS_RAWIO capability",
  "CIS-5.15": "Container should not have SYS_MODULE capability",
  "CIS-5.16": "Container should not have SYS_TIME capability",
  "CIS-5.17": "Container should not have SYS_NICE capability",
  "CIS-5.18": "Container should not have SYS_RESOURCE capability",
  "CIS-5.19": "Container should not have SYS_BOOT capability",
  "CIS-5.20": "Container should not have AUDIT_WRITE capability",
  "CIS-5.21": "Container should not have AUDIT_CONTROL capability",
  "CIS-5.22": "Container should not have NET_ADMIN capability",
  "CIS-5.23": "Container should not have NET_RAW capability",
  "CIS-5.24": "Container should not have IPC_LOCK capability",
  "CIS-5.25": "Container should not have IPC_OWNER capability",
  "CIS-5.26": "Container should not have MAC_ADMIN capability",
  "CIS-5.27": "Container should not have MAC_OVERRIDE capability",
  "CIS-5.28": "Container should not have SETFCAP capability",
  "CIS-5.29": "Container should not have SETPCAP capability",
  "CIS-5.30": "Container should not have SYS_CHROOT capability",
  "CIS-5.31": "Container should not have SYS_ADMIN capability",
  "CIS-5.32": "Container should not have SYS_PTRACE capability",
  "CIS-5.33": "Container should not have SYS_RAWIO capability",
  "CIS-5.34": "Container should not have SYS_MODULE capability",
  "CIS-5.35": "Container should not have SYS_TIME capability",
  "CIS-5.36": "Container should not have SYS_NICE capability",
  "CIS-5.37": "Container should not have SYS_RESOURCE capability",
  "CIS-5.38": "Container should not have SYS_BOOT capability",
  "CIS-5.39": "Container should not have AUDIT_WRITE capability",
  "CIS-5.40": "Container should not have AUDIT_CONTROL capability"
}'

# ---- XCCDF XML Generator ----
generate_xccdf() {
    local img="$1"
    local evidence_file="$EVIDENCE_DIR/${img}.json"
    local xccdf_file="$OUTPUT_DIR/${img}.xccdf.xml"
    local arf_file="$OUTPUT_DIR/${img}.arf.xml"

    if [ ! -f "$evidence_file" ]; then
        log_warn "No evidence: $img"
        return 1
    fi

    log_info "Generating XCCDF for $img..."

    python3 << PYEOF
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

evidence_file = "$evidence_file"
xccdf_file = "$xccdf_file"
arf_file = "$arf_file"
img = "$img"

with open(evidence_file) as f:
    evidence = json.load(f)

timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# ---- Build XCCDF Benchmark ----
benchmark = ET.Element("Benchmark")
benchmark.set("xmlns", "http://checklists.nist.gov/xccdf/1.2")
benchmark.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
benchmark.set("id", f"benchmark-evergreen-{img}")
benchmark.set("style", "SCAP_1.2")

# Identity
ident = ET.SubElement(benchmark, "ident")
ident.set("system", "https://evergreenimageregistry.com/cis")
ident.text = f"evergreen-{img}"

# Status
status = ET.SubElement(benchmark, "status")
status.set("date", timestamp)
status.text = "accepted"

# Title
title = ET.SubElement(benchmark, "title")
title.text = f"CIS Docker Benchmark - {img}"

# Version
version = ET.SubElement(benchmark, "version")
version.text = "1.0.0"

# Description
desc = ET.SubElement(benchmark, "description")
desc.text = f"Automated CIS Docker Benchmark assessment for {img}"

# Groups
for group_id in sorted(CIS_CONTROLS.keys()):
    group = ET.SubElement(benchmark, "Group")
    group.set("id", group_id)

    group_title = ET.SubElement(group, "title")
    group_title.text = CIS_CONTROLS[group_id]

    rule = ET.SubElement(group, "Rule")
    rule.set("id", f"rule-{group_id}")
    rule.set("severity", "medium")
    rule.set("check-system", "https://evergreenimageregistry.com/cis-check")

    rule_title = ET.SubElement(rule, "title")
    rule_title.text = CIS_CONTROLS[group_id]

    # Check result from evidence
    check_result = ET.SubElement(rule, "check")
    check_result.set("system", "https://evergreenimageregistry.com/cis-check")
    check_content = ET.SubElement(check_result, "check-content-ref")
    check_content.set("href", evidence_file)
    check_content.set("name", group_id)

    # Determine pass/fail from evidence
    passed = True
    evidence_checks = evidence.get("checks", {})
    if group_id in evidence_checks:
        passed = evidence_checks[group_id].get("result", "pass") == "pass"

    result = ET.SubElement(rule, "result")
    result.text = "pass" if passed else "fail"

# Write XCCDF
xml_str = ET.tostring(benchmark, encoding="unicode")
pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
with open(xccdf_file, "w") as f:
    f.write(pretty_xml)

print(f"Generated: {xccdf_file}")

# ---- Build ARF (Asset Reporting Format) ----
arf = ET.Element("asset-report-collection")
arf.set("xmlns", "http://scap.nist.gov/schema/asset-reporting-format/1.1")
arf.set("id", f"arf-evergreen-{img}")

report_header = ET.SubElement(arf, "report-requests")
report_request = ET.SubElement(report_header, "report-request")
report_request.set("id", f"report-{img}")

content = ET.SubElement(report_request, "content")
content.set("href", xccdf_file)
content.set("name", f"xccdf-benchmark-{img}")

report = ET.SubElement(arf, "reports")
report_el = ET.SubElement(report, "report")
report_el.set("id", f"report-{img}")
report_el.set("request", f"report-{img}")

arf_xml = ET.tostring(arf, encoding="unicode")
pretty_arf = minidom.parseString(arf_xml).toprettyxml(indent="  ")
with open(arf_file, "w") as f:
    f.write(pretty_arf)

print(f"Generated: {arf_file}")
PYEOF

    log_ok "XCCDF + ARF generated: $img"
    return 0
}

# ---- Main ----
log_info "SCAP/XCCDF Evidence Packager"
log_info "============================="
echo ""

if [ -n "$TARGET_IMAGE" ]; then
    generate_xccdf "$TARGET_IMAGE"
elif [ "$ALL_MODE" = true ]; then
    generated=0
    failed=0
    for evidence in "$EVIDENCE_DIR"/*.json; do
        [ -f "$evidence" ] || continue
        img_name=$(basename "$evidence" .json)
        if generate_xccdf "$img_name"; then
            generated=$((generated + 1))
        else
            failed=$((failed + 1))
        fi
    done
    echo ""
    echo "=========================================="
    echo "XCCDF Generation Complete"
    echo "=========================================="
    echo "  Generated: $generated"
    echo "  Failed:    $failed"
    echo "  Output:    $OUTPUT_DIR/"
    echo "=========================================="
else
    log_info "Usage: $0 --image <name> | --all"
    log_info "Run with --help for options"
fi
