#!/usr/bin/env python3
"""Generate manifest.toml for images without one, and migrate existing ones to new format."""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "images")


def parse_dockerfile(path):
    with open(path) as f:
        content = f.read()

    info = {}

    m = re.search(r"ARG\s+VERSION[=\s]([^\s]+)", content)
    version = m.group(1) if m else ""
    if not version or version.startswith("$"):
        version = ""
    if not version:
        m = re.search(r"releases/download/v?(\d+\.\d+[\.\d]*(?:-[\w\.\+]+)?)", content)
        if m:
            version = m.group(1)
    if not version:
        m = re.search(r'org\.opencontainers\.image\.version="([^"]+)"', content)
        if m:
            v = m.group(1)
            if not v.startswith("$") and v != "latest":
                version = v
    if not version:
        version = "unknown"
    info["version"] = version

    froms = re.findall(r"^FROM\s+(\S+)", content, re.MULTILINE)
    if froms:
        info["base"] = froms[-1]
    else:
        info["base"] = "scratch"

    m = re.search(r"^USER\s+(\S+)", content, re.MULTILINE)
    info["user"] = m.group(1) if m else "65532:65532"

    m = re.search(r"^STOPSIGNAL\s+(\S+)", content, re.MULTILINE)
    info["stopsignal"] = m.group(1) if m else "SIGTERM"

    info["expose"] = re.findall(r"^EXPOSE\s+(\S+)", content, re.MULTILINE)

    m = re.search(r"^ENTRYPOINT\s+\[(.+)\]", content, re.MULTILINE)
    if m:
        info["entrypoint"] = [
            x.strip().strip('"').strip("'") for x in m.group(1).split(",")
        ]

    m = re.search(r"^CMD\s+\[(.+)\]", content, re.MULTILINE)
    if m:
        info["cmd"] = [x.strip().strip('"').strip("'") for x in m.group(1).split(",")]

    labels = {}
    for m in re.finditer(r'LABEL\s+(evergreen\.\S+?)=["\']([^"\']+)["\']', content):
        labels[m.group(1)] = m.group(2)
    for m in re.finditer(
        r'LABEL\s+(org\.opencontainers\.\S+?)=["\']([^"\']+)["\']', content
    ):
        labels[m.group(1)] = m.group(2)
    for m in re.finditer(r'LABEL\s+(maintainer\S+?)=["\']([^"\']+)["\']', content):
        labels[m.group(1)] = m.group(2)
    label_blocks = re.findall(
        r"LABEL\s+(.+?)(?=\n(?:LABEL|EXPOSE|STOPSIGNAL|ENTRYPOINT|CMD|USER|FROM|HEALTHCHECK|#|\n\n|$))",
        content,
        re.DOTALL,
    )
    for block in label_blocks:
        for m in re.finditer(r'(\S+?)="([^"]*)"', block):
            k, v = m.group(1), m.group(2)
            if (
                k.startswith("evergreen.")
                or k.startswith("org.opencontainers.")
                or k == "maintainer"
            ):
                labels[k] = v
    info["labels"] = labels

    if re.search(r"AS\s+upstream", content, re.IGNORECASE):
        info["source_type"] = "docker-image"
        m = re.search(r"FROM\s+(\S+)\s+AS\s+upstream", content, re.IGNORECASE)
        if m:
            info["source_url"] = m.group(1)
    elif (
        re.search(r"apk add|apk fetch", content)
        or re.search(r"apt-get install|apt-get update", content)
        or re.search(r"microdnf install|dnf install|yum install", content)
    ):
        info["source_type"] = "package-manager"
    elif re.search(r"git clone|git checkout", content):
        info["source_type"] = "git-clone"
    elif re.search(r"go build|go install|go mod", content):
        info["source_type"] = "go-source"
    elif re.search(r"cargo build|cargo install|Cargo\.toml", content):
        info["source_type"] = "cargo-source"
    elif re.search(r"cmake|make\s+install|\.\/configure", content):
        info["source_type"] = "build-from-source"
    elif re.search(r"curl.*-o\s|wget\s+-O", content):
        info["source_type"] = "direct-download"
        urls = re.findall(r'curl[^|\n]*?["\']?(https?://[^"\'\s\|]+)["\']?', content)
        if urls:
            info["source_url"] = urls[0]
    elif re.search(r"pip install|pip3 install", content):
        info["source_type"] = "package-manager"
    else:
        info["source_type"] = "base-image"

    return info


def generate_manifest(image_name, info):
    lines = []
    lines.append("[metadata]")
    lines.append(f'name = "{image_name}"')
    lines.append(f'version = "{info.get("version", "unknown")}"')
    desc = f"{image_name} container image"
    if info.get("labels", {}).get("org.opencontainers.image.description"):
        desc = info["labels"]["org.opencontainers.image.description"]
    lines.append(f'description = "{desc}"')
    lines.append("")

    lines.append("[build]")
    base = info.get("base", "scratch")
    lines.append(f'base = "{base}"')
    lines.append(f'user = "{info.get("user", "65532:65532")}"')
    lines.append(f'stopsignal = "{info.get("stopsignal", "SIGTERM")}"')
    lines.append("")

    lines.append("[source]")
    lines.append(f'type = "{info.get("source_type", "unknown")}"')
    if info.get("source_url"):
        lines.append(f'url = "{info["source_url"]}"')
    lines.append("")

    if info.get("entrypoint") or info.get("cmd"):
        lines.append("[runtime]")
        if info.get("entrypoint"):
            ep = ", ".join(f'"{x}"' for x in info["entrypoint"])
            lines.append(f"entrypoint = [{ep}]")
        if info.get("cmd"):
            cmd = ", ".join(f'"{x}"' for x in info["cmd"])
            lines.append(f"cmd = [{cmd}]")
        lines.append("")

    expose = info.get("expose", [])
    if expose:
        lines.append("[ports]")
        ports = ", ".join(expose)
        lines.append(f"expose = [{ports}]")
        lines.append("")

    labels = info.get("labels", {})
    if labels:
        lines.append("[labels]")
        oc_keys = sorted([k for k in labels if k.startswith("org.opencontainers.")])
        for k in oc_keys:
            lines.append(f'"{k}" = "{labels[k]}"')
        sov_keys = sorted([k for k in labels if k.startswith("evergreen.")])
        for k in sov_keys:
            lines.append(f'"{k}" = "{labels[k]}"')
        other_keys = sorted(
            [
                k
                for k in labels
                if not k.startswith("org.opencontainers.")
                and not k.startswith("evergreen.")
            ]
        )
        for k in other_keys:
            lines.append(f'"{k}" = "{labels[k]}"')
        lines.append("")

    return "\n".join(lines) + "\n"


def migrate_existing_manifest(manifest_path, dockerfile_path):
    with open(dockerfile_path) as f:
        df_content = f.read()

    df_info = parse_dockerfile(dockerfile_path)

    with open(manifest_path) as f:
        old_content = f.read()

    image_name = os.path.basename(os.path.dirname(manifest_path))

    old_base_image = ""
    old_runtime_image = ""
    m = re.search(r'^base_image\s*=\s*"([^"]+)"', old_content, re.MULTILINE)
    if m:
        old_base_image = m.group(1)
    m = re.search(r'^runtime_image\s*=\s*"([^"]+)"', old_content, re.MULTILINE)
    if m:
        old_runtime_image = m.group(1)

    base = df_info.get("base", old_runtime_image or old_base_image or "scratch")

    old_version = ""
    m = re.search(r'^version\s*=\s*"([^"]+)"', old_content, re.MULTILINE)
    if m:
        old_version = m.group(1)

    old_description = ""
    m = re.search(r'^description\s*=\s*"([^"]+)"', old_content, re.MULTILINE)
    if m:
        old_description = m.group(1)

    old_vendor = ""
    m = re.search(r'^vendor\s*=\s*"([^"]+)"', old_content, re.MULTILINE)
    if m:
        old_vendor = m.group(1)

    old_source = ""
    m = re.search(r'^source\s*=\s*"([^"]+)"', old_content, re.MULTILINE)
    if m:
        old_source = m.group(1)

    old_license = ""
    m = re.search(r'^license\s*=\s*"([^"]+)"', old_content, re.MULTILINE)
    if m:
        old_license = m.group(1)

    old_tier = ""
    m = re.search(r'^tier\s*=\s*"([^"]+)"', old_content, re.MULTILINE)
    if m:
        old_tier = m.group(1)

    old_user = ""
    m = re.search(r"^USER\s+(\S+)", df_content, re.MULTILINE)
    if m:
        old_user = m.group(1)
    else:
        old_user = "65532:65532"

    old_stopsignal = ""
    m = re.search(r"^STOPSIGNAL\s+(\S+)", df_content, re.MULTILINE)
    if m:
        old_stopsignal = m.group(1)
    else:
        old_stopsignal = "SIGTERM"

    old_download_url = ""
    m = re.search(r'^url\s*=\s*"([^"]+)"', old_content, re.MULTILINE)
    if m:
        old_download_url = m.group(1)

    source_type = df_info.get("source_type", "direct-download")
    source_url = df_info.get("source_url", old_download_url)

    old_expose = re.findall(r"^EXPOSE\s+(\S+)", df_content, re.MULTILINE)

    old_entrypoint = df_info.get("entrypoint")
    old_cmd = df_info.get("cmd")

    old_labels = df_info.get("labels", {})

    lines = []
    lines.append("[metadata]")
    lines.append(f'name = "{image_name}"')
    lines.append(f'version = "{old_version or df_info.get("version", "unknown")}"')
    lines.append(
        f'description = "{old_description or f"{image_name} container image"}"'
    )
    if old_vendor:
        lines.append(f'vendor = "{old_vendor}"')
    if old_source:
        lines.append(f'source = "{old_source}"')
    if old_license:
        lines.append(f'license = "{old_license}"')
    if old_tier:
        lines.append(f'tier = "{old_tier}"')
    lines.append("")

    lines.append("[build]")
    lines.append(f'base = "{base}"')
    lines.append(f'user = "{old_user}"')
    lines.append(f'stopsignal = "{old_stopsignal}"')
    lines.append("")

    lines.append("[source]")
    lines.append(f'type = "{source_type}"')
    if source_url:
        lines.append(f'url = "{source_url}"')
    lines.append("")

    if old_entrypoint or old_cmd:
        lines.append("[runtime]")
        if old_entrypoint:
            ep = ", ".join(f'"{x}"' for x in old_entrypoint)
            lines.append(f"entrypoint = [{ep}]")
        if old_cmd:
            cmd = ", ".join(f'"{x}"' for x in old_cmd)
            lines.append(f"cmd = [{cmd}]")
        lines.append("")

    if old_expose:
        lines.append("[ports]")
        ports = ", ".join(old_expose)
        lines.append(f"expose = [{ports}]")
        lines.append("")

    if old_labels:
        lines.append("[labels]")
        oc_keys = sorted([k for k in old_labels if k.startswith("org.opencontainers.")])
        for k in oc_keys:
            lines.append(f'"{k}" = "{old_labels[k]}"')
        sov_keys = sorted([k for k in old_labels if k.startswith("evergreen.")])
        for k in sov_keys:
            lines.append(f'"{k}" = "{old_labels[k]}"')
        other_keys = sorted(
            [
                k
                for k in old_labels
                if not k.startswith("org.opencontainers.")
                and not k.startswith("evergreen.")
            ]
        )
        for k in other_keys:
            lines.append(f'"{k}" = "{old_labels[k]}"')
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    generated = 0
    migrated = 0
    errors = []

    for d in sorted(os.listdir(IMAGES_DIR)):
        img_dir = os.path.join(IMAGES_DIR, d)
        if not os.path.isdir(img_dir) or d.startswith("_") or d == "tests":
            continue

        dockerfile_path = os.path.join(img_dir, "Dockerfile")
        manifest_path = os.path.join(img_dir, "manifest.toml")

        if not os.path.exists(dockerfile_path):
            continue

        if not os.path.exists(manifest_path):
            try:
                info = parse_dockerfile(dockerfile_path)
                content = generate_manifest(d, info)
                with open(manifest_path, "w") as f:
                    f.write(content)
                generated += 1
                if generated % 100 == 0:
                    print(f"  generated {generated} so far...")
            except Exception as e:
                errors.append(f"  ERROR generating {d}: {e}")
        else:
            try:
                new_content = migrate_existing_manifest(manifest_path, dockerfile_path)
                with open(manifest_path, "w") as f:
                    f.write(new_content)
                migrated += 1
                if migrated % 100 == 0:
                    print(f"  migrated {migrated} so far...")
            except Exception as e:
                errors.append(f"  ERROR migrating {d}: {e}")

    print(f"\nDone: {generated} generated, {migrated} migrated")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(e)


if __name__ == "__main__":
    main()
