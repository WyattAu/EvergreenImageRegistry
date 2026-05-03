#!/usr/bin/env python3
"""Generate manifest.toml files for images that have Dockerfiles but no manifest."""

import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TIER1_IMAGES = [
    "prometheus", "grafana", "alertmanager", "loki", "thanos",
    "redis", "postgres", "mysql", "mongodb", "cockroachdb",
    "vault", "keycloak", "dex",
    "envoy", "nginx", "traefik", "consul", "coredns",
    "elasticsearch", "opensearch", "kibana",
    "minio", "s3",
    "node-exporter",
    "kafka", "rabbitmq", "nats",
    "jaeger", "zipkin",
    "fluent-bit",
    "trivy", "falco",
    "argo-cd",
    "jenkins", "drone", "tekton",
]

TIER2_IMAGES = [
    "redis-exporter", "postgres-exporter",
    "grafana-image-renderer",
    "prometheus-nginx-exporter", "prometheus-mysqld-exporter",
    "valkey", "scylladb", "tidb",
    "etcd",
    "mariadb", "couchdb", "cassandra",
    "vector", "logstash",
    "heimdall", "authelia",
    "duckdb", "questdb",
    "minio-console", "minio-operator",
    "k3s", "kubectl",
]

TIER3_IMAGES = [
    "memcached", "haproxy", "influxdb", "telegraf", "caddy",
    "postgresql", "mysql-exporter", "redis-cluster", "redis-sentinel",
    "nextcloud", "portainer", "homeassistant", "jellyfin", "plex",
    "sonarr", "radarr", "prowlarr", "lidarr",
    "gitea", "forgejo",
    "n8n", "dagster",
    "kafka-connect", "kafka-exporter", "kafka-ui",
    "rabbitmq-management", "rabbitmq-exporter",
    "neo4j", "couchbase",
    "meilisearch", "dragonfly",
    "unbound", "bind",
    "step-ca", "trufflehog",
    "kubescape",
    "oauth2-proxy", "headscale",
    "wireguard",
    "miniflux", "immich",
    "pi-hole", "traefik-v2",
    "prometheus-pushgateway", "prometheus-operator",
    "kube-bench", "kube-state-metrics",
    "kube-apiserver", "kube-controller", "kube-proxy", "kube-scheduler",
    "kustomize", "helm",
    "mysql-backup", "postgres-operator",
    "redis-insight", "vaultwarden",
    "cosign", "rekor", "fulcio",
    "grafana-operator", "grafana-lite",
    "coredns-alpine", "nginx-exporter",
    "consul-exporter", "consul-template",
    "emqx", "mosquitto",
    "cadvisor",
    "influxdb-2",
    "cockroachdb-exporter",
    "falcosidekick",
    "prometheus-blackbox-exporter",
    "prometheus-consul-exporter",
    "prometheus-elasticsearch-exporter",
    "prometheus-postgres-exporter",
    "prometheus-node-exporter",
]

DESCRIPTIONS = {
    "prometheus": "Prometheus - monitoring and alerting toolkit",
    "grafana": "Grafana - observability dashboard and visualization",
    "alertmanager": "Alertmanager - handles alerts sent by Prometheus",
    "loki": "Loki - horizontally-scalable log aggregation system",
    "thanos": "Thanos - highly available Prometheus with long-term storage",
    "redis": "Redis - in-memory data structure store and cache",
    "postgres": "PostgreSQL - advanced open source relational database",
    "mysql": "MySQL - open source relational database management system",
    "mongodb": "MongoDB - document-oriented NoSQL database",
    "cockroachdb": "CockroachDB - distributed SQL database",
    "vault": "Vault - secrets management and data protection by HashiCorp",
    "keycloak": "Keycloak - identity and access management",
    "dex": "Dex - federated OpenID Connect provider",
    "envoy": "Envoy - high-performance edge and service proxy",
    "nginx": "Nginx - HTTP and reverse proxy server",
    "traefik": "Traefik - modern HTTP reverse proxy and load balancer",
    "consul": "Consul - service mesh, service discovery, and configuration",
    "coredns": "CoreDNS - DNS server and service discovery for Kubernetes",
    "elasticsearch": "Elasticsearch - distributed search and analytics engine",
    "opensearch": "OpenSearch - community-driven search and analytics engine",
    "kibana": "Kibana - data visualization dashboard for Elasticsearch",
    "minio": "MinIO - high-performance object storage compatible with S3",
    "s3": "S3 - AWS S3 compatible object storage client",
    "node-exporter": "Node Exporter - hardware and OS metrics exporter for Prometheus",
    "kafka": "Apache Kafka - distributed event streaming platform",
    "rabbitmq": "RabbitMQ - message broker software",
    "nats": "NATS - high-performance messaging system",
    "jaeger": "Jaeger - end-to-end distributed tracing",
    "zipkin": "Zipkin - distributed tracing system",
    "fluent-bit": "Fluent Bit - fast lightweight log processor and forwarder",
    "trivy": "Trivy - security scanner for containers and dependencies",
    "falco": "Falco - cloud-native runtime security monitoring",
    "argo-cd": "Argo CD - declarative GitOps continuous delivery for Kubernetes",
    "jenkins": "Jenkins - open source automation server for CI/CD",
    "drone": "Drone - cloud-native continuous integration and delivery platform",
    "tekton": "Tekton - cloud-native CI/CD solution for Kubernetes",
    "redis-exporter": "Redis Exporter - Prometheus exporter for Redis",
    "postgres-exporter": "Postgres Exporter - Prometheus exporter for PostgreSQL",
    "grafana-image-renderer": "Grafana Image Renderer - server-side image rendering for Grafana",
    "prometheus-nginx-exporter": "Nginx Prometheus Exporter - metrics exporter for Nginx",
    "prometheus-mysqld-exporter": "MySQL Prometheus Exporter - metrics exporter for MySQL",
    "valkey": "Valkey - open source Redis-compatible in-memory data store",
    "scylladb": "ScyllaDB - high-performance NoSQL columnar database",
    "tidb": "TiDB - distributed NewSQL database compatible with MySQL",
    "etcd": "etcd - distributed reliable key-value store",
    "mariadb": "MariaDB - community-developed fork of MySQL",
    "couchdb": "CouchDB - document-oriented NoSQL database",
    "cassandra": "Apache Cassandra - distributed NoSQL database",
    "vector": "Vector - high-performance observability data pipeline",
    "logstash": "Logstash - server-side data processing pipeline",
    "heimdall": "Heimdall - application dashboard and launcher",
    "authelia": "Authelia - single sign-on and two-factor authentication portal",
    "duckdb": "DuckDB - in-process SQL OLAP database management system",
    "questdb": "QuestDB - time-series SQL database",
    "minio-console": "MinIO Console - web-based administration UI for MinIO",
    "minio-operator": "MinIO Operator - Kubernetes operator for MinIO",
    "k3s": "K3s - lightweight Kubernetes distribution",
    "kubectl": "kubectl - command line tool for controlling Kubernetes clusters",
    "memcached": "Memcached - high-performance distributed memory caching system",
    "haproxy": "HAProxy - reliable high-performance TCP/HTTP load balancer",
    "influxdb": "InfluxDB - time series database for metrics and events",
    "telegraf": "Telegraf - metrics collection agent",
    "caddy": "Caddy - powerful enterprise-ready open source web server",
    "postgresql": "PostgreSQL - advanced open source relational database",
    "mysql-exporter": "MySQL Exporter - Prometheus exporter for MySQL server",
    "redis-cluster": "Redis Cluster - distributed Redis implementation",
    "redis-sentinel": "Redis Sentinel - high availability for Redis",
    "nextcloud": "Nextcloud - self-hosted productivity platform",
    "portainer": "Portainer - container management UI",
    "homeassistant": "Home Assistant - open source home automation platform",
    "jellyfin": "Jellyfin - free software media system",
    "plex": "Plex - streaming media server and client",
    "sonarr": "Sonarr - PVR for Usenet and BitTorrent users",
    "radarr": "Radarr - movie collection manager for Usenet and BitTorrent",
    "prowlarr": "Prowlarr - indexer manager and proxy for PVR software",
    "lidarr": "Lidarr - music collection manager for Usenet and BitTorrent",
    "gitea": "Gitea - lightweight self-hosted Git service",
    "forgejo": "Forgejo - community-owned lightweight software forge",
    "n8n": "n8n - workflow automation platform",
    "dagster": "Dagster - data orchestration platform",
    "kafka-connect": "Kafka Connect - scalable and reliable data streaming integration",
    "kafka-exporter": "Kafka Exporter - Prometheus exporter for Apache Kafka",
    "kafka-ui": "Kafka UI - open source web UI for Apache Kafka",
    "rabbitmq-management": "RabbitMQ Management - web-based management plugin for RabbitMQ",
    "rabbitmq-exporter": "RabbitMQ Exporter - Prometheus exporter for RabbitMQ",
    "neo4j": "Neo4j - native graph database",
    "couchbase": "Couchbase - distributed NoSQL cloud database",
    "meilisearch": "Meilisearch - fast, relevant, and typo-tolerant search engine",
    "dragonfly": "Dragonfly - in-memory data store compatible with Redis and Memcached",
    "unbound": "Unbound - validating, recursive, and caching DNS resolver",
    "bind": "BIND - DNS server software",
    "step-ca": "Step CA - private certificate authority for automated PKI",
    "trufflehog": "TruffleHog - secrets scanner for Git repositories",
    "kubescape": "Kubescape - Kubernetes security platform",
    "oauth2-proxy": "OAuth2 Proxy - reverse proxy with authentication provider",
    "headscale": "Headscale - open source implementation of the Tailscale control server",
    "wireguard": "WireGuard - fast, modern, secure VPN tunnel",
    "miniflux": "Miniflux - minimalist RSS/Atom feed reader",
    "immich": "Immich - self-hosted photo and video backup solution",
    "pi-hole": "Pi-hole - network-level ad blocking via your own Linux hardware",
    "traefik-v2": "Traefik v2 - modern HTTP reverse proxy and load balancer",
    "prometheus-pushgateway": "Prometheus Pushgateway - intermediary service for metrics push",
    "prometheus-operator": "Prometheus Operator - manages Prometheus monitoring instances",
    "kube-bench": "Kube-bench - checks whether Kubernetes is deployed securely",
    "kube-state-metrics": "Kube-state-metrics - metrics about Kubernetes objects",
    "kube-apiserver": "Kubernetes API Server - control plane component",
    "kube-controller": "Kubernetes Controller Manager - control plane component",
    "kube-proxy": "Kube-proxy - network proxy on every node",
    "kube-scheduler": "Kubernetes Scheduler - control plane component",
    "kustomize": "Kustomize - template-free configuration customization for Kubernetes",
    "helm": "Helm - package manager for Kubernetes",
    "mysql-backup": "MySQL Backup - automated backup solution for MySQL",
    "postgres-operator": "Postgres Operator - manages PostgreSQL clusters on Kubernetes",
    "redis-insight": "RedisInsight - visualization and management tool for Redis",
    "vaultwarden": "Vaultwarden - lightweight Bitwarden-compatible password manager",
    "cosign": "Cosign - container signing and verification tool",
    "rekor": "Rekor - transparency log for supply chain security",
    "fulcio": "Fulcio - certificate authority for Sigstore",
    "grafana-operator": "Grafana Operator - manages Grafana instances on Kubernetes",
    "grafana-lite": "Grafana Lite - lightweight Grafana dashboard",
    "coredns-alpine": "CoreDNS Alpine - lightweight DNS server based on Alpine",
    "nginx-exporter": "Nginx Exporter - Prometheus metrics exporter for Nginx",
    "consul-exporter": "Consul Exporter - Prometheus exporter for Consul",
    "consul-template": "Consul Template - template rendering with Consul data",
    "emqx": "EMQX - massively scalable MQTT message broker",
    "mosquitto": "Mosquitto - lightweight MQTT message broker",
    "cadvisor": "cAdvisor - container resource usage and performance analysis",
    "influxdb-2": "InfluxDB 2 - time series database with Flux query engine",
    "cockroachdb-exporter": "CockroachDB Exporter - Prometheus exporter for CockroachDB",
    "falcosidekick": "Falco Sidekick - event forwarder for Falco alerts",
    "prometheus-blackbox-exporter": "Blackbox Exporter - probing endpoints for Prometheus",
    "prometheus-consul-exporter": "Consul Exporter - Prometheus exporter for Consul",
    "prometheus-elasticsearch-exporter": "Elasticsearch Exporter - Prometheus exporter for Elasticsearch",
    "prometheus-postgres-exporter": "Postgres Exporter - Prometheus exporter for PostgreSQL",
    "prometheus-node-exporter": "Node Exporter - hardware and OS metrics exporter for Prometheus",
}

VENDORS = {
    "prometheus": "Prometheus", "grafana": "Grafana Labs", "alertmanager": "Prometheus",
    "loki": "Grafana Labs", "thanos": "Thanos", "redis": "Redis",
    "postgres": "PostgreSQL", "mysql": "Oracle", "mongodb": "MongoDB",
    "cockroachdb": "Cockroach Labs", "vault": "HashiCorp", "keycloak": "Red Hat",
    "dex": "Dex", "envoy": "Envoy Proxy", "nginx": "Nginx Inc",
    "traefik": "Traefik Labs", "consul": "HashiCorp", "coredns": "CNCF",
    "elasticsearch": "Elastic", "opensearch": "AWS", "kibana": "Elastic",
    "minio": "MinIO", "s3": "AWS",
    "node-exporter": "Prometheus", "kafka": "Apache", "rabbitmq": "VMware",
    "nats": "CNCF", "jaeger": "Jaeger", "zipkin": "Zipkin",
    "fluent-bit": "Fluent", "trivy": "Aqua Security", "falco": "CNCFSys",
    "argo-cd": "Argo Project", "jenkins": "Jenkins", "drone": "Harness",
    "tekton": "TektonCD",
    "redis-exporter": "Prometheus", "postgres-exporter": "Prometheus",
    "grafana-image-renderer": "Grafana Labs",
    "prometheus-nginx-exporter": "Prometheus", "prometheus-mysqld-exporter": "Prometheus",
    "valkey": "Linux Foundation", "scylladb": "ScyllaDB", "tidb": "PingCAP",
    "etcd": "CNCF", "mariadb": "MariaDB Foundation", "couchdb": "Apache",
    "cassandra": "Apache", "vector": "Datadog", "logstash": "Elastic",
    "heimdall": "Heimdall", "authelia": "Authelia",
    "duckdb": "DuckDB Labs", "questdb": "QuestDB",
    "minio-console": "MinIO", "minio-operator": "MinIO",
    "k3s": "SUSE", "kubectl": "Kubernetes",
    "memcached": "Memcached", "haproxy": "HAProxy", "influxdb": "InfluxData",
    "telegraf": "InfluxData", "caddy": "Caddy", "postgresql": "PostgreSQL",
    "mysql-exporter": "Prometheus", "redis-cluster": "Redis",
    "redis-sentinel": "Redis", "nextcloud": "Nextcloud",
    "portainer": "Portainer", "homeassistant": "Home Assistant",
    "jellyfin": "Jellyfin", "plex": "Plex",
    "sonarr": "Sonarr", "radarr": "Radarr", "prowlarr": "Prowlarr",
    "lidarr": "Lidarr", "gitea": "Gitea", "forgejo": "Forgejo",
    "n8n": "n8n", "dagster": "Dagster",
    "kafka-connect": "Apache", "kafka-exporter": "Prometheus",
    "kafka-ui": "Kafka UI", "rabbitmq-management": "VMware",
    "rabbitmq-exporter": "Prometheus", "neo4j": "Neo4j",
    "couchbase": "Couchbase", "meilisearch": "Meilisearch",
    "dragonfly": "Dragonfly", "unbound": "NLnet Labs",
    "bind": "ISC", "step-ca": "Smallstep",
    "trufflehog": "TruffleHog", "kubescape": "Kubescape",
    "oauth2-proxy": "OAuth2 Proxy", "headscale": "Headscale",
    "wireguard": "WireGuard", "miniflux": "Miniflux",
    "immich": "Immich", "pi-hole": "Pi-hole",
    "traefik-v2": "Traefik Labs",
    "prometheus-pushgateway": "Prometheus", "prometheus-operator": "Prometheus",
    "kube-bench": "Aqua Security", "kube-state-metrics": "Kubernetes",
    "kube-apiserver": "Kubernetes", "kube-controller": "Kubernetes",
    "kube-proxy": "Kubernetes", "kube-scheduler": "Kubernetes",
    "kustomize": "Kubernetes", "helm": "Helm",
    "mysql-backup": "Community", "postgres-operator": "Zalando",
    "redis-insight": "Redis", "vaultwarden": "Vaultwarden",
    "cosign": "Sigstore", "rekor": "Sigstore", "fulcio": "Sigstore",
    "grafana-operator": "Grafana Labs", "grafana-lite": "Grafana Labs",
    "coredns-alpine": "CNCF", "nginx-exporter": "Prometheus",
    "consul-exporter": "Prometheus", "consul-template": "HashiCorp",
    "emqx": "EMQX", "mosquitto": "Eclipse",
    "cadvisor": "Google", "influxdb-2": "InfluxData",
    "cockroachdb-exporter": "Cockroach Labs", "falcosidekick": "Falco",
    "prometheus-blackbox-exporter": "Prometheus",
    "prometheus-consul-exporter": "Prometheus",
    "prometheus-elasticsearch-exporter": "Prometheus",
    "prometheus-postgres-exporter": "Prometheus",
    "prometheus-node-exporter": "Prometheus",
}

SOURCES = {
    "prometheus": "https://github.com/prometheus/prometheus",
    "grafana": "https://github.com/grafana/grafana",
    "alertmanager": "https://github.com/prometheus/alertmanager",
    "loki": "https://github.com/grafana/loki",
    "thanos": "https://github.com/thanos-io/thanos",
    "redis": "https://github.com/redis/redis",
    "postgres": "https://github.com/postgres/postgres",
    "mysql": "https://github.com/mysql/mysql-server",
    "mongodb": "https://github.com/mongodb/mongo",
    "cockroachdb": "https://github.com/cockroachdb/cockroach",
    "vault": "https://github.com/hashicorp/vault",
    "keycloak": "https://github.com/keycloak/keycloak",
    "dex": "https://github.com/dexidp/dex",
    "envoy": "https://github.com/envoyproxy/envoy",
    "nginx": "https://github.com/nginx/nginx",
    "traefik": "https://github.com/traefik/traefik",
    "consul": "https://github.com/hashicorp/consul",
    "coredns": "https://github.com/coredns/coredns",
    "elasticsearch": "https://github.com/elastic/elasticsearch",
    "opensearch": "https://github.com/opensearch-project/opensearch",
    "kibana": "https://github.com/elastic/kibana",
    "minio": "https://github.com/minio/minio",
    "s3": "https://github.com/aws/aws-cli",
    "node-exporter": "https://github.com/prometheus/node_exporter",
    "kafka": "https://github.com/apache/kafka",
    "rabbitmq": "https://github.com/rabbitmq/rabbitmq-server",
    "nats": "https://github.com/nats-io/nats-server",
    "jaeger": "https://github.com/jaegertracing/jaeger",
    "zipkin": "https://github.com/openzipkin/zipkin",
    "fluent-bit": "https://github.com/fluent/fluent-bit",
    "trivy": "https://github.com/aquasecurity/trivy",
    "falco": "https://github.com/falcosecurity/falco",
    "argo-cd": "https://github.com/argoproj/argo-cd",
    "jenkins": "https://github.com/jenkinsci/jenkins",
    "drone": "https://github.com/harness/drone",
    "tekton": "https://github.com/tektoncd/pipeline",
    "redis-exporter": "https://github.com/oliver006/redis_exporter",
    "postgres-exporter": "https://github.com/prometheus-community/postgres_exporter",
    "grafana-image-renderer": "https://github.com/grafana/grafana-image-renderer",
    "prometheus-nginx-exporter": "https://github.com/nginxinc/nginx-prometheus-exporter",
    "prometheus-mysqld-exporter": "https://github.com/prometheus/mysqld_exporter",
    "valkey": "https://github.com/valkey-io/valkey",
    "scylladb": "https://github.com/scylladb/scylladb",
    "tidb": "https://github.com/pingcap/tidb",
    "etcd": "https://github.com/etcd-io/etcd",
    "mariadb": "https://github.com/MariaDB/server",
    "couchdb": "https://github.com/apache/couchdb",
    "cassandra": "https://github.com/apache/cassandra",
    "vector": "https://github.com/vectordotdev/vector",
    "logstash": "https://github.com/elastic/logstash",
    "heimdall": "https://github.com/linuxserver/heimdall",
    "authelia": "https://github.com/authelia/authelia",
    "duckdb": "https://github.com/duckdb/duckdb",
    "questdb": "https://github.com/questdb/questdb",
    "minio-console": "https://github.com/minio/console",
    "minio-operator": "https://github.com/minio/operator",
    "k3s": "https://github.com/k3s-io/k3s",
    "kubectl": "https://github.com/kubernetes/kubernetes",
    "memcached": "https://github.com/memcached/memcached",
    "haproxy": "https://github.com/haproxy/haproxy",
    "influxdb": "https://github.com/influxdata/influxdb",
    "telegraf": "https://github.com/influxdata/telegraf",
    "caddy": "https://github.com/caddyserver/caddy",
    "postgresql": "https://github.com/postgres/postgres",
    "mysql-exporter": "https://github.com/prometheus/mysqld_exporter",
    "redis-cluster": "https://github.com/redis/redis",
    "redis-sentinel": "https://github.com/redis/redis",
    "nextcloud": "https://github.com/nextcloud/server",
    "portainer": "https://github.com/portainer/portainer",
    "homeassistant": "https://github.com/home-assistant/core",
    "jellyfin": "https://github.com/jellyfin/jellyfin",
    "plex": "https://github.com/plexinc/pms-docker",
    "sonarr": "https://github.com/Sonarr/Sonarr",
    "radarr": "https://github.com/Radarr/Radarr",
    "prowlarr": "https://github.com/Prowlarr/Prowlarr",
    "lidarr": "https://github.com/Lidarr/Lidarr",
    "gitea": "https://github.com/go-gitea/gitea",
    "forgejo": "https://github.com/forgejo/forgejo",
    "n8n": "https://github.com/n8n-io/n8n",
    "dagster": "https://github.com/dagster-io/dagster",
    "kafka-connect": "https://github.com/apache/kafka",
    "kafka-exporter": "https://github.com/danielqsj/kafka_exporter",
    "kafka-ui": "https://github.com/provectus/kafka-ui",
    "rabbitmq-management": "https://github.com/rabbitmq/rabbitmq-server",
    "rabbitmq-exporter": "https://github.com/kbudde/rabbitmq_exporter",
    "neo4j": "https://github.com/neo4j/neo4j",
    "couchbase": "https://github.com/couchbase/couchbase-cli",
    "meilisearch": "https://github.com/meilisearch/meilisearch",
    "dragonfly": "https://github.com/dragonflydb/dragonfly",
    "unbound": "https://github.com/NLnetLabs/unbound",
    "bind": "https://github.com/isc-projects/bind9",
    "step-ca": "https://github.com/smallstep/certificates",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog",
    "kubescape": "https://github.com/kubescape/kubescape",
    "oauth2-proxy": "https://github.com/oauth2-proxy/oauth2-proxy",
    "headscale": "https://github.com/juanfont/headscale",
    "wireguard": "https://github.com/WireGuard/wireguard-go",
    "miniflux": "https://github.com/miniflux/v2",
    "immich": "https://github.com/immich-app/immich",
    "pi-hole": "https://github.com/pi-hole/pi-hole",
    "traefik-v2": "https://github.com/traefik/traefik",
    "prometheus-pushgateway": "https://github.com/prometheus/pushgateway",
    "prometheus-operator": "https://github.com/prometheus-operator/prometheus-operator",
    "kube-bench": "https://github.com/aquasecurity/kube-bench",
    "kube-state-metrics": "https://github.com/kubernetes/kube-state-metrics",
    "kube-apiserver": "https://github.com/kubernetes/kubernetes",
    "kube-controller": "https://github.com/kubernetes/kubernetes",
    "kube-proxy": "https://github.com/kubernetes/kubernetes",
    "kube-scheduler": "https://github.com/kubernetes/kubernetes",
    "kustomize": "https://github.com/kubernetes-sigs/kustomize",
    "helm": "https://github.com/helm/helm",
    "mysql-backup": "https://github.com/databack/mysql-backup4sh",
    "postgres-operator": "https://github.com/zalando/postgres-operator",
    "redis-insight": "https://github.com/RedisInsight/RedisInsight",
    "vaultwarden": "https://github.com/dani-garcia/vaultwarden",
    "cosign": "https://github.com/sigstore/cosign",
    "rekor": "https://github.com/sigstore/rekor",
    "fulcio": "https://github.com/sigstore/fulcio",
    "grafana-operator": "https://github.com/grafana-operator/grafana-operator",
    "grafana-lite": "https://github.com/grafana/grafana",
    "coredns-alpine": "https://github.com/coredns/coredns",
    "nginx-exporter": "https://github.com/nginxinc/nginx-prometheus-exporter",
    "consul-exporter": "https://github.com/prometheus/consul_exporter",
    "consul-template": "https://github.com/hashicorp/consul-template",
    "emqx": "https://github.com/emqx/emqx",
    "mosquitto": "https://github.com/eclipse-mosquitto/mosquitto",
    "cadvisor": "https://github.com/google/cadvisor",
    "influxdb-2": "https://github.com/influxdata/influxdb",
    "cockroachdb-exporter": "https://github.com/cockroachdb/cockroach",
    "falcosidekick": "https://github.com/falcosecurity/falcosidekick",
    "prometheus-blackbox-exporter": "https://github.com/prometheus/blackbox_exporter",
    "prometheus-consul-exporter": "https://github.com/prometheus/consul_exporter",
    "prometheus-elasticsearch-exporter": "https://github.com/prometheus-community/elasticsearch_exporter",
    "prometheus-postgres-exporter": "https://github.com/prometheus-community/postgres_exporter",
    "prometheus-node-exporter": "https://github.com/prometheus/node_exporter",
}

VERSION_OVERRIDES = {
    "alertmanager": "0.32.1",
    "jaeger": "1.62.0",
    "tekton": "0.60.0",
    "falco": "0.38.3",
    "heimdall": "2.6.1",
    "fluent-bit": "3.2.4",
    "tidb": "8.4.0",
    "prowlarr": "1.27.0",
    "lidarr": "2.4.3",
    "kafka-exporter": "1.8.0",
    "kafka-ui": "0.7.2",
    "cockroachdb-exporter": "24.3.3",
    "couchbase": "7.6.1",
    "pi-hole": "5.18.2",
    "mosquitto": "2.0.20",
    "minio-operator": "6.0.4",
}

LICENSES = {
    "prometheus": "Apache-2.0", "grafana": "AGPL-3.0", "alertmanager": "Apache-2.0",
    "loki": "AGPL-3.0", "thanos": "Apache-2.0", "redis": "BSD-3-Clause",
    "postgres": "PostgreSQL", "mysql": "GPL-2.0", "mongodb": "SSPL",
    "cockroachdb": "BSL-1.1", "vault": "MPL-2.0", "keycloak": "Apache-2.0",
    "dex": "Apache-2.0", "envoy": "Apache-2.0", "nginx": "BSD-2-Clause",
    "traefik": "MIT", "consul": "MPL-2.0", "coredns": "Apache-2.0",
    "elasticsearch": "Elastic-2.0", "opensearch": "Apache-2.0", "kibana": "Elastic-2.0",
    "minio": "AGPL-3.0", "s3": "Apache-2.0",
    "node-exporter": "Apache-2.0", "kafka": "Apache-2.0", "rabbitmq": "MPL-2.0",
    "nats": "Apache-2.0", "jaeger": "Apache-2.0", "zipkin": "Apache-2.0",
    "fluent-bit": "Apache-2.0", "trivy": "Apache-2.0", "falco": "Apache-2.0",
    "argo-cd": "Apache-2.0", "jenkins": "MIT", "drone": "Apache-2.0",
    "tekton": "Apache-2.0",
}


def parse_dockerfile(path):
    with open(path) as f:
        content = f.read()

    name = os.path.basename(os.path.dirname(path))

    if name in VERSION_OVERRIDES:
        version = VERSION_OVERRIDES[name]
    else:
        version_match = re.search(r'ARG\s+VERSION[=\s]([^\s]+)', content)
        version = version_match.group(1) if version_match else ""

        if not version or version.startswith("$") or version.startswith("${"):
            version = ""

        if not version:
            url_match = re.search(r'releases/download/v?(\d+\.\d+[\.\d]*(?:-[\w\.\+]+)?)', content)
            if url_match:
                version = url_match.group(1)
            else:
                url_match = re.search(r'/v(\d+\.\d+[\.\d]*(?:-[\w\.\+]+)?)/', content)
                if url_match:
                    version = url_match.group(1)

        if not version:
            label_ver = re.search(r'org\.opencontainers\.image\.version="([^"]+)"', content)
            if label_ver:
                v = label_ver.group(1)
                if not v.startswith("$") and v != "latest":
                    version = v

        if not version:
            version = "unknown"

    from_lines = re.findall(r'^FROM\s+([^\s]+)', content, re.MULTILINE)
    base_image = from_lines[0] if from_lines else "unknown"

    runtime_from = "scratch"
    for fl in from_lines:
        if fl == "scratch":
            runtime_from = "scratch"
            break
        if "wolfi" in fl:
            runtime_from = fl
            break
        if "distroless" in fl:
            runtime_from = fl
            break
        if "bookworm-slim" in fl:
            runtime_from = fl
            break
    if len(from_lines) > 1:
        runtime_from = from_lines[-1]
        for fl in reversed(from_lines):
            if "AS" not in fl.split() and "as" not in fl.lower():
                pass
            if fl == "scratch":
                runtime_from = "scratch"
                break
            if "wolfi" in fl:
                runtime_from = fl
                break
            if "distroless" in fl:
                runtime_from = fl
                break

    user_match = re.search(r'^USER\s+(\S+)', content, re.MULTILINE)
    user = user_match.group(1) if user_match else "65532:65532"

    expose = re.findall(r'^EXPOSE\s+(\S+)', content, re.MULTILINE)

    stopsignal_match = re.search(r'^STOPSIGNAL\s+(\S+)', content, re.MULTILINE)
    stopsignal = stopsignal_match.group(1) if stopsignal_match else "SIGTERM"

    entrypoint_match = re.search(r'^ENTRYPOINT\s+\[(.+)\]', content, re.MULTILINE)
    entrypoint = None
    if entrypoint_match:
        entrypoint = [s.strip().strip('"').strip("'") for s in entrypoint_match.group(1).split(",")]

    cmd_match = re.search(r'^CMD\s+\[(.+)\]', content, re.MULTILINE)
    cmd = None
    if cmd_match:
        cmd = [s.strip().strip('"').strip("'") for s in cmd_match.group(1).split(",")]

    labels = {}
    label_matches = re.findall(r'LABEL\s+(.+?)(?=\n(?:LABEL|EXPOSE|STOPSIGNAL|ENTRYPOINT|CMD|USER|FROM|HEALTHCHECK|#|\n\n|$))', content, re.DOTALL)
    for label_block in label_matches:
        for label_match in re.finditer(r'(\S+?)="([^"]*)"', label_block):
            labels[label_match.group(1)] = label_match.group(2)

    tier_label = labels.get("evergreen.image.tier", "2")
    nonroot = labels.get("evergreen.constraint.nonroot", "true") == "true"
    scratch = labels.get("evergreen.constraint.scratch", "false") == "true"
    base_img = labels.get("evergreen.base.image", "scratch" if runtime_from == "scratch" else "debian-slim")

    return {
        "version": version,
        "base_image": base_image,
        "runtime_image": runtime_from if runtime_from != base_image else "scratch",
        "user": user,
        "expose": expose,
        "stopsignal": stopsignal,
        "entrypoint": entrypoint,
        "cmd": cmd,
        "labels": labels,
        "tier": tier_label,
        "nonroot": nonroot,
        "scratch": scratch,
        "base": base_img,
    }


def get_download_info(name, version):
    download_info = {}
    if name == "prometheus":
        download_info = {
            "url": f"https://github.com/prometheus/prometheus/releases/download/v{version}/prometheus-{version}.linux-amd64.tar.gz",
            "binary_name": "prometheus",
            "filename": f"prometheus-{version}.linux-amd64.tar.gz",
        }
    elif name == "grafana":
        download_info = {
            "url": f"https://dl.grafana.com/oss/release/grafana-{version}.linux-amd64.tar.gz",
            "binary_name": "grafana-server",
            "filename": f"grafana-{version}.linux-amd64.tar.gz",
        }
    elif name == "alertmanager":
        download_info = {
            "url": f"https://github.com/prometheus/alertmanager/releases/download/v{version}/alertmanager-{version}.linux-amd64.tar.gz",
            "binary_name": "alertmanager",
            "filename": f"alertmanager-{version}.linux-amd64.tar.gz",
        }
    elif name == "loki":
        download_info = {
            "url": f"https://github.com/grafana/loki/releases/download/v{version}/loki-linux-amd64.zip",
            "binary_name": "loki",
            "filename": f"loki-linux-amd64.zip",
        }
    elif name == "thanos":
        download_info = {
            "url": f"https://github.com/thanos-io/thanos/releases/download/v{version}/thanos-{version}.linux-amd64.tar.gz",
            "binary_name": "thanos",
            "filename": f"thanos-{version}.linux-amd64.tar.gz",
        }
    elif name == "vault":
        download_info = {
            "url": f"https://releases.hashicorp.com/vault/{version}/vault_{version}_linux_amd64.zip",
            "binary_name": "vault",
            "filename": f"vault_{version}_linux_amd64.zip",
        }
    elif name == "consul":
        download_info = {
            "url": f"https://releases.hashicorp.com/consul/{version}/consul_{version}_linux_amd64.zip",
            "binary_name": "consul",
            "filename": f"consul_{version}_linux_amd64.zip",
        }
    elif name == "envoy":
        download_info = {
            "url": f"https://github.com/envoyproxy/envoy/releases/download/v{version}/envoy-{version}-linux-x86_64",
            "binary_name": "envoy",
            "filename": f"envoy-{version}-linux-x86_64",
        }
    elif name == "trivy":
        download_info = {
            "url": f"https://github.com/aquasecurity/trivy/releases/download/v{version}/trivy_{version}_Linux-64bit.tar.gz",
            "binary_name": "trivy",
            "filename": f"trivy_{version}_Linux-64bit.tar.gz",
        }
    elif name == "falco":
        download_info = {
            "url": f"https://github.com/falcosecurity/falco/releases/download/v{version}/falco-{version}-x86_64.tar.gz",
            "binary_name": "falco",
            "filename": f"falco-{version}-x86_64.tar.gz",
        }
    elif name == "tekton":
        download_info = {
            "url": f"https://github.com/tektoncd/pipeline/releases/download/{version}/tekton-linux-amd64.tar.gz",
            "binary_name": "tekton",
            "filename": f"tekton-linux-amd64.tar.gz",
        }
    elif name == "node-exporter":
        download_info = {
            "url": f"https://github.com/prometheus/node_exporter/releases/download/v{version}/node_exporter-{version}.linux-amd64.tar.gz",
            "binary_name": "node_exporter",
            "filename": f"node_exporter-{version}.linux-amd64.tar.gz",
        }
    elif name == "jaeger":
        download_info = {
            "url": f"https://github.com/jaegertracing/jaeger/releases/download/v{version}/jaeger-{version}-linux-amd64.tar.gz",
            "binary_name": "jaeger",
            "filename": f"jaeger-{version}-linux-amd64.tar.gz",
        }
    elif name == "zipkin":
        download_info = {
            "url": f"https://github.com/openzipkin/zipkin/releases/download/{version}/zipkin.jar",
            "binary_name": "zipkin",
            "filename": "zipkin.jar",
        }
    elif name == "fluent-bit":
        download_info = {
            "url": f"https://github.com/fluent/fluent-bit/releases/download/v{version}/fluent-bit-{version}-x86_64.tar.gz",
            "binary_name": "fluent-bit",
            "filename": f"fluent-bit-{version}-x86_64.tar.gz",
        }
    elif name == "argo-cd":
        download_info = {
            "url": f"https://github.com/argoproj/argo-cd/releases/download/v{version}/argocd-linux-amd64",
            "binary_name": "argocd",
            "filename": "argocd-linux-amd64",
        }
    elif name == "redis":
        download_info = {
            "url": f"https://github.com/redis/redis/archive/refs/tags/{version}.tar.gz",
            "binary_name": "redis-server",
            "filename": f"redis-{version}.tar.gz",
        }
    elif name == "etcd":
        download_info = {
            "url": f"https://github.com/etcd-io/etcd/releases/download/v{version}/etcd-v{version}-linux-amd64.tar.gz",
            "binary_name": "etcd",
            "filename": f"etcd-v{version}-linux-amd64.tar.gz",
        }
    elif name == "vector":
        download_info = {
            "url": f"https://github.com/vectordotdev/vector/releases/download/v{version}/vector-x86_64-unknown-linux-gnu.tar.gz",
            "binary_name": "vector",
            "filename": f"vector-x86_64-unknown-linux-gnu.tar.gz",
        }
    elif name == "cosign":
        download_info = {
            "url": f"https://github.com/sigstore/cosign/releases/download/v{version}/cosign-linux-amd64",
            "binary_name": "cosign",
            "filename": "cosign-linux-amd64",
        }
    elif name == "trufflehog":
        download_info = {
            "url": f"https://github.com/trufflesecurity/trufflehog/releases/download/v{version}/trufflehog_{version}_linux_amd64.tar.gz",
            "binary_name": "trufflehog",
            "filename": f"trufflehog_{version}_linux_amd64.tar.gz",
        }
    elif name == "kubescape":
        download_info = {
            "url": f"https://github.com/kubescape/kubescape/releases/download/v{version}/kubescape-ubuntu-amd64",
            "binary_name": "kubescape",
            "filename": "kubescape-ubuntu-amd64",
        }
    elif name == "kubectl":
        download_info = {
            "url": f"https://dl.k8s.io/release/v{version}/bin/linux/amd64/kubectl",
            "binary_name": "kubectl",
            "filename": "kubectl",
        }
    elif name == "helm":
        download_info = {
            "url": f"https://get.helm.sh/helm-v{version}-linux-amd64.tar.gz",
            "binary_name": "helm",
            "filename": f"helm-v{version}-linux-amd64.tar.gz",
        }
    elif name == "kustomize":
        download_info = {
            "url": f"https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv{version}/kustomize_v{version}_linux_amd64.tar.gz",
            "binary_name": "kustomize",
            "filename": f"kustomize_v{version}_linux_amd64.tar.gz",
        }
    elif name == "step-ca":
        download_info = {
            "url": f"https://github.com/smallstep/certificates/releases/download/v{version}/step-ca_{version}_linux_amd64.tar.gz",
            "binary_name": "step-ca",
            "filename": f"step-ca_{version}_linux_amd64.tar.gz",
        }
    elif name == "rekor":
        download_info = {
            "url": f"https://github.com/sigstore/rekor/releases/download/v{version}/rekor-linux-amd64",
            "binary_name": "rekor",
            "filename": "rekor-linux-amd64",
        }
    elif name == "fulcio":
        download_info = {
            "url": f"https://github.com/sigstore/fulcio/releases/download/v{version}/fulcio-linux-amd64",
            "binary_name": "fulcio",
            "filename": "fulcio-linux-amd64",
        }
    elif name == "duckdb":
        download_info = {
            "url": f"https://github.com/duckdb/duckdb/releases/download/v{version}/duckdb_cli-linux-amd64.zip",
            "binary_name": "duckdb",
            "filename": "duckdb_cli-linux-amd64.zip",
        }
    elif name == "minio":
        download_info = {
            "url": f"https://dl.min.io/server/minio/release/linux-amd64/minio",
            "binary_name": "minio",
            "filename": "minio",
        }
    else:
        download_info = {
            "url": f"https://github.com/{name}/{name}/releases/download/v{version}/{name}-{version}-linux-amd64.tar.gz",
            "binary_name": name,
            "filename": f"{name}-{version}-linux-amd64.tar.gz",
        }
    return download_info


def generate_port_section(name, expose):
    ports = {}
    app_ports = [p for p in expose if p != "9101"]
    if app_ports:
        if len(app_ports) == 1:
            ports["application"] = app_ports[0]
        else:
            port_names = {
                "80": "http", "443": "https", "8080": "http", "8443": "https",
                "9090": "web", "9092": "broker", "9093": "web",
                "5432": "database", "6379": "redis", "27017": "database",
                "8500": "http", "8200": "api", "8201": "cluster",
                "10902": "http", "3000": "web", "5140": "http",
                "24224": "forward", "14268": "jaeger-collector",
                "16686": "jaeger-ui", "9411": "api",
                "9901": "admin", "1883": "mqtt", "18830": "mqtt",
                "15672": "management", "5672": "amqp",
                "2181": "client", "2379": "client", "2380": "peer",
                "8086": "api", "8123": "http",
                "7474": "browser", "7687": "bolt",
                "7700": "http",
            }
            for p in app_ports:
                pname = port_names.get(p, f"port_{p}")
                ports[pname] = p
    if "9101" in expose:
        ports["metrics"] = "9101"
    return ports


def generate_manifest(name, info):
    version = info["version"]
    tier_num = 1 if name in TIER1_IMAGES else (2 if name in TIER2_IMAGES else 3)
    tier_str = str(tier_num)

    description = DESCRIPTIONS.get(name, f"{name} - container image")
    vendor = VENDORS.get(name, "Community")
    source = SOURCES.get(name, "")
    license_val = LICENSES.get(name, "Apache-2.0")

    ports = generate_port_section(name, info["expose"])
    is_scratch = info["scratch"] or info["runtime_image"] == "scratch"
    runtime_img = "scratch" if is_scratch else info["runtime_image"]

    lines = []
    lines.append("[metadata]")
    lines.append(f'name = "{name}"')
    lines.append(f'version = "{version}"')
    lines.append(f'description = "{description}"')
    lines.append(f'vendor = "{vendor}"')
    if source:
        lines.append(f'source = "{source}"')
    lines.append(f'license = "{license_val}"')
    lines.append(f'tier = "{tier_str}"')
    lines.append("")

    lines.append("[build]")
    lines.append(f'base_image = "{info["base_image"]}"')
    lines.append(f'runtime_image = "{runtime_img}"')
    lines.append('arch = "amd64"')
    lines.append("")

    dl = get_download_info(name, version)
    lines.append("[download]")
    lines.append(f'url = "{dl["url"]}"')
    lines.append(f'binary_name = "{dl["binary_name"]}"')
    lines.append(f'filename = "{dl["filename"]}"')
    lines.append(f'checksum = "PENDING"')
    lines.append("")

    lines.append("[constraints]")
    lines.append(f'nonroot = {str(info["nonroot"]).lower()}')
    lines.append(f'scratch = {str(is_scratch).lower()}')
    lines.append("")

    if ports:
        lines.append("[ports]")
        for k, v in ports.items():
            lines.append(f'{k} = {v}')
        lines.append("")

    ep = info["entrypoint"]
    cmd = info["cmd"]

    lines.append("[labels]")
    lines.append(f'"org.opencontainers.image.title" = "{name}"')
    lines.append(f'"org.opencontainers.image.description" = "{description}"')
    lines.append(f'"org.opencontainers.image.version" = "{version}"')
    lines.append(f'"org.opencontainers.image.vendor" = "{vendor}"')
    if source:
        lines.append(f'"org.opencontainers.image.source" = "{source}"')
    lines.append(f'"evergreen.image.tier" = "{tier_str}"')
    lines.append(f'"evergreen.constraint.nonroot" = "{str(info["nonroot"]).lower()}"')
    lines.append(f'"evergreen.constraint.scratch" = "{str(is_scratch).lower()}"')
    lines.append(f'"evergreen.base.image" = "{runtime_img}"')

    metrics_native = info["labels"].get("evergreen.metrics.native", "ztunnel")
    lines.append(f'"evergreen.metrics.native" = "{metrics_native}"')

    health_type = info["labels"].get("evergreen.health.type", "exec")
    lines.append(f'"evergreen.health.type" = "{health_type}"')

    signal_handling = info["labels"].get("evergreen.hft.signal-handling", "")
    if signal_handling:
        lines.append(f'"evergreen.hft.signal-handling" = "{signal_handling}"')

    shutdown_timeout = info["labels"].get("evergreen.hft.shutdown-timeout", "")
    if shutdown_timeout:
        lines.append(f'"evergreen.hft.shutdown-timeout" = "{shutdown_timeout}"')

    return "\n".join(lines) + "\n"


def main():
    images_dir = os.path.join(BASE_DIR, "images")

    all_targets = TIER1_IMAGES + TIER2_IMAGES + TIER3_IMAGES

    generated = 0
    skipped = 0
    missing = []

    for name in all_targets:
        img_dir = os.path.join(images_dir, name)
        manifest_path = os.path.join(img_dir, "manifest.toml")
        dockerfile_path = os.path.join(img_dir, "Dockerfile")

        if os.path.exists(manifest_path):
            skipped += 1
            continue

        if not os.path.exists(dockerfile_path):
            missing.append(name)
            continue

        info = parse_dockerfile(dockerfile_path)
        manifest = generate_manifest(name, info)

        os.makedirs(img_dir, exist_ok=True)
        with open(manifest_path, "w") as f:
            f.write(manifest)
        generated += 1
        print(f"  generated: {name} (v{info['version']}, tier {info['tier']})")

    print(f"\nDone: {generated} generated, {skipped} skipped (already exist)")
    if missing:
        print(f"Missing Dockerfiles ({len(missing)}): {', '.join(missing)}")


if __name__ == "__main__":
    main()
