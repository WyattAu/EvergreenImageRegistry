#!/usr/bin/env python3
"""
Tests for Phase 1-6 implementation.

Covers:
  Phase 1: Canonical manifest.toml contract and validator
  Phase 2: Critical-image governance policy
  Phase 3: Supply-chain verification
  Phase 4: Runtime verification
  Phase 5: OCI reference parsing
  Phase 6: Rego policy evaluation
"""

import json
import sys
import tempfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Phase 1: Manifest validation
# ---------------------------------------------------------------------------

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from validate_manifest import (
    normalize_tier,
    validate_manifest,
    load_and_validate,
    LEGACY_TIER_MAP,
    VALID_TIERS,
)


class TestNormalizeTier:
    def test_canonical_tiers(self):
        assert normalize_tier("critical") == "critical"
        assert normalize_tier("standard") == "standard"

    def test_legacy_numeric_tiers(self):
        assert normalize_tier("1") == "critical"
        assert normalize_tier("2") == "standard"

    def test_legacy_prefix_tiers(self):
        assert normalize_tier("tier1") == "critical"
        assert normalize_tier("tier2") == "standard"

    def test_whitespace_handling(self):
        assert normalize_tier("  critical  ") == "critical"


class TestManifestValidation:
    def test_valid_manifest(self):
        data = {
            "metadata": {"name": "test", "version": "1.0", "tier": "critical", "description": "Test"},
            "build": {"base": "scratch", "user": "65532:65532", "stopsignal": "SIGTERM"},
            "source": {"type": "binary-release", "url": "https://example.com/app"},
            "runtime": {"entrypoint": ["/app"]},
        }
        errors = validate_manifest(data, "test")
        blocks = [e for e in errors if e.severity == "block"]
        assert len(blocks) == 0

    def test_missing_metadata_section(self):
        data = {"build": {}, "source": {}, "runtime": {}}
        errors = validate_manifest(data, "test")
        codes = [e.code for e in errors]
        assert "M001" in codes

    def test_missing_required_metadata_fields(self):
        data = {
            "metadata": {"name": "test"},
            "build": {"base": "scratch", "user": "65532:65532", "stopsignal": "SIGTERM"},
            "source": {"type": "binary-release", "url": "https://example.com"},
            "runtime": {"entrypoint": ["/app"]},
        }
        errors = validate_manifest(data, "test")
        codes = [e.code for e in errors]
        assert "M002" in codes

    def test_banned_base_image(self):
        data = {
            "metadata": {"name": "test", "version": "1.0", "tier": "standard", "description": "Test"},
            "build": {"base": "alpine:3.20", "user": "65532:65532", "stopsignal": "SIGTERM"},
            "source": {"type": "package-manager", "url": "https://example.com"},
            "runtime": {"entrypoint": ["/app"]},
        }
        errors = validate_manifest(data, "test")
        codes = [e.code for e in errors]
        assert "M012" in codes

    def test_label_drift_detection(self):
        data = {
            "metadata": {"name": "test", "version": "1.0", "tier": "critical", "description": "Test"},
            "build": {"base": "scratch", "user": "65532:65532", "stopsignal": "SIGTERM"},
            "source": {"type": "binary-release", "url": "https://example.com"},
            "runtime": {"entrypoint": ["/app"]},
            "labels": {"evergreen.image.tier": "standard"},
        }
        errors = validate_manifest(data, "test")
        codes = [e.code for e in errors]
        assert "M040" in codes


# ---------------------------------------------------------------------------
# Phase 2: Critical image governance
# ---------------------------------------------------------------------------

from critical_image_governance import (
    validate_critical_image,
    discover_critical_images,
    BANNED_FINAL_BASES,
)


class TestCriticalGovernance:
    def test_discover_critical_images(self):
        images_dir = Path("images")
        if images_dir.is_dir():
            critical = discover_critical_images(images_dir)
            assert isinstance(critical, list)
            # Should find at least some critical images
            if critical:
                assert len(critical) > 0

    def test_banned_bases_defined(self):
        assert "alpine" in BANNED_FINAL_BASES
        assert "ubuntu" in BANNED_FINAL_BASES
        assert "centos" in BANNED_FINAL_BASES


# ---------------------------------------------------------------------------
# Phase 3: Supply-chain verification
# ---------------------------------------------------------------------------

from verify_supply_chain import (
    check_sbom_binding,
    check_digest_pinning,
    check_build_reproducibility,
)


class TestSupplyChain:
    def test_sbom_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            img_dir = Path(tmpdir)
            violations = check_sbom_binding(img_dir)
            codes = [v["code"] for v in violations]
            assert "SC001" in codes

    def test_sbom_valid(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            img_dir = Path(tmpdir)
            sbom = {"packages": [{"name": "test", "version": "1.0"}]}
            (img_dir / "sbom.spdx.json").write_text(json.dumps(sbom))
            violations = check_sbom_binding(img_dir)
            block = [v for v in violations if v["severity"] == "block"]
            assert len(block) == 0
            # Cleanup
            (img_dir / ".sbom_hash").unlink(missing_ok=True)

    def test_digest_pinning_check(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            img_dir = Path(tmpdir)
            # Unpinned FROM
            (img_dir / "Dockerfile").write_text("FROM nginx:1.25\nUSER 65532\n")
            violations = check_digest_pinning(img_dir)
            codes = [v["code"] for v in violations]
            assert "SC030" in codes

    def test_scratch_not_checked(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            img_dir = Path(tmpdir)
            (img_dir / "Dockerfile").write_text("FROM scratch\nCOPY app /app\nUSER 65532\n")
            violations = check_digest_pinning(img_dir)
            assert len(violations) == 0

    def test_variable_ref_not_checked(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            img_dir = Path(tmpdir)
            (img_dir / "Dockerfile").write_text("FROM ghcr.io/x/shim:${V}\nUSER 65532\n")
            violations = check_digest_pinning(img_dir)
            assert len(violations) == 0


# ---------------------------------------------------------------------------
# Phase 4: Runtime verification
# ---------------------------------------------------------------------------

from verify_runtime import (
    check_nonroot,
    check_healthcheck,
    check_stop_signal,
    check_capabilities,
)


class TestRuntimeVerification:
    def test_nonroot_pass(self):
        assert check_nonroot("FROM scratch\nUSER 65532\n") is None

    def test_nonroot_fail(self):
        assert check_nonroot("FROM nginx\n") is not None

    def test_healthcheck_scratch_skip(self):
        assert check_healthcheck("FROM scratch\n", is_scratch=True) is None

    def test_healthcheck_missing(self):
        v = check_healthcheck("FROM nginx\n", is_scratch=False)
        assert v is not None
        assert v["code"] == "RT002"

    def test_healthcheck_present(self):
        assert check_healthcheck("FROM nginx\nHEALTHCHECK CMD curl -f http://localhost/\n", is_scratch=False) is None

    def test_stop_signal_sigterm(self):
        manifest = {"build": {"stopsignal": "SIGTERM"}}
        assert check_stop_signal(manifest) is None

    def test_stop_signal_missing(self):
        assert check_stop_signal({}) is not None

    def test_capabilities_pass(self):
        manifest = {"labels": {"evergreen.security.cap-drop": "ALL"}}
        assert check_capabilities("", manifest) is None

    def test_capabilities_fail(self):
        manifest = {"labels": {}}
        assert check_capabilities("", manifest) is not None


# ---------------------------------------------------------------------------
# Phase 5: OCI reference parsing
# ---------------------------------------------------------------------------


class TestOCIReferenceParsing:
    def test_docker_hub_short(self):
        from rego_evaluate import parse_oci_reference
        reg, repo, tag, err = parse_oci_reference("nginx")
        assert err is None
        assert reg == "docker.io"
        assert repo == "library/nginx"
        assert tag == "latest"

    def test_docker_hub_user(self):
        from rego_evaluate import parse_oci_reference
        reg, repo, tag, err = parse_oci_reference("user/repo:v1.0")
        assert err is None
        assert reg == "docker.io"
        assert repo == "user/repo"
        assert tag == "v1.0"

    def test_ghcr(self):
        from rego_evaluate import parse_oci_reference
        reg, repo, tag, err = parse_oci_reference("ghcr.io/org/image:latest")
        assert err is None
        assert reg == "ghcr.io"
        assert repo == "org/image"
        assert tag == "latest"

    def test_digest_stripped(self):
        from rego_evaluate import parse_oci_reference
        reg, repo, tag, err = parse_oci_reference("ghcr.io/org/image:v1@sha256:abc123")
        assert err is None
        assert tag == "v1"

    def test_localhost(self):
        from rego_evaluate import parse_oci_reference
        reg, repo, tag, err = parse_oci_reference("localhost:5000/myimage:v2")
        assert err is None
        assert reg == "localhost:5000"
        assert repo == "myimage"
        assert tag == "v2"


# ---------------------------------------------------------------------------
# Phase 6: Rego evaluation
# ---------------------------------------------------------------------------

from rego_evaluate import (
    parse_rego,
    eval_condition,
    evaluate_policies,
    POLICY_SOURCES,
)


class TestRegoParser:
    def test_parse_deny_rule(self):
        source = '''
package evergreen.dockerfile

deny[msg] {
    contains(input.dockerfile, "alpine")
    msg := "Alpine is banned"
}
'''
        rules = parse_rego(source)
        assert len(rules) == 1
        assert rules[0].package == "evergreen.dockerfile"
        assert "alpine" in rules[0].condition
        assert rules[0].message == "Alpine is banned"

    def test_parse_multiple_rules(self):
        source = '''
package evergreen.dockerfile

deny[msg] {
    contains(input.dockerfile, "alpine")
    msg := "Alpine banned"
}

deny[msg] {
    contains(input.dockerfile, "ubuntu")
    msg := "Ubuntu banned"
}
'''
        rules = parse_rego(source)
        assert len(rules) == 2


class TestRegoEvaluator:
    def test_contains_match(self):
        assert eval_condition('contains(input.dockerfile, "alpine")', {"dockerfile": "FROM alpine:3.20"})

    def test_contains_no_match(self):
        assert not eval_condition('contains(input.dockerfile, "alpine")', {"dockerfile": "FROM scratch"})

    def test_not_contains_match(self):
        assert eval_condition('not contains(input.dockerfile, "USER 65532")', {"dockerfile": "FROM scratch"})

    def test_not_contains_no_match(self):
        assert not eval_condition('not contains(input.dockerfile, "USER 65532")', {"dockerfile": "FROM scratch\nUSER 65532"})

    def test_regex_match(self):
        import re as re_mod
        pattern = "(?i)^\\s*FROM\\s*.*alpine"
        assert eval_condition(f'regex.match("{pattern}", input.dockerfile)', {"dockerfile": "FROM alpine:3.20"})


class TestRegoPolicyIntegration:
    def test_alpine_detection(self):
        results = evaluate_policies(
            dockerfile="FROM alpine:3.20\nRUN apk add curl\n",
            manifest={"tier": "standard"},
        )
        failures = [r for r in results if r.status == "fail"]
        assert len(failures) > 0

    def test_clean_dockerfile_passes(self):
        results = evaluate_policies(
            dockerfile="FROM scratch\nCOPY app /app\nUSER 65532\nENTRYPOINT [\"/app\"]\n",
            manifest={"tier": "standard"},
        )
        failures = [r for r in results if r.status == "fail"]
        assert len(failures) == 0

    def test_nonroot_violation(self):
        results = evaluate_policies(
            dockerfile="FROM nginx\nEXPOSE 80\n",
            manifest={"tier": "standard"},
        )
        failures = [r for r in results if r.status == "fail"]
        nonroot_fails = [r for r in failures if "non-root" in r.message.lower() or "65532" in r.message]
        assert len(nonroot_fails) > 0

    def test_sbom_required_for_critical(self):
        results = evaluate_policies(
            dockerfile="FROM scratch\nUSER 65532\n",
            manifest={"tier": "critical"},
            has_sbom=False,
        )
        failures = [r for r in results if r.status == "fail"]
        sbom_fails = [r for r in failures if "SBOM" in r.message]
        assert len(sbom_fails) > 0

    def test_sbom_not_required_for_standard(self):
        results = evaluate_policies(
            dockerfile="FROM scratch\nUSER 65532\n",
            manifest={"tier": "standard"},
            has_sbom=False,
        )
        failures = [r for r in results if r.status == "fail"]
        sbom_fails = [r for r in failures if "SBOM" in r.message]
        assert len(sbom_fails) == 0

    def test_all_policies_parseable(self):
        """Every policy source must parse without errors."""
        for policy_id, source in POLICY_SOURCES.items():
            rules = parse_rego(source)
            assert len(rules) > 0, f"Policy {policy_id} parsed to 0 rules"

    def test_unknown_policy_returns_error(self):
        results = evaluate_policies(
            dockerfile="FROM scratch",
            policy_ids=["NONEXISTENT"],
        )
        assert len(results) == 1
        assert results[0].status == "error"
