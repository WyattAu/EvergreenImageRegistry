#!/usr/bin/env python3
"""Mirror ALL remaining Docker Hub upstreams to GHCR."""
import re, subprocess, sys, time
from collections import defaultdict
from pathlib import Path

IMAGES_DIR = Path("/home/wyatt/dev/src/github.com/WyattAu/EvergreenImageRegistry/images")
REGISTRY = "ghcr.io/wyattau/evergreenimageregistry"
MIRROR_PREFIX = f"{REGISTRY}/mirror"

SKIP_REGISTRIES = {"ghcr.io","quay.io","cgr.dev","lscr.io","docker.dragonflydb.io","public.ecr.aws","gcr.io","k8s.gcr.io","registry.k8s.io","mcr.microsoft.com"}
SKIP_IMAGES_PREFIX = {"pytorch/pytorch", "tensorflow/tensorflow", "nvidia/cuda", "gitlab/gitlab"}

def is_docker_hub(image):
    if image.startswith("docker.io/"): return True
    for reg in SKIP_REGISTRIES:
        if image.startswith(reg+"/"): return False
    first_part = image.split("/")[0]
    fp_no_port = first_part.split(":")[0]
    if "." not in fp_no_port:
        return True
    return False

def sanitize_name(image):
    if "@sha256:" in image:
        name, digest = image.split("@sha256:")
        name = name.replace("docker.io/","").replace("/","-")
        return f"{name}-{digest[:12]}"
    name = image.replace("docker.io/","").replace("/","-").replace(":","-")
    return re.sub(r"[^a-zA-Z0-9._-]","",name).lower()

def find_all_upstreams():
    upstreams = defaultdict(list)
    for img_dir in sorted(IMAGES_DIR.iterdir()):
        if not img_dir.is_dir() or img_dir.name.startswith("_") or img_dir.name == "clawdius":
            continue
        dockerfile = img_dir / "Dockerfile"
        if not dockerfile.exists(): continue
        text = dockerfile.read_text()
        for line in text.splitlines():
            s = line.strip()
            if not s.startswith("FROM "): continue
            if any(x in s for x in ["health-shim","evergreenshim","scratch","mirror-"]): continue
            parts = s.split()
            if len(parts) < 2: continue
            ref = parts[1]
            if is_docker_hub(ref):
                upstreams[ref].append(dockerfile)
    return upstreams

def update_dockerfile(dockerfile, upstream, mirror_ref):
    text = dockerfile.read_text()
    pattern = re.compile(rf"(FROM\s+){re.escape(upstream)}(\s+AS\s+|\s*$|\s+--platform=)", re.MULTILINE)
    new_text = pattern.sub(rf"\1{mirror_ref}\2", text)
    if new_text != text:
        dockerfile.write_text(new_text)
        return True
    return False

def main():
    upstreams = find_all_upstreams()
    items = sorted(upstreams.items(), key=lambda x: (-len(x[1]), x[0]))

    filtered = {}
    for upstream, dfs in items:
        if any(upstream.startswith(skip) for skip in SKIP_IMAGES_PREFIX):
            print(f"SKIP: {upstream} (too large)")
            continue
        filtered[upstream] = dfs

    print(f"\nTotal to mirror: {len(filtered)}")

    # GHCR login
    subprocess.run("gh auth token | docker login ghcr.io -u WyattAu --password-stdin",
                   shell=True, timeout=30, capture_output=True)

    mirrored = 0
    failed = 0
    updated = 0
    failed_list = []

    for i, (upstream, dfs) in enumerate(filtered.items()):
        mirror_name = sanitize_name(upstream)
        mirror_ref = f"{MIRROR_PREFIX}-{mirror_name}:latest"

        if i % 10 == 0:
            print(f"\n--- Progress: {i}/{len(filtered)} (mirrored={mirrored}, failed={failed}) ---")

        r = subprocess.run(["docker","pull",upstream], capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            err = r.stderr.strip()[:80]
            print(f"[{i+1}] FAIL PULL: {upstream} - {err}")
            failed += 1
            failed_list.append(upstream)
            continue
        subprocess.run(["docker","tag",upstream,mirror_ref], capture_output=True, timeout=30)
        r = subprocess.run(["docker","push",mirror_ref], capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            err = r.stderr.strip()[:80]
            print(f"[{i+1}] FAIL PUSH: {upstream} - {err}")
            failed += 1
            failed_list.append(upstream)
            subprocess.run(["docker","rmi",upstream,mirror_ref], capture_output=True, timeout=60)
            continue

        mirrored += 1
        updates = 0
        for df in dfs:
            if update_dockerfile(df, upstream, mirror_ref):
                updated += 1
                updates += 1
        print(f"[{i+1}] OK: {upstream} -> mirror-{mirror_name} ({updates} files)")

        subprocess.run(["docker","rmi",upstream,mirror_ref], capture_output=True, timeout=60)

        if mirrored % 20 == 0:
            subprocess.run(["docker","image","prune","-f"], capture_output=True, timeout=60)

    print(f"\n{'='*60}")
    print(f"Mirrored: {mirrored} | Failed: {failed} | Updated files: {updated}")
    if failed_list:
        print(f"\nFailed upstreams:")
        for f in failed_list:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
