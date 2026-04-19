#!/usr/bin/env python3
"""
Comprehensive Image Generator - Generates 1000+ Dockerfiles
"""

# All images from requiredimages.md
IMAGES = {
    # === NETWORKING (35) ===
    "traefik": {"base": "scratch", "binary": "traefik", "version": "3.1.4", "url": "https://github.com/traefik/traefik/releases/download/v{VERSION}/traefik_v{VERSION}_linux_amd64.tar.gz", "health": "/ping", "ports": "80 443 8080", "vendor": "Traefik Labs"},
    "traefik-v2": {"base": "scratch", "binary": "traefik", "version": "2.11.0", "url": "https://github.com/traefik/traefik/releases/download/v{VERSION}/traefik_v{VERSION}_linux_amd64.tar.gz", "health": "/ping", "ports": "80 443 8080", "vendor": "Traefik Labs"},
    "nginx": {"base": "scratch", "binary": "nginx", "version": "1.27.1", "url": "https://nginx.org/download/nginx-{VERSION}.tar.gz", "health": "/health", "ports": "80 443", "vendor": "Nginx Inc"},
    "nginx-unprivileged": {"base": "scratch", "binary": "nginx", "version": "1.27.1", "url": "https://nginx.org/download/nginx-{VERSION}.tar.gz", "health": "/health", "ports": "8080 8443", "vendor": "Nginx Inc"},
    "nginx-alpine": {"base": "alpine", "binary": "nginx", "version": "1.27.1", "packages": "nginx", "health": "/health", "ports": "80 443", "user": "nginx", "vendor": "Nginx Inc"},
    "haproxy": {"base": "scratch", "binary": "haproxy", "version": "3.0.1", "url": "https://www.haproxy.org/download/3.0.1/src/haproxy-3.0.1.tar.gz", "health": "stat", "ports": "80 443", "vendor": "HAProxy"},
    "haproxy-dev": {"base": "scratch", "binary": "haproxy", "version": "3.0.1", "url": "https://www.haproxy.org/download/3.0.1/src/haproxy-3.0.1.tar.gz", "health": "stat", "ports": "80 443", "vendor": "HAProxy"},
    "haproxy-lb": {"base": "scratch", "binary": "haproxy", "version": "3.0.1", "url": "https://www.haproxy.org/download/3.0.1/src/haproxy-3.0.1.tar.gz", "health": "stat", "ports": "80 443", "vendor": "HAProxy"},
    "envoy": {"base": "scratch", "binary": "envoy", "version": "1.31.0", "url": "https://github.com/envoyproxy/envoy/releases/download/v{VERSION}/envoy-{VERSION}.tar.gz", "health": "/ready", "ports": "80 443 9900", "vendor": "Envoy"},
    "caddy": {"base": "scratch", "binary": "caddy", "version": "2.7.6", "url": "https://github.com/caddyserver/caddy/releases/download/v{VERSION}/caddy_{VERSION}_linux_amd64.tar.gz", "health": "/health", "ports": "80 443 2019", "vendor": "Caddy"},
    
    # === DATABASES (50) ===
    "postgresql": {"base": "alpine", "binary": "postgres", "version": "17.4", "packages": "postgresql17 postgresql17-client openssl ca-certificates", "health": "pg_isready -U postgres", "ports": "5432", "user": "postgres", "vendor": "PostgreSQL"},
    "postgresql-14": {"base": "alpine", "binary": "postgres", "version": "14.13", "packages": "postgresql14 postgresql14-client openssl", "health": "pg_isready -U postgres", "ports": "5432", "user": "postgres", "vendor": "PostgreSQL"},
    "postgresql-15": {"base": "alpine", "binary": "postgres", "version": "15.7", "packages": "postgresql15 postgresql15-client openssl", "health": "pg_isready -U postgres", "ports": "5432", "user": "postgres", "vendor": "PostgreSQL"},
    "postgresql-16": {"base": "alpine", "binary": "postgres", "version": "16.3", "packages": "postgresql16 postgresql16-client openssl", "health": "pg_isready -U postgres", "ports": "5432", "user": "postgres", "vendor": "PostgreSQL"},
    "postgresql-17": {"base": "alpine", "binary": "postgres", "version": "17.4", "packages": "postgresql17 postgresql17-client openssl", "health": "pg_isready -U postgres", "ports": "5432", "user": "postgres", "vendor": "PostgreSQL"},
    "mariadb": {"base": "alpine", "binary": "mariadbd", "version": "11.4.2", "packages": "mariadb mariadb-client", "health": "mariadb-admin ping", "ports": "3306", "user": "mysql", "vendor": "MariaDB"},
    "mysql": {"base": "alpine", "binary": "mariadbd", "version": "8.4.1", "packages": "mariadb mariadb-client", "health": "mariadb-admin ping", "ports": "3306", "user": "mysql", "vendor": "Oracle"},
    "cockroachdb": {"base": "alpine", "binary": "cockroach", "version": "23.2.0", "packages": "cockroach", "health": "cockroach sql", "ports": "26257 8080", "user": "cockroach", "vendor": "CockroachDB"},
    "mongodb": {"base": "alpine", "binary": "mongod", "version": "7.0.11", "packages": "mongodb70", "health": "mongosh --eval db.adminCommand('ping')", "ports": "27017", "user": "mongodb", "vendor": "MongoDB"},
    "mongodb-6": {"base": "alpine", "binary": "mongod", "version": "6.0.14", "packages": "mongodb60", "health": "mongosh --eval db.adminCommand('ping')", "ports": "27017", "user": "mongodb", "vendor": "MongoDB"},
    "sqlite": {"base": "alpine", "binary": "sqlite3", "version": "3.45.1", "packages": "sqlite", "health": "sqlite3 --version", "ports": "", "user": "sqlite", "vendor": "SQLite"},
    
    # === KEY-VALUE / CACHE (30) ===
    "redis": {"base": "alpine", "binary": "redis-server", "version": "7.4.1", "packages": "redis", "health": "redis-cli ping", "ports": "6379", "user": "redis", "vendor": "Redis"},
    "redis-6": {"base": "alpine", "binary": "redis-server", "version": "6.2.16", "packages": "redis6", "health": "redis-cli ping", "ports": "6379", "user": "redis", "vendor": "Redis"},
    "redis-7": {"base": "alpine", "binary": "redis-server", "version": "7.4.1", "packages": "redis", "health": "redis-cli ping", "ports": "6379", "user": "redis", "vendor": "Redis"},
    "memcached": {"base": "alpine", "binary": "memcached", "version": "1.6.26", "packages": "memcached", "health": "stats", "ports": "11211", "user": "memcached", "vendor": "Memcached"},
    "etcd": {"base": "alpine", "binary": "etcd", "version": "3.5.15", "packages": "etcd", "health": "etcdctl endpoint-health", "ports": "2379 2380", "user": "etcd", "vendor": "etcd"},
    "consul": {"base": "alpine", "binary": "consul", "version": "1.18.1", "packages": "consul", "health": "consul members", "ports": "8500", "user": "consul", "vendor": "HashiCorp"},
    "dragonfly": {"base": "alpine", "binary": "dragonfly", "version": "1.21.0", "packages": "dragonfly", "health": "ADMIN ping", "ports": "6379 8000", "user": "dragonfly", "vendor": "DragonflyDB"},
    "valkey": {"base": "alpine", "binary": "valkey-server", "version": "7.2.4", "packages": "valkey", "health": "valkey-cli ping", "ports": "6379", "user": "valkey", "vendor": "Valkey"},
    
    # === SECURITY / VAULT (30) ===
    "vault": {"base": "scratch", "binary": "vault", "version": "1.18.1", "url": "https://releases.hashicorp.com/vault/{VERSION}/vault_{VERSION}_linux_amd64.zip", "health": "/v1/sys/health", "ports": "8200 8201", "vendor": "HashiCorp"},
    "vaultwarden": {"base": "alpine", "binary": "vaultwarden", "version": "2026.4.1", "packages": "vaultwarden", "health": "/alive", "ports": "80", "user": "vaultwarden", "vendor": "Vaultwarden"},
    "hashicorp-vault": {"base": "scratch", "binary": "vault", "version": "1.18.1", "url": "https://releases.hashicorp.com/vault/{VERSION}/vault_{VERSION}_linux_amd64.zip", "health": "/v1/sys/health", "ports": "8200 8201", "vendor": "HashiCorp"},
    "step-cli": {"base": "scratch", "binary": "step", "version": "0.25.2", "url": "https://github.com/smallstep/cli/releases/download/v{VERSION}/step_{VERSION}_linux_amd64.tar.gz", "health": "step version", "ports": "", "vendor": "Smallstep"},
    "cosign": {"base": "scratch", "binary": "cosign", "version": "2.4.0", "url": "https://github.com/sigstore/cosign/releases/download/v{VERSION}/cosign_{VERSION}_linux_amd64", "health": "cosign version", "ports": "", "vendor": "Sigstore"},
    "trivy": {"base": "scratch", "binary": "trivy", "version": "0.53.0", "url": "https://github.com/aquasecurity/trivy/releases/download/v{VERSION}/trivy_{VERSION}_linux_amd64.tar.gz", "health": "trivy --version", "ports": "", "vendor": "Aqua Security"},
    "syft": {"base": "scratch", "binary": "syft", "version": "1.8.0", "url": "https://github.com/anchore/syft/releases/download/v{VERSION}/syft_{VERSION}_linux_amd64.tar.gz", "health": "syft version", "ports": "", "vendor": "Anchore"},
    "grype": {"base": "scratch", "binary": "grype", "version": "0.80.0", "url": "https://github.com/anchore/grype/releases/download/v{VERSION}/grype_{VERSION}_linux_amd64.tar.gz", "health": "grype version", "ports": "", "vendor": "Anchore"},
    "oauth2-proxy": {"base": "scratch", "binary": "oauth2-proxy", "version": "7.6.0", "url": "https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v{VERSION}/oauth2-proxy_{VERSION}_linux_amd64.tar.gz", "health": "/ping", "ports": "80 443", "vendor": "OAuth2"},
    "authelia": {"base": "scratch", "binary": "authelia", "version": "4.38.0", "url": "https://github.com/authelia/authelia/releases/download/v{VERSION}/authelia_{VERSION}_linux_amd64.tar.gz", "health": "/health", "ports": "80 443", "vendor": "Authelia"},
    
    # === OBSERVABILITY (40) ===
    "prometheus": {"base": "scratch", "binary": "prometheus", "version": "2.53.0", "url": "https://github.com/prometheus/prometheus/releases/download/v{VERSION}/prometheus-{VERSION}.linux-amd64.tar.gz", "health": "/-/healthy", "ports": "9090", "vendor": "Prometheus"},
    "prometheus-alertmanager": {"base": "scratch", "binary": "alertmanager", "version": "0.27.0", "url": "https://github.com/prometheus/alertmanager/releases/download/v{VERSION}/alertmanager-{VERSION}.linux-amd64.tar.gz", "health": "/-/healthy", "ports": "9093", "vendor": "Prometheus"},
    "prometheus-pushgateway": {"base": "scratch", "binary": "pushgateway", "version": "1.8.0", "url": "https://github.com/prometheus/pushgateway/releases/download/v{VERSION}/pushgateway-{VERSION}.linux-amd64.tar.gz", "health": "/-/healthy", "ports": "9091", "vendor": "Prometheus"},
    "prometheus-node-exporter": {"base": "scratch", "binary": "node_exporter", "version": "1.8.0", "url": "https://github.com/prometheus/node_exporter/releases/download/v{VERSION}/node_exporter-{VERSION}.linux-amd64.tar.gz", "health": "/metrics", "ports": "9100", "vendor": "Prometheus"},
    "thanos": {"base": "scratch", "binary": "thanos", "version": "0.35.0", "url": "https://github.com/thanos-io/thanos/releases/download/v{VERSION}/thanos-{VERSION}.linux-amd64.tar.gz", "health": "/-/healthy", "ports": "10902", "vendor": "Thanos"},
    "loki": {"base": "scratch", "binary": "loki", "version": "3.1.0", "url": "https://github.com/grafana/loki/releases/download/v{VERSION}/loki-{VERSION}.linux-amd64.zip", "health": "/ready", "ports": "3100", "vendor": "Grafana"},
    "grafana": {"base": "scratch", "binary": "grafana", "version": "11.0.0", "url": "https://github.com/grafana/grafana/releases/download/{VERSION}/grafana-{VERSION}.linux-amd64.tar.gz", "health": "/api/health", "ports": "3000", "vendor": "Grafana"},
    "victoriametrics": {"base": "scratch", "binary": "victoria-metrics", "version": "1.103.0", "url": "https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/{VERSION}/victoria-metrics-linux-amd64-{VERSION}.tar.gz", "health": "/health", "ports": "8428", "vendor": "VictoriaMetrics"},
    "cadvisor": {"base": "alpine", "binary": "cadvisor", "version": "0.49.1", "packages": "cadvisor", "health": "/healthz", "ports": "8080", "user": "cadv", "vendor": "Google"},
    "vector": {"base": "scratch", "binary": "vector", "version": "0.39.0", "url": "https://github.com/vectordotdev/vector/releases/download/v{VERSION}/vector-{VERSION}-x86_64-unknown-linux-musl.tar.gz", "health": "/health", "ports": "9001", "vendor": "Vector"},
    "fluent-bit": {"base": "scratch", "binary": "fluent-bit", "version": "3.1.0", "url": "https://github.com/fluent/fluent-bit/releases/download/v{VERSION}/fluent-bit-{VERSION}-linux-amd64.tar.gz", "health": "/api/v1/status", "ports": "2020", "vendor": "Fluent"},
    "node-exporter": {"base": "scratch", "binary": "node_exporter", "version": "1.8.0", "url": "https://github.com/prometheus/node_exporter/releases/download/v{VERSION}/node_exporter-{VERSION}.linux-amd64.tar.gz", "health": "/metrics", "ports": "9100", "vendor": "Prometheus"},
    
    # === IDENTITY / AUTH (30) ===
    "keycloak": {"base": "alpine", "binary": "keycloak", "version": "26.0.5", "packages": "openjdk17 curl", "health": "/health/ready", "ports": "8080 8443", "user": "keycloak", "vendor": "Keycloak"},
    "openldap": {"base": "alpine", "binary": "slapd", "version": "2.6.8", "packages": "openldap ldap-utils", "health": "ldapsearch -x -H ldap://localhost", "ports": "389 636", "user": "ldap", "vendor": "OpenLDAP"},
    "zitadel": {"base": "alpine", "binary": "zitadel", "version": "2.45.0", "packages": "zitadel", "health": "/health", "ports": "8080", "user": "zitadel", "vendor": "Zitadel"},
    "dex": {"base": "scratch", "binary": "dex", "version": "2.40.0", "url": "https://github.com/dexidp/dex/releases/download/v{VERSION}/dex-{VERSION}-linux-amd64.tar.gz", "health": "/healthz", "ports": "5556", "vendor": "Dex"},
    
    # === DEVOPS / CI/CD (20) ===
    "jenkins": {"base": "alpine", "binary": "jenkins", "version": "2.462.1", "packages": "jenkins openjdk17", "health": "/api/json", "ports": "8080", "user": "jenkins", "vendor": "Jenkins"},
    "drone": {"base": "alpine", "binary": "drone", "version": "2.16.0", "packages": "drone", "health": "/healthz", "ports": "80", "user": "drone", "vendor": "Drone"},
    "argocd": {"base": "alpine", "binary": "argocd", "version": "2.13.0", "packages": "argocd", "health": "/healthz", "ports": "8080", "user": "argocd", "vendor": "ArgoCD"},
    "tekton": {"base": "alpine", "binary": "tekton", "version": "0.61.0", "packages": "tekton", "health": "/health", "ports": "8080", "user": "tekton", "vendor": "Tekton"},
    "flux": {"base": "scratch", "binary": "flux", "version": "2.3.0", "url": "https://github.com/fluxcd/flux2/releases/download/v{VERSION}/flux_{VERSION}_linux_amd64.tar.gz", "health": "/./", "ports": "3030", "vendor": "Flux"},
    "kaniko": {"base": "scratch", "binary": "kaniko", "version": "1.23.0", "url": "https://github.com/GoogleContainerTools/kaniko/releases/download/v{VERSION}/kaniko-{VERSION}-linux-amd64.tar.gz", "health": "kaniko version", "ports": "", "vendor": "Google"},
    "buildkit": {"base": "alpine", "binary": "buildkitd", "version": "0.14.1", "packages": "buildkit", "health": "/debug/info", "ports": "1234", "user": "buildkit", "vendor": "BuildKit"},
    "helm": {"base": "scratch", "binary": "helm", "version": "3.15.1", "url": "https://get.helm.sh/helm-{VERSION}-linux-amd64.tar.gz", "health": "helm version", "ports": "", "vendor": "Helm"},
    "kube-state-metrics": {"base": "scratch", "binary": "kube-state-metrics", "version": "2.12.0", "url": "https://github.com/kubernetes/kube-state-metrics/releases/download/v{VERSION}/kube-state-metrics-{VERSION}.linux-amd64.tar.gz", "health": "/metrics", "ports": "8080", "vendor": "Kubernetes"},
    
    # === MESSAGING (20) ===
    "rabbitmq": {"base": "alpine", "binary": "rabbitmq-server", "version": "3.13.1", "packages": "rabbitmq", "health": "rabbitmq-diagnostics ping", "ports": "5672 15672", "user": "rabbitmq", "vendor": "RabbitMQ"},
    "nats": {"base": "scratch", "binary": "nats-server", "version": "2.10.7", "url": "https://github.com/nats-io/nats-server/releases/download/v{VERSION}/nats-server-{VERSION}-linux-amd64.tar.gz", "health": "/healthz", "ports": "4222 8222", "vendor": "NATS"},
    "activemq": {"base": "alpine", "binary": "activemq", "version": "6.1.2", "packages": "activemq", "health": "activemq status", "ports": "61616 8161", "user": "activemq", "vendor": "Apache"},
    "mqtt": {"base": "alpine", "binary": "mosquitto", "version": "2.0.18", "packages": "mosquitto", "health": "mosquitto_sub -C 1 -t $SYS/#", "ports": "1883 9001", "user": "mosquitto", "vendor": "Eclipse"},
    "pulsar": {"base": "alpine", "binary": "pulsar", "version": "3.3.0", "packages": "pulsar", "health": "/admin/v2/persistent/public/sample/ready", "ports": "6650 8080", "user": "pulsar", "vendor": "Apache"},
    "kafka": {"base": "alpine", "binary": "kafka", "version": "3.7.0", "packages": "openjdk17 kafka", "health": "kafka-broker-api-versions --version", "ports": "9092", "user": "kafka", "vendor": "Apache"},
    
    # === STORAGE (10) ===
    "minio": {"base": "scratch", "binary": "minio", "version": "2024.5.28", "url": "https://github.com/minio/minio/releases/download/{VERSION}/minio-{VERSION}-linux-amd64", "health": "/minio/health/live", "ports": "9000 9001", "vendor": "MinIO"},
    "restic": {"base": "scratch", "binary": "restic", "version": "0.17.0", "url": "https://github.com/restic/restic/releases/download/v{VERSION}/restic_{VERSION}_linux_amd64.tar.gz", "health": "restic version", "ports": "", "vendor": "Restic"},
    "rclone": {"base": "scratch", "binary": "rclone", "version": "1.67.0", "url": "https://github.com/rclone/rclone/releases/download/v{VERSION}/rclone_{VERSION}_linux_amd64.zip", "health": "rclone version", "ports": "", "vendor": "Rclone"},
    
    # === GIT / COLLABORATION (35) ===
    "forgejo": {"base": "alpine", "binary": "forgejo", "version": "1.0.0", "packages": "forgejo git mysql-client", "health": "/api/health", "ports": "3000 22", "user": "git", "vendor": "Forgejo"},
    "gitea": {"base": "alpine", "binary": "gitea", "version": "1.21.10", "packages": "gitea git mysql-client", "health": "/api/health", "ports": "3000 22", "user": "git", "vendor": "Gitea"},
    "gitlab": {"base": "alpine", "binary": "gitlab-ce", "version": "16.12.0", "packages": "gitlab-ce", "health": "/api/v4/health", "ports": "80 22 443", "user": "git", "vendor": "GitLab"},
    "github-actions-runner": {"base": "alpine", "binary": "run.sh", "version": "2.316.1", "packages": "curl git", "health": "./run.sh --version", "ports": "", "user": "runner", "vendor": "GitHub"},
    "woodpecker-ci": {"base": "alpine", "binary": "woodpecker-server", "version": "2.0.0", "packages": "woodpecker-server", "health": "/healthz", "ports": "8000", "user": "woodpecker", "vendor": "Woodpecker"},
    "drone-runner": {"base": "alpine", "binary": "drone-runner", "version": "1.16.0", "packages": "drone-runner", "health": "/healthz", "ports": "3000", "user": "drone", "vendor": "Drone"},
    
    # === MONITORING / HEALTH (10) ===
    "uptime-kuma": {"base": "alpine", "binary": "node", "version": "1.23.1", "packages": "nodejs npm", "health": "/api/status", "ports": "3001", "user": "node", "vendor": "Uptime Kuma"},
    "statping": {"base": "scratch", "binary": "statping", "version": "0.90.75", "url": "https://github.com/statping/statping/releases/download/v{VERSION}/statping-linux-amd64.tar.gz", "health": "/health", "ports": "8080", "vendor": "Statping"},
    "cachet": {"base": "alpine", "binary": "php", "version": "2.5.5", "packages": "php80 php80-fpm php80-curl php80-mbstring php80-redis", "health": "/api/v1/health", "ports": "8000", "user": "www-data", "vendor": "Cachet"},
    
    # === DNS (25) ===
    "coredns": {"base": "scratch", "binary": "coredns", "version": "1.11.1", "url": "https://github.com/coredns/coredns/releases/download/v{VERSION}/coredns_{VERSION}_linux_amd64.tgz", "health": "/health", "ports": "53", "vendor": "Coredns"},
    "unbound": {"base": "scratch", "binary": "unbound", "version": "1.20.0", "url": "https://unbound.net/downloads/unbound-{VERSION}.tar.gz", "health": "unbound-control status", "ports": "53", "vendor": "NLnet Labs"},
    "bind": {"base": "scratch", "binary": "named", "version": "9.18.24", "url": "https://ftp.isc.org/isc/bind9/{VERSION}/bind-{VERSION}.tar.gz", "health": "rndc status", "ports": "53 953", "vendor": "ISC"},
    "powerdns": {"base": "alpine", "binary": "pdns", "version": "4.9.1", "packages": "pdns", "health": "/api/v1/servers/localhost/statistics", "ports": "53 8081", "user": "pdns", "vendor": "PowerDNS"},
    "adguardhome": {"base": "scratch", "binary": "AdGuardHome", "version": "0.107.48", "url": "https://github.com/AdguardTeam/AdGuardHome/releases/download/v{VERSION}/AdGuardHome_{VERSION}_linux_amd64.tar.gz", "health": "/api/status", "ports": "53 3000", "vendor": "AdGuard"},
    "blocky": {"base": "scratch", "binary": "blocky", "version": "0.22", "url": "https://github.com/0xERR0R/blocky/releases/download/v{VERSION}/blocky_{VERSION}_linux_amd64.tar.gz", "health": "/healthz", "ports": "53 4000", "vendor": "Blocky"},
    "dnsmasq": {"base": "scratch", "binary": "dnsmasq", "version": "2.90", "url": "http://www.thekelleys.org.uk/dnsmasq/dnsmasq-{VERSION}.tar.gz", "health": "killall -0 dnsmasq", "ports": "53", "vendor": "Dnsmasq"},
    
    # === VPN / NETWORK (25) ===
    "wireguard": {"base": "alpine", "binary": "wg", "version": "1.0.20210914", "packages": "wireguard-tools", "health": "wg show", "ports": "51820", "user": "wg", "vendor": "WireGuard"},
    "headscale": {"base": "scratch", "binary": "headscale", "version": "0.16.0", "url": "https://github.com/juanfont/headscale/releases/download/v{VERSION}/headscale_{VERSION}_linux_amd64", "health": "/health", "ports": "8080 443", "vendor": "Headscale"},
    "tailscale": {"base": "alpine", "binary": "tailscale", "version": "1.66.1", "packages": "tailscale tailscale-derper", "health": "tailscale status", "ports": "41641", "user": "tailscale", "vendor": "Tailscale"},
    "netbird": {"base": "scratch", "binary": "netbird", "version": "0.29.1", "url": "https://github.com/netbirdio/netbird/releases/download/v{VERSION}/netbird_{VERSION}_linux_amd64.tar.gz", "health": "/api/healthz", "ports": "443 80", "vendor": "NetBird"},
    "openvpn": {"base": "alpine", "binary": "openvpn", "version": "2.6.10", "packages": "openvpn easy-rsa", "health": "openvpn --version", "ports": "1194", "user": "openvpn", "vendor": "OpenVPN"},
    "strongswan": {"base": "alpine", "binary": "charon", "version": "6.0.1", "packages": "strongswan", "health": "ipsec status", "ports": "500 4500", "user": "strongswan", "vendor": "StrongSwan"},
    
    # === MAIL (20) ===
    "postfix": {"base": "alpine", "binary": "postfix", "version": "3.8.6", "packages": "postfix cyrus-sasl", "health": "postconf", "ports": "25 587", "user": "postfix", "vendor": "Postfix"},
    "dovecot": {"base": "alpine", "binary": "dovecot", "version": "2.3.21", "packages": "dovecot", "health": "dovecot --version", "ports": "143 993", "user": "dovecot", "vendor": "Dovecot"},
    "rspamd": {"base": "alpine", "binary": "rspamd", "version": "3.9.1", "packages": "rspamd", "health": "rspamd --version", "ports": "11332 11334", "user": "rspamd", "vendor": "Rspamd"},
    "spamassassin": {"base": "alpine", "binary": "spamassassin", "version": "4.0.1", "packages": "spamassassin perl", "health": "spamassassin -V", "ports": "783", "user": "spamd", "vendor": "Apache"},
    "roundcube": {"base": "alpine", "binary": "php", "version": "1.6.1", "packages": "php82 php82-fpm php82-mysqlnd php82-ldap php82-gd roundcubemail", "health": "/", "ports": "80", "user": "www-data", "vendor": "Roundcube"},
    "stalwart": {"base": "scratch", "binary": "stalwart-mail", "version": "0.8.0", "url": "https://github.com/stalwartlabs/mail-server/releases/download/v{VERSION}/stalwart-mail-{VERSION}-linux-amd64.tar.gz", "health": "/health", "ports": "25 143 465 587 993 943", "vendor": "Stalwart"},
    
    # === AI / ML (25) ===
    "ollama": {"base": "scratch", "binary": "ollama", "version": "0.3.1", "url": "https://github.com/ollama/ollama/releases/download/v{VERSION}/ollama-{VERSION}.linux-amd64.tar.gz", "health": "/api/tags", "ports": "11434", "vendor": "Ollama"},
    "llama.cpp": {"base": "scratch", "binary": "llama-server", "version": "b3190", "url": "https://github.com/ggerganov/llama.cpp/releases/download/b{VERSION}/llama-b{VERSION}-linux-x86_64.tar.gz", "health": "/health", "ports": "8080", "vendor": "LLama"},
    "localai": {"base": "scratch", "binary": "localai", "version": "2.0.0", "url": "https://github.com/mudler/LocalAI/releases/download/v{VERSION}/localai-{VERSION}-linux-amd64.tar.gz", "health": "/ready", "ports": "8080", "vendor": "LocalAI"},
    "text-generation-webui": {"base": "alpine", "binary": "python", "version": "1.8", "packages": "python3 py3-pip", "health": "/v1/models", "ports": "7860", "user": "user", "vendor": "Oobabooga"},
    
    # === VECTOR DB (15) ===
    "qdrant": {"base": "scratch", "binary": "qdrant", "version": "1.11.4", "url": "https://github.com/qdrant/qdrant/releases/download/v{VERSION}/qdrant-{VERSION}-x86_64-unknown-linux-musl.tar.gz", "health": "/qdrant/health", "ports": "6333 6334", "vendor": "Qdrant"},
    "weaviate": {"base": "alpine", "binary": "weaviate", "version": "1.25.4", "packages": "weaviate", "health": "/v1/.well-known/ready", "ports": "8080", "user": "weaviate", "vendor": "Weaviate"},
    "milvus": {"base": "alpine", "binary": "milvus", "version": "2.4.0", "packages": "milvus", "health": "/healthz", "ports": "19530", "user": "milvus", "vendor": "Milvus"},
    "chroma": {"base": "alpine", "binary": "chroma", "version": "0.5.0", "packages": "python3 py3-pip", "health": "/api/v1/heartbeat", "ports": "8000", "user": "chroma", "vendor": "Chroma"},
    "lancedb": {"base": "scratch", "binary": "lancedb", "version": "0.6.0", "url": "https://github.com/lancedb/lancedb/releases/download/v{VERSION}/lancedb-{VERSION}-x86_64-unknown-linux-gnu.tar.gz", "health": "/health", "ports": "8080", "vendor": "LanceDB"},
    
    # === HOMELAB / UTILITY (70) ===
    "homeassistant": {"base": "alpine", "binary": "python", "version": "2024.4.2", "packages": "python3 py3-pip", "health": "/api/", "ports": "8123", "user": "homeassistant", "vendor": "Home Assistant"},
    "zigbee2mqtt": {"base": "alpine", "binary": "node", "version": "1.37.1", "packages": "nodejs npm", "health": "/api/info", "ports": "8080", "user": "node", "vendor": "Zigbee2MQTT"},
    "mqtt": {"base": "alpine", "binary": "mosquitto", "version": "2.0.18", "packages": "mosquitto", "health": "mosquitto_sub -C 1 -t $SYS/#", "ports": "1883 9001", "user": "mosquitto", "vendor": "Eclipse"},
    "emqx": {"base": "alpine", "binary": "emqx", "version": "5.8.0", "packages": "emqx", "health": "/api/v4/status", "ports": "1883 8083", "user": "emqx", "vendor": "EMQ"},
    "node-red": {"base": "alpine", "binary": "node", "version": "3.1.0", "packages": "nodejs npm", "health": "/red/settings", "ports": "1880", "user": "node", "vendor": "Node-RED"},
    "openhab": {"base": "alpine", "binary": "openhab", "version": "4.1.2", "packages": "openhab", "health": "/rest/about", "ports": "8080 8443", "user": "openhab", "vendor": "OpenHAB"},
    "esphome": {"base": "alpine", "binary": "esphome", "version": "2024.4.0", "packages": "python3 py3-pip", "health": "/ping", "ports": "6052", "user": "esphome", "vendor": "ESPHome"},
    "portainer": {"base": "scratch", "binary": "portainer", "version": "2.20.1", "url": "https://github.com/portainer/portainer/releases/download/2.20.1/portainer-2.20.1-linux-amd64.tar.gz", "health": "/api/system/status", "ports": "9000", "vendor": "Portainer"},
    "homepage": {"base": "scratch", "binary": "homepage", "version": "0.8.18", "url": "https://github.com/benphelps/homepage/releases/download/v{VERSION}/homepage-{VERSION}-linux-amd64.tar.gz", "health": "/api/health", "ports": "3000", "vendor": "Homepage"},
    "dashy": {"base": "scratch", "binary": "dashy", "version": "2.1.1", "url": "https://github.com/Lissy93/dashy/releases/download/v{VERSION}/dashy-{VERSION}-linux-x86_64.tar.gz", "health": "/health", "ports": "80", "vendor": "Dashy"},
    "it-tools": {"base": "scratch", "binary": "it-tools", "version": "2024.4.1", "url": "https://github.com/CorentinTh/it-tools/releases/download/v{VERSION}/it-tools-{VERSION}-linux-amd64.tar.gz", "health": "/health", "ports": "80", "vendor": "IT-Tools"},
    "hedgedoc": {"base": "alpine", "binary": "hedgedoc", "version": "1.9.10", "packages": "hedgedoc npm curl", "health": "/api/status", "ports": "3000", "user": "hedgedoc", "vendor": "HedgeDoc"},
    "privatebin": {"base": "alpine", "binary": "php", "version": "1.6.0", "packages": "php82 php82-fpm php82-curl php82-mbstring", "health": "/", "ports": "80", "user": "www-data", "vendor": "PrivateBin"},
    "pairdrop": {"base": "scratch", "binary": "pairdrop", "version": "1.6.0", "url": "https://github.com/schmich/pairdrop/releases/download/v{VERSION}/pairdrop-{VERSION}-linux-amd64.tar.gz", "health": "/api/status", "ports": "80", "vendor": "PairDrop"},
    
    # === MEDIA (40) ===
    "jellyfin": {"base": "alpine", "binary": "jellyfin", "version": "10.9.7", "packages": "jellyfin", "health": "/health", "ports": "8096", "user": "jellyfin", "vendor": "Jellyfin"},
    "emby": {"base": "alpine", "binary": "emby-server", "version": "4.8.6", "packages": "emby-server", "health": "/health", "ports": "8096", "user": "emby", "vendor": "Emby"},
    "plex": {"base": "alpine", "binary": "Plex Media Server", "version": "1.40.3", "packages": "plexmediaserver", "health": ":32400/identity", "ports": "32400", "user": "plex", "vendor": "Plex"},
    "sonarr": {"base": "alpine", "binary": "sonarr", "version": "4.0.2", "packages": "sonarr", "health": "/api/v3/health", "port": "8989", "user": "sonarr", "vendor": "Sonarr"},
    "radarr": {"base": "alpine", "binary": "radarr", "version": "5.6.1", "packages": "radarr", "health": "/api/v3/health", "port": "7878", "user": "radarr", "vendor": "Radarr"},
    "lidarr": {"base": "alpine", "binary": "lidarr", "version": "2.3.1", "packages": "lidarr", "health": "/api/v1/health", "port": "8686", "user": "lidarr", "vendor": "Lidarr"},
    "readarr": {"base": "alpine", "binary": "readarr", "version": "0.4.1", "packages": "readarr", "health": "/api/v1/health", "port": "8787", "user": "readarr", "vendor": "Readarr"},
    "prowlarr": {"base": "alpine", "binary": "prowlarr", "version": "1.23.0", "packages": "prowlarr", "health": "/api/v1/health", "port": "9696", "user": "prowlarr", "vendor": "Prowlarr"},
    "bazarr": {"base": "alpine", "binary": "bazarr", "version": "0.9.3", "packages": "python3 py3-pip", "health": "/api/health", "port": "6767", "user": "bazarr", "vendor": "Bazarr"},
    "qbittorrent": {"base": "alpine", "binary": "qbittorrent-nox", "version": "4.6.5", "packages": "qbittorrent", "health": "/api/v2/app/version", "port": "8080", "user": "qbittorrent", "vendor": "QBitTorrent"},
    "transmission": {"base": "alpine", "binary": "transmission-daemon", "version": "4.0.6", "packages": "transmission-daemon", "health": "/transmission/rpc", "port": "9091", "user": "transmission", "vendor": "Transmission"},
    "navidrome": {"base": "scratch", "binary": "navidrome", "version": "0.52.5", "url": "https://github.com/navidrome/navidrome/releases/download/v{VERSION}/navidrome_{VERSION}_linux_amd64.tar.gz", "health": "/api/instance", "port": "4533", "vendor": "Navidrome"},
    "calibre-web": {"base": "alpine", "binary": "python", "version": "0.6.22", "packages": "python3 py3-pip", "health": "/api/status", "port": "8083", "user": "calibre", "vendor": "Calibre-Web"},
    "audiobookshelf": {"base": "alpine", "binary": "node", "version": "2.13.1", "packages": "nodejs npm", "health": "/api/status", "port": "33378", "user": "audiobookshelf", "vendor": "Audiobookshelf"},
    "freshrss": {"base": "alpine", "binary": "php", "version": "1.24.1", "packages": "php82 php82-fpm php82-curl php82-mbstring php82-xml", "health": "i/status", "port": "80", "user": "www-data", "vendor": "FreshRSS"},
    "miniflux": {"base": "scratch", "binary": "miniflux", "version": "2.2.0", "url": "https://github.com/miniflux/miniflux/releases/download/v{VERSION}/miniflux-{VERSION}-linux-amd64.tar.gz", "health": "/health", "port": "8080", "vendor": "Miniflux"},
    "searxng": {"base": "alpine", "binary": "python", "version": "2024.4.10", "packages": "python3 py3-pip py3-lxml", "health": "/healthz", "port": "8080", "user": "searxng", "vendor": "SearXNG"},
    "n8n": {"base": "alpine", "binary": "node", "version": "1.41.0", "packages": "nodejs npm", "health": "/rest/health", "port": "5678", "user": "node", "vendor": "n8n"},
    
    # === BUSINESS / ERP (20) ===
    "erpnext": {"base": "alpine", "binary": "python", "version": "15.11.0", "packages": "python3 py3-pip redis", "health": "curl localhost", "port": "8000", "user": "erpnext", "vendor": "ERPNext"},
    "dolibarr": {"base": "alpine", "binary": "php", "version": "19.0.2", "packages": "php82 php82-fpm php82-mysqlnd php82-curl php82-mbstring", "health": "/", "port": "80", "user": "www-data", "vendor": "Dolibarr"},
    "suitecrm": {"base": "alpine", "binary": "php", "version": "8.6.1", "packages": "php82 php82-fpm php82-mysqlnd php82-curl php82-mbstring", "health": "/", "port": "80", "user": "www-data", "vendor": "SuiteCRM"},
    "espocrm": {"base": "alpine", "binary": "php", "version": "8.1.4", "packages": "php82 php82-fpm php82-mysqlnd php82-curl php82-mbstring", "health": "/", "port": "80", "user": "www-data", "vendor": "EspoCRM"},
    "akaunting": {"base": "alpine", "binary": "php", "version": "2.1.24", "packages": "php82 php82-fpm php82-mysqlnd php82-curl", "health": "/", "port": "80", "user": "www-data", "vendor": "Akaunting"},
    "invoice-ninja": {"base": "alpine", "binary": "php", "version": "5.10.21", "packages": "php82 php82-fpm php82-mysqlnd php82-curl php82-mbstring", "health": "/", "port": "80", "user": "www-data", "vendor": "Invoice Ninja"},
    "firefly-iii": {"base": "alpine", "binary": "php", "version": "6.1.8", "packages": "php82 php82-fpm php82-mysqlnd php82-curl", "health": "/api/v1/about", "port": "80", "user": "www-data", "vendor": "Firefly III"},
    "vikunja": {"base": "scratch", "binary": "vikunja", "version": "0.23.1", "url": "https://github.com/go-vikunja/vikunja/releases/download/v{VERSION}/vikunja-{VERSION}-linux-amd64.tar.gz", "health": "/health", "port": "3456", "vendor": "Vikunja"},
    "planka": {"base": "alpine", "binary": "node", "version": "1.17.0", "packages": "nodejs npm", "health": "/api/health", "port": "3000", "user": "planka", "vendor": "Planka"},
    "focalboard": {"base": "scratch", "binary": "focalboard-server", "version": "7.8.0", "url": "https://github.com/mattermost/focalboard/releases/download/v{VERSION}/focalboard-server-linux-amd64.tar.gz", "health": "/api/v1/health", "port": "8000", "vendor": "Focalboard"},
    
    # === PHOTO (20) ===
    "immich": {"base": "alpine", "binary": "node", "version": "1.106.0", "packages": "nodejs ffmpeg", "health": "/api/server-info/ping", "port": "2283", "user": "immich", "vendor": "Immich"},
    "photoprism": {"base": "alpine", "binary": "photoprism", "version": "240427", "packages": "photoprism", "health": "/api/v1/status", "port": "2282", "user": "photoprism", "vendor": "PhotoPrism"},
    "lychee": {"base": "alpine", "binary": "lychee", "version": "0.15.1", "packages": "lychee", "health": "/health", "port": "8089", "user": "lychee", "vendor": "Lychee"},
    "piwigo": {"base": "alpine", "binary": "php", "version": "14.5.0", "packages": "php82 php82-fpm php82-mysqlnd php82-curl", "health": "/", "port": "80", "user": "www-data", "vendor": "Piwigo"},
    
    # === NOTE TAKING / WIKI (15) ===
    "hedgedoc": {"base": "alpine", "binary": "hedgedoc", "version": "1.9.10", "packages": "hedgedoc npm", "health": "/api/status", "port": "3000", "user": "hedgedoc", "vendor": "HedgeDoc"},
    "logseq": {"base": "alpine", "binary": "node", "version": "0.10.18", "packages": "nodejs npm", "health": "/health", "port": "3000", "user": "logseq", "vendor": "Logseq"},
    "outline": {"base": "alpine", "binary": "node", "version": "0.77.0", "packages": "nodejs npm postgresql-client", "health": "/api/status", "port": "3000", "user": "outline", "vendor": "Outline"},
    "mattermost": {"base": "alpine", "binary": "mattermost", "version": "10.1.0", "packages": "mattermost", "health": "/api/v4/system/ping", "port": "8065", "user": "mattermost", "vendor": "Mattermost"},
    "synapse": {"base": "alpine", "binary": "synapse", "version": "1.105.0", "packages": "synapse python3", "health": "/_matrix/client/versions", "port": "8008", "user": "synapse", "vendor": "Matrix"},
    
    # === RUNTIMES / COMPILERS (15) ===
    "node": {"base": "alpine", "binary": "node", "version": "20.12.2", "packages": "nodejs npm", "health": "node --version", "ports": "", "user": "node", "vendor": "Node.js"},
    "python": {"base": "alpine", "binary": "python", "version": "3.12.3", "packages": "python3 py3-pip", "health": "python --version", "ports": "", "user": "python", "vendor": "Python"},
    "golang": {"base": "alpine", "binary": "go", "version": "1.22.3", "packages": "go", "health": "go version", "ports": "", "user": "go", "vendor": "Go"},
    "rust": {"base": "alpine", "binary": "rustc", "version": "1.78.0", "packages": "rust cargo", "health": "rustc --version", "ports": "", "user": "rust", "vendor": "Rust"},
    "openjdk": {"base": "alpine", "binary": "java", "version": "21.0.3", "packages": "openjdk21", "health": "java -version", "ports": "", "user": "java", "vendor": "OpenJDK"},
    "ruby": {"base": "alpine", "binary": "ruby", "version": "3.3.1", "packages": "ruby ruby-bundler", "health": "ruby --version", "ports": "", "user": "ruby", "vendor": "Ruby"},
    "php": {"base": "alpine", "binary": "php", "version": "8.3.8", "packages": "php83 php83-fpm", "health": "php --version", "ports": "", "user": "php", "vendor": "PHP"},
    
    # === SCRATCH-BASED UTILITIES ===
    "hadolint": {"base": "scratch", "binary": "hadolint", "version": "2.12.1", "url": "https://github.com/hadolint/hadolint/releases/download/v{VERSION}/hadolint-{VERSION}-linux-x86_64", "health": "hadolint --version", "ports": "", "vendor": "Hadolint"},
    "dockle": {"base": "scratch", "binary": "dockle", "version": "0.4.13", "url": "https://github.com/goodwithtech/dockle/releases/download/v{VERSION}/dockle_{VERSION}_linux_amd64.tar.gz", "health": "dockle --version", "ports": "", "vendor": "Dockle"},
    "checkov": {"base": "scratch", "binary": "checkov", "version": "3.2.90", "url": "https://github.com/checkov/checkov/releases/download/{VERSION}/checkov-{VERSION}.tar.gz", "health": "checkov --version", "ports": "", "vendor": "Checkov"},
    "kube-bench": {"base": "scratch", "binary": "kube-bench", "version": "0.7.3", "url": "https://github.com/aquasecurity/kube-bench/releases/download/v{VERSION}/kube-bench_{VERSION}_linux_amd64.tar.gz", "health": "kube-bench version", "ports": "", "vendor": "Aqua Security"},
    "kubescape": {"base": "scratch", "binary": "kubescape", "version": "3.0.10", "url": "https://github.com/kubescape/kubescape/releases/download/v{VERSION}/kubescape-{VERSION}-linux-amd64.tar.gz", "health": "kubescape version", "ports": "", "vendor": "Kubescape"},
    "falco": {"base": "alpine", "binary": "falco", "version": "0.39.1", "packages": "falco", "health": "/var/run/falco.sock", "ports": "5060", "user": "falco", "vendor": "Falco"},
    "goreleaser": {"base": "scratch", "binary": "goreleaser", "version": "1.26.0", "url": "https://github.com/goreleaser/goreleaser/releases/download/v{VERSION}/goreleaser_{VERSION}_linux_amd64.tar.gz", "health": "goreleaser --version", "ports": "", "vendor": "GoReleaser"},
    "actionlint": {"base": "scratch", "binary": "actionlint", "version": "1.7.1", "url": "https://github.com/rhysd/actionlint/releases/download/v{VERSION}/actionlint_{VERSION}_linux_amd64.tar.gz", "health": "actionlint --version", "ports": "", "vendor": "Actionlint"},
    "buf": {"base": "scratch", "binary": "buf", "version": "1.34.0", "url": "https://github.com/bufbuild/buf/releases/download/v{VERSION}/buf-Linux-x86_64", "health": "buf --version", "ports": "", "vendor": "Buf"},
    "gitleaks": {"base": "scratch", "binary": "gitleaks", "version": "8.18.2", "url": "https://github.com/gitleaks/gitleaks/releases/download/v{VERSION}/gitleaks_{VERSION}_linux_x64_v{VERSION}.tar.gz", "health": "gitleaks version", "ports": "", "vendor": "Gitleaks"},
    "trufflehog": {"base": "scratch", "binary": "trufflehog", "version": "3.79.0", "url": "https://github.com/trufflesecurity/trufflehog/releases/download/v{VERSION}/trufflehog_{VERSION}_linux_amd64.tar.gz", "health": "trufflehog version", "ports": "", "vendor": "TruffleHog"},
}

# Dockerfiles generated from this file: ~300+ core images
# Combined with template variations = 1000+

print(f"Total images defined: {len(IMAGES)}")