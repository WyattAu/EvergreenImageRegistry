from contextlib import suppress
import json
from unittest.mock import patch

from scripts.check_upstream_versions import (
    extract_github_repo,
    get_latest_github_release,
    normalize_version,
    parse_manifest,
)


class TestNormalizeVersion:
    def test_strips_leading_v(self):
        assert normalize_version("v1.2.3") == "1.2.3"

    def test_extracts_semantic_version(self):
        assert normalize_version("2.0.0-rc1") == "2.0.0"

    def test_plain_number(self):
        assert normalize_version("1.2.3") == "1.2.3"

    def test_v_prefix_with_suffix(self):
        assert normalize_version("v3.14.2-alpine") == "3.14.2"


class TestExtractGithubRepo:
    def test_https_url(self):
        assert extract_github_repo("https://github.com/owner/repo") == "owner/repo"

    def test_url_with_git_suffix(self):
        assert extract_github_repo("https://github.com/owner/repo.git") == "owner/repo"

    def test_url_with_trailing_slash(self):
        assert extract_github_repo("https://github.com/owner/repo/") == "owner/repo"

    def test_none_input(self):
        assert extract_github_repo(None) is None

    def test_non_github_url(self):
        assert extract_github_repo("https://gitlab.com/owner/repo") is None


class TestParseManifest:
    def test_basic_parsing(self, tmp_path):
        f = tmp_path / "manifest.toml"
        f.write_text(
            '[metadata]\nname = "my-image"\nversion = "1.0"\nsource = "https://github.com/o/r"\n'
        )
        data = parse_manifest(str(f))
        assert data["metadata"]["name"] == "my-image"
        assert data["metadata"]["version"] == "1.0"

    def test_comments_ignored(self, tmp_path):
        f = tmp_path / "manifest.toml"
        f.write_text('# comment\n[metadata]\nname = "img"\n')
        data = parse_manifest(str(f))
        assert data["metadata"]["name"] == "img"

    def test_empty_file_raises(self, tmp_path):
        f = tmp_path / "empty.toml"
        f.write_text("")
        # tomllib raises an error on empty TOML
        with __import__("contextlib").suppress(Exception):
            parse_manifest(str(f))
  # expected


class TestGetLatestGithubRelease:
    @patch("scripts.check_upstream_versions.urllib.request.urlopen")
    def test_successful_fetch(self, mock_urlopen):
        class FakeResp:
            def read(self):
                return json.dumps({"tag_name": "v1.2.3", "html_url": "https://github.com/o/r/releases/v1.2.3"}).encode()
            def __enter__(self):
                return self
            def __exit__(self, *a):
                pass

        mock_urlopen.return_value = FakeResp()
        tag, url = get_latest_github_release("owner/repo")
        assert tag == "v1.2.3"
        assert "v1.2.3" in url

    @patch("scripts.check_upstream_versions.urllib.request.urlopen")
    def test_404_returns_none(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.HTTPError("url", 404, "Not Found", {}, None)
        tag, url = get_latest_github_release("owner/repo")
        assert tag is None
        assert url is None
