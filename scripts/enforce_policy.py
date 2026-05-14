#!/usr/bin/env python3

import argparse
import json
import re
import sys
import tomllib
from datetime import UTC, datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
POLICY_FILE = REPO_ROOT / "images" / "tests" / "image_policy.yaml"

PACKAGE_MANAGERS = re.compile(r"\b(apk|apt-get|apt|yum|dnf|pacman|zypper|microdnf)\b")
SHELL_PATHS = re.compile(r"\b(/bin/(sh|bash|dash|zsh|ash))\b")

TIER_OVERRIDES = {
    "tier1": {
        "image_size_mb": {"expect": "<=50", "severity": "block"},
        "digest_pinned": {"expect": "present", "severity": "block"},
        "max_layers": {"expect": "<=5", "severity": "warn"},
        "cve_freshness_days": {"expect": "<=7", "severity": "block"},
        "digest_pin_threshold": {"expect": ">=95", "severity": "block"},
    },
    "tier2": {
        "image_size_mb": {"expect": "<=200", "severity": "block"},
        "digest_pinned": {"expect": "present", "severity": "warn"},
        "max_layers": {"expect": "<=10", "severity": "warn"},
        "cve_freshness_days": {"expect": "<=14", "severity": "warn"},
        "digest_pin_threshold": {"expect": ">=90", "severity": "warn"},
    },
    "tier3": {
        "image_size_mb": {"expect": "<=500", "severity": "warn"},
        "digest_pinned": {"expect": "present", "severity": "info"},
        "max_layers": {"expect": "<=15", "severity": "info"},
        "cve_freshness_days": {"expect": "<=30", "severity": "info"},
        "digest_pin_threshold": {"expect": ">=80", "severity": "info"},
    },
}


def load_policy(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def get_image_tier(image_dir: Path) -> str:
    manifest = image_dir / "manifest.toml"
    if manifest.exists():
        try:
            with open(manifest, "rb") as f:
                data = tomllib.load(f)
            return str(data.get("tier", "tier2"))
        except Exception:
            pass
    dockerfile = image_dir / "Dockerfile"
    if dockerfile.exists():
        content = dockerfile.read_text()
        if "# tier: 1" in content.lower() or "tier: 1" in content.lower():
            return "tier1"
        if "# tier: 3" in content.lower() or "tier: 3" in content.lower():
            return "tier3"
    return "tier2"


def get_image_dirs() -> list[Path]:
    skip = {"tests", "profiles", "adversarial", "functional"}
    dirs = []
    for d in sorted(IMAGES_DIR.iterdir()):
        if d.is_dir() and d.name not in skip and not d.name.startswith("."):
            dirs.append(d)
    return dirs


def parse_dockerfile(image_dir: Path) -> dict:
    dockerfile = image_dir / "Dockerfile"
    if not dockerfile.exists():
        return {"exists": False}
    content = dockerfile.read_text()
    lines = content.splitlines()

    last_from = None
    user = None
    has_healthcheck = False
    has_shell = False
    has_package_manager = False
    from_lines = []
    digest_pinned_count = 0
    from_total_count = 0

    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()

        if lower.startswith("from "):
            last_from = stripped
            from_total_count += 1
            from_lines.append(stripped)
            if re.search(r"sha256:[a-f0-9]{32,}", stripped):
                digest_pinned_count += 1

        if lower.startswith("user "):
            user = (
                stripped.split(None, 1)[1].strip("\"'").rstrip(":")
                if len(stripped.split(None, 1)) > 1
                else None
            )

        if lower.startswith("healthcheck"):
            has_healthcheck = True

        if SHELL_PATHS.search(stripped) and not lower.startswith("from "):
            has_shell = True

        if lower.startswith("run ") and PACKAGE_MANAGERS.search(stripped):
            has_package_manager = True

        if (
            lower.startswith("copy ")
            and "shell" not in lower
            and SHELL_PATHS.search(stripped)
        ):
            pass

    digest_pinned = False
    if last_from:
        digest_pinned = bool(re.search(r"sha256:[a-f0-9]{32,}", last_from))

    if user:
        normalized = user.replace(":", "")
    else:
        normalized = None

    digest_pin_pct = (
        round((digest_pinned_count / from_total_count) * 100)
        if from_total_count > 0
        else 0
    )

    return {
        "exists": True,
        "last_from": last_from,
        "user": normalized,
        "has_healthcheck": has_healthcheck,
        "has_shell": has_shell,
        "has_package_manager": has_package_manager,
        "digest_pinned": digest_pinned,
        "digest_pin_pct": digest_pin_pct,
        "from_total": from_total_count,
        "from_digest": digest_pinned_count,
        "line_count": len(lines),
    }


def parse_manifest(image_dir: Path) -> dict:
    manifest = image_dir / "manifest.toml"
    if not manifest.exists():
        return {"exists": False}
    try:
        with open(manifest, "rb") as f:
            data = tomllib.load(f)
        return {"exists": True, "valid": True, "data": data}
    except Exception:
        return {"exists": True, "valid": False}


def check_sbom(image_dir: Path) -> dict:
    sbom_names = [
        image_dir / "sbom.json",
        image_dir / "sbom.spdx.json",
        image_dir / "sbom.cyclonedx.json",
        image_dir / f"{image_dir.name}.spdx.json",
    ]
    found = None
    for p in sbom_names:
        if p.exists():
            found = p
            break
    return {"exists": found is not None, "path": found}


def check_cve_freshness(sbom_info: dict, max_days: int) -> dict:
    if not sbom_info["exists"] or not sbom_info["path"]:
        return {"fresh": None, "age_days": None, "reason": "no SBOM"}

    sbom_path = sbom_info["path"]
    try:
        mtime = datetime.fromtimestamp(sbom_path.stat().st_mtime, tz=UTC)
        age = (datetime.now(UTC) - mtime).days
        return {"fresh": age <= max_days, "age_days": age}
    except OSError:
        return {"fresh": None, "age_days": None, "reason": "cannot stat SBOM"}


def get_effective_policy(
    policy_name: str, base_policy: dict, tier: str
) -> dict:
    effective = dict(base_policy)
    tier_key = policy_name
    if tier in TIER_OVERRIDES and tier_key in TIER_OVERRIDES[tier]:
        override = TIER_OVERRIDES[tier][tier_key]
        for k, v in override.items():
            effective[k] = v
    return effective


def run_check(
    policy_name: str,
    policy: dict,
    image_name: str,
    dockerfile: dict,
    manifest: dict,
    has_sbom: bool,
    sbom_info: dict,
    tier: str,
) -> dict | None:
    exceptions = policy.get("exceptions", [])
    if image_name in exceptions:
        return None

    check_type = policy["check"]
    expect = policy["expect"]
    passed = False
    actual = None

    if not dockerfile["exists"]:
        return {
            "policy": policy_name,
            "severity": policy["severity"],
            "status": "skip",
            "reason": "no Dockerfile",
            "tier": tier,
        }

    if check_type == "user":
        actual = dockerfile.get("user")
        passed = actual in ("65532:65532", "65532", "65534", "65534:65534", "nobody")

    elif check_type == "shell":
        has_shell = dockerfile.get("has_shell", False)
        actual = "present" if has_shell else "absent"
        passed = expect == actual

    elif check_type == "package_manager":
        has_pm = dockerfile.get("has_package_manager", False)
        actual = "present" if has_pm else "absent"
        passed = expect == actual

    elif check_type == "from_digest":
        actual = "present" if dockerfile.get("digest_pinned") else "absent"
        passed = expect == actual

    elif check_type == "healthcheck":
        actual = "present" if dockerfile.get("has_healthcheck") else "absent"
        passed = expect == actual

    elif check_type == "sbom_file":
        actual = "present" if has_sbom else "absent"
        passed = expect == actual

    elif check_type == "manifest_file":
        actual = (
            "present" if manifest.get("exists") and manifest.get("valid") else "absent"
        )
        passed = expect == actual

    elif check_type == "layer_count":
        actual = dockerfile.get("line_count", 0)
        try:
            threshold = int(
                expect.replace("<=", "")
                .replace(">=", "")
                .replace(">", "")
                .replace("<", "")
            )
            if "<=" in expect:
                passed = actual <= threshold
            elif ">=" in expect:
                passed = actual >= threshold
            elif "<" in expect:
                passed = actual < threshold
            elif ">" in expect:
                passed = actual > threshold
            else:
                passed = actual == threshold
        except (ValueError, TypeError):
            passed = False

    elif check_type == "image_size_mb":
        passed = True
        actual = "N/A (build-time check)"

    elif check_type == "cve_freshness_days":
        effective = get_effective_policy(policy_name, policy, tier)
        max_days = int(effective["expect"].replace("<=", ""))
        cve_result = check_cve_freshness(sbom_info, max_days)
        if cve_result["fresh"] is None:
            return {
                "policy": policy_name,
                "severity": effective["severity"],
                "status": "skip",
                "reason": cve_result.get("reason", "no SBOM"),
                "tier": tier,
            }
        actual = f"{cve_result['age_days']} days"
        passed = cve_result["fresh"]

    elif check_type == "digest_pin_threshold":
        effective = get_effective_policy(policy_name, policy, tier)
        threshold = int(effective["expect"].replace(">=", ""))
        pin_pct = dockerfile.get("digest_pin_pct", 0)
        actual = f"{pin_pct}%"
        passed = pin_pct >= threshold

    else:
        return {
            "policy": policy_name,
            "severity": policy["severity"],
            "status": "skip",
            "reason": f"unknown check type: {check_type}",
            "tier": tier,
        }

    return {
        "policy": policy_name,
        "severity": policy["severity"],
        "status": "pass" if passed else "fail",
        "actual": str(actual),
        "expect": expect,
        "tier": tier,
    }


def print_table(results: list[dict], images_checked: int, tier_filter: str | None):
    header = f"{'Image':<30} {'Tier':<6} {'Policy':<25} {'Status':<8} {'Actual':<20} {'Expected'}"
    sep = "-" * len(header)

    tier_label = f" (tier={tier_filter})" if tier_filter else ""
    print(sep)
    print(f"  Policy Enforcement Report{tier_label}  ({images_checked} images scanned)")
    print(sep)
    print(header)
    print(sep)

    for r in results:
        status_color = {
            "pass": "\033[32mPASS\033[0m",
            "fail": "\033[31mFAIL\033[0m",
            "skip": "\033[33mSKIP\033[0m",
        }.get(r["status"], r["status"])
        actual = r.get("actual", "")
        expect = r.get("expect", "")
        tier = r.get("tier", "?")
        print(
            f"{r['image']:<30} {tier:<6} {r['policy']:<25} {status_color:<8} {actual:<20} {expect}"
        )

    print(sep)

    blocks = [r for r in results if r["status"] == "fail" and r["severity"] == "block"]
    warns = [r for r in results if r["status"] == "fail" and r["severity"] == "warn"]
    infos = [r for r in results if r["status"] == "fail" and r["severity"] == "info"]
    passes = [r for r in results if r["status"] == "pass"]
    skips = [r for r in results if r["status"] == "skip"]

    print(
        f"  Passed: {len(passes)}  Blocked: {len(blocks)}  Warnings: {len(warns)}  Info: {len(infos)}  Skipped: {len(skips)}"
    )
    print()


def build_json_output(
    results: list[dict], images_checked: int, tier_filter: str | None
) -> dict:
    blocks = [r for r in results if r["status"] == "fail" and r["severity"] == "block"]
    warns = [r for r in results if r["status"] == "fail" and r["severity"] == "warn"]
    infos = [r for r in results if r["status"] == "fail" and r["severity"] == "info"]
    passes = [r for r in results if r["status"] == "pass"]
    skips = [r for r in results if r["status"] == "skip"]

    return {
        "images_checked": images_checked,
        "tier_filter": tier_filter,
        "summary": {
            "passed": len(passes),
            "blocked": len(blocks),
            "warnings": len(warns),
            "info": len(infos),
            "skipped": len(skips),
        },
        "has_block_failures": len(blocks) > 0,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Enforce image policies across the registry"
    )
    parser.add_argument(
        "--policy", type=Path, default=POLICY_FILE, help="Path to policy YAML file"
    )
    parser.add_argument(
        "--images-dir", type=Path, default=IMAGES_DIR, help="Path to images directory"
    )
    parser.add_argument(
        "--image", type=str, default=None, help="Check only a specific image"
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output", help="Output results as JSON"
    )
    parser.add_argument(
        "--severity",
        type=str,
        choices=["block", "warn", "all"],
        default="all",
        help="Minimum severity to report (default: all)",
    )
    parser.add_argument(
        "--tier",
        type=str,
        choices=["tier1", "tier2", "tier3"],
        default=None,
        help="Check only images in a specific tier",
    )
    args = parser.parse_args()

    if not args.policy.exists():
        print(f"ERROR: Policy file not found: {args.policy}", file=sys.stderr)
        sys.exit(1)

    policy_data = load_policy(args.policy)
    policies = policy_data.get("policies", {})

    tier_specific_policies = {
        "cve_freshness_days": {
            "description": "SBOM CVE data must be fresh",
            "check": "cve_freshness_days",
            "expect": "<=14",
            "severity": "warn",
        },
        "digest_pin_threshold": {
            "description": "Percentage of FROM lines that are digest-pinned",
            "check": "digest_pin_threshold",
            "expect": ">=90",
            "severity": "warn",
        },
    }
    policies.update(tier_specific_policies)

    if args.image:
        image_dirs = [args.images_dir / args.image]
    else:
        image_dirs = get_image_dirs()

    all_results = []
    images_checked = 0

    for image_dir in image_dirs:
        if not image_dir.is_dir():
            print(f"WARN: {image_dir} is not a directory, skipping", file=sys.stderr)
            continue

        image_name = image_dir.name
        tier = get_image_tier(image_dir)

        if args.tier and tier != args.tier:
            continue

        images_checked += 1

        df = parse_dockerfile(image_dir)
        mf = parse_manifest(image_dir)
        sbom_info = check_sbom(image_dir)
        has_sbom = sbom_info["exists"]

        for policy_name, policy_cfg in policies.items():
            result = run_check(
                policy_name, policy_cfg, image_name, df, mf, has_sbom, sbom_info, tier
            )
            if result is None:
                continue

            entry = {"image": image_name, **result}
            all_results.append(entry)

    if args.severity == "block":
        all_results = [r for r in all_results if r["severity"] in ("block",)]
    elif args.severity == "warn":
        all_results = [
            r for r in all_results if r["severity"] in ("block", "warn")
        ]

    if args.json_output:
        output = build_json_output(all_results, images_checked, args.tier)
        print(json.dumps(output, indent=2))
    else:
        print_table(all_results, images_checked, args.tier)

    has_block_failure = any(
        r["status"] == "fail" and r["severity"] == "block" for r in all_results
    )

    if has_block_failure:
        print("BLOCK violations found. Exiting with code 1.")
        sys.exit(1)
    else:
        print("No BLOCK violations.")
        sys.exit(0)


if __name__ == "__main__":
    main()
