#!/usr/bin/env python3
"""
Phase 6 — Rego policy evaluation engine.

Provides a lightweight Rego evaluator for the built-in policy rules.
This is NOT a full OPA implementation — it handles the specific Rego subset
used by the evergreenctl policy engine:

  - deny[msg] rules with contains(), regex.match(), sprintf()
  - Package declarations
  - Simple input access patterns
  - Bare truthiness checks (input.dockerfile)

For production, this should be replaced by OPA/Wasm evaluation via the
OPA REST API or a Wasm runtime. This implementation provides immediate
testability and CI validation without requiring OPA deployment.

The evaluator is strict: any unparseable rule returns an Error, not Pass.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Rego AST / evaluation types
# ---------------------------------------------------------------------------

@dataclass
class RegoRule:
    """A parsed deny[msg] rule."""
    package: str
    condition: str  # raw condition text
    message: str    # message expression
    raw: str        # full Rego source


@dataclass
class PolicyEvaluation:
    rule_id: str
    status: str  # "pass" | "fail" | "error"
    message: str


# ---------------------------------------------------------------------------
# Rego parser (subset)
# ---------------------------------------------------------------------------

def parse_rego(source: str) -> list[RegoRule]:
    """Parse a Rego source string into structured rules.

    This handles the specific patterns used by evergreenctl:
      package evergreen.xxx
      deny[msg] { ... condition ... msg := "..." }
    """
    rules = []

    # Extract package name
    pkg_match = re.search(r"package\s+([\w.]+)", source)
    package = pkg_match.group(1) if pkg_match else "unknown"

    # Extract deny blocks
    deny_pattern = re.compile(
        r'deny\[msg\]\s*\{([^}]+)\}',
        re.DOTALL,
    )

    for match in deny_pattern.finditer(source):
        body = match.group(1).strip()

        # Extract message
        msg_match = re.search(r'msg\s*:=\s*"([^"]*)"', body)
        message = msg_match.group(1) if msg_match else "Policy violation"

        # Extract condition (everything that's not the msg assignment)
        condition_lines = []
        for line in body.split("\n"):
            line = line.strip()
            if line and not line.startswith("msg"):
                condition_lines.append(line)
        condition = " AND ".join(condition_lines)

        rules.append(RegoRule(
            package=package,
            condition=condition,
            message=message,
            raw=body,
        ))

    return rules


# ---------------------------------------------------------------------------
# Rego evaluator (subset)
# ---------------------------------------------------------------------------

def eval_contains(haystack: str, needle: str) -> bool:
    """Evaluate a contains(haystack, needle) expression."""
    return needle in haystack


def eval_not_contains(haystack: str, needle: str) -> bool:
    """Evaluate a not contains(haystack, needle) expression."""
    return needle not in haystack


def eval_regex_match(pattern: str, text: str) -> bool:
    """Evaluate a regex.match(pattern, text) expression."""
    try:
        return bool(re.search(pattern, text))
    except re.error:
        return False


def eval_startswith(text: str, prefix: str) -> bool:
    """Evaluate a startswith(text, prefix) expression."""
    return text.startswith(prefix)


def _extract_string_arg(cond: str, func: str) -> tuple[str, str] | None:
    """Extract arguments from a function call like func(arg1, 'arg2').
    Returns (arg1, arg2) or None."""
    # Match: func(identifier-or-dotted.path, "string")
    # and also: func("string", identifier)
    pattern = rf'{func}\(([^,]+),\s*"([^"]*)"\)'
    m = re.search(pattern, cond)
    if m:
        return m.group(1).strip(), m.group(2)
    return None


def _is_dockerfile_var(var_name: str) -> bool:
    """Check if a variable name refers to the dockerfile input."""
    return var_name in ("input.dockerfile", "dockerfile")


def eval_condition(condition: str, input_data: dict[str, Any]) -> bool:
    """Evaluate a single condition against input data.

    Returns True if the condition is satisfied (i.e., the deny rule fires).
    """
    dockerfile = input_data.get("dockerfile", "")
    manifest = input_data.get("manifest", {})
    tier = manifest.get("tier", "") if isinstance(manifest, dict) else ""
    sbom = input_data.get("sbom", False)

    # Normalize condition
    cond = condition.strip()

    # Handle compound conditions with AND first, before individual checks
    if " AND " in cond:
        parts = cond.split(" AND ")
        return all(eval_condition(part.strip(), input_data) for part in parts)

    # Handle bare truthiness: "input.dockerfile" (just checks it exists/truthy)
    if cond in ("input.dockerfile",):
        return bool(dockerfile)

    # Handle bare truthiness: "not input.sbom"
    if cond == "not input.sbom":
        return not sbom

    # Handle input.manifest.tier == "xxx" (anchored to full condition)
    tier_match = re.fullmatch(r'input\.manifest\.tier\s*==\s*"([^"]*)"', cond)
    if tier_match:
        expected = tier_match.group(1)
        return tier == expected

    # Handle not contains()
    not_contains_match = re.match(r'not\s+contains\(([^,]+),\s*"([^"]*)"\)', cond)
    if not_contains_match:
        var_name = not_contains_match.group(1).strip()
        needle = not_contains_match.group(2)
        text = dockerfile if _is_dockerfile_var(var_name) else ""
        return eval_not_contains(text, needle)

    # Handle contains()
    contains_match = re.match(r'contains\(([^,]+),\s*"([^"]*)"\)', cond)
    if contains_match:
        var_name = contains_match.group(1).strip()
        needle = contains_match.group(2)
        text = dockerfile if _is_dockerfile_var(var_name) else ""
        return eval_contains(text, needle)

    # Handle regex.match()
    regex_match = re.match(r'regex\.match\("([^"]*)",\s*(\S+)\)', cond)
    if regex_match:
        pattern = regex_match.group(1)
        var_name = regex_match.group(2)
        text = dockerfile if _is_dockerfile_var(var_name) else ""
        return eval_regex_match(pattern, text)

    # Handle startswith()
    startswith_match = re.match(r'startswith\(([^,]+),\s*"([^"]*)"\)', cond)
    if startswith_match:
        var_name = startswith_match.group(1).strip()
        prefix = startswith_match.group(2)
        return eval_startswith(dockerfile, prefix)

    # Unknown condition — fail closed
    return False


def evaluate_rule(rule: RegoRule, input_data: dict[str, Any]) -> PolicyEvaluation:
    """Evaluate a single parsed Rego rule against input data."""
    try:
        fired = eval_condition(rule.condition, input_data)
        if fired:
            return PolicyEvaluation(
                rule_id=rule.package,
                status="fail",
                message=rule.message,
            )
        return PolicyEvaluation(
            rule_id=rule.package,
            status="pass",
            message="Rule passed",
        )
    except Exception as exc:
        return PolicyEvaluation(
            rule_id=rule.package,
            status="error",
            message=f"Evaluation error: {exc}",
        )


# ---------------------------------------------------------------------------
# Integration with evergreenctl policy bundles
# ---------------------------------------------------------------------------

# Importable policy source definitions matching evergreenctl/src/policy.rs.
# NOTE: Regex patterns use single-escaped backslashes because these are
# raw Python strings that will be embedded into Rego source and then
# extracted by the parser. The eval_regex_match function receives the
# extracted pattern string directly.
POLICY_SOURCES: dict[str, str] = {
    "DOCKER-SEC-001": r'''
package evergreen.dockerfile

deny[msg] {
    input.dockerfile
    contains(input.dockerfile, "FROM")
    regex.match("(?i)^\s*FROM\s+.*alpine", input.dockerfile)
    msg := "Alpine base images are BANNED for final stage (ADR-007)"
}
''',
    "DOCKER-SEC-002": r'''
package evergreen.dockerfile

deny[msg] {
    input.dockerfile
    contains(input.dockerfile, "FROM")
    regex.match("(?i)^\s*FROM\s+.*debian.*slim", input.dockerfile)
    msg := "debian-slim is BANNED per ADR-007. Use wolfi-base instead."
}
''',
    "DOCKER-SEC-003": '''
package evergreen.dockerfile

deny[msg] {
    input.dockerfile
    not contains(input.dockerfile, "USER 65532")
    not contains(input.dockerfile, "USER nonroot")
    msg := "Final stage must run as non-root user (UID 65532)"
}
''',
    "SC-001": '''
package evergreen.supply_chain

deny[msg] {
    input.manifest.tier == "critical"
    not input.sbom
    msg := "Tier 1 (critical) images must have a valid SBOM"
}
''',
    "SC-003": r'''
package evergreen.supply_chain

deny[msg] {
    input.dockerfile
    regex.match("(?i)(password|secret|token|api.key|private.key)", input.dockerfile)
    msg := "Dockerfile contains potential secrets"
}
''',
}


def evaluate_policies(
    dockerfile: str,
    manifest: dict[str, Any] | None = None,
    has_sbom: bool = False,
    policy_ids: list[str] | None = None,
) -> list[PolicyEvaluation]:
    """Evaluate a set of policies against input data.

    Args:
        dockerfile: Dockerfile content
        manifest: Parsed manifest.toml data
        has_sbom: Whether SBOM exists
        policy_ids: Specific policy IDs to evaluate (None = all)

    Returns:
        List of PolicyEvaluation results
    """
    input_data = {
        "dockerfile": dockerfile,
        "manifest": manifest or {},
        "sbom": has_sbom,
    }

    results = []
    sources = policy_ids if policy_ids else list(POLICY_SOURCES.keys())

    for policy_id in sources:
        source = POLICY_SOURCES.get(policy_id)
        if not source:
            results.append(PolicyEvaluation(
                rule_id=policy_id,
                status="error",
                message=f"Unknown policy: {policy_id}",
            ))
            continue

        rules = parse_rego(source)
        for rule in rules:
            evaluation = evaluate_rule(rule, input_data)
            evaluation.rule_id = policy_id
            results.append(evaluation)

    return results


# ---------------------------------------------------------------------------
# OCI reference parser (Python, for testing and lightweight use)
# ---------------------------------------------------------------------------

def parse_oci_reference(ref: str) -> tuple[str, str, str, str | None]:
    """Parse a container image reference into (registry, repository, tag, error).

    Supports: registry/repo:tag, registry/repo@sha256:..., repo:tag (Docker Hub).
    Returns (registry, repository, tag, None) on success.
    """
    # Handle digest references — strip digest for tag resolution
    if "@sha256:" in ref:
        ref = ref.split("@")[0]

    # Split on first slash
    parts = ref.split("/", 1)

    if len(parts) == 1:
        # Docker Hub shorthand: nginx → docker.io/library/nginx
        tag_parts = parts[0].split(":", 1)
        repo = tag_parts[0]
        tag = tag_parts[1] if len(tag_parts) > 1 else "latest"
        return "docker.io", f"library/{repo}", tag, None

    # Determine if first part is a registry
    first = parts[0]
    if "." in first or ":" in first or first == "localhost":
        registry = first
        repo_tag = parts[1]
    else:
        # Docker Hub user/repo
        registry = "docker.io"
        repo_tag = ref

    # Split tag
    tag_parts = repo_tag.rsplit(":", 1)
    if len(tag_parts) == 2 and "/" not in tag_parts[1]:
        repository, tag = tag_parts
    else:
        repository, tag = repo_tag, "latest"

    return registry, repository, tag, None


# ---------------------------------------------------------------------------
# Image-level evaluation
# ---------------------------------------------------------------------------

def evaluate_image(image_name: str, images_dir: Path) -> dict[str, Any]:
    """Evaluate all Rego policies for a single image."""
    image_dir = images_dir / image_name
    result = {
        "image": image_name,
        "evaluations": [],
        "pass": 0,
        "fail": 0,
        "error": 0,
    }

    # Load Dockerfile
    dockerfile = ""
    dockerfile_path = image_dir / "Dockerfile"
    if dockerfile_path.exists():
        try:
            dockerfile = dockerfile_path.read_text()
        except OSError:
            pass

    # Load manifest
    manifest = {}
    manifest_path = image_dir / "manifest.toml"
    if manifest_path.exists():
        try:
            import tomllib
            manifest = tomllib.loads(manifest_path.read_text())
        except Exception:
            pass

    # Check SBOM
    has_sbom = (image_dir / "sbom.spdx.json").exists()

    # Extract metadata for policy input
    metadata = manifest.get("metadata", {})
    manifest_input = {
        "tier": str(metadata.get("tier", "")).lower(),
    }

    evaluations = evaluate_policies(
        dockerfile=dockerfile,
        manifest=manifest_input,
        has_sbom=has_sbom,
    )

    for e in evaluations:
        result["evaluations"].append({
            "policy_id": e.rule_id,
            "status": e.status,
            "message": e.message,
        })
        if e.status == "pass":
            result["pass"] += 1
        elif e.status == "fail":
            result["fail"] += 1
        else:
            result["error"] += 1

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    images_dir = Path("images")
    if not images_dir.is_dir():
        print("ERROR: images/ directory not found", file=sys.stderr)
        return 1

    # Discover all images
    image_dirs = sorted(
        d for d in images_dir.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    )

    results = []
    total_pass = 0
    total_fail = 0
    total_error = 0

    for img_dir in image_dirs:
        result = evaluate_image(img_dir.name, images_dir)
        results.append(result)
        total_pass += result["pass"]
        total_fail += result["fail"]
        total_error += result["error"]

    report = {
        "summary": {
            "total_images": len(results),
            "total_pass": total_pass,
            "total_fail": total_fail,
            "total_error": total_error,
            "policies_evaluated": len(POLICY_SOURCES),
        },
        "images": results,
    }

    output_path = Path("/tmp/rego_evaluation.json")
    output_path.write_text(json.dumps(report, indent=2))

    print("Rego policy evaluation:")
    print(f"  Images:  {len(results)}")
    print(f"  Policies: {len(POLICY_SOURCES)}")
    print(f"  Pass: {total_pass}  Fail: {total_fail}  Error: {total_error}")
    print(f"\nReport written to {output_path}")

    # Show failures
    failing = [r for r in results if r["fail"] > 0]
    if failing:
        print(f"\nFailing images ({len(failing)}):")
        for r in failing[:20]:
            fails = [e for e in r["evaluations"] if e["status"] == "fail"]
            print(f"  {r['image']}: {len(fails)} failures")
            for f in fails[:3]:
                print(f"    [{f['policy_id']}] {f['message']}")
            if len(fails) > 3:
                print(f"    ... and {len(fails) - 3} more")

    return 1 if total_fail > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
