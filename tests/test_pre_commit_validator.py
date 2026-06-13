
from scripts.pre_commit_validator import validate_dockerfile


class TestValidateDockerfileAlpine:
    def test_alpine_rejected(self, tmp_path, capsys):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM alpine:3.19\nUSER 65534\n")
        assert validate_dockerfile(str(df)) is False
        captured = capsys.readouterr()
        assert "Alpine" in captured.out

    def test_no_alpine_passes(self, tmp_path, capsys):
        df = tmp_path / "Dockerfile"
        df.write_text(
            "FROM cgr.dev/chainguard/wolfi-base\n"
            "USER 65534\n"
            "HEALTHCHECK CMD true\n"
            "LABEL org.opencontainers.image.title=test\n"
        )
        result = validate_dockerfile(str(df))
        captured = capsys.readouterr()
        assert "Alpine" not in captured.out


class TestValidateDockerfileUser:
    def test_missing_user_fails(self, tmp_path, capsys):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\n")
        assert validate_dockerfile(str(df)) is False
        captured = capsys.readouterr()
        assert "C001" in captured.out or "USER" in captured.out

    def test_user_65532_passes(self, tmp_path, capsys):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\nUSER 65532\n")
        result = validate_dockerfile(str(df))
        captured = capsys.readouterr()
        assert "C001 FAILED" not in captured.out

    def test_user_65534_passes(self, tmp_path, capsys):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\nUSER 65534\n")
        result = validate_dockerfile(str(df))
        captured = capsys.readouterr()
        assert "C001 FAILED" not in captured.out


class TestValidateDockerfileHealthcheck:
    def test_missing_healthcheck_warns(self, tmp_path, capsys):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\nUSER 65534\n")
        validate_dockerfile(str(df))
        captured = capsys.readouterr()
        assert "C010" in captured.out or "HEALTHCHECK" in captured.out

    def test_healthcheck_present_no_warning(self, tmp_path, capsys):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\nUSER 65534\nHEALTHCHECK CMD true\n")
        validate_dockerfile(str(df))
        captured = capsys.readouterr()
        assert "C010 WARNING" not in captured.out


class TestValidateDockerfileFileNotFound:
    def test_missing_file_fails(self, tmp_path):
        result = validate_dockerfile(str(tmp_path / "nonexistent"))
        assert result is False


class TestValidateDockerfileLabels:
    def test_missing_labels_warns(self, tmp_path, capsys):
        df = tmp_path / "Dockerfile"
        df.write_text("FROM scratch\nUSER 65534\nHEALTHCHECK CMD true\n")
        validate_dockerfile(str(df))
        captured = capsys.readouterr()
        assert "LABEL" in captured.out
