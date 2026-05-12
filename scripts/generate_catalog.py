#!/usr/bin/env python3
"""Generate a static HTML catalog of all Docker images in the repository."""

import json
import os
import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
OUTPUT_DIR = REPO_ROOT / "docs" / "catalog"
OUTPUT_FILE = OUTPUT_DIR / "index.html"

CATEGORY_PATTERNS = {
    "database": [
        "postgres", "postgresql", "mysql", "mariadb", "redis", "mongodb", "mongo",
        "cockroachdb", "crdb", "scylladb", "tidb", "valkey", "cassandra",
        "couchdb", "couchbase", "etcd", "memcached", "dragonfly", "dragonflydb",
        "libsql", "sqlite", "sqlcipher", "h2", "derby", "firebird", "cubrid",
        "neo4j", "janusgraph", "orientdb", "rethinkdb", "questdb", "duckdb",
        "surrealdb", "timescaledb", " Crate", "singlestore", "milvus",
        "qdrant", "lancedb", "chroma", "weaviate", "pinecone", "hazelcast",
        "badger", "nutsdb", "immudb", "pgbouncer", "pgpool", "rqlite",
        "ferretdb", "tigergraph", "voltdb", "ejdb", "kdb", "kdb-plus",
        "innodb", "vaultwarden-sqlite", "vaultwarden-mysql", "vaultwarden-postgres",
    ],
    "monitoring": [
        "prometheus", "grafana", "alertmanager", "thanos", "victoriametrics",
        "vm-agent", "vm-operator", "mimir", "cadvisor", "node-exporter",
        "windows-exporter", "consul-exporter", "bind-exporter", "haproxy-exporter",
        "memcached-exporter", "redis-exporter", "mysql-exporter", "postgres-exporter",
        "postgresql-exporter", "mongodb-exporter", "mongo-exporter", "kafka-exporter",
        "snmp-exporter", "blackbox-exporter", "statsd-exporter", "x509-exporter",
        "elasticsearch-exporter", "nginx-exporter", "cockroachdb-exporter",
        "cloudwatch-agent", "datadog-agent", "telegraf", "statping-ng",
        "kafka-exporter", "ipmi-exporter", "promxy", "uptimes", "betteruptime",
    ],
    "security": [
        "vault", "hashicorp-vault", "keycloak", "dex", "trivy", "falco",
        "clair", "opa", "cosign", "fulcio", "rekor", "step-ca", "step-cli",
        "step-acme", "step-certificates", "certificates", "crowdsec",
        "fail2ban", "clamav", "freshclam", "lynis", "chkrootkit", "rkhunter",
        "maldet", "modsecurity", "openscap", "kube-bench", "kube-hunter",
        "kubescape", "snyk", "docker-bench", "trufflehog", "truffelsh",
        "truffleshog", "gitleaks", "detect-secrets", "ggshield", "gitguardian",
        "git-secrets", "gitrob", "keynuker", "secrets-scanner", "secretz",
        "age", "shield", "hadolint", "checkov", "safeguard", "ct-log",
        "kube-state-metrics", "pip-audit", "npm-audit", "cargo-audit",
        "govulncheck", "composer-audit", "gem-audit", "conan-audit",
        "yarn-audit", "r2c-bench", "dockerfile-lint", "repo-security",
        "oauth2-proxy", "zitadel", "kanidm", "authelia", "authentik",
        "headscale", "netbird", "innernet", "tailscale", "wireguard",
        "zerotier", "strongswan", "openvpn", "ocserv", "pptpd", "softether",
        "wireguard-ui", "netmaker",
    ],
    "networking": [
        "envoy", "nginx", "traefik", "consul", "coredns", "istio", "haproxy",
        "caddy", "bind", "unbound", "dnsmasq", "powerdns", "blocky",
        "adguardhome", "pi-hole", "adguard-dns", "smartdns", "knot-resolver",
        "dnsdist", "mosquitto", "mosquito", "emqx", "vernemq", "nats",
        "rabbitmq", "kafka", "zeromq", "pulsar", "rocketmq", "activemq",
        "fluent-bit", "fluentd", "vector", "loki", "filebeat", "metricbeat",
        "heartbeat", "journalbeat", "auditbeat", "packetbeat", "logstash",
        "elasticsearch", "opensearch", "graylog", "syslog-ng", "rsyslog",
        "nxlog", "splunk-forwarder", "promtail", "awslogs", "azurelogs",
        "gcplogs", "cors-proxy", "basic-auth-proxy", "rate-limiter",
    ],
    "observability": [
        "jaeger", "zipkin", "opentelemetry", "tempo", "pyroscope",
        "otel", "parca", "phlare",
    ],
    "storage": [
        "minio", "s3", "ceph", "seafile", "restic", "rclone", "duplicati",
        "nextcloud", "syncthing",
    ],
    "ci-cd": [
        "jenkins", "drone", "tekton", "argo", "argocd", "argo-cd", "woodpecker",
        "gitea", "forgejo", "gitlab", "buildkit", "buildah", "kaniko",
        "helm", "kustomize", "flux", "dependabot", "renovate", "renovatebot",
        "prefect", "dagster", "mlflow", "github-actions", "portainer",
        "skaffold", "tilt",
    ],
    "logging": [
        "fluentd", "fluent-bit", "loki", "elasticsearch", "opensearch",
        "logstash", "graylog", "vector", "filebeat", "syslog-ng",
        "rsyslog", "promtail", "journalbeat", "auditbeat", "metricbeat",
        "heartbeat", "packetbeat", "splunk-forwarder", "awslogs",
        "azurelogs", "gcplogs", "nxlog",
    ],
    "container-runtime": [
        "containerd", "crio", "podman", "buildkit", "buildah", "docker",
        "k3s", "k3d", "runc", "kubelet",
    ],
    "operator": [],
    "tool": [
        "hadolint", "syft", "grype", "cosign", "crane", "helm", "kubectl",
        "kubescape", "trivy", "rclone", "restic", "lazydocker", "tig",
        "jq", "yq", "mc", "dbmate", "step-cli", "airgap", "health-shim",
        "healthcheck", "go-static", "scratch-base", "scratch-go",
        "wolfi-python", "wolfi-jdk", "wolfi-node", "wolfi-gcc",
        "debian-slim", "distroless", "alpine", "musl",
    ],
    "messaging": [
        "kafka", "rabbitmq", "nats", "zeromq", "pulsar", "rocketmq",
        "activemq", "emqx", "vernemq", "mosquitto", "mqtt",
    ],
    "identity": [
        "keycloak", "dex", "zitadel", "kanidm", "authelia", "authentik",
        "ldap", "openldap", "389ds", "freeipa", "lldap", "headscale",
        "vault", "hashicorp-vault",
    ],
    "home-automation": [
        "homeassistant", "homebridge", "esphome", "zigbee2mqtt", "node-red",
        "mqtt", "zigbee", "tasmota", "domoticz", "jeedom", "iobroker",
        "openhab", "homekit",
    ],
    "media": [
        "plex", "jellyfin", "emby", "sonarr", "radarr", "lidarr", "prowlarr",
        "bazarr", "whisparr", "readarr", "tautulli", "overseerr", "jellyseer",
        "navidrome", "airsonic", "subsonic", "audiotracks", "koel",
        "calibre", "audiobookshelf", "immich", "photoprism", "piwigo",
        "lychee", "photocha", "photoshow", "gallery3", "sigal", "ulogger",
    ],
    "web-app": [
        "nextcloud", "wordpress", "drupal", "joomla", "mastodon", "matrix",
        "element", "dendrite", "conduit", "cinny", "hedgedoc", "outline",
        "codimd", "cryptpad", "collabora", "onlyoffice", "appsmith",
        "budibase", "tooljet", "retool", "redash", "metabase", "superset",
        "grafana", "dashy", "homepage", "flame", "heimdall", "homarr",
        "stirling-pdf", "paperless", "vaultwarden", "bitwarden",
        "freshrss", "miniflux", "tinytinyrss", "newsboat", "newsblur",
        "PrivateBin", "hledger", "gnucash", "firefly-iii", "invoice-ninja",
        "erpnext", "dolibarr", "suitecrm", "vtigercrm", "odoo", "akaunting",
        "taiga", "focalboard", "planka", "vikunja", "wekan", "taskcafe",
        "ntfy", "gotify", "matrix", "mattermost", "rocketchat", "zulip",
        "zulip", "element-web", "element-x", "nheko",
    ],
}


def categorize(name):
    if name.endswith("-operator") or name.endswith("-controller"):
        return "operator"
    name_lower = name.lower()
    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() == name_lower or name_lower.startswith(pattern.lower() + "-"):
                return category
    return "other"


def parse_dockerfile(path):
    if not path.exists():
        return None
    text = path.read_text(errors="replace")

    version = ""
    m = re.search(r'^ARG\s+(?:IMAGE_)?VERSION\s*=\s*"?([^"\s]+)"?', text, re.MULTILINE)
    if m:
        version = m.group(1)

    base_image = ""
    for m in re.finditer(r'^FROM\s+(\S+)', text, re.MULTILINE):
        candidate = m.group(1)
        if candidate.lower().endswith((" as builder", " as downloader", " as compile")):
            continue
        if "AS " not in candidate.upper():
            base_image = candidate
            break
        parts = candidate.split()
        if len(parts) >= 1:
            base_image = parts[0]

    if not base_image:
        for m in re.finditer(r'^FROM\s+(\S+)', text, re.MULTILINE):
            base_image = m.group(1)
            break

    ports = re.findall(r'^EXPOSE\s+(\S+)', text, re.MULTILINE)

    user = ""
    m = re.search(r'^USER\s+(\S+)', text, re.MULTILINE)
    if m:
        user = m.group(1)

    entrypoint = ""
    m = re.search(r'^ENTRYPOINT\s+\[?"([^"]+)"?\]?', text, re.MULTILINE)
    if m:
        entrypoint = m.group(1)

    labels = {}
    label_blocks = re.findall(
        r'LABEL\s+((?:[^\n\\]|\\\n)*(?=\n\s*(?:FROM|LABEL|ENTRYPOINT|CMD|EXPOSE|USER|RUN|COPY|ADD|WORKDIR|VOLUME|ARG|ENV|STOPSIGNAL|HEALTHCHECK|SHELL|ONBUILD)|\Z))',
        text, re.MULTILINE
    )
    for block in label_blocks:
        block = block.replace('\\\n', ' ')
        for m in re.finditer(r'(\S+?)\s*=\s*"([^"]*)"', block):
            labels[m.group(1)] = m.group(2)

    stop_signal = ""
    m = re.search(r'^STOPSIGNAL\s+(\S+)', text, re.MULTILINE)
    if m:
        stop_signal = m.group(1)

    return {
        "version": version,
        "base_image": base_image,
        "ports": ports,
        "user": user,
        "entrypoint": entrypoint,
        "labels": labels,
        "stop_signal": stop_signal,
    }


def parse_checksums(path):
    if not path.exists():
        return "missing"
    text = path.read_text(errors="replace")
    if "Status: VERIFIED" in text:
        return "verified"
    elif "Status: PENDING" in text or "expected_sha256 = \"PENDING" in text:
        return "pending"
    return "unknown"


def parse_manifest(path):
    if not path.exists():
        return {}
    text = path.read_text(errors="replace")
    data = {}
    for m in re.finditer(r'^(\w+)\s*=\s*"([^"]*)"', text, re.MULTILINE):
        data[m.group(1)] = m.group(2)
    return data


def scan_images():
    images = []
    for entry in sorted(IMAGES_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("_") or entry.name.startswith("."):
            continue
        dockerfile = entry / "Dockerfile"
        if not dockerfile.exists():
            continue

        name = entry.name
        meta = parse_dockerfile(dockerfile)
        if meta is None:
            continue

        checksums_status = parse_checksums(entry / "CHECKSUMS")
        manifest = parse_manifest(entry / "manifest.toml")
        category = categorize(name)

        version = meta["version"] or manifest.get("version", "N/A")
        vendor = meta["labels"].get("org.opencontainers.image.vendor", "")
        if not vendor:
            vendor = manifest.get("vendor", "")
        tier = meta["labels"].get("evergreen.image.tier", manifest.get("tier", ""))
        base_image = meta["base_image"] or manifest.get("base_image", manifest.get("runtime_image", "unknown"))

        base_type = "scratch"
        bl = base_image.lower()
        if "wolfi" in bl:
            base_type = "wolfi"
        elif "debian" in bl:
            base_type = "debian"
        elif "alpine" in bl:
            base_type = "alpine"
        elif "ubuntu" in bl:
            base_type = "ubuntu"
        elif "scratch" in bl:
            base_type = "scratch"
        elif "distroless" in bl:
            base_type = "distroless"
        elif "chainguard" in bl:
            base_type = "wolfi"

        nonroot = meta["labels"].get("evergreen.constraint.nonroot", "false") == "true"
        hardened = meta["labels"].get("evergreen.constraint.hardened", "false") == "true"

        images.append({
            "name": name,
            "version": version,
            "vendor": vendor,
            "tier": tier,
            "category": category,
            "base_image": base_image,
            "base_type": base_type,
            "ports": meta["ports"],
            "user": meta["user"],
            "entrypoint": meta["entrypoint"],
            "labels": meta["labels"],
            "checksums": checksums_status,
            "stop_signal": meta["stop_signal"],
            "nonroot": nonroot,
            "hardened": hardened,
            "manifest": manifest,
        })

    return images


def generate_html(images):
    category_counts = defaultdict(int)
    for img in images:
        category_counts[img["category"]] += 1

    categories_sorted = sorted(category_counts.items(), key=lambda x: -x[1])
    verified_count = sum(1 for img in images if img["checksums"] == "verified")
    pending_count = sum(1 for img in images if img["checksums"] == "pending")
    missing_count = sum(1 for img in images if img["checksums"] == "missing")

    images_json = json.dumps(images, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Evergreen Image Registry Catalog</title>
<style>
:root {{
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-tertiary: #21262d;
    --border: #30363d;
    --text-primary: #e6edf3;
    --text-secondary: #8b949e;
    --text-muted: #6e7681;
    --accent: #58a6ff;
    --accent-dim: #1f6feb;
    --green: #3fb950;
    --green-dim: #238636;
    --yellow: #d29922;
    --yellow-dim: #9e6a03;
    --red: #f85149;
    --red-dim: #da3633;
    --purple: #bc8cff;
    --orange: #f0883e;
    --radius: 8px;
    --radius-sm: 6px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.5;
    min-height: 100vh;
}}

.container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 24px 20px;
}}

header {{
    margin-bottom: 32px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 24px;
}}

header h1 {{
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 4px;
}}

header h1 a {{
    color: var(--text-primary);
    text-decoration: none;
}}

header h1 a:hover {{
    color: var(--accent);
}}

header p {{
    color: var(--text-secondary);
    font-size: 14px;
}}

.stats {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin: 20px 0;
}}

.stat-card {{
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 12px 18px;
    min-width: 120px;
    flex: 1;
}}

.stat-card .stat-value {{
    font-size: 24px;
    font-weight: 700;
}}

.stat-card .stat-label {{
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.stat-card.verified .stat-value {{ color: var(--green); }}
.stat-card.pending .stat-value {{ color: var(--yellow); }}
.stat-card.missing .stat-value {{ color: var(--red); }}

.categories {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 16px 0;
}}

.cat-btn {{
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.15s ease;
    font-family: inherit;
}}

.cat-btn:hover {{
    border-color: var(--accent);
    color: var(--text-primary);
}}

.cat-btn.active {{
    background: var(--accent-dim);
    border-color: var(--accent);
    color: #fff;
}}

.cat-btn .count {{
    color: var(--text-muted);
    margin-left: 4px;
    font-size: 11px;
}}

.cat-btn.active .count {{
    color: rgba(255,255,255,0.7);
}}

.controls {{
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
    flex-wrap: wrap;
    align-items: center;
}}

.search {{
    flex: 1;
    min-width: 250px;
    position: relative;
}}

.search input {{
    width: 100%;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 10px 14px 10px 38px;
    color: var(--text-primary);
    font-size: 14px;
    font-family: inherit;
    outline: none;
    transition: border-color 0.15s ease;
}}

.search input:focus {{
    border-color: var(--accent);
}}

.search::before {{
    content: "\\1F50D";
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 14px;
    opacity: 0.5;
}}

.sort-select {{
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 10px 14px;
    color: var(--text-primary);
    font-size: 14px;
    font-family: inherit;
    outline: none;
    cursor: pointer;
}}

.sort-select:focus {{
    border-color: var(--accent);
}}

.count-label {{
    color: var(--text-secondary);
    font-size: 13px;
    white-space: nowrap;
}}

.table-wrap {{
    overflow-x: auto;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--bg-secondary);
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}}

thead {{
    position: sticky;
    top: 0;
    z-index: 10;
}}

th {{
    background: var(--bg-tertiary);
    color: var(--text-secondary);
    font-weight: 600;
    text-align: left;
    padding: 12px 16px;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
    border-bottom: 1px solid var(--border);
}}

th:hover {{
    color: var(--text-primary);
}}

th .sort-arrow {{
    margin-left: 4px;
    opacity: 0.4;
    font-size: 10px;
}}

th.sorted .sort-arrow {{
    opacity: 1;
    color: var(--accent);
}}

td {{
    padding: 10px 16px;
    border-bottom: 1px solid var(--border);
    vertical-align: middle;
}}

tr:last-child td {{
    border-bottom: none;
}}

tr.image-row {{
    cursor: pointer;
    transition: background 0.1s ease;
}}

tr.image-row:hover {{
    background: rgba(88, 166, 255, 0.04);
}}

tr.image-row.expanded {{
    background: rgba(88, 166, 255, 0.06);
}}

.img-name {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 13px;
    color: var(--accent);
    word-break: break-all;
}}

.version {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 13px;
}}

.base {{
    font-size: 12px;
    color: var(--text-secondary);
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
}}

.base-type {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 500;
}}

.base-type.scratch {{ background: rgba(56,139,253,0.15); color: #79c0ff; }}
.base-type.wolfi {{ background: rgba(63,185,80,0.15); color: #56d364; }}
.base-type.debian {{ background: rgba(210,153,34,0.15); color: #e3b341; }}
.base-type.alpine {{ background: rgba(56,139,253,0.15); color: #79c0ff; }}
.base-type.distroless {{ background: rgba(188,140,255,0.15); color: #d2a8ff; }}
.base-type.ubuntu {{ background: rgba(240,136,62,0.15); color: #f0883e; }}

.category-tag {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 500;
    background: var(--bg-tertiary);
    color: var(--text-secondary);
    white-space: nowrap;
}}

.verification {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    font-weight: 500;
    white-space: nowrap;
}}

.verification.verified {{ color: var(--green); }}
.verification.pending {{ color: var(--yellow); }}
.verification.missing {{ color: var(--red); }}
.verification.unknown {{ color: var(--text-muted); }}

.verification .dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
}}

.verification.verified .dot {{ background: var(--green); }}
.verification.pending .dot {{ background: var(--yellow); }}
.verification.missing .dot {{ background: var(--red); }}
.verification.unknown .dot {{ background: var(--text-muted); }}

.tier {{
    display: inline-block;
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
}}

.tier-1 {{ background: rgba(63,185,80,0.2); color: var(--green); }}
.tier-2 {{ background: rgba(210,153,34,0.2); color: var(--yellow); }}
.tier-3 {{ background: rgba(240,136,62,0.2); color: var(--orange); }}

.detail-row {{
    display: none;
}}

.detail-row.visible {{
    display: table-row;
}}

.detail-row td {{
    background: var(--bg-primary);
    padding: 16px 20px;
}}

.detail-content {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
}}

.detail-section h4 {{
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin-bottom: 8px;
}}

.detail-section .kv {{
    font-size: 13px;
    line-height: 1.7;
}}

.detail-section .kv .key {{
    color: var(--text-secondary);
}}

.detail-section .kv .val {{
    color: var(--text-primary);
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 12px;
}}

.detail-section .ports-list {{
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}}

.detail-section .port {{
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
}}

.evergreen-label {{
    color: var(--purple);
}}

.expand-icon {{
    color: var(--text-muted);
    font-size: 10px;
    transition: transform 0.15s ease;
    display: inline-block;
}}

tr.expanded .expand-icon {{
    transform: rotate(90deg);
}}

.no-results {{
    text-align: center;
    padding: 60px 20px;
    color: var(--text-secondary);
}}

.no-results .icon {{
    font-size: 48px;
    margin-bottom: 12px;
    opacity: 0.3;
}}

footer {{
    margin-top: 40px;
    padding: 20px 0;
    border-top: 1px solid var(--border);
    text-align: center;
    color: var(--text-muted);
    font-size: 12px;
}}

@media (max-width: 768px) {{
    .container {{
        padding: 16px 12px;
    }}

    header h1 {{
        font-size: 22px;
    }}

    .stat-card {{
        min-width: 80px;
        padding: 8px 12px;
    }}

    .stat-card .stat-value {{
        font-size: 20px;
    }}

    .controls {{
        flex-direction: column;
    }}

    .search {{
        min-width: 100%;
    }}

    td, th {{
        padding: 8px 10px;
    }}

    .detail-content {{
        grid-template-columns: 1fr;
    }}

    .categories {{
        gap: 6px;
    }}

    .cat-btn {{
        padding: 5px 10px;
        font-size: 12px;
    }}
}}

@media (max-width: 480px) {{
    .hide-mobile {{
        display: none;
    }}

    .stats {{
        gap: 8px;
    }}

    .stat-card {{
        min-width: 70px;
        padding: 6px 10px;
    }}

    .stat-card .stat-value {{
        font-size: 18px;
    }}

    .stat-card .stat-label {{
        font-size: 10px;
    }}
}}
</style>
</head>
<body>
<div class="container">
    <header>
        <h1><a href="https://github.com/WyattAu/EvergreenImageRegistry">Evergreen Image Registry</a></h1>
        <p>Evergreen, hardened container images catalog &mdash; {len(images)} images across {len(category_counts)} categories</p>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{len(images)}</div>
                <div class="stat-label">Total Images</div>
            </div>
            <div class="stat-card verified">
                <div class="stat-value">{verified_count}</div>
                <div class="stat-label">Verified</div>
            </div>
            <div class="stat-card pending">
                <div class="stat-value">{pending_count}</div>
                <div class="stat-label">Pending</div>
            </div>
            <div class="stat-card missing">
                <div class="stat-value">{missing_count}</div>
                <div class="stat-label">Missing Checksums</div>
            </div>
        </div>
        <div class="categories">
            <button class="cat-btn active" data-cat="all">All<span class="count">({len(images)})</span></button>
            {" ".join(f'<button class="cat-btn" data-cat="{cat}">{cat.replace("-", " ").title()}<span class="count">({count})</span></button>' for cat, count in categories_sorted)}
        </div>
    </header>

    <div class="controls">
        <div class="search">
            <input type="text" id="search" placeholder="Search images..." autocomplete="off">
        </div>
        <select class="sort-select" id="sort">
            <option value="name-asc">Name A-Z</option>
            <option value="name-desc">Name Z-A</option>
            <option value="category-asc">Category A-Z</option>
            <option value="version-desc">Newest Version</option>
            <option value="checksums">Verification</option>
            <option value="tier">Tier</option>
        </select>
        <span class="count-label" id="count-label">Showing {len(images)} images</span>
    </div>

    <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th data-sort="name">Image <span class="sort-arrow">&#9650;</span></th>
                    <th data-sort="version">Version <span class="sort-arrow">&#9650;</span></th>
                    <th data-sort="base_type">Base <span class="sort-arrow">&#9650;</span></th>
                    <th data-sort="category" class="hide-mobile">Category <span class="sort-arrow">&#9650;</span></th>
                    <th data-sort="checksums">Status <span class="sort-arrow">&#9650;</span></th>
                    <th data-sort="tier" class="hide-mobile">Tier <span class="sort-arrow">&#9650;</span></th>
                </tr>
            </thead>
            <tbody id="tbody"></tbody>
        </table>
    </div>

    <div class="no-results" id="no-results" style="display:none;">
        <div class="icon">&#128269;</div>
        <div>No images match your search.</div>
    </div>

    <footer>
        Generated by <code>scripts/generate_catalog.py</code> &mdash; Evergreen Image Registry
    </footer>
</div>

<script>
const IMAGES = {images_json};

const tbody = document.getElementById("tbody");
const searchInput = document.getElementById("search");
const sortSelect = document.getElementById("sort");
const countLabel = document.getElementById("count-label");
const noResults = document.getElementById("no-results");
const catButtons = document.querySelectorAll(".cat-btn");
const thHeaders = document.querySelectorAll("th[data-sort]");

let activeCategory = "all";
let expandedRows = new Set();

function esc(s) {{
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
}}

function tierClass(tier) {{
    if (tier === "1") return "tier tier-1";
    if (tier === "2") return "tier tier-2";
    if (tier === "3") return "tier tier-3";
    return "tier";
}}

function checksumBadge(status) {{
    const cls = status === "verified" ? "verified" : status === "pending" ? "pending" : status === "missing" ? "missing" : "unknown";
    const label = status.charAt(0).toUpperCase() + status.slice(1);
    return '<span class="verification ' + cls + '"><span class="dot"></span>' + label + '</span>';
}}

function filterAndSort() {{
    const query = searchInput.value.toLowerCase().trim();
    const sortVal = sortSelect.value;
    const [sortKey, sortDir] = sortVal.split("-");

    let filtered = IMAGES.filter(function(img) {{
        if (activeCategory !== "all" && img.category !== activeCategory) return false;
        if (query && img.name.toLowerCase().indexOf(query) === -1 &&
            img.version.toLowerCase().indexOf(query) === -1 &&
            img.vendor.toLowerCase().indexOf(query) === -1 &&
            img.category.toLowerCase().indexOf(query) === -1) return false;
        return true;
    }});

    filtered.sort(function(a, b) {{
        let va, vb;
        if (sortKey === "name") {{ va = a.name; vb = b.name; }}
        else if (sortKey === "version") {{ va = a.version; vb = b.version; }}
        else if (sortKey === "base_type") {{ va = a.base_type; vb = b.base_type; }}
        else if (sortKey === "category") {{ va = a.category; vb = b.category; }}
        else if (sortKey === "checksums") {{ va = a.checksums; vb = b.checksums; }}
        else if (sortKey === "tier") {{ va = a.tier; vb = b.tier; }}
        else {{ va = a.name; vb = b.name; }}

        if (va < vb) return sortDir === "asc" ? -1 : 1;
        if (va > vb) return sortDir === "asc" ? 1 : -1;
        return 0;
    }});

    return filtered;
}}

function renderLabels(labels) {{
    const keys = Object.keys(labels);
    if (keys.length === 0) return '<span style="color:var(--text-muted)">None</span>';

    let html = "";
    const ociKeys = keys.filter(function(k) {{ return k.startsWith("org.opencontainers."); }});
    const sovKeys = keys.filter(function(k) {{ return k.startsWith("evergreen."); }});

    if (ociKeys.length > 0) {{
        html += "<div style='margin-bottom:8px'>";
        ociKeys.forEach(function(k) {{
            html += '<div class="kv"><span class="key">' + esc(k) + ":</span> <span class='val'>" + esc(labels[k]) + "</span></div>";
        }});
        html += "</div>";
    }}

    if (sovKeys.length > 0) {{
        html += "<div>";
        sovKeys.forEach(function(k) {{
            html += '<div class="kv evergreen-label"><span class="key">' + esc(k) + ":</span> <span class='val'>" + esc(labels[k]) + "</span></div>";
        }});
        html += "</div>";
    }}

    return html;
}}

function renderDetail(img) {{
    let portsHtml = img.ports.length > 0
        ? img.ports.map(function(p) {{ return '<span class="port">' + esc(p) + '</span>'; }}).join("")
        : '<span style="color:var(--text-muted)">None</span>';

    return '<div class="detail-content">' +
        '<div class="detail-section"><h4>Info</h4><div class="kv">' +
        '<span class="key">Base Image:</span> <span class="val">' + esc(img.base_image) + '</span><br>' +
        '<span class="key">User:</span> <span class="val">' + esc(img.user || "default") + '</span><br>' +
        '<span class="key">Entrypoint:</span> <span class="val">' + esc(img.entrypoint || "default") + '</span><br>' +
        (img.stop_signal ? '<span class="key">Stop Signal:</span> <span class="val">' + esc(img.stop_signal) + '</span><br>' : '') +
        '<span class="key">Non-Root:</span> <span class="val">' + (img.nonroot ? "Yes" : "No") + '</span><br>' +
        '<span class="key">Hardened:</span> <span class="val">' + (img.hardened ? "Yes" : "No") + '</span>' +
        '</div></div>' +
        '<div class="detail-section"><h4>Ports</h4><div class="ports-list">' + portsHtml + '</div></div>' +
        '<div class="detail-section"><h4>Labels</h4>' + renderLabels(img.labels) + '</div>' +
        '</div>';
}}

function render() {{
    const filtered = filterAndSort();
    countLabel.textContent = "Showing " + filtered.length + " image" + (filtered.length !== 1 ? "s" : "");
    noResults.style.display = filtered.length === 0 ? "block" : "none";

    let html = "";
    filtered.forEach(function(img) {{
        const isExpanded = expandedRows.has(img.name);
        html += '<tr class="image-row' + (isExpanded ? " expanded" : "") + '" data-name="' + esc(img.name) + '">' +
            '<td><span class="expand-icon">&#9654;</span> <span class="img-name">' + esc(img.name) + '</span></td>' +
            '<td><span class="version">' + esc(img.version) + '</span></td>' +
            '<td><span class="base-type ' + esc(img.base_type) + '">' + esc(img.base_type) + '</span> <span class="base hide-mobile">' + esc(img.base_image.split(":")[0]) + '</span></td>' +
            '<td class="hide-mobile"><span class="category-tag">' + esc(img.category) + '</span></td>' +
            '<td>' + checksumBadge(img.checksums) + '</td>' +
            '<td class="hide-mobile"><span class="' + tierClass(img.tier) + '">' + esc(img.tier || "-") + '</span></td>' +
            '</tr>';
        html += '<tr class="detail-row' + (isExpanded ? " visible" : "") + '" data-detail="' + esc(img.name) + '">' +
            '<td colspan="6">' + renderDetail(img) + '</td></tr>';
    }});

    tbody.innerHTML = html;

    tbody.querySelectorAll(".image-row").forEach(function(row) {{
        row.addEventListener("click", function() {{
            const name = row.getAttribute("data-name");
            if (expandedRows.has(name)) expandedRows.delete(name);
            else expandedRows.add(name);
            render();
        }});
    }});
}}

catButtons.forEach(function(btn) {{
    btn.addEventListener("click", function() {{
        catButtons.forEach(function(b) {{ b.classList.remove("active"); }});
        btn.classList.add("active");
        activeCategory = btn.getAttribute("data-cat");
        render();
    }});
}});

searchInput.addEventListener("input", render);
sortSelect.addEventListener("change", render);

thHeaders.forEach(function(th) {{
    th.addEventListener("click", function() {{
        const key = th.getAttribute("data-sort");
        const current = sortSelect.value;
        const parts = current.split("-");
        if (parts[0] === key) {{
            parts[1] = parts[1] === "asc" ? "desc" : "asc";
        }} else {{
            parts[0] = key;
            parts[1] = "asc";
        }}
        sortSelect.value = parts.join("-");
        render();
    }});
}});

render();
</script>
</body>
</html>'''


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    images = scan_images()
    html_content = generate_html(images)
    OUTPUT_FILE.write_text(html_content, encoding="utf-8")
    print(f"Generated catalog with {len(images)} images -> {OUTPUT_FILE}")
    categories = defaultdict(int)
    for img in images:
        categories[img["category"]] += 1
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
