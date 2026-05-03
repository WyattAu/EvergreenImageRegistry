#!/usr/bin/env python3
"""Backfill evergreen labels, EXPOSE 9101, and STOPSIGNAL SIGTERM into Dockerfiles missing them."""

import re
import glob
import os

IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'images')
DOCKERFILE_PATTERN = os.path.join(IMAGES_DIR, '*', 'Dockerfile')

CHECKS = [
    ('evergreen.base.image', r'evergreen\.base\.image\s*=\s*"'),
    ('evergreen.metrics.native', r'evergreen\.metrics\.native\s*=\s*"'),
    ('evergreen.health.type', r'evergreen\.health\.type\s*=\s*"'),
    ('EXPOSE 9101', r'EXPOSE\s+9101\b'),
    ('STOPSIGNAL', r'STOPSIGNAL\s+'),
]


def get_last_from(content):
    last_from = None
    for line in content.splitlines():
        stripped = line.strip()
        if re.match(r'^FROM\s+', stripped, re.IGNORECASE):
            last_from = stripped
    if last_from is None:
        return None
    match = re.match(r'FROM\s+(.+?)(?:\s+AS\s+.*)?$', last_from, re.IGNORECASE)
    return match.group(1).strip() if match else None


def classify_base(image_ref):
    if not image_ref:
        return None
    lower = image_ref.lower()
    if lower == 'scratch' or lower.endswith('/scratch'):
        return 'scratch'
    if 'wolfi' in lower:
        return 'wolfi'
    if 'distroless' in lower:
        return 'distroless'
    if 'ubi' in lower:
        if 'ubi-micro' in lower:
            return 'ubi-micro'
        if 'ubi-minimal' in lower:
            return 'ubi-minimal'
        return 'ubi-standard'
    return None


def classify_metrics(content, base):
    return 'ztunnel'


def determine_health_type(content):
    if re.search(r'HEALTHCHECK\s+', content, re.IGNORECASE):
        return 'exec'
    return 'none'


def process_dockerfile(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    missing = {}
    for name, pattern in CHECKS:
        if not re.search(pattern, content):
            missing[name] = True

    if not missing:
        return None

    last_from = get_last_from(content)
    base = classify_base(last_from)

    additions = []
    added_items = []

    if 'evergreen.base.image' in missing:
        if base:
            added_items.append('evergreen.base.image')
            additions.append(f'LABEL evergreen.base.image="{base}"')
        else:
            print(f'  SKIP evergreen.base.image for {os.path.basename(os.path.dirname(filepath))} (base: {last_from})')

    if 'evergreen.metrics.native' in missing:
        metrics = classify_metrics(content, base)
        added_items.append('evergreen.metrics.native')
        additions.append(f'LABEL evergreen.metrics.native="{metrics}"')

    if 'evergreen.health.type' in missing:
        health = determine_health_type(content)
        added_items.append('evergreen.health.type')
        additions.append(f'LABEL evergreen.health.type="{health}"')

    if 'EXPOSE 9101' in missing:
        added_items.append('EXPOSE 9101')
        additions.append('EXPOSE 9101')

    if 'STOPSIGNAL' in missing:
        added_items.append('STOPSIGNAL SIGTERM')
        additions.append('STOPSIGNAL SIGTERM')

    if not additions:
        return None

    name = os.path.basename(os.path.dirname(filepath))
    print(f'  {name}: added {", ".join(added_items)}')

    new_content = content.rstrip('\n') + '\n\n' + '\n'.join(additions) + '\n'
    with open(filepath, 'w') as f:
        f.write(new_content)

    return added_items


def main():
    dockerfiles = sorted(glob.glob(DOCKERFILE_PATTERN))
    if not dockerfiles:
        print('No Dockerfiles found.')
        return

    counts = {
        'evergreen.base.image': 0,
        'evergreen.metrics.native': 0,
        'evergreen.health.type': 0,
        'EXPOSE 9101': 0,
        'STOPSIGNAL SIGTERM': 0,
    }
    modified_files = 0

    print(f'Scanning {len(dockerfiles)} Dockerfiles...\n')
    for df in dockerfiles:
        result = process_dockerfile(df)
        if result:
            modified_files += 1
            for item in result:
                if item in counts:
                    counts[item] += 1

    total_added = sum(counts.values())
    print(f'\n{"="*60}')
    print(f'BACKFILL SUMMARY')
    print(f'{"="*60}')
    print(f'Total Dockerfiles scanned:    {len(dockerfiles)}')
    print(f'Files modified:               {modified_files}')
    print(f'Files already complete:       {len(dockerfiles) - modified_files}')
    print(f'---')
    print(f'Items added:')
    for item, count in counts.items():
        print(f'  {item:<30} {count}')
    print(f'---')
    print(f'Total items added:            {total_added}')
    print(f'{"="*60}')


if __name__ == '__main__':
    main()
