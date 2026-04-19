#!/usr/bin/env python3
"""
Image Generator - Generates Dockerfiles from templates
Usage: python generate_templates.py [category|all]
"""

import os
import sys

# Image definitions - sourced from requiredimages.md
IMAGES = {
    # Category 1: Gateways (Static binaries) - ~50 images
    "gateways": [
        {"name": "traefik", "base": "scratch", "binary": "traefik", "version": "3.1.4", 
         "url": "https://github.com/traefik/traefik/releases/download/v{VERSION}/traefik_{VERSION}_linux_amd64.tar.gz",
         "health": "/ping", "ports": "80 443 8080", "vendor": "Traefik Labs"},
        {"name": "nginx", "base": "scratch", "binary": "nginx", "version": "1.27.1",
         "url": "https://nginx.org/download/nginx-{VERSION}.tar.gz",
         "health": "/health_status.html", "ports": "80 443", "vendor": "Nginx Inc"},
        {"name": "caddy", "base": "scratch", "binary": "caddy", "version": "2.7.6",
         "url": "https://github.com/caddyserver/caddy/releases/download/v{VERSION}/caddy_{VERSION}_linux_amd64.tar.gz",
         "health": "/health", "ports": "80 443 2019", "vendor": "Caddy"},
        {"name": "haproxy", "base": "scratch", "binary": "haproxy", "version": "3.0.1",
         "url": "https://www.haproxy.org/download/{VERSION}/src/haproxy-{VERSION}.tar.gz",
         "health": "stat", "ports": "80 443", "vendor": "HAProxy"},
        {"name": "envoy", "base": "scratch", "binary": "envoy", "version": "1.31.0",
         "url": "https://envoy.io/",  # Requires special download
         "health": "/ready", "ports": "80 443 9900", "vendor": "Envoy"},
        {"name": "apache", "base": "scratch", "binary": "httpd", "version": "2.4.61",
         "url": "https://httpd.apache.org/", 
         "health": "/", "ports": "80 443", "vendor": "Apache"},
        {"name": "coredns", "base": "scratch", "binary": "coredns", "version": "1.12.0",
         "url": "https://github.com/coredns/coredns/releases/download/v{VERSION}/coredns_{VERSION}_linux_amd64.tgz",
         "health": "/health", "ports": "53", "vendor": "Coredns"},
        {"name": "unbound", "base": "scratch", "binary": "unbound", "version": "1.20.0",
         "url": "https://unbound.net/",
         "health": "-", "ports": "53", "vendor": "NLnet Labs"},
        {"name": "bind", "base": "scratch", "binary": "named", "version": "9.18.0",
         "url": "https://www.isc.org/bind/",
         "health": "-", "ports": "53 953", "vendor": "ISC"},
    ],
    # Category 2: Databases (Alpine/Dynamic) - ~50 images
    "databases": [
        {"name": "postgres", "base": "alpine", "binary": "postgres", "version": "17.4",
         "packages": "postgresql17 postgresql17-client openssl ca-certificates",
         "health": "pg_isready -U postgres", "ports": "5432", "user": "postgres", "vendor": "PostgreSQL"},
        {"name": "mysql", "base": "alpine", "binary": "mariadbd", "version": "11.4",
         "packages": "mariadb mariadb-client mariadb-backup", 
         "health": "mariadb-admin ping", "ports": "3306", "user": "mysql", "vendor": "MariaDB"},
        {"name": "mariadb", "base": "alpine", "binary": "mariadbd", "version": "11.4",
         "packages": "mariadb mariadb-client", 
         "health": "mariadb-admin ping", "ports": "3306", "user": "mysql", "vendor": "MariaDB"},
        {"name": "postgresql", "base": "alpine", "binary": "postgres", "version": "17.4",
         "packages": "postgresql17 postgresql17-client", 
         "health": "pg_isready", "ports": "5432", "user": "postgres", "vendor": "PostgreSQL"},
        {"name": "sqlite", "base": "alpine", "binary": "sqlite3", "version": "3.45.0",
         "packages": "sqlite", "health": "sqlite3 --version", "ports": "", "user": "sqlite", "vendor": "SQLite"},
        {"name": "cockroachdb", "base": "alpine", "binary": "cockroach", "version": "23.2.0",
         "packages": "cockroach", "health": "cockroach sql", "ports": "26257 8080", "user": "cockroach", "vendor": "CockroachDB"},
    ],
    # Category 3: Key-Value Stores - ~30 images
    "keyvalue": [
        {"name": "redis", "base": "alpine", "binary": "redis-server", "version": "7.4.1",
         "packages": "redis", "health": "redis-cli ping", "ports": "6379", "user": "redis", "vendor": "Redis"},
        {"name": "redis7", "base": "alpine", "binary": "redis-server", "version": "7.4.1",
         "packages": "redis", "health": "redis-cli ping", "ports": "6379", "user": "redis", "vendor": "Redis"},
        {"name": "memcached", "base": "alpine", "binary": "memcached", "version": "1.6.26",
         "packages": "memcached", "health": "stats", "ports": "11211", "user": "memcached", "vendor": "Memcached"},
        {"name": "etcd", "base": "alpine", "binary": "etcd", "version": "3.5.15",
         "packages": "etcd", "health": "etcdctl endpoint-health", "ports": "2379 2380", "user": "etcd", "vendor": "etcd"},
        {"name": "consul", "base": "alpine", "binary": "consul", "version": "1.18.1",
         "packages": "consul", "health": "consul members", "ports": "8500", "user": "consul", "vendor": "HashiCorp"},
        {"name": "dragonfly", "base": "alpine", "binary": "dragonfly", "version": "1.21.0",
         "packages": "dragonfly", "health": "ADMIN ping", "ports": "6379 8000", "user": "dragonfly", "vendor": "DragonflyDB"},
    ],
    # Category 4: Security - ~40 images
    "security": [
        {"name": "vault", "base": "scratch", "binary": "vault", "version": "1.18.1",
         "url": "https://releases.hashicorp.com/vault/{VERSION}/vault_{VERSION}_linux_amd64.zip",
         "health": "/v1/sys/health", "ports": "8200 8201", "vendor": "HashiCorp"},
        {"name": "vaultwarden", "base": "alpine", "binary": "vaultwarden", "version": "2026.4.1",
         "packages": "vaultwarden", "health": "/alive", "ports": "80", "user": "vaultwarden", "vendor": "Vaultwarden"},
        {"name": "hashicorp-vault", "base": "scratch", "binary": "vault", "version": "1.18.1",
         "url": "https://releases.hashicorp.com/vault/{VERSION}/vault_{VERSION}_linux_amd64.zip",
         "health": "/v1/sys/health", "ports": "8200 8201", "vendor": "HashiCorp"},
        {"name": "step-cli", "base": "scratch", "binary": "step", "version": "0.25.2",
         "url": "https://github.com/smallstep/cli/releases/download/v{VERSION}/step_{_VERSION}_linux_amd64.tar.gz",
         "health": "step version", "ports": "", "vendor": "Smallstep"},
        {"name": "trivy", "base": "scratch", "binary": "trivy", "version": "0.53.0",
         "url": "https://github.com/aquasecurity/trivy/releases/download/v{VERSION}/trivy_{VERSION}_linux_amd64.tar.gz",
         "health": "trivy --version", "ports": "", "vendor": "Aqua Security"},
        {"name": "cosign", "base": "scratch", "binary": "cosign", "version": "2.4.0",
         "url": "https://github.com/sigstore/cosign/releases/download/v{VERSION}/cosign_{VERSION}_linux_amd64",
         "health": "cosign version", "ports": "", "vendor": "Sigstore"},
        {"name": "syft", "base": "scratch", "binary": "syft", "version": "1.8.0",
         "url": "https://github.com/anchore/syft/releases/download/v{VERSION}/syft_{VERSION}_linux_amd64.tar.gz",
         "health": "syft version", "ports": "", "vendor": "Anchore"},
        {"name": "grype", "base": "scratch", "binary": "grype", "version": "0.80.0",
         "url": "https://github.com/anchore/grype/releases/download/v{VERSION}/grype_{VERSION}_linux_amd64.tar.gz",
         "health": "grype version", "ports": "", "vendor": "Anchore"},
    ],
    # Category 5: Observability - ~50 images  
    "observability": [
        {"name": "prometheus", "base": "alpine", "binary": "prometheus", "version": "2.53.0",
         "packages": "prometheus", "health": "/-/healthy", "ports": "9090", "user": "prometheus", "vendor": "Prometheus"},
        {"name": "loki", "base": "alpine", "binary": "loki", "version": "3.1.0",
         "packages": "loki", "health": "/ready", "ports": "3100", "user": "loki", "vendor": "Grafana"},
        {"name": "grafana", "base": "alpine", "binary": "grafana", "version": "11.0.0",
         "packages": "grafana", "health": "/api/health", "ports": "3000", "user": "grafana", "vendor": "Grafana"},
        {"name": "thanos", "base": "alpine", "binary": "thanos", "version": "0.35.0",
         "packages": "thanos", "health": "/-/healthy", "ports": "10902", "user": "thanos", "vendor": "Thanos"},
        {"name": "victoriametrics", "base": "alpine", "binary": "victoria-metrics", "version": "1.103.0",
         "packages": "victoria-metrics", "health": "/health", "ports": "8428", "user": "victoria", "vendor": "VictoriaMetrics"},
        {"name": "node-exporter", "base": "alpine", "binary": "node_exporter", "version": "1.8.0",
         "packages": "node_exporter", "health": "/metrics", "ports": "9100", "user": "node-exporter", "vendor": "Prometheus"},
        {"name": "cadvisor", "base": "alpine", "binary": "cadvisor", "version": "0.49.0",
         "packages": "cadvisor", "health": "/healthz", "ports": "8080", "user": "cadv", "vendor": "Google"},
    ],
    # Category 6: Identity & Auth - ~30 images
    "identity": [
        {"name": "keycloak", "base": "ubi-minimal", "binary": "keycloak", "version": "26.0.5",
         "base_url": "quay.io/keycloak/keycloak", "health": "/health/ready", "ports": "8080 8443", "user": "keycloak", "vendor": "Keycloak"},
        {"name": "openldap", "base": "alpine", "binary": "slapd", "version": "2.6.8",
         "packages": "openldap", "health": "ldapsearch", "ports": "389 636", "user": "ldap", "vendor": "OpenLDAP"},
        {"name": "ldap", "base": "alpine", "binary": "slapd", "version": "2.6.8",
         "packages": "openldap", "health": "ldapsearch", "ports": "389 636", "user": "ldap", "vendor": "OpenLDAP"},
        {"name": "zitadel", "base": "alpine", "binary": "zitadel", "version": "2.45.0",
         "packages": "zitadel", "health": "/health", "ports": "8080", "user": "zitadel", "vendor": "Zitadel"},
    ],
    # Category 7: DevOps & CI/CD - ~50 images
    "devops": [
        {"name": "jenkins", "base": "alpine", "binary": "jenkins", "version": "2.462",
         "packages": "jenkins", "health": "/api/json", "ports": "8080", "user": "jenkins", "vendor": "Jenkins"},
        {"name": "drone", "base": "alpine", "binary": "drone", "version": "2.16.0",
         "packages": "drone", "health": "/healthz", "ports": "80", "user": "drone", "vendor": "Drone"},
        {"name": "argocd", "base": "alpine", "binary": "argocd", "version": "2.13.0",
         "packages": "argocd", "health": "/healthz", "ports": "8080", "user": "argocd", "vendor": "ArgoCD"},
        {"name": "tekton", "base": "alpine", "binary": "tekton", "version": "0.61.0",
         "packages": "tekton", "health": "/health", "ports": "8080", "user": "tekton", "vendor": "Tekton"},
        {"name": "flux", "base": "alpine", "binary": "flux", "version": "2.3.0",
         "packages": "flux", "health": "/./", "ports": "3030", "user": "flux", "vendor": "Flux"},
    ],
    # Category 8: Messaging & Queue - ~30 images
    "messaging": [
        {"name": "rabbitmq", "base": "alpine", "binary": "rabbitmq-server", "version": "3.13.0",
         "packages": "rabbitmq", "health": "rabbitmq-diagnostics ping", "ports": "5672 15672", "user": "rabbitmq", "vendor": "RabbitMQ"},
        {"name": "mqtt", "base": "alpine", "binary": "mosquitto", "version": "2.0.18",
         "packages": "mosquitto", "health": "mosquitto_sub", "ports": "1883 9001", "user": "mosquitto", "vendor": "Eclipse"},
        {"name": "nats", "base": "alpine", "binary": "nats-server", "version": "2.10.0",
         "packages": "nats", "health": "nats-server -v", "ports": "4222 8222", "user": "nats", "vendor": "NATS"},
        {"name": "activemq", "base": "alpine", "binary": "activemq", "version": "6.1.0",
         "packages": "activemq", "health": "activemq status", "ports": "61616 8161", "user": "activemq", "vendor": "Apache"},
    ],
    # Category 9: File & Storage - ~30 images
    "storage": [
        {"name": "minio", "base": "alpine", "binary": "minio", "version": "2024.5.28",
         "packages": "minio", "health": "/minio/health/live", "ports": "9000 9001", "user": "minio", "vendor": "MinIO"},
        {"name": "s3", "base": "alpine", "binary": "minio", "version": "2024.5.28",
         "packages": "minio", "health": "/minio/health/live", "ports": "9000 9001", "user": "minio", "vendor": "MinIO"},
        {"name": "restic", "base": "scratch", "binary": "restic", "version": "0.17.0",
         "url": "https://github.com/restic/restic/releases/download/v{VERSION}/restic_{VERSION}_linux_amd64.tar.gz",
         "health": "restic version", "ports": "", "vendor": "Restic"},
        {"name": "rclone", "base": "scratch", "binary": "rclone", "version": "1.67.0",
         "url": "https://github.com/rclone/rclone/releases/download/v{VERSION}/rclone_{VERSION}_linux_amd64.zip",
         "health": "rclone version", "ports": "", "vendor": "Rclone"},
    ],
    # Category 10: Git & Collaboration - ~20 images  
    "collaboration": [
        {"name": "gitea", "base": "alpine", "binary": "gitea", "version": "1.21.0",
         "packages": "gitea", "health": "/api/health", "ports": "3000 22", "user": "git", "vendor": "Gitea"},
        {"name": "forgejo", "base": "alpine", "binary": "forgejo", "version": "1.0.0",
         "packages": "forgejo", "health": "/api/health", "ports": "3000 22", "user": "git", "vendor": "Forgejo"},
        {"name": "gitlab", "base": "alpine", "binary": "gitlab-ce", "version": "16.12.0",
         "packages": "gitlab-ce", "health": "/api/v4/health", "ports": "80 22 443", "user": "git", "vendor": "GitLab"},
    ],
}

# Static gateway Dockerfile template
STATIC_TEMPLATE = '''# =============================================================================
# SOVEREIGN HARDENED {name_upper}
# Generated from template - Version: {version}
# =============================================================================

ARG VERSION={version}
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "{binary_url}" -o /{binary}.tar.gz && \\
    tar -xzf /{binary}.tar.gz -C / && rm /{binary}.tar.gz && chmod +x /{binary}

FROM scratch
COPY --from=downloader /{binary} /{binary}
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app /var/log/{binary} /var/cache/{binary}
USER 65534:65534
WORKDIR /app
EXPOSE {ports}
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD wget -q --spider http://localhost:{health_port}/{health} || exit 1
ENTRYPOINT ["/{binary}"]
LABEL org.opencontainers.image.title="{name}" \\
      org.opencontainers.image.version="{version}" \\
      org.opencontainers.image.vendor="{vendor}" \\
      sovereign.image.tier="1" \\
      sovereign.constraint.nonroot="true" \\
      sovereign.constraint.static="true"
'''

# Alpine/Dynamic Dockerfile template  
ALPINE_TEMPLATE = '''# =============================================================================
# SOVEREIGN HARDENED {name_upper}
# Generated from template - Version: {version}
# =============================================================================

ARG VERSION={version}
ARG BUILD_DATE

FROM {base}:{version}-alpine
RUN apk add --no-cache {packages} ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
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
      sovereign.constraint.nonroot="true"
'''

def generate_static_image(img_def, output_dir):
    """Generate Dockerfile for static binary images"""
    name = img_def["name"]
    version = img_def.get("version", "latest")
    binary = img_def["binary"]
    
    # Handle URL with version placeholder
    url = img_def.get("url", "")
    if url and "{VERSION}" in url:
        url = url.replace("{VERSION}", version)
    
    vendor = img_def.get("vendor", "Official")
    
    # Determine health port - handle empty ports
    ports = img_def.get("ports", "")
    health_port = img_def.get("health_port", ports.split()[0]) if ports else "8080"
    health = img_def.get("health", "health")
    
    content = STATIC_TEMPLATE.format(
        name_upper=name.upper(),
        name=name,
        version=version,
        binary=binary,
        binary_url=url,
        vendor=vendor,
        ports=img_def["ports"],
        health=health,
        health_port=health_port,
    )
    
    filepath = os.path.join(output_dir, f"{name}/Dockerfile")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Generated: {filepath}")

def generate_alpine_image(img_def, output_dir):
    """Generate Dockerfile for Alpine/dynamic images"""
    name = img_def["name"]
    version = img_def.get("version", "latest")
    packages = img_def.get("packages", name)
    vendor = img_def.get("vendor", "Official")
    binary = img_def.get("binary", name)
    user = img_def.get("user", name)
    
    content = ALPINE_TEMPLATE.format(
        name_upper=name.upper(),
        name=name,
        version=version,
        base=img_def.get("base", "alpine"),
        packages=packages,
        vendor=vendor,
        binary=binary,
        ports=img_def["ports"],
        health=img_def.get("health", f"{binary} --version"),
        user=user,
    )
    
    filepath = os.path.join(output_dir, f"{name}/Dockerfile")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Generated: {filepath}")

def generate_all(category=None):
    """Generate all Dockerfiles"""
    output_dir = "images"
    
    categories = IMAGES.keys() if category is None or category == "all" else [category]
    
    total = 0
    for cat in categories:
        if cat not in IMAGES:
            print(f"Unknown category: {cat}")
            continue
            
        for img_def in IMAGES[cat]:
            base = img_def.get("base", "alpine")
            if base == "scratch":
                generate_static_image(img_def, output_dir)
            else:
                generate_alpine_image(img_def, output_dir)
            total += 1
    
    print(f"\nGenerated {total} Dockerfiles")

if __name__ == "__main__":
    category = sys.argv[1] if len(sys.argv) > 1 else "all"
    generate_all(category)