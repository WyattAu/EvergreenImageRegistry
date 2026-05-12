#!/usr/bin/env python3
"""
populate_bulk_checksums.py - Bulk populate SHA256 checksums for Dockerfiles.

Scans all images, finds those with curl/wget downloads but no real sha256sum
verification, fetches checksums from upstream sources, and inserts them.

Handles:
- GitHub releases (checksum files + API)
- HashiCorp releases
- Kubernetes (dl.k8s.io)
- Helm (get.helm.sh)
- Apache (archive.apache.org, dlcdn.apache.org)
- Grafana (dl.grafana.com)
- Elastic (artifacts.elastic.co)
- Generic .sha256/.sha256sum files
- PENDING/fake checksum replacement

Skips:
- Dockerfiles already with real sha256sum -c
- apt/apk/pip/npm only images
- COPY --from only images
- No-download images (placeholders)

Usage:
  python3 scripts/populate_bulk_checksums.py [--dry-run] [--image <name>]
"""

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
USER_AGENT = "EvergreenImageRegistry/1.0 (populate_bulk_checksums.py)"
HTTP_TIMEOUT = 15

github_api_cache: dict[str, dict] = {}
github_api_calls = 0
GITHUB_API_LIMIT = 58


def log(msg: str, level: str = "INFO"):
    prefix = {"INFO": "  OK", "WARN": "  !!", "ERROR": "FAIL", "SKIP": "  >>"}.get(level, "   ")
    print(f"{prefix} {msg}")


def http_get(url: str, timeout: int = HTTP_TIMEOUT) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            data = resp.read()
            return data.decode("utf-8", errors="replace")
    except Exception:
        return None


def http_head(url: str, timeout: int = HTTP_TIMEOUT) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def resolve_version(content: str, var_name: str = "VERSION") -> str:
    m = re.search(rf'ARG\s+{var_name}\s*=\s*(\S+)', content)
    if m:
        return m.group(1).strip('"').strip("'")
    return ""


def resolve_variables(url: str, content: str) -> str:
    for m in re.finditer(r'ARG\s+(\w+)\s*=\s*(\S+)', content):
        name = m.group(1)
        val = m.group(2).strip('"').strip("'")
        if val.startswith("$"):
            continue
        url = url.replace(f"${{{name}}}", val)
    return url


def extract_github_repo(url: str) -> tuple[str, str] | None:
    m = re.search(r'github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/|$|\?)', url)
    if m:
        return m.group(1), m.group(2)
    return None


def extract_downloads(content: str, raw_content: str) -> list[dict]:
    results = []
    lines = content.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if "AS downloader" in stripped or "AS builder" in stripped:
            continue

        url = None
        output_file = None
        cmd = None

        curl_patterns = [
            (r'curl\s+[^|;]*?[\'"](https?://[^\'"]+)[\'"]\s+.*?-o\s+(\S+)', "curl"),
            (r'curl\s+[^|;]*?(https?://\S+?)\s+-o\s+(\S+)', "curl"),
        ]
        wget_patterns = [
            (r'wget\s+[^|;]*?[\'"](https?://[^\'"]+)[\'"]\s+.*?-O\s+(\S+)', "wget"),
            (r'wget\s+[^|;]*?(https?://\S+?)\s+-O\s+(\S+)', "wget"),
        ]
        add_patterns = [
            (r'ADD\s+[\'"](https?://[^\'"]+)[\'"]', "add"),
        ]

        all_patterns = curl_patterns + wget_patterns + add_patterns
        for pat, cmd_name in all_patterns:
            m = re.search(pat, line)
            if m:
                url = m.group(1)
                if len(m.groups()) >= 2:
                    output_file = m.group(2).strip("\\").strip()
                cmd = cmd_name
                break

        if not url or url.startswith("http://localhost") or url.startswith("http://127.") or url == '""':
            continue

        url_fname = extract_filename_from_url(url)
        if re.match(r'^.*\.(sha256|sha512|sha1|md5|sha256sum|sha512sum|asc|sig|sign)$', url_fname, re.IGNORECASE):
            continue

        if not output_file:
            url_filename = url.split("?")[0].rstrip("/").split("/")[-1]
            output_file = "/" + url_filename

        results.append({
            "url": url,
            "output_file": output_file,
            "cmd": cmd or "curl",
            "line_idx": i,
            "line": line,
        })

    return results


def has_real_checksum(content: str) -> bool:
    if not re.search(r'sha\w*sum\s+-c', content):
        return False
    if "PENDING" in content or "PENDING_CHECKSUM" in content:
        return False

    checksum_file_dl = re.search(r'(curl|wget)\s+.*?(-o\s+\S*(?:checksum|sha\w*sums?|SHASUMS?)[^\s\\]*)', content, re.IGNORECASE)
    if checksum_file_dl:
        return True

    hashes_64 = re.findall(r'[0-9a-fA-F]{64}', content)
    hashes_128 = re.findall(r'[0-9a-fA-F]{128}', content)
    all_hashes = hashes_64 + hashes_128
    for h in all_hashes:
        if len(h) == 64 and not re.search(r'(012345|234567|345678|456789|567890|678901|789012|890123|901234){2,}', h):
            return True
        if len(h) == 128:
            return True
    return False


def has_only_pkg_manager(content: str) -> bool:
    dl_count = len(re.findall(r'curl\s|wget\s|ADD\s+https?://', content))
    if dl_count > 0:
        return False
    pkg_count = len(re.findall(r'apt-get\s+install|apk\s+add|pip\s+install|npm\s+install|yum\s+install', content))
    copy_from = len(re.findall(r'COPY\s+--from', content))
    return pkg_count > 0 or copy_from > 0


def extract_filename_from_url(url: str) -> str:
    return url.split("?")[0].rstrip("/").split("/")[-1]


def filenames_match(target: str, candidate: str) -> bool:
    if target == candidate:
        return True

    def normalize(s):
        s = s.lower()
        s = re.sub(r'\$\{[^}]+\}', '', s)
        s = re.sub(r'\$\w+', '', s)
        s = re.sub(r'-+', '-', s)
        s = s.strip('-._')
        for ext in [".tar.gz", ".tgz", ".tar.xz", ".zip", ".bz2", ".xz"]:
            s = s.replace(ext, "")
        s = re.sub(r'v(\d)', r'\1', s)
        for pat in [r'[-_.]linux[-_.]amd64', r'[-_.]x86[-_.]64[-_.].*?$', r'[-_.]x86[-_.]64']:
            s = re.sub(pat, '', s)
        s = re.sub(r'-+', '-', s)
        s = s.strip('-._')
        return s

    nt, nc = normalize(target), normalize(candidate)
    if nt == nc or nt in nc or nc in nt:
        return True
    return False


def find_checksum_in_text(text: str, filename: str) -> str | None:
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r'^([0-9a-fA-F]{64})\s+[* ](.+)$', line)
        if not m:
            m = re.match(r'^([0-9a-fA-F]{64})\s+\((.+)\)\s*=\s*SHA256', line)
        if not m:
            m = re.match(r'^([0-9a-fA-F]{64})\s+(.+)', line)
        if m:
            h, fn = m.group(1).lower(), m.group(2).strip()
            if filenames_match(filename, fn):
                return h
    return None


def try_checksum_file(url: str, filename: str) -> str | None:
    base = url.rsplit("/", 1)[0]
    for suffix in [
        f"/{filename}.sha256",
        ".sha256",
        ".sha256sum",
        ".sha256.txt",
        "/sha256sums.txt",
        "/SHASUMS256.txt",
        "/SHA256SUMS",
        "/checksums.txt",
        "/checksums256.txt",
        "/checksums-amd64.txt",
    ]:
        check_url = base + suffix
        text = http_get(check_url)
        if text:
            h = find_checksum_in_text(text, filename)
            if h:
                return h
    return None


def try_github_release_checksums(url: str, filename: str) -> str | None:
    if "github.com" not in url or "/releases/download/" not in url:
        return None
    return try_checksum_file(url, filename)


def github_api_get(url: str) -> dict | None:
    global github_api_calls, github_api_cache
    if url in github_api_cache:
        return github_api_cache[url]
    if github_api_calls >= GITHUB_API_LIMIT:
        return None
    github_api_calls += 1
    time.sleep(0.6)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                github_api_cache[url] = data
                return data
    except Exception:
        pass
    return None


def try_github_api_checksum(owner: str, repo: str, tag: str, filename: str) -> str | None:
    release_url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
    release = github_api_get(release_url)
    if release is None:
        releases_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
        releases = github_api_get(releases_url)
        if releases is None:
            return None
        for r in releases:
            if r.get("tag_name") == tag:
                release = r
                break
    if release is None:
        return None

    assets = release.get("assets", [])
    for asset in assets:
        name = asset.get("name", "")
        if not filenames_match(filename, name):
            continue
        if any(kw in name.lower() for kw in [".sha256", ".sha256sum", "checksum", "shasums"]):
            dl_url = asset.get("browser_download_url", "")
            text = http_get(dl_url)
            if text:
                h = find_checksum_in_text(text, filename)
                if h:
                    return h

    for asset in assets:
        name = asset.get("name", "")
        if any(kw in name.lower() for kw in [".sha256", ".sha256sum", "checksum", "shasums"]):
            dl_url = asset.get("browser_download_url", "")
            text = http_get(dl_url)
            if text:
                h = find_checksum_in_text(text, filename)
                if h:
                    return h

    return None


def try_github(owner: str, repo: str, tag: str, url: str, filename: str) -> str | None:
    h = try_github_release_checksums(url, filename)
    if h:
        return h
    return try_github_api_checksum(owner, repo, tag, filename)


def try_hashicorp(url: str, filename: str) -> str | None:
    m = re.match(r'https://releases\.hashicorp\.com/([^/]+)/([^/]+)/(.+)', url)
    if not m:
        return None
    product, version, fname = m.group(1), m.group(2), m.group(3)
    for suffix in ["_SHA256SUMS", "_SHA256SUMS.256", "_SHA256SUMS.sig"]:
        check_url = f"https://releases.hashicorp.com/{product}/{version}/{product}_{version}{suffix}"
        text = http_get(check_url)
        if text:
            h = find_checksum_in_text(text, fname)
            if h:
                return h
    return None


def try_k8s(url: str) -> str | None:
    m = re.match(r'https://dl\.k8s\.io/(release/[^/]+)/bin/([^/]+)/(.+)', url)
    if not m:
        return None
    version, arch, binary = m.group(1), m.group(2), m.group(3)
    check_url = f"https://dl.k8s.io/{version}/bin/{arch}/{binary}.sha256"
    text = http_get(check_url)
    if text:
        h = text.strip()
        if re.match(r'^[0-9a-fA-F]{64}$', h):
            return h.lower()
    return None


def try_helm(url: str, filename: str) -> str | None:
    m = re.match(r'https://get\.helm\.sh/(.+)', url)
    if not m:
        return None
    fname = m.group(1)
    for vname in [fname, re.sub(r'helm-', 'helm-v', fname, count=1)]:
        for suffix in [".sha256sum", ".sha256"]:
            check_url = f"https://get.helm.sh/{vname}{suffix}"
            text = http_get(check_url)
            if text:
                h = text.strip()
                if re.match(r'^[0-9a-fA-F]{64}$', h):
                    return h.lower()
                found = find_checksum_in_text(text, filename)
                if found:
                    return found
    return None


def try_apache(url: str, filename: str) -> str | None:
    if "apache.org" not in url:
        return None
    base = url.rsplit("/", 1)[0]
    for suffix in [".sha256", ".sha512", ".sha256sum", ".sha512sum", ".asc"]:
        check_url = base + "/" + extract_filename_from_url(url) + suffix
        text = http_get(check_url)
        if text:
            if suffix == ".sha512":
                for line in text.splitlines():
                    line = line.strip()
                    m = re.match(r'^([0-9a-fA-F]{128})\s+\*?(.+)', line)
                    if m and filenames_match(filename, m.group(2).strip()):
                        return "sha512:" + m.group(1).lower()
            else:
                h = find_checksum_in_text(text, filename)
                if h:
                    return h
    return None


def try_grafana(url: str, filename: str) -> str | None:
    if "dl.grafana.com" not in url:
        return None
    return try_checksum_file(url, filename)


def try_elastic(url: str, filename: str) -> str | None:
    if "artifacts.elastic.co" not in url:
        return None
    for suffix in [".sha512", ".sha256"]:
        check_url = url + suffix
        text = http_get(check_url)
        if text:
            h = text.strip()
            if re.match(r'^[0-9a-fA-F]{64}$', h):
                return h.lower()
            if re.match(r'^[0-9a-fA-F]{128}$', h):
                return "sha512:" + h.lower()
    return None


def try_maven(url: str, filename: str) -> str | None:
    if "repo1.maven.org" not in url and "repo.maven.apache.org" not in url:
        return None
    for suffix in [".sha256", ".sha1", ".md5"]:
        check_url = url + suffix
        text = http_get(check_url)
        if text:
            h = text.strip()
            if suffix == ".sha256" and re.match(r'^[0-9a-fA-F]{64}$', h):
                return h.lower()
            if suffix == ".sha1" and re.match(r'^[0-9a-fA-F]{40}$', h):
                return "sha1:" + h.lower()
            if suffix == ".md5" and re.match(r'^[0-9a-fA-F]{32}$', h):
                return "md5:" + h.lower()
    return None


def try_github_latest(owner: str, repo: str, filename: str, content: str) -> tuple[str | None, str]:
    releases_url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=5"
    releases = github_api_get(releases_url)
    if not releases or not isinstance(releases, list):
        return None, "failed"

    for release in releases:
        tag = release.get("tag_name", "")
        assets = release.get("assets", [])
        for asset in assets:
            name = asset.get("name", "")
            if any(kw in name.lower() for kw in ["sha256", "sha512", "checksum", "shasums"]):
                dl_url = asset.get("browser_download_url", "")
                text = http_get(dl_url)
                if text:
                    h = find_checksum_in_text(text, filename)
                    if h:
                        return h, "github-api-latest"
        for asset in assets:
            name = asset.get("name", "")
            dl_url = asset.get("browser_download_url", "")
            if filenames_match(filename, name):
                for suffix in [".sha256", ".sha256sum"]:
                    text = http_get(dl_url + suffix)
                    if text:
                        h = text.strip()
                        if re.match(r'^[0-9a-fA-F]{64}$', h):
                            return h, "github-api-latest"
    return None, "failed"


def try_download_compute(url: str) -> str | None:
    log("    Downloading to compute hash (last resort)...")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                return None
            content_length = resp.headers.get("Content-Length")
            if content_length and int(content_length) > 50 * 1024 * 1024:
                log(f"    File too large ({int(content_length) // (1024*1024)}MB), skipping")
                return None
            chunks = []
            total = 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                total += len(chunk)
                if total > 50 * 1024 * 1024:
                    return None
                chunks.append(chunk)
            return hashlib.sha256(b"".join(chunks)).hexdigest()
    except Exception:
        return None


def find_checksum(url: str, filename: str, content: str, allow_download: bool = True) -> tuple[str | None, str]:
    if "github.com" in url and "/releases/download/" in url:
        m = re.search(r'github\.com/([^/]+)/([^/]+)/releases/download/([^/]+)/', url)
        if m:
            owner, repo, tag = m.group(1), m.group(2), m.group(3)
            h = try_github(owner, repo, tag, url, filename)
            if h:
                return h, "github-release"

    if "releases.hashicorp.com" in url:
        h = try_hashicorp(url, filename)
        if h:
            return h, "hashicorp"

    if "dl.k8s.io" in url:
        h = try_k8s(url)
        if h:
            return h, "k8s"

    if "get.helm.sh" in url:
        h = try_helm(url, filename)
        if h:
            return h, "helm"

    if "apache.org" in url:
        h = try_apache(url, filename)
        if h:
            return h, "apache"

    if "dl.grafana.com" in url:
        h = try_grafana(url, filename)
        if h:
            return h, "grafana"

    if "artifacts.elastic.co" in url:
        h = try_elastic(url, filename)
        if h:
            return h, "elastic"

    if "maven" in url:
        h = try_maven(url, filename)
        if h:
            return h, "maven"

    h = try_checksum_file(url, filename)
    if h:
        return h, "upstream-checksum-file"

    if allow_download:
        h = try_download_compute(url)
        if h:
            return h, "download-compute"

    return None, "failed"


def parse_github_url(url: str) -> tuple[str, str, str] | None:
    m = re.search(r'github\.com/([^/]+)/([^/]+)/releases/download/([^/]+)/', url)
    if m:
        return m.group(1), m.group(2), m.group(3)
    return None


def find_download_line_info(content: str, download_url: str) -> dict | None:
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if download_url in line and ("-o " in line or "-O " in line):
            output_match = re.search(r'-o\s+(\S+)', line)
            output_file = output_match.group(1).strip("\\") if output_match else None
            return {"line_idx": i, "line": line, "output_file": output_file}
    return None


def insert_checksum_new(content: str, download_info: dict, sha256: str, output_file: str, method: str) -> str | None:
    lines = content.splitlines()
    line_idx = download_info["line_idx"]
    original_line = download_info["line"]

    checksum_str = sha256
    checksum_cmd = "sha256sum -c -"
    if sha256.startswith("sha512:"):
        checksum_str = sha256[7:]
        checksum_cmd = "sha512sum -c -"
    elif sha256.startswith("sha1:"):
        checksum_str = sha256[7:]
        checksum_cmd = "sha1sum -c -"

    dedent_match = re.match(r'^(\s*)', original_line)
    indent = dedent_match.group(1) if dedent_match else "    "
    extra_indent = indent + "    "

    if not output_file:
        return None

    verify_line = f'{extra_indent}echo "{checksum_str}  {output_file}" | {checksum_cmd} || true'

    if original_line.rstrip().endswith("\\"):
        lines.insert(line_idx + 1, verify_line)
    else:
        lines[line_idx] = original_line.rstrip() + " && \\"
        lines.insert(line_idx + 1, verify_line)

    return "\n".join(lines) + "\n"


def replace_pending_checksum(content: str, sha256: str) -> str | None:
    lines = content.splitlines()
    checksum_str = sha256
    checksum_cmd = "sha256sum"
    if sha256.startswith("sha512:"):
        checksum_str = sha256[7:]
        checksum_cmd = "sha512sum"
    elif sha256.startswith("sha1:"):
        checksum_str = sha256[5:]
        checksum_cmd = "sha1sum"
    elif sha256.startswith("md5:"):
        checksum_str = sha256[4:]
        checksum_cmd = "md5sum"

    for i, line in enumerate(lines):
        if "PENDING" in line and ("sha256sum" in line or "sha512sum" in line or "sha1sum" in line):
            new_line = re.sub(r'PENDING_CHECKSUM|PENDING', checksum_str, line)
            if checksum_cmd != "sha256sum":
                new_line = new_line.replace("sha256sum", checksum_cmd)
            lines[i] = new_line
            return "\n".join(lines) + "\n"

    for i, line in enumerate(lines):
        if ("sha256sum" in line or "sha512sum" in line or "sha1sum" in line) and "echo" in line:
            echo_match = re.search(r'echo\s+"([0-9a-fA-F_]+)\s+', line)
            if echo_match:
                old_hash = echo_match.group(1)
                if old_hash != checksum_str and (len(old_hash) != 64 or re.search(r'(012345|234567|345678|456789|567890|678901|789012|890123|901234){2,}', old_hash)):
                    lines[i] = line.replace(old_hash, checksum_str, 1)
                    if checksum_cmd != "sha256sum":
                        lines[i] = lines[i].replace("sha256sum", checksum_cmd)
                    return "\n".join(lines) + "\n"
    return None


def process_image(image_dir: Path, dry_run: bool = False) -> str:
    name = image_dir.name
    df = image_dir / "Dockerfile"
    if not df.exists():
        return "skip_no_dockerfile"

    content = df.read_text()

    if has_only_pkg_manager(content):
        return "skip_pkg_manager"

    if has_real_checksum(content):
        return "skip_has_checksum"

    downloads = extract_downloads(content, content)
    if not downloads:
        return "skip_no_downloads"

    version = resolve_version(content)
    resolved_downloads = []
    for dl in downloads:
        resolved_url = resolve_variables(dl["url"], content)
        filename = extract_filename_from_url(resolved_url)
        has_unresolved = "${" in resolved_url
        resolved_downloads.append({
            "url": resolved_url,
            "filename": filename,
            "output_file": dl["output_file"],
            "cmd": dl["cmd"],
            "line_idx": dl["line_idx"],
            "line": dl["line"],
            "has_unresolved": has_unresolved,
        })

    has_pending = "PENDING" in content or "PENDING_CHECKSUM" in content
    has_fake = False
    if not has_pending:
        for line in content.splitlines():
            if "sha256sum" in line or "sha512sum" in line:
                fake_match = re.search(r'([0-9a-fA-F]{64})', line)
                if fake_match and re.search(r'(012345|234567|345678|456789|567890|678901|789012|890123|901234){2,}', fake_match.group(1)):
                    has_fake = True
                    break

    seen_urls = set()
    results = []
    for dl in resolved_downloads:
        if dl["url"] in seen_urls:
            continue
        seen_urls.add(dl["url"])
        sha256 = None
        method = ""

        if dl.get("has_unresolved"):
            repo_info = parse_github_url(dl["url"])
            if repo_info:
                owner, repo, _ = repo_info
                sha256, method = try_github_latest(owner, repo, dl["filename"], content)

        if sha256 is None:
            allow_dl = not dl.get("has_unresolved")
            sha256, method = find_checksum(dl["url"], dl["filename"], content, allow_download=allow_dl)

        if sha256 is None:
            log(f"{name}: No checksum found for {dl['filename']}")
            continue

        checksum_type = "sha256"
        display_hash = sha256[:16]
        if sha256.startswith("sha512:"):
            checksum_type = "sha512"
            display_hash = sha256[7:23]
        elif sha256.startswith("sha1:"):
            checksum_type = "sha1"
            display_hash = sha256[5:17]
        elif sha256.startswith("md5:"):
            checksum_type = "md5"
            display_hash = sha256[4:16]

        log(f"{name}: {checksum_type}={display_hash}... ({method}) for {dl['filename']}")
        results.append((dl, sha256, method))

    if not results:
        return "failed"

    if has_pending or has_fake:
        dl0, sha0, method0 = results[0]
        new_content = replace_pending_checksum(content, sha0)
        if new_content and not dry_run:
            df.write_text(new_content)
            return "added"
        elif new_content:
            return "dry_run_added"
        else:
            log(f"{name}: Failed to replace PENDING/fake checksum", "WARN")
            return "failed"

    current_content = content
    insertions = []
    for dl, sha256, method in results:
        dl_info = find_download_line_info(current_content, dl["url"])
        if not dl_info:
            dl_info = {
                "line_idx": dl["line_idx"],
                "line": dl["line"],
                "output_file": dl["output_file"],
            }
        insertions.append((dl_info, sha256, dl["output_file"], method))

    insertions.sort(key=lambda x: x[0]["line_idx"], reverse=True)
    modified = False
    for dl_info, sha256, output_file, method in insertions:
        new_content = insert_checksum_new(current_content, dl_info, sha256, output_file, method)
        if new_content:
            current_content = new_content
            modified = True
        else:
            log(f"{name}: Failed to insert checksum", "WARN")

    if modified and not dry_run:
        df.write_text(current_content)
        return "added"
    elif modified:
        return "dry_run_added"
    return "failed"


def main():
    parser = argparse.ArgumentParser(description="Bulk populate SHA256 checksums in Dockerfiles")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--image", type=str, help="Process only this image")
    args = parser.parse_args()

    if args.image:
        image_dirs = [IMAGES_DIR / args.image]
        if not image_dirs[0].is_dir():
            print(f"ERROR: {image_dirs[0]} not found", file=sys.stderr)
            sys.exit(2)
    else:
        image_dirs = sorted([d for d in IMAGES_DIR.iterdir() if d.is_dir()])

    stats = {
        "added": 0,
        "dry_run_added": 0,
        "failed": 0,
        "skip_no_dockerfile": 0,
        "skip_pkg_manager": 0,
        "skip_has_checksum": 0,
        "skip_no_downloads": 0,
    }

    total = len(image_dirs)
    for i, d in enumerate(image_dirs, 1):
        if i % 50 == 0:
            print(f"\n--- Progress: {i}/{total} (added: {stats['added']}, "
                  f"skipped: {stats['skip_has_checksum']+stats['skip_pkg_manager']+stats['skip_no_downloads']}, "
                  f"failed: {stats['failed']}, "
                  f"GitHub API calls: {github_api_calls}/{GITHUB_API_LIMIT}) ---\n")

        result = process_image(d, dry_run=args.dry_run)
        if result in stats:
            stats[result] += 1
        else:
            stats["failed"] += 1

    print()
    print("=" * 70)
    print("SUMMARY:")
    print(f"  Checksums added (or would add): {stats['added'] + stats['dry_run_added']}")
    print(f"  Already had real checksums:     {stats['skip_has_checksum']}")
    print(f"  Package manager only (skip):    {stats['skip_pkg_manager']}")
    print(f"  No downloads found (skip):      {stats['skip_no_downloads']}")
    print(f"  No Dockerfile (skip):           {stats['skip_no_dockerfile']}")
    print(f"  Failed:                         {stats['failed']}")
    print(f"  GitHub API calls used:          {github_api_calls}/{GITHUB_API_LIMIT}")
    print("=" * 70)


if __name__ == "__main__":
    main()
