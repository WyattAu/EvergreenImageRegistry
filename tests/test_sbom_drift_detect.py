import json

from scripts.sbom_drift_detect import (
    DriftResult,
    extract_dockerfile_packages,
    extract_sbom_packages,
    format_json,
    normalize,
)


class TestNormalize:
    def test_strips_version_specifier(self):
        assert normalize("curl=1.2.3") == "curl"

    def test_lowercase_and_strip(self):
        assert normalize("  CURL>=1.0  ") == "curl"

    def test_takes_last_path_component(self):
        assert normalize("python3/distutils") == "distutils"

    def test_plain_name(self):
        assert normalize("bash") == "bash"


class TestDriftResult:
    def test_compute_finds_orphaned_and_missing(self):
        r = DriftResult(
            image="test",
            dockerfile_packages=["curl", "wget"],
            sbom_packages=["curl", "git"],
        )
        r.compute()
        assert "git" in r.orphaned_sbom
        assert "wget" in r.missing_sbom
        assert r.discrepancies == 2

    def test_compute_no_drift(self):
        r = DriftResult(
            image="test",
            dockerfile_packages=["curl"],
            sbom_packages=["curl"],
        )
        r.compute()
        assert r.orphaned_sbom == []
        assert r.missing_sbom == []
        assert r.discrepancies == 0


class TestExtractDockerfilePackages:
    def test_apk_add(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text("RUN true && apk add --no-cache curl wget\n")
        pkgs = extract_dockerfile_packages(tmp_path)
        assert "curl" in pkgs
        assert "wget" in pkgs

    def test_apt_get_install(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text("RUN apt-get update && apt-get install -y git make\n")
        pkgs = extract_dockerfile_packages(tmp_path)
        assert "git" in pkgs
        assert "make" in pkgs

    def test_no_dockerfile(self, tmp_path):
        assert extract_dockerfile_packages(tmp_path) == []

    def test_pip_install(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text("RUN true && pip install requests flask\n")
        pkgs = extract_dockerfile_packages(tmp_path)
        assert "requests" in pkgs
        assert "flask" in pkgs


class TestExtractSbomPackages:
    def test_reads_sbom(self, tmp_path):
        sbom = tmp_path / "sbom.spdx.json"
        sbom.write_text(json.dumps({
            "packages": [
                {"name": "curl", "primaryPackagePurpose": "LIBRARY"},
                {"name": "wolfi-base", "primaryPackagePurpose": "CONTAINER"},
                {"name": "git"},
            ]
        }))
        pkgs = extract_sbom_packages(tmp_path)
        assert "curl" in pkgs
        assert "git" in pkgs
        assert "wolfi-base" not in pkgs

    def test_no_sbom(self, tmp_path):
        assert extract_sbom_packages(tmp_path) == []


class TestFormatJson:
    def test_output_structure(self):
        results = [
            DriftResult(
                image="img1",
                dockerfile_packages=["a"],
                sbom_packages=["b"],
            )
        ]
        results[0].compute()
        output = json.loads(format_json(results))
        assert output["total_images"] == 1
        assert output["images_with_discrepancies"] == 1
        assert output["images"][0]["image"] == "img1"
