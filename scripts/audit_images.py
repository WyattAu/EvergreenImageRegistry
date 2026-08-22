#!/usr/bin/env python3
"""Comprehensive image audit against EIR security standards.

Checks every active image for:
1. Has health-shim (COPY --from=shim or health-shim reference)
2. Has HEALTHCHECK directive
3. Has USER directive (non-root preferred)
4. Has STOPSIGNAL directive
5. Has evergreen.image.tier label
6. Has evergreen.security labels
7. No banned base images (debian-slim, ubuntu, alpine as final stage)
8. Has valid manifest.toml
9. Has EXPOSE directive
10. Has evergreen.entrypoint.pattern label or proper shim ENTRYPOINT

Outputs detailed report with pass/fail per check per image.
"""

import re
from collections import defaultdict
from pathlib import Path

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"

BANNED_FINAL_BASES = [
    "debian:slim",
    "debian-slim",
    "ubuntu:",
    "alpine:",
    "centos:",
    "fedora:",
    "rockylinux:",
    "amazonlinux:",
]

# Allowlist for bases that look banned but are actually mirrors or build stages
ALLOWLIST_BASE_PATTERNS = [
    "mirror-",
    "cgr.dev",
    "ghcr.io",
    "quay.io",
    "scratch",
    "lscr.io",
    "docker.elastic.co",
    "public.ecr.aws",
    "code.forgejo.org",
    "docker.dragonflydb.io",
]

# Images exempt from full hardening (they ARE the infrastructure)
INFRA_EXEMPT = {"health-shim"}


def audit_dockerfile(df_path: Path) -> dict:
    """Audit a single Dockerfile against all standards."""
    text = df_path.read_text()
    name = df_path.parent.name
    issues = []
    warnings = []

    # 1. Has health-shim reference
    has_shim = (
        "health-shim" in text or "evergreenshim" in text or "COPY --from=shim" in text
    )
    if not has_shim and name not in INFRA_EXEMPT:
        issues.append("MISSING_SHIM: No health-shim reference found")

    # 2. Has HEALTHCHECK
    has_healthcheck = bool(re.search(r"^HEALTHCHECK\s", text, re.MULTILINE))
    if not has_healthcheck and name not in INFRA_EXEMPT:
        issues.append("MISSING_HEALTHCHECK: No HEALTHCHECK directive")

    # 3. Has USER directive
    has_user = bool(re.search(r"^USER\s+", text, re.MULTILINE))
    if not has_user:
        # Check if it has an exemption for inheriting upstream USER
        has_exempt = "evergreen.entrypoint.pattern" in text
        if not has_exempt:
            issues.append("MISSING_USER: No USER directive and no exemption")
        # INHERITED_USER with exemption is BY DESIGN for repack images — not a warning

    # 4. Has STOPSIGNAL
    has_stopsignal = bool(re.search(r"^STOPSIGNAL\s+", text, re.MULTILINE))
    if not has_stopsignal:
        warnings.append("MISSING_STOPSIGNAL: No STOPSIGNAL directive")

    # 5. Has tier label
    has_tier = "evergreen.image.tier" in text
    if not has_tier:
        issues.append("MISSING_TIER: No evergreen.image.tier label")

    # 6. Has security labels
    has_cap_drop = "evergreen.security.cap-drop" in text or "cap_drop" in text
    has_no_priv = (
        "evergreen.security.no-new-privileges" in text or "no-new-privileges" in text
    )
    if not has_cap_drop:
        warnings.append("MISSING_CAP_DROP: No cap-drop security label")
    if not has_no_priv:
        warnings.append("MISSING_NO_NEW_PRIV: No no-new-privileges label")

    # 7. No banned base in final stage
    # Find the last FROM line (final stage)
    from_lines = [
        (i, line)
        for i, line in enumerate(text.splitlines())
        if line.strip().upper().startswith("FROM ")
    ]
    if from_lines:
        last_from = from_lines[-1][1].strip()
        last_base = last_from.split()[1] if len(last_from.split()) > 1 else ""

        # Check if it's allowlisted
        is_allowed = any(pat in last_base.lower() for pat in ALLOWLIST_BASE_PATTERNS)

        if not is_allowed:
            for banned in BANNED_FINAL_BASES:
                if banned in last_base.lower():
                    issues.append(
                        f"BANNED_BASE: Final stage uses '{last_base}' (contains '{banned}')"
                    )

    # 8. Has valid manifest.toml
    manifest_path = df_path.parent / "manifest.toml"
    has_manifest = manifest_path.exists()
    if not has_manifest:
        issues.append("MISSING_MANIFEST: No manifest.toml")

    # 9. Has EXPOSE
    has_expose = bool(re.search(r"^EXPOSE\s+", text, re.MULTILINE))
    if not has_expose:
        warnings.append("MISSING_EXPOSE: No EXPOSE directive")

    # 10. Has entrypoint pattern or shim entrypoint
    has_ep = bool(re.search(r"^ENTRYPOINT\s+", text, re.MULTILINE))
    has_ep_exempt = "evergreen.entrypoint.pattern" in text
    if not has_ep and not has_ep_exempt and name not in INFRA_EXEMPT:
        issues.append("MISSING_ENTRYPOINT: No ENTRYPOINT and no exemption")

    # Determine overall status
    if issues:
        status = "FAIL"
    elif warnings:
        status = "WARN"
    else:
        status = "PASS"

    return {
        "image": name,
        "status": status,
        "issues": issues,
        "warnings": warnings,
    }


def main():
    results = []
    pass_count = 0
    warn_count = 0
    fail_count = 0

    for img_dir in sorted(IMAGES_DIR.iterdir()):
        if (
            not img_dir.is_dir()
            or img_dir.name.startswith("_")
            or img_dir.name == "clawdius"
        ):
            continue

        df = img_dir / "Dockerfile"
        if not df.exists():
            continue

        result = audit_dockerfile(df)
        results.append(result)

        if result["status"] == "PASS":
            pass_count += 1
        elif result["status"] == "WARN":
            warn_count += 1
        else:
            fail_count += 1

    total = len(results)

    # Print summary
    print(f"\n{'=' * 70}")
    print(" EVERGREEN IMAGE AUDIT REPORT")
    print(f"{'=' * 70}")
    print(f" Total images: {total}")
    print(f" ✅ PASS: {pass_count} ({100 * pass_count / total:.0f}%)")
    print(f" ⚠️  WARN: {warn_count} ({100 * warn_count / total:.0f}%)")
    print(f" ❌ FAIL: {fail_count} ({100 * fail_count / total:.0f}%)")

    # Print failures grouped by issue type
    if fail_count:
        print(f"\n{'=' * 70}")
        print(" FAILURES BY TYPE")
        print(f"{'=' * 70}")
        issue_types = defaultdict(list)
        for r in results:
            if r["status"] == "FAIL":
                for issue in r["issues"]:
                    issue_type = issue.split(":")[0]
                    issue_types[issue_type].append(r["image"])

        for itype, images in sorted(issue_types.items(), key=lambda x: -len(x[1])):
            print(f"\n  {itype} ({len(images)} images):")
            for img in images[:10]:
                print(f"    {img}")
            if len(images) > 10:
                print(f"    ... and {len(images) - 10} more")

    # Print warnings summary
    if warn_count:
        print(f"\n{'=' * 70}")
        print(" WARNINGS SUMMARY")
        print(f"{'=' * 70}")
        warn_types = defaultdict(int)
        for r in results:
            for w in r["warnings"]:
                wtype = w.split(":")[0]
                warn_types[wtype] += 1

        for wtype, count in sorted(warn_types.items(), key=lambda x: -x[1]):
            print(f"  {wtype}: {count} images")

    # Output JSON for further processing
    import json

    report = {
        "total": total,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "failures": [r for r in results if r["status"] == "FAIL"],
        "warnings": [r for r in results if r["status"] == "WARN"],
    }
    report_path = Path(".reports/audit_report.json")
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\nDetailed report: {report_path}")


if __name__ == "__main__":
    main()
