#!/usr/bin/env python3

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
POLICY_FILE = REPO_ROOT / "images" / "tests" / "image_policy.yaml"

PACKAGE_MANAGERS = re.compile(r"\b(apk|apt-get|apt|yum|dnf|pacman|zypper|microdnf)\b")
SHELL_PATHS = re.compile(r"\b(/bin/(sh|bash|dash|zsh|ash))\b")


def load_policy(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


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

    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()

        if lower.startswith("from "):
            last_from = stripped

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

    return {
        "exists": True,
        "last_from": last_from,
        "user": normalized,
        "has_healthcheck": has_healthcheck,
        "has_shell": has_shell,
        "has_package_manager": has_package_manager,
        "digest_pinned": digest_pinned,
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


def check_sbom(image_dir: Path) -> bool:
    sbom_names = [
        image_dir / "sbom.json",
        image_dir / "sbom.spdx.json",
        image_dir / "sbom.cyclonedx.json",
        image_dir / f"{image_dir.name}.spdx.json",
    ]
    return any(p.exists() for p in sbom_names)


def run_check(
    policy_name: str,
    policy: dict,
    image_name: str,
    dockerfile: dict,
    manifest: dict,
    has_sbom: bool,
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

    else:
        return {
            "policy": policy_name,
            "severity": policy["severity"],
            "status": "skip",
            "reason": f"unknown check type: {check_type}",
        }

    return {
        "policy": policy_name,
        "severity": policy["severity"],
        "status": "pass" if passed else "fail",
        "actual": str(actual),
        "expect": expect,
    }


def print_table(results: list[dict], images_checked: int):
    header = f"{'Image':<30} {'Policy':<25} {'Status':<8} {'Actual':<20} {'Expected'}"
    sep = "-" * len(header)

    print(sep)
    print(f"  Policy Enforcement Report  ({images_checked} images scanned)")
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
        print(
            f"{r['image']:<30} {r['policy']:<25} {status_color:<8} {actual:<20} {expect}"
        )

    print(sep)

    blocks = [r for r in results if r["status"] == "fail" and r["severity"] == "block"]
    warns = [r for r in results if r["status"] == "fail" and r["severity"] == "warn"]
    passes = [r for r in results if r["status"] == "pass"]
    skips = [r for r in results if r["status"] == "skip"]

    print(
        f"  Passed: {len(passes)}  Blocked: {len(blocks)}  Warnings: {len(warns)}  Skipped: {len(skips)}"
    )
    print()


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
    args = parser.parse_args()

    if not args.policy.exists():
        print(f"ERROR: Policy file not found: {args.policy}", file=sys.stderr)
        sys.exit(1)

    policy_data = load_policy(args.policy)
    policies = policy_data.get("policies", {})

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
        images_checked += 1

        df = parse_dockerfile(image_dir)
        mf = parse_manifest(image_dir)
        sbom = check_sbom(image_dir)

        for policy_name, policy_cfg in policies.items():
            result = run_check(policy_name, policy_cfg, image_name, df, mf, sbom)
            if result is None:
                continue

            entry = {"image": image_name, **result}
            all_results.append(entry)

    if args.json_output:
        print(json.dumps(all_results, indent=2))
    else:
        print_table(all_results, images_checked)

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
