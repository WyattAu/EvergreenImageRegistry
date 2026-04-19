#!/usr/bin/env python3
"""
Image Generator - Generates Dockerfiles from templates
Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
NO ALPINE - NEVER USE ALPINE
"""

import os
import sys

# Image definitions - sourced from requiredimages.md
IMAGES = {
    # Category 1: Gateways (Static binaries) - prefer scratch
    "gateways": [
        {"name": "traefik", "base": "scratch", "binary": "traefik", "version": "3.1.4", 
         "url": "https://github.com/traefik/traefik/releases/download/v{VERSION}/traefik_{VERSION}_linux_amd64.tar.gz",
         "health": "--version", "ports": "80 443 8080", "vendor": "Traefik Labs"},
        {"name": "nginx", "base": "scratch", "binary": "nginx", "version": "1.27.1",
         "url": "https://nginx.org/download/nginx-{VERSION}.tar.gz",
         "health": "-v", "ports": "80 443", "vendor": "Nginx Inc"},
        {"name": "caddy", "base": "scratch", "binary": "caddy", "version": "2.7.6",
         "url": "https://github.com/caddyserver/caddy/releases/download/v{VERSION}/caddy_{VERSION}_linux_amd64.tar.gz",
         "health": "version", "ports": "80 443 2019", "vendor": "Caddy"},
        {"name": "haproxy", "base": "distroless", "binary": "haproxy", "version": "3.0.1",
         "url": "https://www.haproxy.org/download/{VERSION}/src/haproxy-{VERSION}.tar.gz",
         "health": "-v", "ports": "80 443", "vendor": "HAProxy"},
        {"name": "envoy", "base": "distroless", "binary": "envoy", "version": "1.31.0",
         "url": "https://envoy.io/",  
         "health": "--version", "ports": "80 443 9900", "vendor": "Envoy"},
        {"name": "coredns", "base": "scratch", "binary": "coredns", "version": "1.12.0",
         "url": "https://github.com/coredns/coredns/releases/download/v{VERSION}/coredns_{VERSION}_linux_amd64.tgz",
         "health": "--version", "ports": "53", "vendor": "Coredns"},
    ],
    # Category 2: Databases - need packages, use wolfi or debian fallback
    "databases": [
        {"name": "postgres", "base": "debian", "binary": "postgres", "version": "17.4",
         "packages": "postgresql-17", "health": "pg_isready", "ports": "5432", "user": "postgres", "vendor": "PostgreSQL"},
        {"name": "mysql", "base": "debian", "binary": "mariadbd", "version": "11.4",
         "packages": "default-mysql-server default-mysql-client", 
         "health": "mariadb-admin ping", "ports": "3306", "user": "mysql", "vendor": "MariaDB"},
        {"name": "mariadb", "base": "debian", "binary": "mariadbd", "version": "11.4",
         "packages": "default-mysql-server default-mysql-client", 
         "health": "mariadb-admin ping", "ports": "3306", "user": "mysql", "vendor": "MariaDB"},
        {"name": "cockroachdb", "base": "debian", "binary": "cockroach", "version": "23.2.0",
         "packages": "cockroachdb", "health": "cockroach sql", "ports": "26257 8080", "user": "cockroach", "vendor": "CockroachDB"},
    ],
    # Category 3: Key-Value Stores
    "keyvalue": [
        {"name": "redis", "base": "debian", "binary": "redis-server", "version": "7.4.1",
         "packages": "redis-server", "health": "redis-cli ping", "ports": "6379", "user": "redis", "vendor": "Redis"},
        {"name": "memcached", "base": "debian", "binary": "memcached", "version": "1.6.26",
         "packages": "memcached", "health": "stats", "ports": "11211", "user": "memcached", "vendor": "Memcached"},
        {"name": "etcd", "base": "debian", "binary": "etcd", "version": "3.5.15",
         "packages": "etcd", "health": "etcdctl endpoint-health", "ports": "2379 2380", "user": "etcd", "vendor": "etcd"},
        {"name": "consul", "base": "debian", "binary": "consul", "version": "1.18.1",
         "packages": "consul", "health": "consul members", "ports": "8500", "user": "consul", "vendor": "HashiCorp"},
    ],
    # Category 4: Security - prefer scratch/distroless
    "security": [
        {"name": "vault", "base": "scratch", "binary": "vault", "version": "1.18.1",
         "url": "https://releases.hashicorp.com/vault/{VERSION}/vault_{VERSION}_linux_amd64.zip",
         "health": "status", "ports": "8200 8201", "vendor": "HashiCorp"},
        {"name": "step-cli", "base": "scratch", "binary": "step", "version": "0.25.2",
         "url": "https://github.com/smallstep/cli/releases/download/v{VERSION}/step_{VERSION}_linux_amd64.tar.gz",
         "health": "version", "ports": "", "vendor": "Smallstep"},
        {"name": "cosign", "base": "scratch", "binary": "cosign", "version": "2.4.0",
         "url": "https://github.com/sigstore/cosign/releases/download/v{VERSION}/cosign_{VERSION}_linux_amd64.tar.gz",
         "health": "version", "ports": "", "vendor": "Sigstore"},
        {"name": "trivy", "base": "scratch", "binary": "trivy", "version": "0.53.0",
         "url": "https://github.com/aquasecurity/trivy/releases/download/v{VERSION}/trivy_{VERSION}_linux_amd64.tar.gz",
         "health": "version", "ports": "", "vendor": "Aqua Security"},
        {"name": "syft", "base": "scratch", "binary": "syft", "version": "1.8.0",
         "url": "https://github.com/anchore/syft/releases/download/v{VERSION}/syft_{VERSION}_linux_amd64.tar.gz",
         "health": "version", "ports": "", "vendor": "Anchore"},
        {"name": "grype", "base": "scratch", "binary": "grype", "version": "0.80.0",
         "url": "https://github.com/anchore/grype/releases/download/v{VERSION}/grype_{VERSION}_linux_amd64.tar.gz",
         "health": "version", "ports": "", "vendor": "Anchore"},
    ],
    # Category 5: Observability - static preferred
    "observability": [
        {"name": "prometheus", "base": "scratch", "binary": "prometheus", "version": "2.53.0",
         "url": "https://github.com/prometheus/prometheus/releases/download/v{VERSION}/prometheus-{VERSION}.linux-amd64.tar.gz",
         "health": "--version", "ports": "9090", "vendor": "Prometheus"},
        {"name": "loki", "base": "scratch", "binary": "loki", "version": "3.1.0",
         "url": "https://github.com/grafana/loki/releases/download/v{VERSION}/loki-{VERSION}.linux-amd64.zip",
         "health": "version", "ports": "3100", "vendor": "Grafana"},
        {"name": "grafana", "base": "distroless", "binary": "grafana", "version": "11.0.0",
         "url": "https://github.com/grafana/grafana/releases/download/{VERSION}/grafana-{VERSION}.linux-amd64.tar.gz",
         "health": "version", "ports": "3000", "vendor": "Grafana"},
        {"name": "node-exporter", "base": "scratch", "binary": "node_exporter", "version": "1.8.0",
         "url": "https://github.com/prometheus/node_exporter/releases/download/v{VERSION}/node_exporter-{VERSION}.linux-amd64.tar.gz",
         "health": "--version", "ports": "9100", "vendor": "Prometheus"},
    ],
    # Category 6: DevOps & CI/CD
    "devops": [
        {"name": "jenkins", "base": "debian", "binary": "jenkins", "version": "2.462",
         "packages": "default-jdk-headless", "health": "/api/json", "ports": "8080", "user": "jenkins", "vendor": "Jenkins"},
        {"name": "argocd", "base": "debian", "binary": "argocd", "version": "2.13.0",
         "packages": "argocd", "health": "/healthz", "ports": "8080", "user": "argocd", "vendor": "ArgoCD"},
    ],
    # Category 7: Messaging
    "messaging": [
        {"name": "rabbitmq", "base": "debian", "binary": "rabbitmq-server", "version": "3.13.0",
         "packages": "rabbitmq-server", "health": "rabbitmq-diagnostics ping", "ports": "5672 15672", "user": "rabbitmq", "vendor": "RabbitMQ"},
        {"name": "nats", "base": "distroless", "binary": "nats-server", "version": "2.10.0",
         "url": "https://github.com/nats-io/nats-server/releases/download/v{VERSION}/nats-server-{VERSION}-linux-amd64.tar.gz",
         "health": "--version", "ports": "4222 8222", "vendor": "NATS"},
    ],
    # Category 8: Storage
    "storage": [
        {"name": "minio", "base": "scratch", "binary": "minio", "version": "2024.5.28",
         "url": "https://github.com/minio/minio/releases/download/{VERSION}/minio-{VERSION}-linux-amd64",
         "health": "version", "ports": "9000 9001", "vendor": "MinIO"},
        {"name": "restic", "base": "scratch", "binary": "restic", "version": "0.17.0",
         "url": "https://github.com/restic/restic/releases/download/v{VERSION}/restic_{VERSION}_linux_amd64.tar.gz",
         "health": "version", "ports": "", "vendor": "Restic"},
        {"name": "rclone", "base": "scratch", "binary": "rclone", "version": "1.67.0",
         "url": "https://github.com/rclone/rclone/releases/download/v{VERSION}/rclone_{VERSION}_linux_amd64.tar.gz",
         "health": "version", "ports": "", "vendor": "Rclone"},
    ],
    # Category 9: Git & Collaboration
    "collaboration": [
        {"name": "gitea", "base": "debian", "binary": "gitea", "version": "1.21.0",
         "packages": "gitea", "health": "/api/health", "ports": "3000 22", "user": "git", "vendor": "Gitea"},
        {"name": "forgejo", "base": "debian", "binary": "forgejo", "version": "1.0.0",
         "packages": "forgejo", "health": "/api/health", "ports": "3000 22", "user": "git", "vendor": "Forgejo"},
    ],
}

# SCRATCH template - BEST (no runtime base, just copy binary)
SCRATCH_TEMPLATE = '''# =============================================================================
# SOVEREIGN HARDENED {name_upper}
# Generated from template - Version: {version}
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION={version}
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "{binary_url}" -o /{binary}.tar.gz && \\
    tar -xzf /{binary}.tar.gz -C / && rm /{binary}.tar.gz && chmod +x /{binary}

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/{binary} /var/cache/{binary}

FROM scratch
COPY --from=downloader /{binary} /{binary}
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/{binary} /var/log/{binary}
COPY --from=builder /var/cache/{binary} /var/cache/{binary}
USER 65534:65534
WORKDIR /app
EXPOSE {ports}
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD {health_command}
ENTRYPOINT ["/{binary}"]
LABEL org.opencontainers.image.title="{name}" \\
      org.opencontainers.image.version="{version}" \\
      org.opencontainers.image.vendor="{vendor}" \\
      sovereign.image.tier="1" \\
      sovereign.constraint.nonroot="true" \\
      sovereign.constraint.scratch="true"
'''

# DISTROLESS template - SECOND BEST (Google's minimal runtime)
DISTROLESS_TEMPLATE = '''# =============================================================================
# SOVEREIGN HARDENED {name_upper}
# Generated from template - Version: {version}
# Constraint: distroless - minimal runtime, no shell, CVE-free
# Priority: scratch > distroless (2nd best) > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION={version}
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "{binary_url}" -o /{binary}.tar.gz && \\
    tar -xzf /{binary}.tar.gz -C / && rm /{binary}.tar.gz && chmod +x /{binary}

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/{binary} /var/cache/{binary}

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /{binary} /{binary}
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/{binary} /var/log/{binary}
COPY --from=builder /var/cache/{binary} /var/cache/{binary}
USER 65534:65534
WORKDIR /app
EXPOSE {ports}
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD {health_command}
ENTRYPOINT ["/{binary}"]
LABEL org.opencontainers.image.title="{name}" \\
      org.opencontainers.image.version="{version}" \\
      org.opencontainers.image.vendor="{vendor}" \\
      sovereign.image.tier="1" \\
      sovereign.constraint.nonroot="true" \\
      sovereign.constraint.distroless="true"
'''

# WOLFI template - THIRD CHOICE (Chainguard's minimal Wolfi OS)
WOLFI_TEMPLATE = '''# =============================================================================
# SOVEREIGN HARDENED {name_upper}
# Generated from template - Version: {version}
# Constraint: wolfi - minimal OS base, CVE-free, better than debian/alpine
# Priority: scratch > distroless > wolfi (3rd) > debian-slim (fallback)
# =============================================================================

ARG VERSION={version}
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache {packages} ca-certificates && rm -rf /var/cache/apk/*
RUN adduser -D -u 65534 {user} 2>/dev/null || true
RUN mkdir -p /app /var/log/{name} /var/cache/{name} && chown -R {user}:{user} /app /var/log/{name} /var/cache/{name} 2>/dev/null || true
USER {user}:{user}
WORKDIR /app
EXPOSE {ports}
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD {health}
ENTRYPOINT ["{binary}"]
LABEL org.opencontainers.image.title="{name}" \\
      org.opencontainers.image.version="{version}" \\
      org.opencontainers.image.vendor="{vendor}" \\
      sovereign.image.tier="1" \\
      sovereign.constraint.nonroot="true" \\
      sovereign.constraint.wolfi="true"
'''

# DEBIAN-SLIM fallback template - LAST RESORT (when no other option works)
DEBIAN_TEMPLATE = '''# =============================================================================
# SOVEREIGN HARDENED {name_upper}
# Generated from template - Version: {version}
# Constraint: debian-slim - fallback when scratch/distroless/wolfi not available
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION={version}
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends {packages} ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' {user} 2>/dev/null || true
RUN mkdir -p /app /var/log/{name} /var/cache/{name} && chown -R {user}:{user} /app /var/log/{name} /var/cache/{name} 2>/dev/null || true
USER {user}:{user}
WORKDIR /app
EXPOSE {ports}
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD {health}
ENTRYPOINT ["{binary}"]
LABEL org.opencontainers.image.title="{name}" \\
      org.opencontainers.image.version="{version}" \\
      org.opencontainers.image.vendor="{vendor}" \\
      sovereign.image.tier="1" \\
      sovereign.constraint.nonroot="true" \\
      sovereign.constraint.debian_slim="true"
'''

def generate_scratch_image(img_def, output_dir):
    """Generate Dockerfile for scratch-based images (BEST)"""
    name = img_def["name"]
    version = img_def.get("version", "latest")
    binary = img_def["binary"]
    
    url = img_def.get("url", "")
    if url and "{VERSION}" in url:
        url = url.replace("{VERSION}", version)
    
    vendor = img_def.get("vendor", "Official")
    health = img_def.get("health", f"{binary} --version")
    health_command = f"{binary} {health} 2>/dev/null || exit 1"
    
    content = SCRATCH_TEMPLATE.format(
        name_upper=name.upper(),
        name=name,
        version=version,
        binary=binary,
        binary_url=url,
        vendor=vendor,
        ports=img_def["ports"],
        health=health,
        health_command=health_command,
    )
    
    filepath = os.path.join(output_dir, f"{name}/Dockerfile")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Generated: {filepath}")

def generate_distroless_image(img_def, output_dir):
    """Generate Dockerfile for distroless images (2ND BEST)"""
    name = img_def["name"]
    version = img_def.get("version", "latest")
    binary = img_def["binary"]
    
    url = img_def.get("url", "")
    if url and "{VERSION}" in url:
        url = url.replace("{VERSION}", version)
    
    vendor = img_def.get("vendor", "Official")
    health = img_def.get("health", f"{binary} --version")
    health_command = f"{binary} {health} 2>/dev/null || exit 1"
    
    content = DISTROLESS_TEMPLATE.format(
        name_upper=name.upper(),
        name=name,
        version=version,
        binary=binary,
        binary_url=url,
        vendor=vendor,
        ports=img_def["ports"],
        health=health,
        health_command=health_command,
    )
    
    filepath = os.path.join(output_dir, f"{name}/Dockerfile")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Generated: {filepath}")

def generate_wolfi_image(img_def, output_dir):
    """Generate Dockerfile for Wolfi images (3RD CHOICE)"""
    name = img_def["name"]
    version = img_def.get("version", "latest")
    packages = img_def.get("packages", name)
    vendor = img_def.get("vendor", "Official")
    binary = img_def.get("binary", name)
    user = img_def.get("user", name)
    health = img_def.get("health", f"{binary} --version")
    
    content = WOLFI_TEMPLATE.format(
        name_upper=name.upper(),
        name=name,
        version=version,
        packages=packages,
        vendor=vendor,
        binary=binary,
        ports=img_def["ports"],
        health=health,
        user=user,
    )
    
    filepath = os.path.join(output_dir, f"{name}/Dockerfile")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Generated: {filepath}")

def generate_debian_image(img_def, output_dir):
    """Generate Dockerfile for Debian images (LAST RESORT)"""
    name = img_def["name"]
    version = img_def.get("version", "latest")
    packages = img_def.get("packages", name)
    vendor = img_def.get("vendor", "Official")
    binary = img_def.get("binary", name)
    user = img_def.get("user", name)
    health = img_def.get("health", f"{binary} --version")
    
    content = DEBIAN_TEMPLATE.format(
        name_upper=name.upper(),
        name=name,
        version=version,
        packages=packages,
        vendor=vendor,
        binary=binary,
        ports=img_def["ports"],
        health=health,
        user=user,
    )
    
    filepath = os.path.join(output_dir, f"{name}/Dockerfile")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Generated: {filepath}")

def generate_all(category=None):
    """Generate all Dockerfiles with priority: scratch > distroless > wolfi > debian"""
    output_dir = "images"
    
    categories = IMAGES.keys() if category is None or category == "all" else [category]
    
    total = 0
    for cat in categories:
        if cat not in IMAGES:
            print(f"Unknown category: {cat}")
            continue
            
        for img_def in IMAGES[cat]:
            base = img_def.get("base", "debian")
            
            # Priority: scratch > distroless > wolfi > debian
            if base == "scratch":
                generate_scratch_image(img_def, output_dir)
            elif base == "distroless":
                generate_distroless_image(img_def, output_dir)
            elif base == "wolfi":
                generate_wolfi_image(img_def, output_dir)
            else:
                # Default to debian (last resort)
                generate_debian_image(img_def, output_dir)
            total += 1
    
    print(f"\nGenerated {total} Dockerfiles")

if __name__ == "__main__":
    category = sys.argv[1] if len(sys.argv) > 1 else "all"
    generate_all(category)