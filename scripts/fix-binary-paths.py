#!/usr/bin/env python3
"""Fix EIR stub Dockerfiles with correct binary paths."""

import os, re, sys
from pathlib import Path

# Correct binary paths from upstream image entrypoints
BINARY_MAP = {
    "victoriametrics": "/victoria-metrics-prod",
    "vmalert": "/vmalert-prod",
    "victoria-logs": "/victoria-logs-prod",
    "node-exporter": "/bin/node_exporter",
    "blackbox-exporter": "/bin/blackbox_exporter",
    "promtail": "/usr/bin/promtail",
    "postgres-exporter": "postgres_exporter",
    "redis-exporter": "/redis_exporter",
    "cadvisor": "/usr/bin/cadvisor",
    "postgres": "docker-entrypoint.sh postgres",
    "mariadb": "docker-entrypoint.sh mariadbd",
    "redis-7": "docker-entrypoint.sh redis-server",
    "freshrss": None,  # No entrypoint, uses Apache+FPM
    "homepage": "docker-entrypoint.sh node server.js",
    "uptime-kuma": "node server/server.js",
}

IMAGES_TO_FIX = list(BINARY_MAP.keys())

for img in IMAGES_TO_FIX:
    dockerfile_path = Path(f"images/{img}/Dockerfile")
    if not dockerfile_path.exists():
        print(f"  ❌ {img}: No Dockerfile")
        continue
    
    content = dockerfile_path.read_text()
    binary = BINARY_MAP[img]
    
    if binary is None:
        print(f"  ⚠️  {img}: No binary mapping (complex entrypoint), skipping ENTRYPOINT")
        continue
    
    # Remove old ENTRYPOINT/USER/LABELS we added
    content = re.sub(r'\nENTRYPOINT \[.*?\]\n', '\n', content)
    content = re.sub(r'\nUSER 65532:65532\n', '\n', content)
    content = re.sub(r'\nLABEL org\.opencontainers\.image\.title.*?evergreen\.image\.tier.*?\n', '\n', content)
    
    # Add correct ENTRYPOINT
    content += f'\nENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "{binary}"]\n'
    
    # Add USER only for images where non-root works
    # Databases need root for init, skip USER for postgres/mariadb/redis
    if img not in ("postgres", "mariadb", "redis-7", "freshrss", "homepage", "uptime-kuma"):
        content += '\nUSER 65532:65532\n'
    
    dockerfile_path.write_text(content)
    print(f"  ✅ {img}: ENTRYPOINT={binary}")

print(f"\nDone: {len(IMAGES_TO_FIX)} images processed")
