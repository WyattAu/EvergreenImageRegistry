
from scripts.pre_commit_validator import ERRORS, WARNINGS, validate_dockerfile


class TestValidateDockerfileAlpine:
    def test_alpine_rejected(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM alpine:3.19\nUSER 65534\n")
        assert validate_dockerfile(str(df)) is False
        assert any("Alpine" in e for e in ERRORS)

    def test_no_alpine_passes(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text(
            "FROM cgr.dev/chainguard/wolfi-base\n"
            "USER 65534\n"
            "HEALTHCHECK CMD true\n"
            "LABEL org.opencontainers.image.title=test\n"
        )
        validate_dockerfile(str(df))
        assert not any("Alpine" in e for e in ERRORS)


class TestValidateDockerfileUser:
    def test_missing_user_fails(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\n")
        validate_dockerfile(str(df))
        assert any("C001" in e or "USER" in e for e in ERRORS)

    def test_user_65534_passes(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\nUSER 65534\n")
        validate_dockerfile(str(df))
        assert not any("C001" in e for e in ERRORS)


class TestValidateDockerfileHealthcheck:
    def test_missing_healthcheck_warns(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\nUSER 65534\n")
        validate_dockerfile(str(df))
        assert any("C010" in w or "HEALTHCHECK" in w for w in WARNINGS)

    def test_healthcheck_present_no_warning(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\nUSER 65534\nHEALTHCHECK CMD true\n")
        validate_dockerfile(str(df))
        assert not any("C010" in w for w in WARNINGS)


class TestValidateDockerfileFileNotFound:
    def test_missing_file_fails(self, tmp_path):
        result = validate_dockerfile(str(tmp_path / "nonexistent"))
        assert result is False
        assert any("not found" in e.lower() for e in ERRORS)


class TestValidateDockerfileLabels:
    def test_missing_labels_warns(self, tmp_path):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\nUSER 65534\nHEALTHCHECK CMD true\n")
        validate_dockerfile(str(df))
        assert any("LABEL" in w for w in WARNINGS)
