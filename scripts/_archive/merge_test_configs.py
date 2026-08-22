#!/usr/bin/env python3
"""Replace stub entries in test_config.yaml with real configs from Dockerfile analysis."""

import logging
import re
from pathlib import Path

import tomllib

logger = logging.getLogger(__name__)

IMAGES_DIR = Path("images")
TEST_CONFIG = IMAGES_DIR / "tests" / "test_config.yaml"


def extract_binary(df: Path) -> str | None:
    content = df.read_text()
    for line in content.split("\n"):
        s = line.strip()
        if s.startswith("ENTRYPOINT [") or s.startswith("CMD ["):
            m = re.search(r'\["([^"]+)"', s)
            if m and m.group(1) not in (
                "/bin/sh",
                "/bin/bash",
                "/busybox/sh",
                "sh",
                "bash",
            ):
                return m.group(1)
        if s.startswith("ENTRYPOINT ") and not s.startswith("ENTRYPOINT ["):
            p = s.split()
            if len(p) > 1 and p[1].strip('"') not in (
                "/bin/sh",
                "/bin/bash",
                "sh",
                "bash",
            ):
                return p[1].strip('"')
        if s.startswith("CMD ") and not s.startswith("CMD ["):
            p = s.split()
            if len(p) > 1 and p[1].strip('"') not in (
                "/bin/sh",
                "/bin/bash",
                "sh",
                "bash",
            ):
                return p[1].strip('"')
    return None


def extract_port(mf: Path, df: Path) -> int:
    if mf.exists():
        try:
            with open(mf, "rb") as f:
                m = tomllib.load(f)
            for p in m.get("ports", {}).get("expose", []):
                if p != 9101:
                    return p
        except Exception:
            pass
    for line in df.read_text().split("\n"):
        if line.strip().startswith("EXPOSE "):
            for n in re.findall(r"\b(\d+)\b", line):
                if n != "9101":
                    return int(n)
    return 8080


CAT_MAP = {
    "database": [
        "sql",
        "db",
        "mongo",
        "redis",
        "postgres",
        "mysql",
        "mariadb",
        "cassandra",
        "couch",
        "etcd",
        "neo4j",
        "influx",
        "timescale",
        "valkey",
        "memcached",
        "arangodb",
        "clickhouse",
        "cockroach",
        "duckdb",
        "elasticsearch",
        "opensearch",
        "meilisearch",
        "questdb",
        "scylla",
        "crate",
    ],
    "monitoring": [
        "prometheus",
        "grafana",
        "alert",
        "metric",
        "monitor",
        "loki",
        "tempo",
        "mimir",
        "thanos",
        "exporter",
        "telegraf",
        "netdata",
        "zabbix",
        "uptime",
    ],
    "security": [
        "vault",
        "cert",
        "scan",
        "trivy",
        "grype",
        "falco",
        "audit",
        "firewall",
        "wazuh",
        "suricata",
        "clamav",
        "authelia",
        "authentik",
        "keycloak",
        "openldap",
        "freeipa",
        "rkhunter",
        "chkrootkit",
    ],
    "proxy": [
        "nginx",
        "traefik",
        "haproxy",
        "envoy",
        "caddy",
        "proxy",
        "gateway",
        "ingress",
        "apache",
        "squid",
    ],
    "messaging": [
        "kafka",
        "rabbit",
        "nats",
        "pulsar",
        "mqtt",
        "zeromq",
        "activemq",
        "emqx",
        "vernemq",
        "rocketmq",
    ],
}


def category(name: str) -> str:
    nl = name.lower()
    for cat, kws in CAT_MAP.items():
        if any(kw in nl for kw in kws):
            return cat
    return "app"


def main():
    # Build real configs
    real = {}
    for d in sorted(IMAGES_DIR.iterdir()):
        if not d.is_dir() or d.name in ("tests", "health-shim"):
            continue
        df = d / "Dockerfile"
        if not df.exists():
            continue
        b = extract_binary(df)
        if not b:
            continue
        mf = d / "manifest.toml"
        p = extract_port(mf, df)
        c = category(d.name)
        real[d.name] = (
            f'  {d.name}:\n    binary: {b}\n    health_port: {p}\n    version_flag: "--version"\n    category: {c}\n    functional_test: {c}\n    adversarial_test: true\n    startup_timeout: 15'
        )

    # Merge: replace stubs
    with open(TEST_CONFIG) as f:
        lines = f.readlines()

    out = []
    i = 0
    replaced = 0
    kept = 0

    while i < len(lines):
        line = lines[i]
        # Detect "  imagename:" followed by "    binary: none"
        if (
            line.startswith("  ")
            and line.rstrip().endswith(":")
            and not line.startswith("    ")
        ):
            name = line.strip().rstrip(":")
            if name in real:
                # Check next line
                if i + 1 < len(lines) and "binary: none" in lines[i + 1]:
                    out.append(real[name] + "\n")
                    replaced += 1
                    # Skip to next image name or end of stub block
                    i += 1
                    while i < len(lines):
                        i += 1
                        if i >= len(lines):
                            break
                        line = lines[i]
                        if (
                            line.startswith("  ")
                            and line.rstrip().endswith(":")
                            and not line.startswith("    ")
                        ):
                            break
                        if line.startswith("#") and "===" in line:
                            break
                    continue
                else:
                    kept += 1
        out.append(line)
        i += 1

    with open(TEST_CONFIG, "w") as f:
        f.writelines(out)

    logger.info("Real configs available: %d", len(real))
    logger.info("Stubs replaced: %d, Real kept: %d", replaced, kept)
    logger.info("test_config.yaml updated")


if __name__ == "__main__":
    main()
