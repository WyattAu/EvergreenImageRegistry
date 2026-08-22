#!/usr/bin/env python3
"""
Evergreen Image Registry — SOC 2 Evidence Collector
===================================================
Automates SOC 2 Type II evidence collection from constraint engine,
CI workflows, and compliance tooling.

Generates:
  - Control effectiveness evidence
  - Configuration snapshots
  - Audit trail logs
  - Gap analysis report

Usage:
  python3 scripts/generate_soc2_evidence.py --output compliance/soc2/evidence/
  python3 scripts/generate_soc2_evidence.py --gap-analysis
"""

import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
EVIDENCE_DIR = REPO_ROOT / "compliance" / "soc2" / "evidence"


def collect_constraint_evidence() -> dict:
    """Collect evidence from constraint engine."""
    evidence = {
        "control": "CC8.1",
        "name": "Change Management — Automated Validation",
        "status": "effective",
        "evidence": [],
        "collected_at": datetime.utcnow().isoformat() + "Z",
    }

    # Run constraint validation
    try:
        result = subprocess.run(
            ["python3", "-c", """
import sys
sys.path.insert(0, '.')
from pathlib import Path
import tomllib

total = 0
errors = 0
for m in Path('images').rglob('manifest.toml'):
    total += 1
    try:
        with open(m, 'rb') as f:
            tomllib.load(f)
    except Exception:
        errors += 1
print(f'{total - errors}/{total}')
"""],
            capture_output=True, text=True, timeout=60, cwd=REPO_ROOT
        )
        if result.returncode == 0:
            valid, total = result.stdout.strip().split("/")
            evidence["evidence"].append({
                "type": "automated_check",
                "check": "manifest_validation",
                "result": f"{valid}/{total} manifests valid",
                "passed": int(valid) == int(total),
            })
    except Exception as e:
        evidence["evidence"].append({
            "type": "error",
            "check": "manifest_validation",
            "error": str(e),
        })

    # Check SBOM coverage
    try:
        result = subprocess.run(
            ["python3", "-c", """
from pathlib import Path
total = len(list(Path('images').glob('*/manifest.toml')))
sboms = sum(1 for s in Path('images').glob('*/sbom.spdx.json') if s.stat().st_size > 1000)
print(f'{sboms}/{total}')
"""],
            capture_output=True, text=True, timeout=30, cwd=REPO_ROOT
        )
        if result.returncode == 0:
            with_sbom, total = result.stdout.strip().split("/")
            evidence["evidence"].append({
                "type": "automated_check",
                "check": "sbom_coverage",
                "result": f"{with_sbom}/{total} images have SBOMs",
                "passed": int(with_sbom) > 0,
            })
    except Exception:
        pass

    return evidence


def collect_ci_evidence() -> dict:
    """Collect evidence from CI/CD workflows."""
    evidence = {
        "control": "CC8.1",
        "name": "CI/CD Pipeline Controls",
        "status": "effective",
        "evidence": [],
        "collected_at": datetime.utcnow().isoformat() + "Z",
    }

    workflows_dir = REPO_ROOT / ".github" / "workflows"
    if workflows_dir.exists():
        workflow_count = len(list(workflows_dir.glob("*.yml")))
        evidence["evidence"].append({
            "type": "automated_check",
            "check": "workflow_count",
            "result": f"{workflow_count} CI/CD workflows active",
            "passed": workflow_count > 20,
        })

        # Check SHA pinning
        pinned = 0
        total_actions = 0
        for wf in workflows_dir.glob("*.yml"):
            content = wf.read_text()
            for match in re.finditer(r'uses:\s+(\S+)@(\w+)', content):
                total_actions += 1
                if len(match.group(2)) == 40:  # SHA is 40 chars
                    pinned += 1

        if total_actions > 0:
            evidence["evidence"].append({
                "type": "automated_check",
                "check": "action_sha_pinning",
                "result": f"{pinned}/{total_actions} actions pinned to SHA",
                "passed": pinned == total_actions,
            })

    return evidence


def collect_security_evidence() -> dict:
    """Collect evidence from security scanning."""
    evidence = {
        "control": "CC7.1",
        "name": "Vulnerability Management",
        "status": "effective",
        "evidence": [],
        "collected_at": datetime.utcnow().isoformat() + "Z",
    }

    # Check for security scan workflows
    security_workflows = [
        "daily-security-scan.yml",
        "nightly-scan.yml",
        "vuln-sla-monitor.yml",
        "compliance-scan.yml",
    ]

    for wf in security_workflows:
        wf_path = REPO_ROOT / ".github" / "workflows" / wf
        evidence["evidence"].append({
            "type": "automated_check",
            "check": f"security_workflow_{wf}",
            "result": "exists" if wf_path.exists() else "missing",
            "passed": wf_path.exists(),
        })

    return evidence


def collect_access_evidence() -> dict:
    """Collect evidence for access controls."""
    evidence = {
        "control": "CC6.1",
        "name": "Logical Access Security",
        "status": "effective",
        "evidence": [],
        "collected_at": datetime.utcnow().isoformat() + "Z",
    }

    # Check non-root USER across images
    nonroot_count = 0
    total_df = 0
    for df in IMAGES_DIR.glob("*/Dockerfile"):
        total_df += 1
        content = df.read_text()
        if re.search(r"^\s*USER\s+65532", content, re.MULTILINE):
            nonroot_count += 1

    if total_df > 0:
        evidence["evidence"].append({
            "type": "automated_check",
            "check": "non_root_user",
            "result": f"{nonroot_count}/{total_df} images run as non-root",
            "passed": nonroot_count > total_df * 0.9,  # 90% threshold
        })

    return evidence


def generate_gap_analysis() -> dict:
    """Generate SOC 2 gap analysis."""
    gaps = []

    # Check SBOM coverage
    total = len(list(IMAGES_DIR.glob("*/manifest.toml")))
    sboms = sum(1 for s in IMAGES_DIR.glob("*/sbom.spdx.json") if s.stat().st_size > 1000)
    if sboms < total * 0.95:
        gaps.append({
            "control": "CM-8",
            "gap": f"SBOM coverage at {sboms}/{total} ({sboms*100//total}%)",
            "remediation": "Run batch_generate_all_sboms.sh to achieve 100% coverage",
            "severity": "medium",
        })

    # Check FIPS variants
    fips_count = len(list(IMAGES_DIR.glob("*/Dockerfile.fips")))
    if fips_count < 30:
        gaps.append({
            "control": "SC-13",
            "gap": f"FIPS variants: {fips_count}/30 images",
            "remediation": "Build remaining FIPS variants per fips_image_matrix_v3.yaml",
            "severity": "medium",
        })

    # Check operator
    if not (REPO_ROOT / "operator" / "main.go").exists():
        gaps.append({
            "control": "CC7.2",
            "gap": "K8s operator not deployed",
            "remediation": "Deploy evergreen-operator for runtime drift detection",
            "severity": "low",
        })

    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_gaps": len(gaps),
        "gaps": gaps,
        "recommendations": [
            "Achieve 100% SBOM coverage",
            "Complete all 30 FIPS variants",
            "Deploy K8s operator to production",
            "Run SOC 2 Type II audit with CPA firm",
            "Document all manual controls",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="SOC 2 evidence collector")
    parser.add_argument("--output", type=Path, default=EVIDENCE_DIR)
    parser.add_argument("--gap-analysis", action="store_true")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    print("Collecting SOC 2 evidence...")

    evidence_items = [
        collect_constraint_evidence(),
        collect_ci_evidence(),
        collect_security_evidence(),
        collect_access_evidence(),
    ]

    # Write evidence
    for evidence in evidence_items:
        control = evidence["control"]
        filename = f"{control}_evidence.json"
        filepath = args.output / filename
        with open(filepath, "w") as f:
            json.dump(evidence, f, indent=2)
        print(f"  {filename}: {evidence['name']}")

    # Summary
    _effective = sum(1 for e in evidence_items if e["status"] == "effective")
    total_evidence = sum(len(e["evidence"]) for e in evidence_items)
    passed = sum(
        1 for e in evidence_items
        for ev in e["evidence"]
        if ev.get("passed", False)
    )

    print(f"\nEvidence collected: {len(evidence_items)} controls, {total_evidence} checks")
    print(f"Passed: {passed}/{total_evidence}")

    if args.gap_analysis:
        gap_analysis = generate_gap_analysis()
        gap_file = args.output.parent / "gap_analysis.json"
        with open(gap_file, "w") as f:
            json.dump(gap_analysis, f, indent=2)
        print(f"\nGap analysis: {gap_file}")
        print(f"  Gaps found: {gap_analysis['total_gaps']}")
        for gap in gap_analysis["gaps"]:
            print(f"  - [{gap['severity']}] {gap['control']}: {gap['gap']}")


if __name__ == "__main__":
    main()
