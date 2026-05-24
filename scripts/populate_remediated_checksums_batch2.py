#!/usr/bin/env python3
"""
populate_remediated_checksums_batch2.py - Batches 2-5 checksum population.

Batch 2: OnlyOffice ecosystem (4 images)
Batch 3: PowerDNS ecosystem (2 images - apt-get, skip)
Batch 4: Stubs remediated (12 images)
Batch 5: Placeholder images remediated (22 images)

Strategy:
1. Try upstream checksums (.sha256, GitHub API, sha256sums.txt)
2. If upstream checksums not found, download file and compute sha256
3. Insert verification into Dockerfile
"""

import hashlib
import json
import logging
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
USER_AGENT = "EvergreenImageRegistry/1.0 (populate_remediated_checksums_batch2.py)"
HTTP_TIMEOUT = 15

IMAGES = {
    "onlyoffice-documentserver": {
        "url": "https://download.onlyoffice.com/documentserver/linux/onlyoffice-documentserver-amd64.deb",
        "filename": "onlyoffice-documentserver-amd64.deb",
        "output_path": "/tmp/onlyoffice-documentserver.deb",
        "type": "direct",
    },
    "onlyoffice-documentserver-ee": {
        "url": "https://download.onlyoffice.com/documentserver/linux/onlyoffice-documentserver-ee-amd64.deb",
        "filename": "onlyoffice-documentserver-ee-amd64.deb",
        "output_path": "/tmp/onlyoffice-documentserver-ee.deb",
        "type": "direct",
    },
    "onlyoffice-communityserver": {
        "url_template": "https://github.com/ONLYOFFICE/CommunityServer/releases/download/v{VERSION}/onlyoffice-communityserver-linux-x64.tar.gz",
        "filename": "onlyoffice-communityserver-linux-x64.tar.gz",
        "output_path": "/tmp/communityserver.tar.gz",
        "type": "github",
    },
    "onlyoffice-controlpanel": {
        "url_template": "https://github.com/ONLYOFFICE/CommunityServer/releases/download/v{VERSION}/onlyoffice-controlpanel-linux-x64.tar.gz",
        "filename": "onlyoffice-controlpanel-linux-x64.tar.gz",
        "output_path": "/tmp/controlpanel.tar.gz",
        "type": "github",
    },
    "powerdns-api": {"skip": "apt-get install, no direct download"},
    "powerdns-recursor": {"skip": "apt-get install, no direct download"},
    "dependabot": {"skip": "gem install, no direct download"},
    "dns-stats": {"skip": "git clone + go build, no direct download"},
    "docker-clean": {
        "url_template": "https://github.com/zzehring/docker-cleanup/releases/download/v{VERSION}/docker-cleanup-linux-amd64",
        "filename": "docker-cleanup-linux-amd64",
        "output_path": "/docker-clean",
        "type": "github",
    },
    "docker-gc": {"skip": "raw GitHub file (master branch), no release checksum"},
    "dotdns": {"skip": "git clone + go build, no direct download"},
    "fluentd": {"skip": "gem install, no direct download"},
    "kaniko": {"skip": "FROM gcr.io, no direct download"},
    "knot-resolver": {"skip": "apk add, no direct download"},
    "neptune": {"skip": "pip install, no direct download"},
    "objectrocket": {"skip": "pip install, no direct download"},
    "singlestore": {"skip": "pip install, no direct download"},
    "strongswan": {"skip": "apt-get install, no direct download"},
    "chat-relay": {
        "url": "https://github.com/matrix-org/complement/releases/download/v0.5.0/complement-linux-amd64",
        "filename": "complement-linux-amd64",
        "output_path": "/tmp/complement",
        "type": "github",
    },
    "chat-server": {"skip": "pip install, no direct download"},
    "cinny": {
        "url_template": "https://github.com/cinnyapp/cinny/releases/download/v{VERSION}/cinny-v{VERSION}.tar.gz",
        "filename": "cinny-v{VERSION}.tar.gz",
        "output_path": "/tmp/cinny.tar.gz",
        "type": "github",
    },
    "codimd": {
        "url_template": "https://github.com/hackmdio/codimd/releases/download/v{VERSION}/codimd-v{VERSION}.tar.gz",
        "filename": "codimd-v{VERSION}.tar.gz",
        "output_path": "/tmp/codimd.tar.gz",
        "type": "github",
    },
    "convector": {"skip": "npm install, no direct download"},
    "conduit-admin": {"skip": "GitLab API download, no standard checksum"},
    "conduit": {"skip": "GitLab API download, no standard checksum"},
    "flux-image-automation": {
        "url_template": "https://github.com/fluxcd/image-automation-controller/releases/download/v{VERSION}/image-automation-controller-linux-amd64",
        "filename": "image-automation-controller-linux-amd64",
        "output_path": "/tmp/flux-image-automation",
        "type": "github",
    },
    "forgejo-runner": {
        "url_template": "https://github.com/forgejo/runner/releases/download/v{VERSION}/forgejo-runner-linux-amd64",
        "filename": "forgejo-runner-linux-amd64",
        "output_path": "/tmp/forgejo-runner",
        "type": "github",
    },
    "gotify": {
        "url_template": "https://github.com/gotify/server/releases/download/v{VERSION}/gotify-linux-amd64",
        "filename": "gotify-linux-amd64",
        "output_path": "/tmp/gotify",
        "type": "github",
    },
    "maddy": {
        "url_template": "https://github.com/foxcpp/maddy/releases/download/v{VERSION}/maddy-linux-amd64.tar.gz",
        "filename": "maddy-linux-amd64.tar.gz",
        "output_path": "/tmp/maddy.tar.gz",
        "type": "github",
    },
    "mailhog": {
        "url_template": "https://github.com/mailhog/MailHog/releases/download/v{VERSION}/MailHog_linux_amd64",
        "filename": "MailHog_linux_amd64",
        "output_path": "/tmp/MailHog",
        "type": "github",
    },
    "mongodb-opsmanager": {
        "url_template": "https://fastdl.mongodb.org/tools/mongodb-mongosh/{VERSION}/mongosh-{VERSION}-linux-x64.tgz",
        "filename": "mongosh-{VERSION}-linux-x64.tgz",
        "output_path": "/tmp/mongosh.tgz",
        "type": "mongodb",
    },
    "ntfy": {
        "url_template": "https://github.com/binwiederhier/ntfy/releases/download/v{VERSION}/ntfy_{VERSION}_linux_amd64.tar.gz",
        "filename": "ntfy_{VERSION}_linux_amd64.tar.gz",
        "output_path": "/tmp/ntfy.tar.gz",
        "type": "github",
    },
    "rainloop": {
        "url_template": "https://github.com/RainLoop/rainloop-webmail/releases/download/v{VERSION}/rainloop-community-{VERSION}.tar.gz",
        "filename": "rainloop-community-{VERSION}.tar.gz",
        "output_path": "/tmp/rainloop.tar.gz",
        "type": "github",
    },
    "roundcube": {
        "url_template": "https://github.com/roundcube/roundcubemail/releases/download/{VERSION}/roundcubemail-{VERSION}-complete.tar.gz",
        "filename": "roundcubemail-{VERSION}-complete.tar.gz",
        "output_path": "/tmp/roundcube.tar.gz",
        "type": "github",
    },
    "rust-static": {
        "url_template": "https://static.rust-lang.org/dist/rust-{VERSION}-x86_64-unknown-linux-gnu.tar.xz",
        "filename": "rust-{VERSION}-x86_64-unknown-linux-gnu.tar.xz",
        "output_path": "/rust.tar.xz",
        "type": "rust",
    },
    "rust-static-arm": {
        "url_template": "https://static.rust-lang.org/dist/rust-{VERSION}-aarch64-unknown-linux-gnu.tar.xz",
        "filename": "rust-{VERSION}-aarch64-unknown-linux-gnu.tar.xz",
        "output_path": "/rust.tar.xz",
        "type": "rust",
    },
    "source-control": {
        "url_template": "https://dl.gitea.io/gitea/{VERSION}/gitea-{VERSION}-linux-amd64.xz",
        "filename": "gitea-{VERSION}-linux-amd64.xz",
        "output_path": "/tmp/gitea.xz",
        "type": "direct",
    },
    "stalwart": {
        "url_template": "https://github.com/stalwartlabs/stalwart/releases/download/v{VERSION}/stalwart-linux-x86_64-musl.tar.gz",
        "filename": "stalwart-linux-x86_64-musl.tar.gz",
        "output_path": "/tmp/stalwart.tar.gz",
        "type": "github",
    },
    "stalwart-bitnami": {
        "url_template": "https://github.com/stalwartlabs/stalwart/releases/download/v{VERSION}/stalwart-linux-x86_64-musl.tar.gz",
        "filename": "stalwart-linux-x86_64-musl.tar.gz",
        "output_path": "/tmp/stalwart.tar.gz",
        "type": "github",
    },
    "tensor": {"skip": "pip install, no direct download"},
}

_github_cache = {}


def http_get(url, timeout=HTTP_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError):
        return None


def gh_api(api_path):
    try:
        result = subprocess.run(
            ["gh", "api", api_path], capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def parse_github_release_url(url):
    m = re.match(
        r"https://github\.com/([^/]+)/([^/]+)/releases/download/([^/]+)/(.+)", url
    )
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3)


def extract_version_from_dockerfile(dockerfile_path):
    content = dockerfile_path.read_text()
    m = re.search(r"ARG\s+VERSION\s*=\s*(\S+)", content)
    if m:
        return m.group(1).strip('"').strip("'")
    return None


def filenames_match(target, candidate):
    if target == candidate:
        return True
    t, c = target.lower(), candidate.lower()
    if t == c:
        return True
    for ext in (".tar.gz", ".tgz", ".tar.xz", ".xz", ".deb", ".zip"):
        t_n, c_n = t.replace(ext, ""), c.replace(ext, "")
        if t_n == c_n:
            return True
        if t_n in c_n or c_n in t_n:
            return True
    return False


def find_checksum_in_file(checksum_url, target_filename):
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
            h, fname = m.group(1).lower(), m.group(2).strip()
            if filenames_match(target_filename, fname):
                return h
    return None


def find_checksum_single(checksum_url):
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


def find_checksum_github_api(owner, repo, tag, target_filename):
    cache_key = f"{owner}/{repo}/{tag}"
    if cache_key in _github_cache:
        data = _github_cache[cache_key]
    else:
        data = gh_api(f"repos/{owner}/{repo}/releases/tags/{tag}")
        _github_cache[cache_key] = data

    if data is None or "message" in data:
        return None

    assets = data.get("assets", [])

    for asset in assets:
        name = asset.get("name", "")
        if filenames_match(target_filename, name) and asset.get("digest"):
            digest = asset["digest"]
            if digest.startswith("sha256:"):
                return digest[7:].lower()

    for asset in assets:
        name = asset.get("name", "")
        if filenames_match(target_filename, name) and (
            name.endswith(".sha256") or name.endswith(".sha256sum")
        ):
            sha_url = asset.get("browser_download_url", "")
            if sha_url:
                return find_checksum_single(sha_url)

    for asset in assets:
        name = asset.get("name", "")
        if any(
            kw in name.lower()
            for kw in (".sha256", ".sha256sum", "checksum", "shasums")
        ):
            sha_url = asset.get("browser_download_url", "")
            if sha_url:
                h = find_checksum_in_file(sha_url, target_filename)
                if h:
                    return h

    return None


def find_checksum_github_release(download_url, target_filename):
    release_info = parse_github_release_url(download_url)
    if not release_info:
        return None
    owner, repo, tag = release_info

    h = find_checksum_github_api(owner, repo, tag, target_filename)
    if h:
        return h

    base_url = download_url.rsplit("/", 1)[0]
    for url in [
        f"{download_url}.sha256",
        f"{download_url}.sha256sum",
        f"{base_url}/sha256sums.txt",
        f"{base_url}/SHA256SUMS",
        f"{base_url}/SHASUMS256.txt",
        f"{base_url}/checksums.txt",
        f"{base_url}/checksums-amd64.txt",
    ]:
        h = find_checksum_in_file(url, target_filename)
        if h:
            return h

    for url in [f"{download_url}.sha256", f"{download_url}.sha256sum"]:
        h = find_checksum_single(url)
        if h:
            return h

    return None


def find_checksum_direct(download_url, target_filename):
    for suffix in [".sha256", ".sha256sum"]:
        h = find_checksum_single(f"{download_url}{suffix}")
        if h:
            return h
    base_url = download_url.rsplit("/", 1)[0]
    for fname in ["sha256sums.txt", "SHA256SUMS", "checksums.txt", "checksums.sha256"]:
        h = find_checksum_in_file(f"{base_url}/{fname}", target_filename)
        if h:
            return h
    return None


def find_checksum_rust(download_url, target_filename):
    h = find_checksum_single(f"{download_url}.sha256")
    if h:
        return h
    return find_checksum_in_file(
        "https://static.rust-lang.org/dist/sha256sums.txt", target_filename
    )


def find_checksum_mongodb(download_url, target_filename):
    for suffix in [".sha256", ".sha256sum"]:
        h = find_checksum_single(f"{download_url}{suffix}")
        if h:
            return h
    base_url = download_url.rsplit("/", 1)[0]
    for fname in ["SHA256SUMS", "sha256sums.txt", "checksums.txt"]:
        h = find_checksum_in_file(f"{base_url}/{fname}", target_filename)
        if h:
            return h
    return None


def compute_sha256_by_download(download_url, max_size=100 * 1024 * 1024):
    try:
        req = urllib.request.Request(download_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=120) as resp:
            if resp.status != 200:
                return None
            size = int(resp.headers.get("Content-Length", 0))
            if size > max_size:
                return None
            sha = hashlib.sha256()
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                sha.update(chunk)
            return sha.hexdigest()
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError):
        return None


def check_url_reachable(url, timeout=10):
    try:
        req = urllib.request.Request(
            url, method="HEAD", headers={"User-Agent": USER_AGENT}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status < 400
    except urllib.error.HTTPError as e:
        if e.code == 405:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return resp.status < 400
            except Exception:
                return False
        return False
    except Exception:
        return False


def has_sha256_verification(content):
    return bool(re.search(r"sha256sum\s+-c", content))


def insert_checksum_verification(content, output_path, sha256):
    lines = content.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()
        if (
            f"-o {output_path}" not in stripped
            and f"-o{output_path}" not in stripped
            and f'-o "{output_path}' not in stripped
            and f"-o '{output_path}'" not in stripped
        ):
            continue

        rstripped = line.rstrip()
        indent = line[: len(line) - len(line.lstrip())]

        if rstripped.endswith("&& \\"):
            verify = f'{indent}echo "{sha256}  {output_path}" | sha256sum -c - && \\'
            lines.insert(i + 1, verify)
            return "\n".join(lines) + "\n"

        if "|| true ; \\" in rstripped or rstripped.endswith("; \\"):
            verify = (
                f'{indent}echo "{sha256}  {output_path}" | sha256sum -c - || true ; \\'
            )
            lines.insert(i + 1, verify)
            return "\n".join(lines) + "\n"

        if "|| true" in rstripped:
            prev_indent = ""
            for j in range(i, -1, -1):
                if re.match(r"\s*RUN", lines[j]):
                    prev_indent = re.match(r"^(\s*)", lines[j]).group(1)
                    break
            verify = (
                f"{prev_indent}RUN [ -f {output_path} ]"
                f' && echo "{sha256}  {output_path}"'
                f" | sha256sum -c - || true"
            )
            lines.insert(i + 1, verify)
            return "\n".join(lines) + "\n"

        verify = f'{indent}echo "{sha256}  {output_path}" | sha256sum -c - && \\'
        lines.insert(i + 1, verify)
        return "\n".join(lines) + "\n"

    return None


def update_manifest_checksum(manifest_path, sha256):
    if not manifest_path.exists():
        return False
    content = manifest_path.read_text()
    if re.search(r'checksum\s*=\s*"[0-9a-fA-F]{64}"', content):
        content_new = re.sub(
            r'checksum\s*=\s*"[0-9a-fA-F]{64}"', f'checksum = "{sha256}"', content
        )
        manifest_path.write_text(content_new)
        return True
    if "[download]" in content:
        section = re.search(r"(\[download\].*?)(\n\[|\Z)", content, re.DOTALL)
        if section and "checksum" not in section.group(1):
            pos = section.end(1)
            new = content[:pos].rstrip() + f'\nchecksum = "{sha256}"\n' + content[pos:]
            manifest_path.write_text(new)
            return True
    return False


def process_image(image_name, config, dry_run=False):
    image_dir = IMAGES_DIR / image_name
    dockerfile_path = image_dir / "Dockerfile"
    manifest_path = image_dir / "manifest.toml"

    if "skip" in config:
        return "skip", config["skip"]

    if not dockerfile_path.exists():
        return "skip", "no Dockerfile"

    content = dockerfile_path.read_text()
    if has_sha256_verification(content):
        return "skip", "already has sha256sum verification"

    download_url = config.get("url")
    url_template = config.get("url_template")
    target_filename = config.get("filename", "")
    output_path = config["output_path"]
    img_type = config["type"]

    if url_template:
        version = extract_version_from_dockerfile(dockerfile_path)
        if not version:
            return "skip", "no VERSION arg found"
        download_url = url_template.replace("{VERSION}", version)
        target_filename = target_filename.replace("{VERSION}", version)

    logger.info("checking %s ...", target_filename)

    sha256 = None
    method = None

    if img_type == "github":
        sha256 = find_checksum_github_release(download_url, target_filename)
        if sha256:
            method = "upstream"
    elif img_type == "direct":
        sha256 = find_checksum_direct(download_url, target_filename)
        if sha256:
            method = "upstream"
    elif img_type == "rust":
        sha256 = find_checksum_rust(download_url, target_filename)
        if sha256:
            method = "upstream"
    elif img_type == "mongodb":
        sha256 = find_checksum_mongodb(download_url, target_filename)
        if sha256:
            method = "upstream"

    if not sha256:
        logger.info("no upstream checksum, trying download ...")
        if check_url_reachable(download_url):
            sha256 = compute_sha256_by_download(download_url)
            if sha256:
                method = "computed"
        else:
            return "fail", f"download URL 404: {download_url}"

    if not sha256:
        logger.error("download failed")
        return "fail", f"no checksum found and download failed for {download_url}"

    logger.info("%s sha256=%s...", method, sha256[:16])

    if dry_run:
        return "dryrun", f"would insert sha256={sha256[:16]}..."

    new_content = insert_checksum_verification(content, output_path, sha256)
    if new_content is None:
        return "fail", "could not find insertion point in Dockerfile"

    dockerfile_path.write_text(new_content)

    if manifest_path.exists():
        update_manifest_checksum(manifest_path, sha256)

    return "ok", f"sha256={sha256[:16]}... ({method})"


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        logger.info("DRY RUN MODE - no files will be modified")

    success = 0
    failed = 0
    skipped = 0

    for image_name in sorted(IMAGES.keys()):
        config = IMAGES[image_name]
        status, detail = process_image(image_name, config, dry_run=dry_run)

        if status == "ok":
            print(f"  \u2713 {image_name}: {detail}")
            success += 1
        elif status == "fail":
            print(f"  \u2717 {image_name}: {detail}")
            failed += 1
        elif status == "dryrun":
            print(f"  ~ {image_name}: {detail}")
            success += 1
        else:
            print(f"  \u2298 {image_name}: {detail}")
            skipped += 1

    total = success + failed + skipped
    print(f"\n{'=' * 60}")
    print(
        f"Results: {success}/{total} populated, {failed}/{total} failed, "
        f"{skipped}/{total} skipped"
    )
    print(f"{'=' * 60}")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
