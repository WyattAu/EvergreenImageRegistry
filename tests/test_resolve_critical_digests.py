import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from resolve_critical_digests import eligible_for_index_pin, expand_reference, inspect_manifest, parse_reference, propose_patch, validate_digest


def test_parse_references():
    assert parse_reference("redis:8") == ("registry-1.docker.io", "library/redis", "8")
    assert parse_reference("ghcr.io/org/image:v1") == ("ghcr.io", "org/image", "v1")
    assert parse_reference("ghcr.io/org/image:${TAG}") is None
    assert parse_reference("ghcr.io/org/image@sha256:" + "a" * 64) is None


def test_expand_declared_arg():
    dockerfile = "ARG VERSION=v1.2.3\nFROM registry.example/app:${VERSION}"
    assert expand_reference("registry.example/app:${VERSION}", dockerfile) == "registry.example/app:v1.2.3"
    assert expand_reference("registry.example/app:${MISSING}", dockerfile) is None


def test_validate_digest():
    digest = "sha256:" + "a" * 64
    assert validate_digest(digest) == digest
    assert validate_digest("sha256:bad") is None
    assert validate_digest(None) is None


def test_index_policy_requires_multi_platform_index():
    assert eligible_for_index_pin("image:v1", "application/vnd.oci.image.index.v1+json", True, ["linux/amd64"])
    assert not eligible_for_index_pin("image:v1", "application/vnd.oci.image.manifest.v1+json", False, ["linux/amd64"])
    assert not eligible_for_index_pin("image:v1", "application/vnd.oci.image.index.v1+json", True, ["windows/amd64"])


def test_propose_patch_is_safe():
    dockerfile = "FROM example/app:v1\nFROM scratch\n"
    digest = "sha256:" + "b" * 64
    assert propose_patch(dockerfile, 1, "example/app:v1", digest) == "FROM example/app:v1@" + digest
    assert propose_patch(dockerfile, 1, "other/app:v1", digest) is None
    assert propose_patch(dockerfile, 1, "example/app:v1", "sha256:bad") is None
    assert propose_patch(dockerfile, 1, "example/app:v1@sha256:" + "a" * 64, digest) is None
    assert propose_patch(dockerfile, 3, "example/app:v1", digest) is None


def test_arg_reference_is_always_rejected_as_not_immutable():
    dockerfile = "ARG SHIM_VERSION=v2.0.0\nFROM ghcr.io/example/shim:${SHIM_VERSION} AS shim\n"
    digest = "sha256:" + "c" * 64
    assert propose_patch(
        dockerfile,
        2,
        "ghcr.io/example/shim:${SHIM_VERSION}",
        digest,
        expanded_reference="ghcr.io/example/shim:v2.0.0",
    ) is None


def test_arg_reference_is_rejected_when_environment_can_change_value():
    dockerfile = "ARG SHIM_VERSION=v2.0.0\nFROM ghcr.io/example/shim:${SHIM_VERSION}\n"
    digest = "sha256:" + "c" * 64
    assert propose_patch(
        dockerfile,
        2,
        "ghcr.io/example/shim:${SHIM_VERSION}",
        digest,
        expanded_reference="ghcr.io/example/shim:v2.0.0",
        environment={"SHIM_VERSION": "v2.1.0"},
    ) is None


def test_arg_reference_is_rejected_without_a_single_effective_value():
    dockerfile = "ARG SHIM_VERSION\nFROM ghcr.io/example/shim:${SHIM_VERSION}\n"
    digest = "sha256:" + "c" * 64
    assert propose_patch(
        dockerfile,
        2,
        "ghcr.io/example/shim:${SHIM_VERSION}",
        digest,
        expanded_reference="ghcr.io/example/shim:v2.0.0",
    ) is None


def test_unsupported_reference_is_read_only():
    result = inspect_manifest("ghcr.io/org/image:${TAG}")
    assert result["status"] == "unsupported-reference"


def test_variable_target_cannot_be_proposal_ready():
    dockerfile = "ARG VERSION=v1\nFROM ghcr.io/example/app:${VERSION}\n"
    digest = "sha256:" + "d" * 64
    assert propose_patch(
        dockerfile,
        2,
        "ghcr.io/example/app:${VERSION}",
        digest,
        expanded_reference="ghcr.io/example/app:v1",
    ) is None
