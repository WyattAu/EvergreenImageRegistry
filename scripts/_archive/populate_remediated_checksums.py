#!/usr/bin/env python3
"""
populate_remediated_checksums.py - Populate SHA256 checksums for remediated images.

Batch 1: GitHub releases (32 images across 10 ecosystems).

Strategy per image:
1. Extract download URL + version from Dockerfile
2. Try upstream checksum files: {url}.sha256, {url}.sha256sum, sha256sums.txt, etc.
3. Try GitHub API release assets for sha256/checksum files
4. Insert `echo "sha256  filename" | sha256sum -c -` into Dockerfile after download
5. Update manifest.toml [download] checksum field if it exists

Usage:
  python3 scripts/populate_remediated_checksums.py [--dry-run]
"""

import json
import logging
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
USER_AGENT = "EvergreenImageRegistry/1.0 (populate_remediated_checksums.py)"
HTTP_TIMEOUT = 15

IMAGES = {
    "argocd": {
        "url_template": "https://github.com/argoproj/argo-cd/releases/download/v{VERSION}/argocd-linux-amd64",
        "filename": "argocd-linux-amd64",
        "output_path": "/tmp/argocd",
        "sha256_file": "argocd-linux-amd64",
    },
    "argocd-application-controller": {
        "url_template": "https://github.com/argoproj/argo-cd/releases/download/v{VERSION}/argocd-linux-amd64",
        "filename": "argocd-linux-amd64",
        "output_path": "/tmp/argocd",
        "sha256_file": "argocd-linux-amd64",
    },
    "argocd-applicationset-controller": {
        "url_template": "https://github.com/argoproj/argo-cd/releases/download/v{VERSION}/argocd-linux-amd64",
        "filename": "argocd-linux-amd64",
        "output_path": "/tmp/argocd",
        "sha256_file": "argocd-linux-amd64",
    },
    "argocd-notifications": {
        "url_template": "https://github.com/argoproj/argo-cd/releases/download/v{VERSION}/argocd-linux-amd64",
        "filename": "argocd-linux-amd64",
        "output_path": "/tmp/argocd",
        "sha256_file": "argocd-linux-amd64",
    },
    "argocd-repo-server": {
        "url_template": "https://github.com/argoproj/argo-cd/releases/download/v{VERSION}/argocd-linux-amd64",
        "filename": "argocd-linux-amd64",
        "output_path": "/tmp/argocd",
        "sha256_file": "argocd-linux-amd64",
    },
    "gitea-actions": {
        "url_template": "https://github.com/go-gitea/gitea/releases/download/v{VERSION}/gitea-{VERSION}-linux-amd64",
        "filename": "gitea-{VERSION}-linux-amd64",
        "output_path": "/tmp/gitea",
        "sha256_file": None,
    },
    "gitea-editor": {
        "url_template": "https://github.com/go-gitea/gitea/releases/download/v{VERSION}/gitea-{VERSION}-linux-amd64",
        "filename": "gitea-{VERSION}-linux-amd64",
        "output_path": "/tmp/gitea",
        "sha256_file": None,
    },
    "gitea-secure": {
        "url_template": "https://github.com/go-gitea/gitea/releases/download/v{VERSION}/gitea-{VERSION}-linux-amd64",
        "filename": "gitea-{VERSION}-linux-amd64",
        "output_path": "/tmp/gitea",
        "sha256_file": None,
    },
    "gitlab-exporter": {
        "url_template": "https://github.com/prometheus-community/gitlab-exporter/releases/download/v{VERSION}/gitlab-exporter_{VERSION}_linux_amd64",
        "filename": "gitlab-exporter_{VERSION}_linux_amd64",
        "output_path": "/tmp/gitlab-exporter",
        "sha256_file": None,
    },
    "drone-agent": {
        "url_template": "https://github.com/harness/drone/releases/download/v{VERSION}/drone_agent_linux_amd64.tar.gz",
        "filename": "drone_agent_linux_amd64.tar.gz",
        "output_path": "/tmp/archive.tar.gz",
        "sha256_file": None,
    },
    "drone-autoscaler": {
        "url_template": "https://github.com/harness/drone/releases/download/v{VERSION}/drone_autoscaler_linux_amd64.tar.gz",
        "filename": "drone_autoscaler_linux_amd64.tar.gz",
        "output_path": "/tmp/archive.tar.gz",
        "sha256_file": None,
    },
    "drone-runner": {
        "url_template": "https://github.com/harness/drone-runner-exec/releases/download/v{VERSION}/drone-runner-exec_linux_amd64.tar.gz",
        "filename": "drone-runner-exec_linux_amd64.tar.gz",
        "output_path": "/tmp/archive.tar.gz",
        "sha256_file": None,
    },
    "woodpecker-agent": {
        "url_template": "https://github.com/woodpecker-ci/woodpecker/releases/download/v{VERSION}/woodpecker-agent_linux_amd64.tar.gz",
        "filename": "woodpecker-agent_linux_amd64.tar.gz",
        "output_path": "/tmp/archive.tar.gz",
        "sha256_file": None,
    },
    "woodpecker-ci": {
        "url_template": "https://github.com/woodpecker-ci/woodpecker/releases/download/v{VERSION}/woodpecker-server_linux_amd64.tar.gz",
        "filename": "woodpecker-server_linux_amd64.tar.gz",
        "output_path": "/tmp/archive.tar.gz",
        "sha256_file": None,
    },
    "woodpecker-server": {
        "url_template": "https://github.com/woodpecker-ci/woodpecker/releases/download/v{VERSION}/woodpecker-server_linux_amd64.tar.gz",
        "filename": "woodpecker-server_linux_amd64.tar.gz",
        "output_path": "/tmp/archive.tar.gz",
        "sha256_file": None,
    },
    "mattermost-bridge": {
        "url_template": "https://github.com/mattermost/mattermost-plugin-github/releases/download/v{VERSION}/github-linux-amd64.tar.gz",
        "filename": "github-linux-amd64.tar.gz",
        "output_path": "/tmp/archive.tar.gz",
        "sha256_file": None,
    },
    "mattermost-operator": {
        "url_template": "https://github.com/mattermost/mattermost-operator/releases/download/v{VERSION}/mattermost-kubernetes-operator-linux-amd64",
        "filename": "mattermost-kubernetes-operator-linux-amd64",
        "output_path": "/tmp/binary",
        "sha256_file": None,
    },
    "mattermost-push-proxy": {
        "url_template": "https://github.com/mattermost/mattermost-push-proxy/releases/download/v{VERSION}/mattermost-push-proxy-linux-amd64",
        "filename": "mattermost-push-proxy-linux-amd64",
        "output_path": "/tmp/binary",
        "sha256_file": None,
    },
    "dendrite": {
        "url_template": "https://github.com/element-hq/dendrite/releases/download/v{VERSION}/dendrite-monolith-linux-amd64",
        "filename": "dendrite-monolith-linux-amd64",
        "output_path": "/tmp/dendrite",
        "sha256_file": None,
    },
    "dendrite-monolith": {
        "url_template": "https://github.com/element-hq/dendrite/releases/download/v{VERSION}/dendrite-monolith-linux-amd64",
        "filename": "dendrite-monolith-linux-amd64",
        "output_path": "/tmp/dendrite",
        "sha256_file": None,
    },
    "dendrite-pot": {
        "url_template": "https://github.com/element-hq/dendrite/releases/download/v{VERSION}/dendrite-monolith-linux-amd64",
        "filename": "dendrite-monolith-linux-amd64",
        "output_path": "/tmp/dendrite",
        "sha256_file": None,
    },
    "element-web": {
        "url_template": "https://github.com/element-hq/element-web/releases/download/v{VERSION}/element-v{VERSION}.tar.gz",
        "filename": "element-v{VERSION}.tar.gz",
        "output_path": "/download.tar.gz",
        "sha256_file": None,
    },
    "element-x": {
        "url_template": "https://github.com/element-hq/element-x/releases/download/v{VERSION}/element-x-v{VERSION}.tar.gz",
        "filename": "element-x-v{VERSION}.tar.gz",
        "output_path": "/download.tar.gz",
        "sha256_file": None,
    },
    "hedgedoc": {
        "url_template": "https://github.com/hedgedoc/hedgedoc/releases/download/v{VERSION}/hedgedoc-v{VERSION}.tar.gz",
        "filename": "hedgedoc-v{VERSION}.tar.gz",
        "output_path": "/app.tar.gz",
        "sha256_file": None,
    },
    "hedgedoc-legacy": {
        "url_template": "https://github.com/hedgedoc/hedgedoc/releases/download/v{VERSION}/hedgedoc-v{VERSION}.tar.gz",
        "filename": "hedgedoc-v{VERSION}.tar.gz",
        "output_path": "/app.tar.gz",
        "sha256_file": None,
    },
    "hackmd": {
        "url_template": "https://github.com/hackmdio/hackmd-ce/releases/download/v{VERSION}/hackmd-ce-v{VERSION}.tar.gz",
        "filename": "hackmd-ce-v{VERSION}.tar.gz",
        "output_path": "/app.tar.gz",
        "sha256_file": None,
    },
}


def log(msg: str, level: str = "INFO"):
    level_map = {"INFO": "info", "WARN": "warning", "ERROR": "error", "SKIP": "info"}
    getattr(logger, level_map.get(level, "info"))(msg)


def http_get(url: str, timeout: int = HTTP_TIMEOUT) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError):
        return None


def http_get_json(url: str, timeout: int = HTTP_TIMEOUT) -> dict | None:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            return json.loads(resp.read().decode("utf-8"))
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        OSError,
        TimeoutError,
        json.JSONDecodeError,
    ):
        return None


def parse_github_release_url(url: str) -> tuple[str, str, str] | None:
    m = re.match(
        r"https://github\.com/([^/]+)/([^/]+)/releases/download/([^/]+)/(.+)", url
    )
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3)


def extract_version_from_dockerfile(dockerfile_path: Path) -> str | None:
    content = dockerfile_path.read_text()
    m = re.search(r"ARG\s+VERSION\s*=\s*(\S+)", content)
    if m:
        return m.group(1).strip('"').strip("'")
    return None


def filenames_match(target: str, candidate: str) -> bool:
    if target == candidate:
        return True
    t = target.lower()
    c = candidate.lower()
    if t == c:
        return True
    t_norm = t.replace(".tar.gz", "").replace(".tgz", "")
    c_norm = c.replace(".tar.gz", "").replace(".tgz", "")
    if t_norm == c_norm:
        return True
    return bool(t_norm in c_norm or c_norm in t_norm)


def find_checksum_in_checksums_file(
    checksum_url: str, target_filename: str
) -> str | None:
    content = http_get(checksum_url)
    if content is None:
        return None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([0-9a-fA-F]{64})\s+[* ](.+)$", line)
        if not m:
            m = re.match(r"^([0-9a-fA-F]{64})\s+\((.+)\)", line)
        if m:
            h = m.group(1).lower()
            fname = m.group(2).strip()
            if filenames_match(target_filename, fname):
                return h
    return None


def find_checksum_single_file(checksum_url: str) -> str | None:
    content = http_get(checksum_url)
    if content is None:
        return None
    h = content.strip()
    if re.match(r"^[0-9a-fA-F]{64}$", h):
        return h.lower()
    m = re.match(r"^([0-9a-fA-F]{64})\s+", h)
    if m:
        return m.group(1).lower()
    return None


def find_checksum_github_api(
    owner: str, repo: str, tag: str, target_filename: str
) -> str | None:
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
    data = http_get_json(api_url)
    if data is None:
        return None
    assets = data.get("assets", [])
    for asset in assets:
        name = asset.get("name", "")
        if not filenames_match(target_filename, name):
            continue
        if asset.get("digest"):
            digest = asset["digest"]
            if digest.startswith("sha256:"):
                return digest[7:].lower()
        if name.endswith(".sha256") or name.endswith(".sha256sum"):
            sha_url = asset.get("browser_download_url", "")
            if sha_url:
                return find_checksum_single_file(sha_url)
    for asset in assets:
        name = asset.get("name", "")
        if any(
            ext in name for ext in (".sha256", ".sha256sum", "checksums", "SHASUMS")
        ):
            sha_url = asset.get("browser_download_url", "")
            if sha_url:
                h = find_checksum_in_checksums_file(sha_url, target_filename)
                if h:
                    return h
    return None


def find_checksum_for_image(
    image_name: str, download_url: str, target_filename: str
) -> str | None:
    release_info = parse_github_release_url(download_url)

    if release_info:
        owner, repo, tag = release_info

        h = find_checksum_github_api(owner, repo, tag, target_filename)
        if h:
            return h

        base_url = download_url.rsplit("/", 1)[0]

        candidates = [
            f"{download_url}.sha256",
            f"{download_url}.sha256sum",
            f"{base_url}/sha256sums.txt",
            f"{base_url}/SHA256SUMS",
            f"{base_url}/SHASUMS256.txt",
            f"{base_url}/checksums.txt",
            f"{base_url}/checksums-amd64.txt",
        ]

        for url in candidates:
            h = find_checksum_in_checksums_file(url, target_filename)
            if h:
                return h

        for url in candidates[:2]:
            h = find_checksum_single_file(url)
            if h:
                return h
    else:
        base_url = download_url.rsplit("/", 1)[0]
        for suffix in [".sha256", ".sha256sum"]:
            h = find_checksum_single_file(f"{download_url}{suffix}")
            if h:
                return h
        for fname in ["sha256sums.txt", "SHA256SUMS", "checksums.txt"]:
            h = find_checksum_in_checksums_file(f"{base_url}/{fname}", target_filename)
            if h:
                return h

    return None


def has_sha256_verification(content: str) -> bool:
    return bool(re.search(r"sha256sum\s+-c", content))


def insert_checksum_verification(
    content: str, output_path: str, sha256: str
) -> str | None:
    lines = content.splitlines()

    curl_start = None
    output_line_idx = None
    run_line_idx = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if curl_start is None and "curl" in stripped:
            curl_start = i
            run_line_idx = i
            while run_line_idx >= 0 and "RUN" not in lines[run_line_idx]:
                run_line_idx -= 1
        if curl_start is not None and output_line_idx is None:
            if f"-o {output_path}" in line or f"-o{output_path}" in line:
                output_line_idx = i
                break
            if f'-o "{output_path}' in line:
                output_line_idx = i
                break
            m = re.search(r"-o\s+(\S+)", line)
            if m:
                found_path = m.group(1).rstrip("\\").strip('"').strip("'")
                if found_path == output_path:
                    output_line_idx = i
                    break
            if i - curl_start > 10:
                break

    if output_line_idx is None or run_line_idx < 0:
        return None

    run_line = lines[run_line_idx]
    indent_match = re.match(r"^(\s*)RUN", run_line)
    indent = indent_match.group(1) if indent_match else ""
    verify_line = f'{indent}    echo "{sha256}  {output_path}" | sha256sum -c - && \\'
    lines.insert(output_line_idx + 1, verify_line)

    return "\n".join(lines) + "\n"


def update_manifest_checksum(manifest_path: Path, sha256: str) -> bool:
    if not manifest_path.exists():
        return False
    content = manifest_path.read_text()
    if re.search(r'checksum\s*=\s*"[0-9a-fA-F]{64}"', content):
        content_new = re.sub(
            r'checksum\s*=\s*"[0-9a-fA-F]{64}"',
            f'checksum = "{sha256}"',
            content,
        )
        manifest_path.write_text(content_new)
        return True
    if "[download]" in content:
        download_section = re.search(r"(\[download\].*?)(\n\[|\Z)", content, re.DOTALL)
        if download_section:
            section = download_section.group(1)
            if "checksum" not in section:
                insert_pos = download_section.end(1)
                new_content = (
                    content[:insert_pos].rstrip()
                    + f'\nchecksum = "{sha256}"\n'
                    + content[insert_pos:]
                )
                manifest_path.write_text(new_content)
                return True
    return False


def process_image(image_name: str, config: dict, dry_run: bool = False) -> str:
    image_dir = IMAGES_DIR / image_name
    dockerfile_path = image_dir / "Dockerfile"
    manifest_path = image_dir / "manifest.toml"

    if not dockerfile_path.exists():
        return "SKIP: no Dockerfile"

    version = extract_version_from_dockerfile(dockerfile_path)
    if not version:
        return "SKIP: no VERSION arg found"

    download_url = config["url_template"].replace("{VERSION}", version)
    target_filename = config["filename"].replace("{VERSION}", version)
    output_path = config["output_path"]

    content = dockerfile_path.read_text()
    if has_sha256_verification(content):
        return "SKIP: already has sha256sum verification"

    logger.info(
        "%s: looking up checksum for %s (v%s)...", image_name, target_filename, version
    )

    sha256 = find_checksum_for_image(image_name, download_url, target_filename)
    if not sha256:
        return f"FAIL: no checksum found for {download_url}"

    logger.info("%s: found sha256=%s...", image_name, sha256[:16])

    if dry_run:
        return "DRY-RUN: would insert checksum"

    new_content = insert_checksum_verification(content, output_path, sha256)
    if new_content is None:
        return "FAIL: could not find insertion point in Dockerfile"

    dockerfile_path.write_text(new_content)

    if manifest_path.exists():
        update_manifest_checksum(manifest_path, sha256)

    return f"OK: sha256={sha256[:16]}... inserted"


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        logger.info("DRY RUN MODE - no files will be modified")

    success = 0
    failed = 0
    skipped = 0

    for image_name in sorted(IMAGES.keys()):
        config = IMAGES[image_name]
        result = process_image(image_name, config, dry_run=args.dry_run)

        if result.startswith("OK"):
            print(f"  + {image_name}: {result}")
            success += 1
        elif result.startswith("FAIL"):
            print(f"  x {image_name}: {result}")
            failed += 1
        elif result.startswith("DRY-RUN"):
            print(f"  ~ {image_name}: {result}")
            success += 1
        else:
            print(f"  - {image_name}: {result}")
            skipped += 1

        time.sleep(1)

    total = success + failed + skipped
    print(f"\n{'=' * 60}")
    print(
        f"Results: {success}/{total} populated, {failed}/{total} failed, {skipped}/{total} skipped"
    )
    print(f"{'=' * 60}")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
