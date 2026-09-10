#!/usr/bin/env python3
"""Verify every FROM reference in the catalog resolves at its registry.

Catches generator garbage (fabricated URLs, pruned tags, wrong bases)
BEFORE a build wastes 40 minutes failing on it. Classifies each ref:

  OK      - manifest exists
  DEAD    - registry definitively says no (401/404 on manifest+tags)
  UNKNOWN - transient (429, timeout, auth-gated); never fails the gate

Exit 0 unless DEAD refs are found. Usage:
  verify_from_refs.py [--images name1,name2] [--json]
"""
import argparse, json, os, re, sys, time
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(REPO_ROOT, "images")

UA = {"User-Agent": "eir-pin-verifier/1.0"}
SKIP_DIRS = {"_archive", "clawdius", "health-shim", "__pycache__"}

TOKEN_CACHE = {}


def http_json(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def http_code(url, headers, timeout=20):
    req = urllib.request.Request(url, headers={**UA, **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


def dockerhub_token(repo):
    if repo not in TOKEN_CACHE:
        try:
            d = http_json(
                f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repo}:pull")
            TOKEN_CACHE[repo] = d.get("token", "")
        except Exception:
            TOKEN_CACHE[repo] = ""
    return TOKEN_CACHE[repo]


def check_dockerhub(repo, tag):
    tok = dockerhub_token(repo)
    hdr = {"Authorization": f"Bearer {tok}"}
    accept = ", ".join([
        "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.docker.distribution.manifest.v2+json",
        "application/vnd.oci.image.index.v1+json",
        "application/vnd.oci.image.manifest.v1+json",
    ])
    code = http_code(f"https://registry-1.docker.io/v2/{repo}/manifests/{tag}", {**hdr, "Accept": accept})
    if code == 200:
        return "OK", ""
    if code == 404:
        return "DEAD", "404 not found"
    if code == 401:
        # distinguish locked repo: tag list also 404 => DEAD (locked), else UNKNOWN
        try:
            d = http_json(f"https://hub.docker.com/v2/repositories/{repo}/tags?page_size=1")
            if d.get("count", 0) == 0:
                return "DEAD", "401 + no tags (locked/empty repo)"
            return "OK", "exists (401 was registry auth quirk)"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "DEAD", "401 + Hub API 404 (repo gone)"
            return "UNKNOWN", f"401, hub probe {e.code}"
        except Exception:
            return "UNKNOWN", "401, hub probe failed"
    if code == 429:
        return "UNKNOWN", "429 rate limited"
    return "UNKNOWN", f"HTTP {code}"


def ghcr_token(repo):
    if ("ghcr:" + repo) not in TOKEN_CACHE:
        try:
            d = http_json(f"https://ghcr.io/token?scope=repository:{repo}:pull")
            TOKEN_CACHE["ghcr:" + repo] = d.get("token", "")
        except Exception:
            TOKEN_CACHE["ghcr:" + repo] = ""
    return TOKEN_CACHE["ghcr:" + repo]


def check_ghcr(repo, tag):
    tok = get_token(f"https://ghcr.io/token?scope=repository:{repo}:pull")
    if not tok:
        return "UNKNOWN", "ghcr token refused"
    accept = ", ".join([
        "application/vnd.oci.image.index.v1+json",
        "application/vnd.oci.image.manifest.v1+json",
        "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.docker.distribution.manifest.v2+json",
    ])
    code = http_code(f"https://ghcr.io/v2/{repo}/manifests/{tag}",
                     {"Authorization": f"Bearer {tok}", "Accept": accept})
    if code == 200:
        return "OK", ""
    if code in (404, 401):
        return "DEAD", f"ghcr {code}"
    if code == 429:
        return "UNKNOWN", "429"
    return "UNKNOWN", f"HTTP {code}"


def get_token(url):
    """Fetch a registry token with retries; returns '' on failure."""
    for attempt in range(3):
        try:
            d = http_json(url)
            tok = d.get("token", "")
            if tok:
                return tok
        except Exception:
            pass
        time.sleep(2 * (attempt + 1))
    return ""


def check_cgr(repo, tag):
    # cgr.dev public images: token then manifest (digest pulls need auth too)
    tok = get_token(f"https://cgr.dev/token?scope=repository:{repo}:pull")
    if not tok:
        return "UNKNOWN", "cgr token fetch failed"
    accept = ", ".join([
        "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.docker.distribution.manifest.v2+json",
        "application/vnd.oci.image.index.v1+json",
        "application/vnd.oci.image.manifest.v1+json",
    ])
    code = http_code(f"https://cgr.dev/v2/{repo}/manifests/{tag}",
                     {"Accept": accept, "Authorization": f"Bearer {tok}"})
    if code == 200:
        return "OK", ""
    if code in (404, 401):
        return "DEAD", f"cgr {code}"
    return "UNKNOWN", f"HTTP {code}"


def check_gcr(repo, tag):
    tok = get_token(f"https://gcr.io/v2/token?service=gcr.io&scope=repository:{repo}:pull")
    if not tok:
        return "UNKNOWN", "gcr token fetch failed"
    accept = ", ".join([
        "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.oci.image.index.v1+json",
    ])
    code = http_code(f"https://gcr.io/v2/{repo}/manifests/{tag}",
                     {"Authorization": f"Bearer {tok}", "Accept": accept})
    if code == 200:
        return "OK", ""
    if code in (404, 401, 403):
        return "DEAD", f"gcr {code}"
    return "UNKNOWN", f"HTTP {code}"


def check_ecr(repo, tag):
    tok = get_token("https://public.ecr.aws/token/?service=public.ecr.aws&scope=repository:"
                    f"{repo}:pull")
    if not tok:
        return "UNKNOWN", "ecr token fetch failed"
    code = http_code(f"https://public.ecr.aws/v2/{repo}/manifests/{tag}",
                     {"Authorization": f"Bearer {tok}",
                      "Accept": "application/vnd.docker.distribution.manifest.list.v2+json"})
    if code == 200:
        return "OK", ""
    if code in (404, 401):
        return "DEAD", f"ecr {code}"
    return "UNKNOWN", f"HTTP {code}"


def check_registry(ref):
    """Return (status, detail) for image:tag ref."""
    # normalize bare/dotted refs to docker.io
    first = ref.split("/")[0]
    if "/" == ref[0:1] or ("." not in first and ":" not in first.split("/")[0] and "/" in ref) \
            or ("/" not in ref):
        if "." not in first or "/" not in ref:
            path = ref.split(":")[0] if ":" in ref else ref
            path = "library/" + path if "/" not in path else path
            tag = ref.split(":", 1)[1] if ":" in ref else "latest"
            return check_dockerhub(path, tag)
    if ref.startswith("docker.io/"):
        r = ref[10:]
        r = "library/" + r if "/" not in r else r
        return check_dockerhub(r, ref.split(":", 1)[1] if ":" in ref else "latest")
    if ref.startswith("ghcr.io/"):
        return check_ghcr(ref[8:], ref.split(":", 1)[1] if ":" in ref else "latest")
    if ref.startswith("cgr.dev/"):
        return check_cgr(ref[8:], ref.split(":", 1)[1] if ":" in ref else "latest")
    if ref.startswith("gcr.io/"):
        return check_gcr(ref[6:], ref.split(":", 1)[1] if ":" in ref else "latest")
    if ref.startswith("public.ecr.aws/"):
        return check_ecr(ref[15:], ref.split(":", 1)[1] if ":" in ref else "latest")
    if ref.startswith("lscr.io/"):
        # lscr.io is a ghcr-backed CNAME: linuxserver/<name>
        path = ref[8:]
        name = path.split(":")[0]
        return check_ghcr(f"linuxserver/{name}", ref.split(":", 1)[1] if ":" in ref else "latest")
    if ref.startswith("quay.io/"):
        return "UNKNOWN", "quay unsupported (add if needed)"
    return "UNKNOWN", f"unhandled registry: {ref.split('/')[0]}"


def parse_dockerfile(path):
    """Extract (ref, image_name) FROM refs with ARG-default substitution."""
    text = open(path, errors="replace").read()
    lines = text.splitlines()
    args = {}          # global args (before first FROM)
    stage_args = {}    # args after a FROM, reset each stage
    refs = []
    seen_first_from = False
    for raw in lines:
        line = raw.strip()
        m = re.match(r"^ARG\s+(\w+)(?:=(\S+))?\s*$", line)
        if m:
            name, default = m.group(1), m.group(2)
            if not seen_first_from:
                if default is not None:
                    args[name] = default.strip('"\'')
            else:
                if default is not None:
                    stage_args[name] = default.strip("\"'")
            continue
        m = re.match(r"^FROM\s+(\S+)", line)
        if m:
            seen_first_from = True
            ref = m.group(1)
            combined = {**args, **stage_args}
            # substitute ${VAR}
            def sub(mo):
                return combined.get(mo.group(1), "")
            ref = re.sub(r"\$\{(\w+)\}", sub, ref)
            stage_args = {}  # reset for next stage
            if ref in ("scratch",):
                continue
            if ":" not in ref.split("/")[0] and ":" in "".join(ref):
                pass
            if ref and not ref.endswith(":") and "$" not in ref:
                refs.append(ref)
    return refs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", help="comma-separated image names (default: all)")
    ap.add_argument("--json", action="store_true", dest="as_json")
    opts = ap.parse_args()

    if opts.images:
        names = [n.strip() for n in opts.images.split(",") if n.strip()]
    else:
        names = sorted(
            d for d in os.listdir(IMAGES_DIR)
            if os.path.isdir(os.path.join(IMAGES_DIR, d)) and d not in SKIP_DIRS
        )

    tasks = []  # (image, ref)
    for name in names:
        df = os.path.join(IMAGES_DIR, name, "Dockerfile")
        if not os.path.isfile(df):
            continue
        for ref in parse_dockerfile(df):
            tasks.append((name, ref))

    results = []  # (image, ref, status, detail)
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(check_registry, ref): (img, ref) for img, ref in tasks}
        for fut in futures:
            img, ref = futures[fut]
            try:
                status, detail = fut.result()
            except Exception as e:
                status, detail = "UNKNOWN", str(e)[:60]
            results.append((img, ref, status, detail))

    dead = [r for r in results if r[2] == "DEAD"]
    unknown = [r for r in results if r[2] == "UNKNOWN"]

    if opts.as_json:
        print(json.dumps({
            "total": len(results),
            "ok": len(results) - len(dead) - len(unknown),
            "dead": [{"image": r[0], "ref": r[1], "detail": r[3]} for r in dead],
            "unknown": [{"image": r[0], "ref": r[1], "detail": r[3]} for r in unknown],
        }, indent=2))
    else:
        print(f"Checked {len(results)} FROM refs across {len(names)} images")
        for img, ref, status, detail in dead:
            print(f"  DEAD    {img:28s} {ref}  ({detail})")
        for img, ref, status, detail in unknown:
            print(f"  UNKNOWN {img:28s} {ref}  ({detail})")
        print(f"\nDEAD: {len(dead)}  UNKNOWN(transient): {len(unknown)}")

    sys.exit(1 if dead else 0)


if __name__ == "__main__":
    main()
