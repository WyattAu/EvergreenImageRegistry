#!/usr/bin/env python3
"""Generate SPDX 2.3 SBOM for all images missing sbom.spdx.json."""
import os
import re
import json
from datetime import datetime, timezone

IMAGES_DIR = "/home/wyatt/dev/src/github.com/WyattAu/EvergreenImageRegistry/images"


def is_valid_package_name(name):
    if not name:
        return False
    if name == "\\":
        return False
    if re.match(r'^[\s-]+$', name):
        return False
    return True


def sanitize_ref(s):
    return re.sub(r'[^a-z0-9.-]', '-', s.lower())


def parse_manifest(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        content = f.read()
    info = {}
    m = re.search(r'^vendor\s*=\s*"([^"]*)"', content, re.MULTILINE)
    if m:
        info['vendor'] = m.group(1)
    m = re.search(r'^version\s*=\s*"([^"]*)"', content, re.MULTILINE)
    if m:
        info['version'] = m.group(1)
    m = re.search(r'^url\s*=\s*"([^"]*)"', content, re.MULTILINE)
    if m:
        url = m.group(1)
        basename = os.path.basename(url)
        for ext in ['.tar.gz', '.tar.xz', '.tar.bz2', '.zip']:
            if basename.endswith(ext):
                basename = basename[:-len(ext)]
                break
        info['downloaded_binary'] = (basename, url)
    for pkg_type in ['builder_packages', 'runtime_packages']:
        m = re.search(rf'^\s+{pkg_type}\s*=\s*\[([^\]]*)\]', content, re.MULTILINE)
        if m:
            pkgs = re.findall(r'"([^"]*)"', m.group(1))
            if pkg_type not in info:
                info['packages'] = []
            info['packages'].extend(pkgs)
    m = re.search(r'^\s+image\s*=\s*"([^"]*)"', content, re.MULTILINE)
    if m:
        info['base_image'] = m.group(1)
    return info


def parse_dockerfile(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        content = f.read()
    info = {}
    m = re.search(r'ARG\s+VERSION=([^\s]+)', content)
    if m:
        info['version'] = m.group(1)
    froms = re.findall(r'^FROM\s+(\S+)', content, re.MULTILINE)
    if froms:
        info['base_images'] = list(dict.fromkeys(froms))
    m = re.search(r'org\.opencontainers\.image\.vendor="([^"]*)"', content)
    if m:
        info['vendor'] = m.group(1)
    content_oneline = content.replace('\\\n', ' ')
    apt_matches = re.findall(r'apt-get\s+install[^|&;]*', content_oneline)
    apt_pkgs = set()
    for match in apt_matches:
        cleaned = match.replace('apt-get install', '').replace('--no-install-recommends', '').replace('-y', '').replace('-q', '').strip()
        for pkg in cleaned.split():
            if pkg in ('&&', '--', 'rm', '-rf', '\\'):
                continue
            if is_valid_package_name(pkg):
                apt_pkgs.add(pkg)
    if apt_pkgs:
        info['apt_packages'] = sorted(apt_pkgs)
    apk_matches = re.findall(r'apk\s+add[^|&;]*', content_oneline)
    apk_pkgs = set()
    for match in apk_matches:
        cleaned = match.replace('apk add', '').replace('--no-cache', '').strip()
        for pkg in cleaned.split():
            if pkg in ('&&', '--', '\\'):
                continue
            if is_valid_package_name(pkg):
                apk_pkgs.add(pkg)
    if apk_pkgs:
        info['apk_packages'] = sorted(apk_pkgs)
    curl_outputs = re.findall(r'curl\b[^|&;]*-o\s+(/\\S+)', content_oneline)
    if curl_outputs:
        info['curl_outputs'] = curl_outputs
    return info


def parse_go_mod(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        lines = f.readlines()
    modules = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('//'):
            continue
        if line.startswith('module ') or line.startswith('go ') or line == 'require (' or line == ')' or line.startswith('replace '):
            continue
        parts = line.split()
        if parts:
            modules.append(parts[0])
    return sorted(set(modules))


def generate_sbom(image_name, image_dir):
    manifest_info = parse_manifest(os.path.join(image_dir, 'manifest.toml'))
    dockerfile_info = parse_dockerfile(os.path.join(image_dir, 'Dockerfile'))
    go_modules = parse_go_mod(os.path.join(image_dir, 'go.mod'))

    version = manifest_info.get('version') or dockerfile_info.get('version', 'unknown')
    vendor = manifest_info.get('vendor') or dockerfile_info.get('vendor', 'NOASSERTION')

    packages = []
    seen_spdxids = set()

    def add_package(spdxid, pkg_data):
        if spdxid not in seen_spdxids:
            seen_spdxids.add(spdxid)
            packages.append(pkg_data)

    base_images = []
    if 'base_image' in manifest_info:
        base_images.append(manifest_info['base_image'])
    if 'base_images' in dockerfile_info:
        base_images.extend(dockerfile_info['base_images'])
    base_images = list(dict.fromkeys(base_images))
    for img in base_images:
        ref = f"SPDXRef-Package-{sanitize_ref(img)}"
        add_package(ref, {
            "SPDXID": ref,
            "name": img,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "primaryPackagePurpose": "CONTAINER",
            "originator": "NOASSERTION"
        })

    all_os_packages = []
    if 'packages' in manifest_info:
        all_os_packages.extend(manifest_info['packages'])
    if 'apt_packages' in dockerfile_info:
        all_os_packages.extend(f"apt:{p}" for p in dockerfile_info['apt_packages'])
    if 'apk_packages' in dockerfile_info:
        all_os_packages.extend(f"apk:{p}" for p in dockerfile_info['apk_packages'])
    all_os_packages = list(dict.fromkeys(all_os_packages))
    for pkg_entry in all_os_packages:
        pkg_type = "generic"
        pkg_name = pkg_entry
        if pkg_entry.startswith('apt:'):
            pkg_name = pkg_entry[4:]
            pkg_type = "debian"
        elif pkg_entry.startswith('apk:'):
            pkg_name = pkg_entry[4:]
            pkg_type = "alpine"
        if not is_valid_package_name(pkg_name):
            continue
        ref = f"SPDXRef-Package-{image_name}-{sanitize_ref(pkg_name)}"
        add_package(ref, {
            "SPDXID": ref,
            "name": pkg_name,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "primaryPackagePurpose": "INSTALLATION",
            "originator": "NOASSERTION",
            "externalRefs": [
                {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": f"pkg:{pkg_type}/{pkg_name}"
                }
            ]
        })

    downloaded_binaries = []
    if 'downloaded_binary' in manifest_info:
        downloaded_binaries.append(manifest_info['downloaded_binary'])
    if 'curl_outputs' in dockerfile_info:
        for out in dockerfile_info['curl_outputs']:
            downloaded_binaries.append((os.path.basename(out), "curl-download"))
    downloaded_binaries = list(dict.fromkeys(downloaded_binaries))
    for bin_name, bin_url in downloaded_binaries:
        ref = f"SPDXRef-Package-{image_name}-{sanitize_ref(bin_name)}"
        add_package(ref, {
            "SPDXID": ref,
            "name": bin_name,
            "downloadLocation": bin_url,
            "filesAnalyzed": False,
            "primaryPackagePurpose": "APPLICATION",
            "originator": vendor
        })

    for mod in go_modules:
        ref = f"SPDXRef-Package-{image_name}-{sanitize_ref(mod)}"
        add_package(ref, {
            "SPDXID": ref,
            "name": mod,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "primaryPackagePurpose": "LIBRARY",
            "originator": "NOASSERTION",
            "externalRefs": [
                {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": f"pkg:golang/{mod}"
                }
            ]
        })

    doc = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": f"SPDXRef-DOCUMENT-{image_name}",
        "name": f"evergreen-{image_name}",
        "documentNamespace": f"https://github.com/WyattAu/EvergreenImageRegistry/images/{image_name}",
        "creationInfo": {
            "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "creators": ["Tool: evergreen-sbom-generator"]
        },
        "packages": packages,
        "relationships": [
            {
                "spdxElementId": f"SPDXRef-DOCUMENT-{image_name}",
                "relationshipType": "DESCRIBES",
                "relatedSpdxElement": f"SPDXRef-Package-{image_name}"
            }
        ]
    }
    return json.dumps(doc, indent=2) + "\n"


def main():
    count = 0
    skipped = 0
    errors = 0
    for d in sorted(os.listdir(IMAGES_DIR)):
        img_dir = os.path.join(IMAGES_DIR, d)
        dockerfile = os.path.join(img_dir, 'Dockerfile')
        sbom = os.path.join(img_dir, 'sbom.spdx.json')
        if not os.path.isdir(img_dir) or not os.path.exists(dockerfile):
            continue
        if os.path.exists(sbom):
            skipped += 1
            continue
        try:
            content = generate_sbom(d, img_dir)
            with open(sbom, 'w') as f:
                f.write(content)
            count += 1
            if count % 200 == 0:
                print(f"Generated {count} SBOMs...")
        except Exception as e:
            errors += 1
            print(f"ERROR processing {d}: {e}")
    print(f"Generated: {count}, Skipped (existing): {skipped}, Errors: {errors}, Total: {count + skipped + errors}")


if __name__ == '__main__':
    main()
