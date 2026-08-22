#!/usr/bin/env python3
"""
Expand test_config.yaml by converting stub entries to real configs.

Reads manifest.toml and Dockerfile for each image to determine:
- Binary name (from ENTRYPOINT or CMD)
- Health port (from EXPOSE or manifest ports)
- Version flag (from --version or -v patterns)
- Category (from directory structure or manifest metadata)

Outputs YAML entries for images that have enough information.
"""

import logging
import re
from pathlib import Path

import tomllib

logger = logging.getLogger(__name__)

IMAGES_DIR = Path("images")
TEST_CONFIG = IMAGES_DIR / "tests" / "test_config.yaml"


def extract_entrypoint_binary(dockerfile_path: Path) -> str | None:
    """Extract binary name from ENTRYPOINT or CMD in Dockerfile."""
    content = dockerfile_path.read_text()
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("ENTRYPOINT [") or line.startswith("CMD ["):
            # Extract first element of JSON array
            match = re.search(r'\["([^"]+)"', line)
            if match:
                binary = match.group(1)
                # Skip shell/script wrappers
                if binary in ("/bin/sh", "/bin/bash", "/busybox/sh", "sh", "bash"):
                    continue
                return binary
            # Try exec form
            match = re.search(r"ENTRYPOINT\s+(\S+)", line)
            if match:
                binary = match.group(1)
                if binary not in ("/bin/sh", "/bin/bash", "sh", "bash"):
                    return binary
            match = re.search(r"CMD\s+(\S+)", line)
            if match:
                binary = match.group(1)
                if binary not in ("/bin/sh", "/bin/bash", "sh", "bash"):
                    return binary
    return None


def extract_port(manifest_path: Path) -> int:
    """Extract primary exposed port from manifest.toml."""
    try:
        with open(manifest_path, "rb") as f:
            manifest = tomllib.load(f)
        ports = manifest.get("ports", {}).get("expose", [])
        if ports:
            return ports[0]
    except Exception:
        pass
    return 8080  # default


def extract_version_flag(dockerfile_path: Path) -> str:
    """Guess version flag from binary name or patterns."""
    content = dockerfile_path.read_text()
    # Common patterns
    if "--version" in content:
        return "--version"
    if " -v " in content or " -V " in content:
        return "-v"
    return "--version"


def determine_category(image_name: str, dockerfile_content: str) -> str:
    """Determine test category from image name and content."""
    name_lower = image_name.lower()
    dockerfile_content.lower()

    # Database
    db_keywords = [
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
    ]
    if any(kw in name_lower for kw in db_keywords):
        return "database"

    # Monitoring
    monitor_keywords = [
        "prometheus",
        "grafana",
        "alert",
        "metric",
        "monitor",
        "loki",
        "tempo",
        "mimir",
        "thanos",
        "node_exporter",
    ]
    if any(kw in name_lower for kw in monitor_keywords):
        return "monitoring"

    # Security
    sec_keywords = [
        "vault",
        "cert",
        "scanner",
        "trivy",
        "grype",
        "falco",
        "audit",
        "firewall",
        "ids",
        "ips",
        "wazuh",
        "suricata",
    ]
    if any(kw in name_lower for kw in sec_keywords):
        return "security"

    # Proxy
    proxy_keywords = [
        "nginx",
        "traefik",
        "haproxy",
        "envoy",
        "caddy",
        "proxy",
        "gateway",
        "ingress",
        "loadbalancer",
    ]
    if any(kw in name_lower for kw in proxy_keywords):
        return "proxy"

    # Messaging
    msg_keywords = ["kafka", "rabbit", "nats", "pulsar", "mqtt", "zeromq", "amqp"]
    if any(kw in name_lower for kw in msg_keywords):
        return "messaging"

    return "app"


def generate_config(
    image_name: str, binary: str, port: int, version_flag: str, category: str
) -> str:
    """Generate a YAML test config entry."""
    return f"""  {image_name}:
    binary: {binary}
    health_port: {port}
    version_flag: "{version_flag}"
    category: {category}
    functional_test: {category}
    adversarial_test: true
    startup_timeout: 15"""


def main():
    # Read current config to find stubs
    with open(TEST_CONFIG) as f:
        for line in f:
            if "binary: none" in line:
                # Find the image name from context
                pass

    # Scan all images for real config opportunities
    configs = []
    scanned = 0

    for img_dir in sorted(IMAGES_DIR.iterdir()):
        if not img_dir.is_dir():
            continue
        if img_dir.name == "tests" or img_dir.name == "health-shim":
            continue

        dockerfile = img_dir / "Dockerfile"
        manifest = img_dir / "manifest.toml"

        if not dockerfile.exists():
            continue

        scanned += 1
        binary = extract_entrypoint_binary(dockerfile)
        if not binary:
            continue

        port = extract_port(manifest) if manifest.exists() else 8080
        version_flag = extract_version_flag(dockerfile)
        category = determine_category(img_dir.name, dockerfile.read_text())

        configs.append(
            generate_config(img_dir.name, binary, port, version_flag, category)
        )

    logger.info("Scanned %d images, found %d with real binaries", scanned, len(configs))
    print("\n# === GENERATED TEST CONFIGS ===")
    for config in sorted(configs):
        print(config)


if __name__ == "__main__":
    main()
