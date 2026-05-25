
from scripts.enforce_policy import (
    build_json_output,
    get_effective_policy,
    get_image_tier,
    parse_dockerfile,
    parse_manifest,
)


class TestParseDockerfile:
    def test_no_dockerfile(self, tmp_path):
        result = parse_dockerfile(tmp_path)
        assert result["exists"] is False

    def test_simple_dockerfile(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text(
            "FROM cgr.dev/chainguard/wolfi-base@sha256:abc123def456abc123def456abc123def456abc123def456abc123def456abc1\n"
            "USER 65532:65532\n"
            "HEALTHCHECK CMD true\n"
        )
        result = parse_dockerfile(tmp_path)
        assert result["exists"] is True
        assert result["user"] == "6553265532"
        assert result["has_healthcheck"] is True
        assert result["digest_pinned"] is True
        assert result["digest_pin_pct"] == 100

    def test_digest_pin_percentage(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text(
            "FROM scratch AS builder\n"
            "FROM cgr.dev/chainguard/wolfi-base@sha256:abc123def456abc123def456abc123def456abc123def456abc123def456abc1\n"
        )
        result = parse_dockerfile(tmp_path)
        assert result["from_total"] == 2
        assert result["from_digest"] == 1
        assert result["digest_pin_pct"] == 50

    def test_package_manager_detected(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text(
            "FROM debian:bookworm-slim\n"
            "RUN apt-get update && apt-get install -y curl\n"
        )
        result = parse_dockerfile(tmp_path)
        assert result["has_package_manager"] is True

    def test_shell_detected(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text(
            "FROM debian:bookworm-slim\n"
            "COPY target/bin/sh /bin/sh\n"
        )
        result = parse_dockerfile(tmp_path)
        assert result["has_shell"] is True


class TestGetImageTier:
    def test_tier_from_manifest(self, tmp_path):
        manifest = tmp_path / "manifest.toml"
        manifest.write_text('tier = "tier1"\n')
        assert get_image_tier(tmp_path) == "tier1"

    def test_default_tier2(self, tmp_path):
        assert get_image_tier(tmp_path) == "tier2"

    def test_tier_from_dockerfile_comment(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text("# tier: 3\nFROM scratch\n")
        assert get_image_tier(tmp_path) == "tier3"


class TestParseManifest:
    def test_no_manifest(self, tmp_path):
        result = parse_manifest(tmp_path)
        assert result["exists"] is False

    def test_valid_manifest(self, tmp_path):
        manifest = tmp_path / "manifest.toml"
        manifest.write_text('[metadata]\nname = "test"\nversion = "1.0"\n')
        result = parse_manifest(tmp_path)
        assert result["exists"] is True
        assert result["valid"] is True
        assert result["data"]["metadata"]["name"] == "test"

    def test_invalid_toml(self, tmp_path):
        manifest = tmp_path / "manifest.toml"
        manifest.write_text("{{invalid toml}}}")
        result = parse_manifest(tmp_path)
        assert result["exists"] is True
        assert result["valid"] is False


class TestGetEffectivePolicy:
    def test_tier_override_applied(self):
        base = {"expect": "<=14", "severity": "warn"}
        result = get_effective_policy("cve_freshness_days", base, "tier1")
        assert result["expect"] == "<=7"
        assert result["severity"] == "block"

    def test_no_override_for_tier2(self):
        base = {"expect": "<=14", "severity": "warn"}
        result = get_effective_policy("cve_freshness_days", base, "tier2")
        assert result["expect"] == "<=14"

    def test_unknown_policy_returns_base(self):
        base = {"expect": "present", "severity": "warn"}
        result = get_effective_policy("nonexistent", base, "tier1")
        assert result == base


class TestBuildJsonOutput:
    def test_counts_by_severity(self):
        results = [
            {"status": "pass", "severity": "block"},
            {"status": "fail", "severity": "block"},
            {"status": "fail", "severity": "warn"},
            {"status": "skip", "severity": "info"},
        ]
        output = build_json_output(results, 5, None)
        assert output["images_checked"] == 5
        assert output["summary"]["passed"] == 1
        assert output["summary"]["blocked"] == 1
        assert output["summary"]["warnings"] == 1
        assert output["summary"]["skipped"] == 1
        assert output["has_block_failures"] is True

    def test_no_block_failures(self):
        results = [{"status": "pass", "severity": "block"}]
        output = build_json_output(results, 1, "tier1")
        assert output["has_block_failures"] is False
        assert output["tier_filter"] == "tier1"
