#!/usr/bin/env python3
"""Resolve eligible Docker image references and emit safe pinning proposals."""

import argparse
import base64
import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
ARG_RE = re.compile(r"^ARG\s+([A-Za-z_][A-Za-z0-9_]*)(?:=(.*))?$")
VAR_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)")


def parse_reference(reference: str) -> tuple[str, str, str] | None:
    if "${" in reference or "$" in reference or "@" in reference or "://" in reference:
        return None
    parts = reference.split("/")
    if len(parts) == 1:
        registry, repo = "registry-1.docker.io", f"library/{parts[0]}"
    elif "." in parts[0] or ":" in parts[0] or parts[0] == "localhost":
        registry, repo = parts[0], "/".join(parts[1:])
    else:
        registry, repo = "registry-1.docker.io", "/".join(parts)
    if ":" in repo.rsplit("/", 1)[-1]:
        repo, tag = repo.rsplit(":", 1)
    else:
        tag = "latest"
    return (registry, repo, tag) if registry and repo and tag else None


def expand_reference(reference: str, dockerfile: str, environment: dict | None = None) -> str | None:
    values = dict(environment or {})
    for raw_line in dockerfile.splitlines():
        match = ARG_RE.match(raw_line.strip())
        if match and match.group(2) is not None:
            values.setdefault(match.group(1), match.group(2).strip().strip('"').strip("'"))
    unresolved = False

    def replace(match: re.Match) -> str:
        nonlocal unresolved
        name = match.group(1) or match.group(2)
        if name not in values:
            unresolved = True
            return match.group(0)
        return values[name]

    expanded = VAR_RE.sub(replace, reference)
    return None if unresolved or "$" in expanded else expanded


def validate_digest(value: str | None) -> str | None:
    value = value.strip().lower() if value else ""
    return value if DIGEST_RE.fullmatch(value) else None


def _manifest_url(registry: str, repository: str, reference: str) -> str:
    return f"https://{registry}/v2/{urllib.parse.quote(repository, safe='/')}/manifests/{urllib.parse.quote(reference, safe='')}"


def _auth_header(challenge: str, timeout: float) -> str | None:
    match = re.match(r"Bearer\s+(.+)", challenge, re.IGNORECASE)
    if not match:
        return None
    params = dict(re.findall(r'(\w+)="([^"]*)"', match.group(1)))
    realm = params.get("realm")
    if not realm:
        return None
    query = {key: value for key, value in params.items() if key in {"service", "scope"}}
    token_url = realm + ("?" + urllib.parse.urlencode(query) if query else "")
    request = urllib.request.Request(token_url, headers={"User-Agent": "evergreen-critical-digest-resolver/1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            token_data = json.loads(response.read())
        token = token_data.get("token") or token_data.get("access_token")
        return f"Bearer {token}" if token else None
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, json.JSONDecodeError):
        return None


def inspect_manifest(reference: str, timeout: float = 15.0, credentials: dict | None = None) -> dict:
    parsed = parse_reference(reference)
    if parsed is None:
        return {"reference": reference, "status": "unsupported-reference"}
    registry, repository, tag = parsed
    headers = {"Accept": ", ".join([
        "application/vnd.oci.image.index.v1+json",
        "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.oci.image.manifest.v1+json",
        "application/vnd.docker.distribution.manifest.v2+json",
    ]), "User-Agent": "evergreen-critical-digest-resolver/1"}
    credentials = credentials or {}
    username, password = credentials.get(registry + "_USERNAME"), credentials.get(registry + "_PASSWORD")
    if username is not None and password is not None:
        headers["Authorization"] = "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()
    for attempt in range(2):
        try:
            request = urllib.request.Request(_manifest_url(registry, repository, tag), headers=headers)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read()
                digest = validate_digest(response.headers.get("Docker-Content-Digest"))
                if digest is None:
                    return {"reference": reference, "status": "invalid-registry-digest"}
                document = json.loads(body)
                manifests = document.get("manifests", [])
                platforms = []
                for item in manifests:
                    platform = item.get("platform", {})
                    value = "/".join(filter(None, [platform.get("os"), platform.get("architecture"), platform.get("variant")]))
                    if value:
                        platforms.append(value)
                return {"reference": reference, "registry": registry, "repository": repository, "tag": tag, "digest": digest, "media_type": response.headers.get("Content-Type", ""), "platforms": sorted(set(platforms)), "is_index": bool(manifests), "status": "resolved"}
        except urllib.error.HTTPError as error:
            if error.code == 401 and attempt == 0:
                token = _auth_header(error.headers.get("WWW-Authenticate", ""), timeout)
                if token:
                    headers["Authorization"] = token
                    continue
            return {"reference": reference, "status": f"http-{error.code}"}
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
            return {"reference": reference, "status": "resolution-error", "error": str(error)}
    return {"reference": reference, "status": "authentication-error"}


def _arg_values(dockerfile: str, environment: dict | None = None) -> dict[str, set[str]]:
    values: dict[str, set[str]] = {}
    environment = environment or {}
    for raw_line in dockerfile.splitlines():
        match = ARG_RE.match(raw_line.strip())
        if not match:
            continue
        name, default = match.group(1), match.group(2)
        candidates = set()
        if default is not None:
            candidates.add(default.strip().strip('"').strip("'"))
        if name in environment:
            candidates.add(str(environment[name]))
        values[name] = candidates
    return values


def propose_patch(dockerfile: str, line_number: int, original: str, digest: str, expanded_reference: str | None = None, environment: dict | None = None) -> str | None:
    if validate_digest(digest) is None or "@" in original:
        return None
    lines = dockerfile.splitlines()
    if line_number < 1 or line_number > len(lines):
        return None
    line = lines[line_number - 1]
    if original not in line or not line.lstrip().upper().startswith("FROM "):
        return None
    if expanded_reference is None:
        expanded_reference = expand_reference(original, dockerfile, environment)
    if expanded_reference is None or "@" in expanded_reference:
        return None
    # Docker build arguments may always be overridden by the caller. A digest
    # attached to a variable expression would therefore not pin the image for
    # all valid builds; refuse such proposals until the ARG is removed or a
    # separately validated allowlist is introduced.
    if VAR_RE.search(original):
        return None
    replacement = line.replace(original, f"{original}@{digest}", 1)
    return replacement if replacement != line else None


def eligible_for_index_pin(reference: str, media_type: str, is_index: bool, platforms: list[str]) -> bool:
    """Allow index pinning only for a valid multi-platform OCI/Docker index."""
    if not is_index or not validate_digest("sha256:" + "a" * 64):
        return False
    if "manifest.list" not in media_type and "image.index" not in media_type:
        return False
    return any(platform.startswith("linux/") for platform in platforms)


def generate_proposals(worklist: dict, resolutions: dict) -> list[dict]:
    """Generate proposal records without modifying repository files."""
    by_key = {(item.get("image"), item.get("line")): item for item in resolutions["entries"]}
    proposals = []
    for entry in worklist["entries"]:
        result = by_key.get((entry["image"], entry["line"]), {})
        if result.get("status") != "resolved":
            continue
        if not eligible_for_index_pin(result.get("reference", ""), result.get("media_type", ""), result.get("is_index", False), result.get("platforms", [])):
            continue
        dockerfile = Path(entry["dockerfile"])
        text = dockerfile.read_text(errors="replace")
        replacement = propose_patch(text, entry["line"], entry["reference"], result["digest"], expanded_reference=result.get("expanded_reference"), environment=os.environ)
        if replacement:
            proposals.append({"image": entry["image"], "dockerfile": entry["dockerfile"], "line": entry["line"], "old": text.splitlines()[entry["line"] - 1], "new": replacement, "digest": result["digest"], "policy": "multi-platform-index", "dockerfile_sha256": result["dockerfile_sha256"]})
    return sorted(proposals, key=lambda item: (item["image"], item["line"]))


def resolve_worklist(path: Path) -> dict:
    worklist = json.loads(path.read_text())
    results = []
    for entry in worklist["entries"]:
        dockerfile_path = Path(entry["dockerfile"])
        dockerfile = dockerfile_path.read_text(errors="replace") if dockerfile_path.exists() else ""
        expanded = expand_reference(entry["reference"], dockerfile, os.environ)
        result = inspect_manifest(expanded, credentials=os.environ) if expanded else {"reference": entry["reference"], "status": "unresolved-build-argument"}
        result.update({"image": entry["image"], "line": entry["line"], "original_reference": entry["reference"], "dockerfile_sha256": hashlib.sha256(dockerfile.encode()).hexdigest()})
        if expanded:
            result["expanded_reference"] = expanded
        if result.get("status") == "resolved":
            result["proposal"] = propose_patch(dockerfile, entry["line"], expanded, result["digest"], environment=os.environ)
            result["proposal_status"] = "ready" if result["proposal"] else "refused-ambiguous-target"
        results.append(result)
    resolutions = {"schema_version": 4, "source_worklist_schema": worklist["schema_version"], "entries": results, "resolved": sum(item["status"] == "resolved" for item in results), "proposals_ready": 0, "unresolved": sum(item["status"] != "resolved" for item in results)}
    resolutions["proposals"] = generate_proposals(worklist, resolutions)
    resolutions["proposals_ready"] = len(resolutions["proposals"])
    return resolutions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("worklist", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args()
    result = resolve_worklist(args.worklist)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"Resolved {result['resolved']}/{result['resolved'] + result['unresolved']} references; proposals ready: {result['proposals_ready']}")


if __name__ == "__main__":
    main()
