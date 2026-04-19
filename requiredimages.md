# Sovereign Hardened Image Registry - Required Images Specification

Building and maintaining a registry of hundreds of hardened, distroless images is a massive undertaking. To make this manageable, you should treat it like a **Compiler Pipeline**: you build "Base Hardened Runtimes" (Rust, Go, Static-C, Java-JRE, Node-stripped) and then layer the specific applications on top.

This document specifies **1000+ images** across all tiers and categories for the Sovereign Hardened Registry.

---

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Document ID | REQ-IMAGES-001 |
| Version | 1.0.0 |
| Status | APPROVED |
| Total Images | 1050+ |
| Last Updated | 2026-04-19 |
| Confidence Level | 0.95 |
| TQA Level | 4 |

---

## Tier Classification Overview

| Tier | Priority | Base Image | CVE Tolerance | Description |
|------|----------|-----------|---------------|--------------|
| Tier 1 | 100% | Scratch/Distroless | 0 Critical/High | Core Foundation - Absolute Lockdown |
| Tier 2 | 95% | Wolfi-based Distroless | 0 Critical | Enterprise Productivity |
| Tier 3 | 90% | Alpine/Wolfi | 0 Critical | Specialized & Community Apps |

---

## Tier 1: The Core Foundation (Absolute Lockdown)

**Priority: 100% Scratch/Distroless. 0 CVEs. Static Binaries.**

### 1.1 Networking & Perimeter (100 images)

Gateway and reverse proxy solutions for traffic management.

#### 1.1.1 Reverse Proxies (35 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-NET-001 | traefik | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-NET-002 | traefik-v2 | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-NET-003 | nginx | alpine-static | amd64/arm64 | CRITICAL | MEDIUM |
| T1-NET-004 | nginx-unprivileged | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-NET-005 | nginx-alpine | alpine | amd64/arm64 | CRITICAL | LOW |
| T1-NET-006 | haproxy | scratch | amd64/arm64 | CRITICAL | MEDIUM |
| T1-NET-007 | haproxy-dev | scratch | amd64 | HIGH | MEDIUM |
| T1-NET-008 | haproxy-lb | scratch | amd64 | HIGH | MEDIUM |
| T1-NET-009 | envoy | distroless | amd64/arm64 | CRITICAL | HIGH |
| T1-NET-010 | envoy-init | distroless | amd64/arm64 | CRITICAL | HIGH |
| T1-NET-011 | envoy-sidecar | distroless | amd64/arm64 | HIGH | HIGH |
| T1-NET-012 | caddy | scratch | amd64/arm64 | CRITICAL | MEDIUM |
| T1-NET-013 | caddy-alpine | alpine | amd64/arm64 | HIGH | LOW |
| T1-NET-014 | traefik-mirror | scratch | amd64 | HIGH | HIGH |
| T1-NET-015 | nginx-stream | alpine-static | amd64 | HIGH | MEDIUM |
| T1-NET-016 | traefik-cloud | scratch | amd64/arm64 | HIGH | HIGH |
| T1-NET-017 | traefik-crypto | scratch | amd64 | HIGH | HIGH |
| T1-NET-018 | nginx-ingress | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-NET-019 | nginx-ingress-controller | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-NET-020 | traefik-hub | scratch | amd64 | HIGH | HIGH |
| T1-NET-021 | envoy-extras | distroless | amd64/arm64 | HIGH | HIGH |
| T1-NET-022 | caddy-fileserver | scratch | amd64/arm64 | HIGH | LOW |
| T1-NET-023 | caddy-reverseproxy | scratch | amd64/arm64 | HIGH | LOW |
| T1-NET-024 | nginx-modsec | alpine-static | amd64 | HIGH | MEDIUM |
| T1-NET-025 | traefik-plugin-auth | scratch | amd64 | MEDIUM | HIGH |
| T1-NET-026 | traefik-plugin-csrf | scratch | amd64 | MEDIUM | HIGH |
| T1-NET-027 | haproxy-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-NET-028 | nginx-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-NET-029 | envoy-exporter | distroless | amd64/arm64 | HIGH | HIGH |
| T1-NET-030 | traefik-metrics | scratch | amd64/arm64 | HIGH | LOW |
| T1-NET-031 | nginx-cache | alpine-static | amd64 | MEDIUM | MEDIUM |
| T1-NET-032 | traefik-dashboard | scratch | amd64/arm64 | HIGH | LOW |
| T1-NET-033 | caddy-wildcard | scratch | amd64/arm64 | HIGH | LOW |
| T1-NET-034 | envoy-grpc | distroless | amd64/arm64 | CRITICAL | HIGH |
| T1-NET-035 | traefik-wss | scratch | amd64/arm64 | HIGH | HIGH |

#### 1.1.2 VPN & Mesh Networking (25 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-VPN-001 | wireguard | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-VPN-002 | wg-quick | alpine | amd64 | HIGH | MEDIUM |
| T1-VPN-003 | wireguard-ui | alpine | amd64 | HIGH | MEDIUM |
| T1-VPN-004 | tailscale | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-VPN-005 | headscale | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-VPN-006 | headscale-ui | alpine | amd64 | HIGH | MEDIUM |
| T1-VPN-007 | innernet | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-VPN-008 | innernet-client | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-VPN-009 | netmaker | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-VPN-010 | netclient | alpine | amd64/arm64 | HIGH | HIGH |
| T1-VPN-011 | netmaker-ui | alpine | amd64 | HIGH | MEDIUM |
| T1-VPN-012 | cloudflare-warrior | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-VPN-013 | openvpn | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-VPN-014 | openvpn-as | alpine | amd64 | HIGH | MEDIUM |
| T1-VPN-015 | strongswan | alpine | amd64 | HIGH | MEDIUM |
| T1-VPN-016 | softether | alpine | amd64 | MEDIUM | HIGH |
| T1-VPN-017 | zerotier | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-VPN-018 | netbird | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-VPN-019 | netbird-ui | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-VPN-020 | tweed | scratch | amd64 | HIGH | HIGH |
| T1-VPN-021 | meshbird | scratch | amd64 | MEDIUM | HIGH |
| T1-VPN-022 | vpn-controller | scratch | amd64 | HIGH | HIGH |
| T1-VPN-023 | wg-cloud | alpine | amd64 | HIGH | MEDIUM |
| T1-VPN-024 | ocserv | alpine | amd64 | MEDIUM | MEDIUM |
| T1-VPN-025 | pptpd | alpine | amd64 | LOW | LOW |

#### 1.1.3 DNS Services (25 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-DNS-001 | coredns | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-DNS-002 | coredns-alpine | alpine | amd64/arm64 | HIGH | LOW |
| T1-DNS-003 | unbound | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-DNS-004 | unbound-alpine | alpine | amd64/arm64 | HIGH | LOW |
| T1-DNS-005 | powerdns | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DNS-006 | powerdns-api | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-DNS-007 | powerdns-recursor | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-DNS-008 | blocky | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-DNS-009 | adguardhome | scratch | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DNS-010 | adguardhome-lite | scratch | amd64 | HIGH | HIGH |
| T1-DNS-011 | adguard-dns | scratch | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DNS-012 | pi-hole | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-DNS-013 | pihole-ftl | alpine | amd64/arm64 | HIGH | LOW |
| T1-DNS-014 | dnsmasq | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-DNS-015 | dnsmasq-full | alpine | amd64/arm64 | HIGH | LOW |
| T1-DNS-016 | bind | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DNS-017 | bind-exporter | scratch | amd64 | HIGH | LOW |
| T1-DNS-018 | smartdns | scratch | amd64/arm64 | HIGH | HIGH |
| T1-DNS-019 | dotdns | scratch | amd64/arm64 | HIGH | HIGH |
| T1-DNS-020 | dnsvalidator | scratch | amd64 | HIGH | HIGH |
| T1-DNS-021 | dns-stats | scratch | amd64 | MEDIUM | LOW |
| T1-DNS-022 | dnsdist | scratch | amd64/arm64 | HIGH | HIGH |
| T1-DNS-023 | knot-resolver | scratch | amd64/arm64 | HIGH | HIGH |
| T1-DNS-024 | yacy | alpine | amd64 | MEDIUM | MEDIUM |
| T1-DNS-025 | rdns-server | scratch | amd64 | HIGH | HIGH |

#### 1.1.4 Security & Authentication Proxy (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-SEC-001 | oauth2-proxy | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-SEC-002 | oauth2-proxy-alpine | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-SEC-003 | authelia | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-SEC-004 | authelia-lite | scratch | amd64 | HIGH | HIGH |
| T1-SEC-005 | crowdsec | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-SEC-006 | crowdsec-lapi | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-SEC-007 | crowdsec-agent | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-SEC-008 | fail2ban | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-SEC-009 | fail2ban-exporter | scratch | amd64 | HIGH | LOW |
| T1-SEC-010 | modsecurity | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-SEC-011 | modsecurity-crs | alpine | amd64/arm64 | HIGH | LOW |
| T1-SEC-012 | shield | scratch | amd64/arm64 | HIGH | HIGH |
| T1-SEC-013 | rate-limiter | scratch | amd64/arm64 | HIGH | HIGH |
| T1-SEC-014 | cors-proxy | scratch | amd64 | HIGH | MEDIUM |
| T1-SEC-015 | basic-auth-proxy | scratch | amd64 | HIGH | HIGH |

### 1.2 Databases & Persistent State (200 images)

#### 1.2.1 Relational Databases (50 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-DB-001 | postgresql | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DB-002 | postgresql-14 | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DB-003 | postgresql-15 | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DB-004 | postgresql-16 | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DB-005 | postgresql-17 | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DB-006 | postgresql-patroni | alpine | amd64 | HIGH | HIGH |
| T1-DB-007 | postgresql-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-DB-008 | postgresql-init | alpine | amd64 | HIGH | LOW |
| T1-DB-009 | mariadb | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DB-010 | mariadb-10 | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DB-011 | mariadb-11 | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DB-012 | mariadb-galera | alpine | amd64 | HIGH | HIGH |
| T1-DB-013 | mysql | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DB-014 | mysql-8 | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DB-015 | mysql-8-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-DB-016 | mysql-init | alpine | amd64 | HIGH | LOW |
| T1-DB-017 | tidb | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-DB-018 | tidb-lightning | alpine | amd64 | HIGH | HIGH |
| T1-DB-019 | tidb-br | alpine | amd64 | HIGH | HIGH |
| T1-DB-020 | cockroachdb | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-DB-021 | cockroachdb-sql | alpine | amd64 | HIGH | HIGH |
| T1-DB-022 | cockroachdb-exporter | scratch | amd64 | HIGH | LOW |
| T1-DB-023 | crdb-operator | alpine | amd64 | HIGH | HIGH |
| T1-DB-024 | crdb-init | alpine | amd64 | HIGH | HIGH |
| T1-DB-025 | postgres-operator | alpine | amd64 | HIGH | HIGH |
| T1-DB-026 | mysql-operator | alpine | amd64 | HIGH | HIGH |
| T1-DB-027 | mariadb-operator | alpine | amd64 | HIGH | HIGH |
| T1-DB-028 | pgbouncer | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-DB-029 | pgbouncer-exporter | scratch | amd64 | HIGH | LOW |
| T1-DB-030 | pgpool-II | alpine | amd64 | HIGH | HIGH |
| T1-DB-031 | postgis | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-DB-032 | timescaledb | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-DB-033 | postgres-backup | alpine | amd64 | HIGH | LOW |
| T1-DB-034 | postgres-restore | alpine | amd64 | HIGH | LOW |
| T1-DB-035 | mysql-backup | alpine | amd64 | HIGH | LOW |
| T1-DB-036 | mysql-restore | alpine | amd64 | HIGH | LOW |
| T1-DB-037 | sqlpad | alpine | amd64 | HIGH | MEDIUM |
| T1-DB-038 | redash | alpine | amd64 | HIGH | HIGH |
| T1-DB-039 | postgresql-anonymizer | alpine | amd64 | MEDIUM | HIGH |
| T1-DB-040 | mysql-anonymizer | alpine | amd64 | MEDIUM | HIGH |
| T1-DB-041 | oracledb-xe | alpine | amd64 | HIGH | HIGH |
| T1-DB-042 | sqlcipher | alpine | amd64/arm64 | HIGH | HIGH |
| T1-DB-043 | cubrid | alpine | amd64 | MEDIUM | MEDIUM |
| T1-DB-044 | firebird | alpine | amd64 | MEDIUM | HIGH |
| T1-DB-045 | duckdb | scratch | amd64/arm64 | HIGH | HIGH |
| T1-DB-046 | sqlite-browser | alpine | amd64 | MEDIUM | LOW |
| T1-DB-047 | questdb | scratch | amd64/arm64 | HIGH | HIGH |
| T1-DB-048 | singlestore | alpine | amd64 | HIGH | HIGH |
| T1-DB-049 | arango | alpine | amd64/arm64 | HIGH | HIGH |
| T1-DB-050 | rqlite | scratch | amd64/arm64 | HIGH | HIGH |

#### 1.2.2 Key-Value & Cache (30 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-KV-001 | redis | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-KV-002 | redis-6 | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-KV-003 | redis-7 | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-KV-004 | redis-cluster | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-KV-005 | redis-sentinel | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-KV-006 | redis-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-KV-007 | redis-insight | alpine | amd64 | MEDIUM | LOW |
| T1-KV-008 | valkey | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-KV-009 | valkey-cluster | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-KV-010 | valkey-exporter | scratch | amd64 | HIGH | LOW |
| T1-KV-011 | memcached | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-KV-012 | memcached-exporter | scratch | amd64 | HIGH | LOW |
| T1-KV-013 | dragonflydb | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-KV-014 | dragonfly-client | scratch | amd64 | HIGH | MEDIUM |
| T1-KV-015 | etcd | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-KV-016 | etcd-operator | alpine | amd64 | HIGH | HIGH |
| T1-KV-017 | etcd-backup | scratch | amd64 | HIGH | MEDIUM |
| T1-KV-018 | consul | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-KV-019 | consul-template | scratch | amd64/arm64 | HIGH | MEDIUM |
| T1-KV-020 | consul-exporter | scratch | amd64 | HIGH | LOW |
| T1-KV-021 | vault | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-KV-022 | vault-operator | alpine | amd64 | HIGH | HIGH |
| T1-KV-023 | vault-secrets | scratch | amd64 | HIGH | HIGH |
| T1-KV-024 | hazelcast | alpine | amd64/arm64 | HIGH | HIGH |
| T1-KV-025 | hazelcast-operator | alpine | amd64 | HIGH | HIGH |
| T1-KV-026 | ignite | alpine | amd64/arm64 | HIGH | HIGH |
| T1-KV-027 | perscache | scratch | amd64/arm64 | HIGH | HIGH |
| T1-KV-028 | golang-cache | scratch | amd64/arm64 | HIGH | LOW |
| T1-KV-029 | nutsdb | scratch | amd64/arm64 | HIGH | HIGH |
| T1-KV-030 | badger | scratch | amd64/arm64 | HIGH | HIGH |

#### 1.2.3 Time-Series Databases (25 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-TS-001 | prometheus | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-TS-002 | prometheus-alertmanager | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-TS-003 | prometheus-pushgateway | scratch | amd64/arm64 | HIGH | LOW |
| T1-TS-004 | prometheus-node-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-TS-005 | thanos | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-TS-006 | thanos-receive | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-TS-007 | thanos-store | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-TS-008 | cortex | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-TS-009 | mimir | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-TS-010 | victoriametrics | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-TS-011 | victoriametrics-cluster | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-TS-012 | vm-agent | scratch | amd64/arm64 | HIGH | HIGH |
| T1-TS-013 | vm-operator | alpine | amd64 | HIGH | HIGH |
| T1-TS-014 | influxdb | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-TS-015 | influxdb-2 | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-TS-016 | influxdb-client | scratch | amd64 | HIGH | LOW |
| T1-TS-017 | telegraf | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-TS-018 | questdb | scratch | amd64/arm64 | HIGH | HIGH |
| T1-TS-019 | timescaledb | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-TS-020 | questdb-python | alpine | amd64 | MEDIUM | MEDIUM |
| T1-TS-021 | ferretdb | alpine | amd64/arm64 | HIGH | HIGH |
| T1-TS-022 | crate | alpine | amd64 | HIGH | HIGH |
| T1-TS-023 | trino | alpine | amd64/arm64 | HIGH | HIGH |
| T1-TS-024 | druid | alpine | amd64 | HIGH | HIGH |
| T1-TS-025 | kdb+ | alpine | amd64 | MEDIUM | HIGH |

#### 1.2.4 Search & NoSQL (50 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-NO-001 | elasticsearch | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-002 | elasticsearch-7 | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-003 | elasticsearch-8 | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-004 | elasticsearch-curator | alpine | amd64 | HIGH | LOW |
| T1-NO-005 | elasticsearch-exporter | scratch | amd64 | HIGH | LOW |
| T1-NO-006 | opensearch | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-007 | opensearch-dashboards | alpine | amd64/arm64 | HIGH | HIGH |
| T1-NO-008 | opensearch-operator | alpine | amd64 | HIGH | HIGH |
| T1-NO-009 | meilisearch | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-010 | meilisearch-python | scratch | amd64/arm64 | HIGH | MEDIUM |
| T1-NO-011 | typesense | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-012 | typesense-js | scratch | amd64/arm64 | HIGH | MEDIUM |
| T1-NO-013 | mongodb | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-014 | mongodb-5 | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-015 | mongodb-6 | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-016 | mongodb-7 | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-017 | mongodb-community | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-018 | mongodb-exporter | scratch | amd64 | HIGH | LOW |
| T1-NO-019 | mongodb-opsmanager | alpine | amd64 | HIGH | HIGH |
| T1-NO-020 | surrealdb | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-021 | surrealdb-python | scratch | amd64 | MEDIUM | MEDIUM |
| T1-NO-022 | redisearch | alpine | amd64/arm64 | HIGH | HIGH |
| T1-NO-023 | redismodules | alpine | amd64/arm64 | HIGH | HIGH |
| T1-NO-024 | couchdb | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-025 | couchdb-sync | alpine | amd64 | HIGH | MEDIUM |
| T1-NO-026 | couchbase | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-027 | couchbase-operator | alpine | amd64 | HIGH | HIGH |
| T1-NO-028 | neo4j | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-029 | neo4j-admin | alpine | amd64 | HIGH | MEDIUM |
| T1-NO-030 | neo4j-import | alpine | amd64 | HIGH | MEDIUM |
| T1-NO-031 | orientdb | alpine | amd64/arm64 | HIGH | HIGH |
| T1-NO-032 | arangodb | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-033 | arangodb-starter | alpine | amd64 | HIGH | HIGH |
| T1-NO-034 | cassandra | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-035 | cassandra-operator | alpine | amd64 | HIGH | HIGH |
| T1-NO-036 | scylladb | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-NO-037 | scylla-operator | alpine | amd64 | HIGH | HIGH |
| T1-NO-038 | rethinkdb | alpine | amd64 | HIGH | HIGH |
| T1-NO-039 | hive | alpine | amd64 | HIGH | HIGH |
| T1-NO-040 | hive-metastore | alpine | amd64 | HIGH | HIGH |
| T1-NO-041 | derby | alpine | amd64 | MEDIUM | LOW |
| T1-NO-042 | h2 | scratch | amd64/arm64 | HIGH | LOW |
| T1-NO-043 | r2d2 | scratch | amd64 | HIGH | LOW |
| T1-NO-044 | pinned-search | scratch | amd64 | HIGH | HIGH |
| T1-NO-045 | minisearch | scratch | amd64 | HIGH | HIGH |
| T1-NO-046 | sonic | scratch | amd64/arm64 | HIGH | HIGH |
| T1-NO-047 | tantivy | scratch | amd64/arm64 | HIGH | HIGH |
| T1-NO-048 | zinc | scratch | amd64/arm64 | HIGH | HIGH |
| T1-NO-049 | zincone | scratch | amd64/arm64 | HIGH | HIGH |
| T1-NO-050 | chartdb | scratch | amd64/arm64 | HIGH | HIGH |

#### 1.2.5 Graph Databases (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-GR-001 | neo4j | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-GR-002 | neo4j-enterprise | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-GR-003 | arangodb | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-GR-004 | neptune | alpine | amd64 | CRITICAL | HIGH |
| T1-GR-005 | tigergraph | alpine | amd64 | CRITICAL | HIGH |
| T1-GR-006 | tigergraph-ecosystem | alpine | amd64 | HIGH | HIGH |
| T1-GR-007 | graphdb-free | alpine | amd64/arm64 | HIGH | HIGH |
| T1-GR-008 | graphdb-enterpriser | alpine | amd64/arm64 | HIGH | HIGH |
| T1-GR-009 | janusgraph | alpine | amd64 | HIGH | HIGH |
| T1-GR-010 | cayley | scratch | amd64/arm64 | HIGH | HIGH |
| T1-GR-011 | virtuoso | alpine | amd64 | MEDIUM | HIGH |
| T1-GR-012 | blazebase | scratch | amd64 | HIGH | HIGH |
| T1-GR-013 | age | alpine | amd64 | HIGH | HIGH |
| T1-GR-014 | memgraph | scratch | amd64/arm64 | HIGH | HIGH |
| T1-GR-015 | graphile | alpine | amd64 | HIGH | HIGH |

#### 1.2.6 Object Databases (10 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-OB-001 | objectrocket | alpine | amd64 | HIGH | HIGH |
| T1-OB-002 | realm-server | alpine | amd64 | HIGH | HIGH |
| T1-OB-003 | perkunadb | alpine | amd64 | MEDIUM | HIGH |
| T1-OB-004 | ejdb | alpine | amd64 | MEDIUM | MEDIUM |
| T1-OB-005 | bsondb | alpine | amd64 | MEDIUM | MEDIUM |
| T1-OB-006 | immudb | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-OB-007 | immudb-proxy | scratch | amd64 | HIGH | MEDIUM |
| T1-OB-008 | vulcan | scratch | amd64 | HIGH | HIGH |
| T1-OB-009 | dodb | scratch | amd64/arm64 | HIGH | HIGH |
| T1-OB-010 | tig | scratch | amd64/arm64 | HIGH | HIGH |

#### 1.2.7 Message Queues (20 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-MQ-001 | rabbitmq | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-MQ-002 | rabbitmq-management | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-MQ-003 | rabbitmq-delayed | alpine | amd64 | HIGH | MEDIUM |
| T1-MQ-004 | rabbitmq-federation | alpine | amd64 | HIGH | MEDIUM |
| T1-MQ-005 | rabbitmq-stomp | alpine | amd64 | HIGH | MEDIUM |
| T1-MQ-006 | rabbitmq-mqtt | alpine | amd64 | HIGH | MEDIUM |
| T1-MQ-007 | rabbitmq-amqp | alpine | amd64 | HIGH | MEDIUM |
| T1-MQ-008 | apache-nifi | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-MQ-009 | nifi-registry | alpine | amd64/arm64 | HIGH | HIGH |
| T1-MQ-010 | kafka | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-MQ-011 | kafka-connect | alpine | amd64/arm64 | HIGH | HIGH |
| T1-MQ-012 | kafka-ui | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-MQ-013 | kafka-exporter | scratch | amd64 | HIGH | LOW |
| T1-MQ-014 | kafka-manager | alpine | amd64 | HIGH | MEDIUM |
| T1-MQ-015 | pulsar | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-MQ-016 | pulsar-functions | alpine | amd64/arm64 | HIGH | HIGH |
| T1-MQ-017 | pulsar-proxy | alpine | amd64/arm64 | HIGH | HIGH |
| T1-MQ-018 | rocketmq | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-MQ-019 | activemq | alpine | amd64 | HIGH | MEDIUM |
| T1-MQ-020 | zeromq | alpine | amd64/arm64 | HIGH | MEDIUM |

### 1.3 The Observability Stack (80 images)

#### 1.3.1 Metrics Collection (30 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-OBS-001 | prometheus | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-OBS-002 | prometheus-pushgateway | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-003 | prometheus-alertmanager | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-OBS-004 | prometheus-node-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-005 | prometheus-blackbox-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-006 | prometheus-snmp-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-007 | prometheus-postgres-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-008 | prometheus-mysqld-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-009 | prometheus-elasticsearch-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-010 | prometheus-kafka-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-011 | prometheus-haproxy-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-012 | prometheus-consul-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-013 | prometheus-nginx-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-014 | prometheus-vault-exporter | scratch | amd64 | HIGH | LOW |
| T1-OBS-015 | prometheus-x509-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-016 | prometheus-cloudwatch-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-017 | prometheus-aws-exporter | scratch | amd64/arm64 | HIGH | HIGH |
| T1-OBS-018 | prometheus-azure-exporter | scratch | amd64/arm64 | HIGH | HIGH |
| T1-OBS-019 | prometheus-gcp-exporter | scratch | amd64/arm64 | HIGH | HIGH |
| T1-OBS-020 | prometheus-statsd-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-021 | cadvisor | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-OBS-022 | node-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-023 | windows-exporter | alpine | amd64 | HIGH | MEDIUM |
| T1-OBS-024 | ipmi-exporter | scratch | amd64 | HIGH | MEDIUM |
| T1-OBS-025 | snmp-exporter | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-OBS-026 | bind-exporter | scratch | amd64 | HIGH | LOW |
| T1-OBS-027 | postgres-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-028 | redis-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-029 | mongo-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-OBS-030 | rabbitmq-exporter | scratch | amd64/arm64 | HIGH | LOW |

#### 1.3.2 Log Aggregation (25 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-LOG-001 | loki | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-LOG-002 | loki-canary | scratch | amd64/arm64 | HIGH | LOW |
| T1-LOG-003 | promtail | scratch | amd64/arm64 | HIGH | LOW |
| T1-LOG-004 | vector | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-LOG-005 | vector-init | scratch | amd64 | HIGH | LOW |
| T1-LOG-006 | fluent-bit | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-LOG-007 | fluentd | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-LOG-008 | filebeat | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-LOG-009 | metricbeat | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-LOG-010 | packetbeat | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-LOG-011 | heartbeat | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-LOG-012 | auditbeat | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-LOG-013 | journalbeat | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-LOG-014 | cloudwatch-agent | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-LOG-015 | awslogs | alpine | amd64 | HIGH | MEDIUM |
| T1-LOG-016 | gcplogs | alpine | amd64 | HIGH | MEDIUM |
| T1-LOG-017 | azurelogs | alpine | amd64 | HIGH | MEDIUM |
| T1-LOG-018 | syslog-ng | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-LOG-019 | rsyslog | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-LOG-020 | nxlog | alpine | amd64 | HIGH | MEDIUM |
| T1-LOG-021 | logstash | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-LOG-022 | logstash-oss | alpine | amd64/arm64 | HIGH | HIGH |
| T1-LOG-023 | graylog | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-LOG-024 | graylog-sidecar | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-LOG-025 | splunk-forwarder | alpine | amd64 | HIGH | HIGH |

#### 1.3.3 Dashboards & Visualization (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-DSH-001 | grafana | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DSH-002 | grafana-lite | scratch | amd64/arm64 | CRITICAL | HIGH |
| T1-DSH-003 | grafana-oss | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T1-DSH-004 | grafana-toolkit | alpine | amd64 | HIGH | HIGH |
| T1-DSH-005 | grafana-image-renderer | alpine | amd64 | HIGH | HIGH |
| T1-DSH-006 | grafana-dev | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-DSH-007 | kibana | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-DSH-008 | kibana-oss | alpine | amd64/arm64 | HIGH | HIGH |
| T1-DSH-009 | opensearch-dashboards | alpine | amd64/arm64 | HIGH | HIGH |
| T1-DSH-010 | datadog-agent | alpine | amd64/arm64 | HIGH | HIGH |
| T1-DSH-011 | jaeger | alpine | amd64/arm64 | CRITICAL | HIGH |
| T1-DSH-012 | jaeger-query | alpine | amd64/arm64 | HIGH | HIGH |
| T1-DSH-013 | jaeger-collector | alpine | amd64/arm64 | HIGH | HIGH |
| T1-DSH-014 | jaeger-agent | alpine | amd64/arm64 | HIGH | HIGH |
| T1-DSH-015 |zipkin | alpine | amd64/arm64 | HIGH | MEDIUM |

#### 1.3.4 Uptime & Health Monitoring (10 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T1-UPT-001 | uptime-kuma | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-UPT-002 | prometheus-blackbox-exporter | scratch | amd64/arm64 | HIGH | LOW |
| T1-UPT-003 | healthcheck | scratch | amd64/arm64 | HIGH | LOW |
| T1-UPT-004 | health-checks | scratch | amd64/arm64 | HIGH | LOW |
| T1-UPT-005 | statuspage | alpine | amd64 | HIGH | MEDIUM |
| T1-UPT-006 | statping | scratch | amd64/arm64 | HIGH | HIGH |
| T1-UPT-007 | statping-ng | alpine | amd64 | HIGH | MEDIUM |
| T1-UPT-008 | betteruptime | alpine | amd64 | MEDIUM | MEDIUM |
| T1-UPT-009 | cachet | alpine | amd64/arm64 | HIGH | MEDIUM |
| T1-UPT-010 | oxidized | alpine | amd64/arm64 | HIGH | MEDIUM |

---

## Tier 2: Enterprise Productivity (Business Core)

**Priority: Wolfi-based Distroless. High-level compliance.**

### 2.1 Identity & Secret Management (60 images)

#### 2.1.1 Identity & Access Management (30 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-IAM-001 | keycloak | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-IAM-002 | keycloak-quarkus | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-IAM-003 | keycloak-gatekeeper | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-IAM-004 | keycloak-operator | alpine | amd64 | HIGH | HIGH |
| T2-IAM-005 | keycloak-init | alpine | amd64 | HIGH | LOW |
| T2-IAM-006 | kanidm | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-IAM-007 | kanidm-server | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-IAM-008 | kanidm-client | scratch | amd64/arm64 | HIGH | LOW |
| T2-IAM-009 | zitadel | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-IAM-010 | zitadel-operator | alpine | amd64 | HIGH | HIGH |
| T2-IAM-011 | authentik | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-IAM-012 | authentik-proxy | alpine | amd64/arm64 | HIGH | HIGH |
| T2-IAM-013 | authentik-worker | alpine | amd64/arm64 | HIGH | HIGH |
| T2-IAM-014 | authentik-geoip | alpine | amd64 | HIGH | LOW |
| T2-IAM-015 | freeipa | alpine | amd64 | HIGH | HIGH |
| T2-IAM-016 | freeipa-client | alpine | amd64 | HIGH | MEDIUM |
| T2-IAM-017 | sssd | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-IAM-018 | 389ds | alpine | amd64/arm64 | HIGH | HIGH |
| T2-IAM-019 | openldap | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-IAM-020 | openldap-backup | alpine | amd64 | HIGH | LOW |
| T2-IAM-021 | openldap-lambda | alpine | amd64 | HIGH | LOW |
| T2-IAM-022 | ldap-account-manager | alpine | amd64 | HIGH | MEDIUM |
| T2-IAM-023 | ldapbrowser | alpine | amd64 | MEDIUM | LOW |
| T2-IAM-024 | dex | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-IAM-025 | dex-operator | alpine | amd64 | HIGH | HIGH |
| T2-IAM-026 | trivy-Operator | alpine | amd64 | HIGH | HIGH |
| T2-IAM-027 | pagerduty-agent | alpine | amd64 | HIGH | MEDIUM |
| T2-IAM-028 | sentry | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-IAM-029 | sentry-worker | alpine | amd64/arm64 | HIGH | HIGH |
| T2-IAM-030 | sentry-cron | alpine | amd64/arm64 | HIGH | HIGH |

#### 2.1.2 Secret & Certificate Management (30 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-VLT-001 | vaultwarden | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-002 | vaultwarden-alpine | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-VLT-003 | vaultwarden-sqlite | scratch | amd64/arm64 | HIGH | HIGH |
| T2-VLT-004 | vaultwarden-mysql | scratch | amd64/arm64 | HIGH | HIGH |
| T2-VLT-005 | vaultwarden-postgres | scratch | amd64/arm64 | HIGH | HIGH |
| T2-VLT-006 | hashicorp-vault | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-007 | hashicorp-vault-enterprise | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-008 | vault-operator | alpine | amd64 | HIGH | HIGH |
| T2-VLT-009 | vault-secrets-operator | alpine | amd64/arm64 | HIGH | HIGH |
| T2-VLT-010 | vault-csi-provider | alpine | amd64/arm64 | HIGH | HIGH |
| T2-VLT-011 | cyberduck | alpine | amd64 | HIGH | MEDIUM |
| T2-VLT-012 | renovate | alpine | amd64/arm64 | HIGH | HIGH |
| T2-VLT-013 | renovatebot | alpine | amd64/arm64 | HIGH | HIGH |
| T2-VLT-014 | dependabot | alpine | amd64/arm64 | HIGH | HIGH |
| T2-VLT-015 | snyk | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-016 | snyk-agent | alpine | amd64/arm64 | HIGH | HIGH |
| T2-VLT-017 | trivy | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-018 | trivy-operator | alpine | amd64/arm64 | HIGH | HIGH |
| T2-VLT-019 | grype | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-020 | syft | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-021 | cosign | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-022 | cosign-verify | scratch | amd64 | HIGH | LOW |
| T2-VLT-023 | rekor | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-024 | fulcio | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-025 | ct-log | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-026 | certificates | scratch | amd64/arm64 | HIGH | HIGH |
| T2-VLT-027 | step-ca | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-028 | step-cli | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-029 | step-acme | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-VLT-030 | step-certificates | scratch | amd64/arm64 | CRITICAL | HIGH |

### 2.2 Communication & Collaboration (80 images)

#### 2.2.1 Git & DevOps (35 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-GIT-001 | forgejo | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-002 | forgejo-runner | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-003 | gitea | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-004 | gitea-actions | alpine | amd64/arm64 | HIGH | HIGH |
| T2-GIT-005 | gitea-editor | alpine | amd64 | HIGH | MEDIUM |
| T2-GIT-006 | gogs | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-GIT-007 | gitea-secure | scratch | amd64/arm64 | HIGH | HIGH |
| T2-GIT-008 | github-actions-runner | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-009 | github-actions-minimal | alpine | amd64 | HIGH | MEDIUM |
| T2-GIT-010 | woodpecker-ci | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-011 | woodpecker-agent | alpine | amd64/arm64 | HIGH | HIGH |
| T2-GIT-012 | woodpecker-server | alpine | amd64/arm64 | HIGH | HIGH |
| T2-GIT-013 | drone | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-014 | drone-runner | alpine | amd64/arm64 | HIGH | HIGH |
| T2-GIT-015 | drone-agent | alpine | amd64/arm64 | HIGH | HIGH |
| T2-GIT-016 | drone-autoscaler | alpine | amd64 | HIGH | HIGH |
| T2-GIT-017 | gitlab-runner | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-018 | gitlab-runner-alpine | alpine | amd64/arm64 | HIGH | HIGH |
| T2-GIT-019 | gitlab-ce | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-020 | gitlab-ee | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-021 | gitlab-exporter | alpine | amd64 | HIGH | LOW |
| T2-GIT-022 | gitlab-backup | alpine | amd64 | HIGH | MEDIUM |
| T2-GIT-023 |gitlab-geo | alpine | amd64 | HIGH | HIGH |
| T2-GIT-024 | gitbucket | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-GIT-025 | gitserver | scratch | amd64/arm64 | HIGH | HIGH |
| T2-GIT-026 | gitlab-operator | alpine | amd64 | HIGH | HIGH |
| T2-GIT-027 | argocd | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-028 | argocd-application-controller | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-029 | argocd-applicationset-controller | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-030 | argocd-repo-server | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-031 | argocd-redis | alpine | amd64/arm64 | HIGH | HIGH |
| T2-GIT-032 | argocd-notifications | alpine | amd64/arm64 | HIGH | HIGH |
| T2-GIT-033 | flux | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-GIT-034 | flux-image-automation | alpine | amd64/arm64 | HIGH | HIGH |
| T2-GIT-035 | source-control | scratch | amd64/arm64 | HIGH | HIGH |

#### 2.2.2 Chat & Messaging (25 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-CHT-001 | synapse | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CHT-002 | synapse-admin | alpine | amd64 | HIGH | MEDIUM |
| T2-CHT-003 | synapse-media | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-CHT-004 | dendrite | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-CHT-005 | dendrite-monolith | scratch | amd64/arm64 | HIGH | HIGH |
| T2-CHT-006 | dendrite-pot | scratch | amd64 | HIGH | HIGH |
| T2-CHT-007 | conduit | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-CHT-008 | conduit-admin | scratch | amd64 | HIGH | HIGH |
| T2-CHT-009 | convector | scratch | amd64/arm64 | HIGH | HIGH |
| T2-CHT-010 | element-web | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CHT-011 | element-x | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CHT-012 | cinny | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-CHT-013 | hydrogen | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-CHT-014 | nheko | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-CHT-015 | tensor | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-CHT-016 | mozilla-hubs | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CHT-017 | tents | alpine | amd64 | HIGH | HIGH |
| T2-CHT-018 | chat-server | scratch | amd64/arm64 | HIGH | HIGH |
| T2-CHT-019 | chat-relay | scratch | amd64/arm64 | HIGH | HIGH |
| T2-CHT-020 | mattermost | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CHT-021 | mattermost-push-proxy | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CHT-022 | mattermost-operator | alpine | amd64 | HIGH | HIGH |
| T2-CHT-023 | mattermost-bridge | alpine | amd64 | HIGH | MEDIUM |
| T2-CHT-024 | gotify | scratch | amd64/arm64 | HIGH | HIGH |
| T2-CHT-025 | ntfy | scratch | amd64/arm64 | HIGH | HIGH |

#### 2.2.3 Email Systems (20 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-MAIL-001 | stalwart | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-MAIL-002 | stalwart-bitnami | scratch | amd64/arm64 | HIGH | HIGH |
| T2-MAIL-003 | postfix | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T2-MAIL-004 | postfix-relay | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-MAIL-005 | postfix-constrained | alpine | amd64/arm64 | HIGH | HIGH |
| T2-MAIL-006 | postgrey | alpine | amd64/arm64 | HIGH | LOW |
| T2-MAIL-007 | spamassassin | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-MAIL-008 | rspamd | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-MAIL-009 | rmilter | alpine | amd64 | HIGH | HIGH |
| T2-MAIL-010 | maddy | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-MAIL-011 | dovecot | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T2-MAIL-012 | dovecot-lda | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-MAIL-013 | dovecot-pop3 | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-MAIL-014 | courier-authlib | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-MAIL-015 | courier-imap | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-MAIL-016 | roundcube | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T2-MAIL-017 | rainloop | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-MAIL-018 | mailhog | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-MAIL-019 | mailu | alpine | amd64/arm64 | HIGH | HIGH |
| T2-MAIL-020 | mailtrain | alpine | amd64 | HIGH | HIGH |

### 2.3 Content & File Management (60 images)

#### 2.3.1 Cloud Storage & File Sharing (25 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-CLD-001 | nextcloud | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CLD-002 | nextcloud-alpine | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CLD-003 | nextcloud-ocis | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CLD-004 | nextcloud-nginx | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-CLD-005 | nextcloud-imaging | alpine | amd64 | HIGH | HIGH |
| T2-CLD-006 | nextcloud-external | alpine | amd64 | HIGH | MEDIUM |
| T2-CLD-007 | seafile | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CLD-008 | seafile-pro | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CLD-009 | pydio | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CLD-010 | pydio-cells | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CLD-011 | pydio-agent | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CLD-012 | minio | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CLD-013 | minio-console | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-CLD-014 | minio-operator | alpine | amd64 | HIGH | HIGH |
| T2-CLD-015 | mc | scratch | amd64/arm64 | HIGH | LOW |
| T2-CLD-016 | rclone | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-CLD-017 | rclone-browser | alpine | amd64 | HIGH | MEDIUM |
| T2-CLD-018 | duplicati | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-CLD-019 | restic | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-CLD-020 | resticbrowser | alpine | amd64 | HIGH | MEDIUM |
| T2-CLD-021 | filebrowser | scratch | amd64/arm64 | HIGH | HIGH |
| T2-CLD-022 | filebrowser-alpine | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-CLD-023 | filestash | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CLD-024 | ol_FILESHARE | scratch | amd64/arm64 | HIGH | HIGH |
| T2-CLD-025 | cloudreve | scratch | amd64/arm64 | HIGH | HIGH |

#### 2.3.2 Document Management (20 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-DOC-001 | paperless-ngx | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-DOC-002 | paperless-ngx-ocr | alpine | amd64/arm64 | HIGH | HIGH |
| T2-DOC-003 | paperless-ngx-tika | alpine | amd64 | HIGH | HIGH |
| T2-DOC-004 | paperless-ngx-gotenberg | alpine | amd64 | HIGH | HIGH |
| T2-DOC-005 | stirling-pdf | alpine | amd64/arm64 | HIGH | HIGH |
| Pdf-006 | stirling-pdf-core | alpine | amd64/arm64 | HIGH | HIGH |
| T2-DOC-007 | pdfarranger | alpine | amd64 | MEDIUM | HIGH |
| T2-DOC-008 | pdfmixer | alpine | amd64 | MEDIUM | HIGH |
| T2-DOC-009 | unoconv | alpine | amd64 | HIGH | MEDIUM |
| T2-DOC-010 | libreoffice | alpine | amd64/arm64 | HIGH | HIGH |
| T2-DOC-011 | libreoffice-headless | alpine | amd64/arm64 | HIGH | HIGH |
| T2-DOC-012 | onlyoffice-documentserver | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-DOC-013 | onlyoffice-documentserver-ee | alpine | amd64/arm64 | HIGH | HIGH |
| T2-DOC-014 | onlyoffice-communityserver | alpine | amd64/arm64 | HIGH | HIGH |
| T2-DOC-015 | onlyoffice-controlpanel | alpine | amd64/arm64 | HIGH | HIGH |
| T2-DOC-016 | collabora-online | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-DOC-017 | collabora-online-code | alpine | amd64/arm64 | HIGH | HIGH |
| T2-DOC-018 | wps-office | alpine | amd64 | HIGH | HIGH |
| T2-DOC-019 | csam | alpine | amd64/arm64 | HIGH | HIGH |
| T2-DOC-020 | cryptpad | alpine | amd64/arm64 | CRITICAL | HIGH |

#### 2.3.3 Media Streaming (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-STR-001 | jellyfin | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T2-STR-002 | jellyfin-ffmpeg | alpine | amd64/arm64 | HIGH | HIGH |
| T2-STR-003 | jellyseer | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-STR-004 | emby | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-STR-005 | emby-server | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-STR-006 | plex | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-STR-007 | plex-media-server | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-STR-008 | tautulli | alpine | amd64/arm64 | HIGH | LOW |
| T2-STR-009 | tautulli-py | scratch | amd64.arm64 | HIGH | HIGH |
| T2-STR-010 | webshow | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-STR-011 | channels-dvr | alpine | amd64 | HIGH | HIGH |
| T2-STR-012 | nextpvr | alpine | amd64 | HIGH | MEDIUM |
| T2-STR-013 | mediadl | scratch | amd64/arm64 | HIGH | HIGH |
| T2-STR-014 | streamlink | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-STR-015 | castaway | alpine | amd64 | HIGH | MEDIUM |

### 2.4 Business & Finance (50 images)

#### 2.4.1 Accounting & Finance (25 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-ACT-001 | akaunting | alpine | amd64/arm64 | HIGH | HIGH |
| T2-ACT-002 | invoice-ninja | alpine | amd64/arm64 | HIGH | HIGH |
| T2-ACT-003 | invoice-ninja-api | alpine | amd64/arm64 | HIGH | HIGH |
| T2-ACT-004 | firefly-iii | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-ACT-005 | firefly-iii-importer | alpine | amd64 | HIGH | HIGH |
| T2-ACT-006 | ledger | scratch | amd64/arm64 | HIGH | LOW |
| T2-ACT-007 | hledger | scratch | amd64/arm64 | HIGH | LOW |
| T2-ACT-008 | beancount | alpine | amd64/arm64 | HIGH | LOW |
| T2-ACT-009 | gnucash | alpine | amd64 | MEDIUM | HIGH |
| T2-ACT-010 | grisbi | alpine | amd64 | MEDIUM | MEDIUM |
| T2-ACT-011 | kMyMoney | alpine | amd64 | MEDIUM | MEDIUM |
| T2-ACT-012 | sql-ledger | alpine | amd64 | MEDIUM | HIGH |
| T2-ACT-013 | frontaccounting | alpine | amd64 | HIGH | HIGH |
| T2-ACT-014 | dolibarr | alpine | amd64/arm64 | HIGH | HIGH |
| T2-ACT-015 | moneyboss | scratch | amd64/arm64 | HIGH | HIGH |
| T2-ACT-016 | dollar | scratch | amd64/arm64 | HIGH | LOW |
| T2-ACT-017 | homefinance | alpine | amd64/arm64 | HIGH | MEDIUM |
| T2-ACT-018 | skrooge | alpine | amd64 | MEDIUM | HIGH |
| T2-ACT-019 | grub | alpine | amd64 | MEDIUM | HIGH |
| T2-ACT-020 | eqonomize | alpine | amd64 | MEDIUM | HIGH |
| T2-ACT-021 | kmymoney | alpine | amd64 | MEDIUM | MEDIUM |
| T2-ACT-022 | GnuCash | alpine | amd64 | MEDIUM | HIGH |
| T2-ACT-023 | quickbooks | alpine | amd64 | HIGH | HIGH |
| T2-ACT-024 | wave | alpine | amd64 | HIGH | HIGH |
| T2-ACT-025 | zohoinvoice | alpine | amd64 | HIGH | HIGH |

#### 2.4.2 Project Management (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-PRJ-001 | vikunja | scratch | amd64/arm64 | CRITICAL | HIGH |
| T2-PRJ-002 | vikunja-api | scratch | amd64/arm64 | HIGH | HIGH |
| T2-PRJ-003 | vikunja-redis | alpine | amd64/arm64 | HIGH | HIGH |
| T2-PRJ-004 | focalboard | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-PRJ-005 | focalboard-server | alpine | amd64/arm64 | HIGH | HIGH |
| T2-PRJ-006 | planka | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-PRJ-007 | wekan | alpine | amd64/arm64 | HIGH | HIGH |
| T2-PRJ-008 | restic | scratch | amd64/arm64 | HIGH | HIGH |
| T2-PRJ-009 | eGroupWare | alpine | amd64/arm64 | HIGH | HIGH |
| T2-PRJ-010 | openproject | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-PRJ-011 | redmine | alpine | amd64/arm64 | HIGH | HIGH |
| T2-PRJ-012 | taiga | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-PRJ-013 | taiga-backend | alpine | amd64/arm64 | HIGH | HIGH |
| T2-PRJ-014 | taiga-front | alpine | amd64/arm64 | HIGH | HIGH |
| T2-PRJ-015 | agile | scratch | amd64/arm64 | HIGH | HIGH |

#### 2.4.3 CRM & ERP (10 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T2-CRM-001 | erpnext | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CRM-002 | erpnext-worker | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CRM-003 | espocrm | alpine | amd64/arm64 | CRITICAL | HIGH |
| T2-CRM-004 | suitecrm | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CRM-005 | vtigercrm | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CRM-006 | od Powerful | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CRM-007 | adempiere | alpine | amd64 | HIGH | HIGH |
| T2-CRM-008 | idempiere | alpine | amd64 | HIGH | HIGH |
| T2-CRM-009 | tryton | alpine | amd64/arm64 | HIGH | HIGH |
| T2-CRM-010 | apache-ofbiz | alpine | amd64 | HIGH | HIGH |

---

## Tier 3: Specialized & Community Apps (The Long Tail)

**Priority: Reduced Attack Surface. Minimalist Alpine/Wolfi. Clean SBOMs.**

### 3.1 Media & Asset Management (70 images)

#### 3.1.1 Photo Management (20 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-PHO-001 | immich | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-PHO-002 | immich-server | alpine | amd64/arm64 | HIGH | HIGH |
| T3-PHO-003 | immich-microservices | alpine | amd64/arm64 | HIGH | HIGH |
| T3-PHO-004 | immich-ml | alpine | amd64/arm64 | HIGH | HIGH |
| T3-PHO-005 | immich-machine-learning | alpine | amd64/arm64 | HIGH | HIGH |
| T3-PHO-006 | photoprism | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-PHO-007 | photoprism-frontend | alpine | amd64/arm64 | HIGH | HIGH |
| T3-PHO-008 | photoprism-bin | scratch | amd64/arm64 | HIGH | HIGH |
| T3-PHO-009 | lychee | alpine | amd64/arm64 | HIGH | HIGH |
| T3-PHO-010 | photoview | scratch | amd64/arm64 | HIGH | HIGH |
| T3-PHO-011 | piwigo | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-PHO-012 | chevereto | alpine | amd64/arm64 | HIGH | HIGH |
| T3-PHO-013 | photocha | scratch | amd64/arm64 | HIGH | HIGH |
| T3-PHO-014 | photoshow | alpine | amd64/arm64 | MEDIUM | LOW |
| T3-PHO-015 | sigal | alpine | amd64 | MEDIUM | LOW |
| T3-PHO-016 | gallery3 | alpine | amd64 | MEDIUM | MEDIUM |
| T3-PHO-017 | zenphoto | alpine | amd64 | MEDIUM | LOW |
| T3-PHO-018 | kopano | alpine | amd64/arm64 | HIGH | HIGH |
| T3-PHO-019 | koken | alpine | amd64 | MEDIUM | MEDIUM |
| T3-PHO-020 | mirror | alpine | amd64/arm64 | HIGH | HIGH |

#### 3.1.2 Video Management (20 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-VID-001 | jellyfin | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T3-VID-002 | jellyfin-server | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VID-003 | jellyfin-ffmpeg | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VID-004 | jellyseer | alpine | amd64/arm64 | HIGH | LOW |
| T3-VID-005 | emby | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VID-006 | emby-server | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VID-007 | plex | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VID-008 | plex-push | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VID-009 | tautulli | alpine | amd64/arm64 | HIGH | LOW |
| T3-VID-010 | tautulli-py | scratch | amd64/arm64 | HIGH | HIGH |
| T3-VID-011 | freenas | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VID-012 | openmediar | alpine | amd64 | HIGH | HIGH |
| T3-VID-013 | channels-dvr | alpine | amd64 | HIGH | HIGH |
| T3-VID-014 | nextpvr | alpine | amd64 | HIGH | MEDIUM |
| T3-VID-015 | media-browser | alpine | amd64 | MEDIUM | LOW |
| T3-VID-016 | mythtv | alpine | amd64 | MEDIUM | HIGH |
| T3-VID-017 | tvheadend | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VID-018 | oscam | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VID-019 | dvblink | alpine | amd64 | MEDIUM | HIGH |
| T3-VID-020 | xteve | alpine | amd64/arm64 | HIGH | HIGH |

#### 3.1.3 Audio & Book Management (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-AUD-001 | audiobookshelf | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-002 | audiobookshelf-opds | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-003 | calibre-web | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-004 | calibre-server | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-005 | calibre | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-006 | calibre-eb | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-007 | koel | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-008 | koel-next | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-009 | navidrome | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-AUD-010 | navidrome-sqlite | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AUD-011 | subsonic | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-012 | airsonic | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-013 | airsonic-advanced | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AUD-014 | tuneshell | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AUD-015 | amplify | alpine | amd64/arm64 | HIGH | MEDIUM |

#### 3.1.4 Download & Indexing (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-DWN-001 | radarr | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T3-DWN-002 | radarr-develop | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DWN-003 | sonarr | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T3-DWN-004 | sonarr-develop | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DWN-005 | bazarr | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DWN-006 | bazarr-subliminal | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DWN-007 | prowlarr | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T3-DWN-008 | prowlarr-develop | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DWN-009 | lidarr | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DWN-010 | readarr | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DWN-011 | whisparr | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DWN-012 | qbitmanage | alpine | amd64 | HIGH | MEDIUM |
| T3-DWN-013 | qbittorrent | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T3-DWN-014 | qbittorrent-nox | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DWN-015 | transmission | alpine | amd64/arm64 | HIGH | MEDIUM |

### 3.2 AI & Data Science (70 images)

#### 3.2.1 LLM & AI Orchestration (25 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-AI-001 | ollama | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-AI-002 | ollama-cuda | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AI-003 | ollama-rocm | scratch | amd64 | HIGH | HIGH |
| T3-AI-004 | ollama-gpu | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AI-005 | llama.cpp | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-AI-006 | llama-cpp-server | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AI-007 | localai | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-AI-008 | localai-cuda | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AI-009 | localai-loadbalancer | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AI-010 | open-webui | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-AI-011 | open-webui-api | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AI-012 | text-generation-webui | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-AI-013 | text-gen-ui | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AI-014 | litellm | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AI-015 | litellm-proxy | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AI-016 | opengpts | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AI-017 | maxbot | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AI-018 | langchain | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AI-019 | langServe | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AI-020 | embeddings | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AI-021 | transformers | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AI-022 | transformers-gpu | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AI-023 | vllm | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AI-024 | vllm-cuda | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AI-025 | ai-engine | scratch | amd64/arm64 | HIGH | HIGH |

#### 3.2.2 Vector Databases (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-VEC-001 | qdrant | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-VEC-002 | qdrant-cpu | scratch | amd64/arm64 | HIGH | HIGH |
| T3-VEC-003 | qdrant-gpu | scratch | amd64/arm64 | HIGH | HIGH |
| T3-VEC-004 | milvus | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-VEC-005 | milvus-etcd | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VEC-006 | milvus-minio | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VEC-007 | milvus-attu | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VEC-008 | weaviate | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-VEC-009 | weaviate-python | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VEC-010 | chroma | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VEC-011 | chroma-all-minimal | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VEC-012 | pinecone | alpine | amd64 | HIGH | HIGH |
| T3-VEC-013 | redis-vert | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VEC-014 | lancedb | scratch | amd64/arm64 | HIGH | HIGH |
| T3-VEC-015 | vecs-db | scratch | amd64/arm64 | HIGH | HIGH |

#### 3.2.3 Machine Learning Training (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-ML-001 | pytorch | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-ML-002 | pytorch-gpu | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ML-003 | pytorch-cuda | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ML-004 | tensorflow | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-ML-005 | tensorflow-gpu | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ML-006 | jupyter-all | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-ML-007 | jupyter-pytorch | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ML-008 | jupyter-tensorflow | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ML-009 | jupyter-scikit | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ML-010 | mlflow | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-ML-011 | mlflow-tracking | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ML-012 | mlflow-server | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ML-013 | weights-biases | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ML-014 | wandb-server | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ML-015 | tensorboard | alpine | amd64/arm64 | HIGH | MEDIUM |

#### 3.2.4 AI Tools & Utilities (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-AIT-001 | whisper | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AIT-002 | whisper-cpp | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AIT-003 | faster-whisper | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AIT-004 | whisper-cuda | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AIT-005 | tts | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AIT-006 | piper | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AIT-007 | coqui-tts | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AIT-008 | stable-diffusion | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AIT-009 | stable-diffusion-webui | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AIT-010 | automatic1111 | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AIT-011 | comfyui | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AIT-012 | invokeai | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AIT-013 | diffusers | scratch | amd64/arm64 | HIGH | HIGH |
| T3-AIT-014 | transformers | alpine | amd64/arm64 | HIGH | HIGH |
| T3-AIT-015 | deepspeed | alpine | amd64/arm64 | HIGH | HIGH |

### 3.3 Automation & Web Tools (60 images)

#### 3.3.1 No-Code/Low-Code Platforms (25 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-NOC-001 | n8n | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-NOC-002 | n8n-nodes | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-003 | n8n-webhook | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-004 | appsmith | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-NOC-005 | appsmith-nginx | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-NOC-006 | appsmith-editor | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-007 | budibase | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-NOC-008 | budibase-worker | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-009 | tooljet | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-NOC-010 | tooljet-server | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-011 | tooljet-client | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-012 | retool | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-013 | rows | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-014 | rowy | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-015 | jitsu | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-016 | airbyte | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-NOC-017 | airbyte-worker | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-018 | airbyte-server | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-019 | singer | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-020 | meltano | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-021 | dagster | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-NOC-022 | dagster-daemon | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-023 | dagster-logs | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-024 | prefect | alpine | amd64/arm64 | HIGH | HIGH |
| T3-NOC-025 | prefect-server | alpine | amd64/arm64 | HIGH | HIGH |

#### 3.3.2 RSS & News Readers (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-RSS-001 | freshrss | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-RSS-002 | freshrss-minimal | alpine | amd64/arm64 | HIGH | HIGH |
| T3-RSS-003 | tinytinyrss | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-RSS-004 | tt-rss | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-RSS-005 | miniflux | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-RSS-006 | miniflux-2 | scratch | amd64/arm64 | HIGH | HIGH |
| T3-RSS-007 | miniflux-21 | scratch | amd64/arm64 | HIGH | HIGH |
| T3-RSS-008 | rss2email | alpine | amd64 | HIGH | LOW |
| T3-RSS-009 | rss2社 | alpine | amd64 | HIGH | LOW |
| T3-RSS-010 | newsboat | scratch | amd64/arm64 | HIGH | LOW |
| T3-RSS-011 | newsblur | alpine | amd64/arm64 | HIGH | HIGH |
| T3-RSS-012 | feedbin | alpine | amd64/arm64 | HIGH | HIGH |
| T3-RSS-013 | feediron | alpine | amd64 | HIGH | LOW |
| T3-RSS-014 | yarr | alpine | amd64 | MEDIUM | MEDIUM |
| T3-RSS-015 | coma | alpine | amd64/arm64 | HIGH | HIGH |

#### 3.3.3 Browser & Scraping Tools (10 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-WEB-001 | browserless | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-WEB-002 | browserless-chrome | alpine | amd64/arm64 | HIGH | HIGH |
| T3-WEB-003 | browserless-edge | alpine | amd64 | HIGH | HIGH |
| T3-WEB-004 | searxng | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-WEB-005 | searxng-meta | alpine | amd64/arm64 | HIGH | HIGH |
| T3-WEB-006 | whoogle | scratch | amd64/arm64 | HIGH | HIGH |
| T3-WEB-007 | yacy | alpine | amd64 | MEDIUM | MEDIUM |
| T3-WEB-008 | crawlergo | scratch | amd64 | HIGH | HIGH |
| T3-WEB-009 | spider | scratch | amd64/arm64 | HIGH | HIGH |
| T3-WEB-010 | scrapyd | scratch | amd64/arm64 | HIGH | HIGH |

#### 3.3.4 Web Development Tools (10 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-DEV-001 | php | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DEV-002 | php-apache | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DEV-003 | php-fpm | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DEV-004 | composer | alpine | amd64/arm64 | HIGH | LOW |
| T3-DEV-005 | node | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DEV-006 | node-alpine | alpine | amd64/arm64 | HIGH | LOW |
| T3-DEV-007 | yarn | alpine | amd64/arm64 | HIGH | LOW |
| T3-DEV-008 | pm2 | alpine | amd64/arm64 | HIGH | LOW |
| T3-DEV-009 | ruby | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DEV-010 | bundler | alpine | amd64/arm64 | HIGH | LOW |

### 3.4 Home & Utility (70 images)

#### 3.4.1 Home Automation (30 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-HOM-001 | homeassistant | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-HOM-002 | homeassistant-core | alpine | amd64/arm64 | HIGH | HIGH |
| T3-HOM-003 | homeassistant-hassio | alpine | amd64/arm64 | HIGH | HIGH |
| T3-HOM-004 | homeassistant-supervisor | alpine | amd64/arm64 | HIGH | HIGH |
| T3-HOM-005 | zigbee2mqtt | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HOM-006 | zzh | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HOM-007 | zoe | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HOM-008 | mqtt | alpine | amd64/arm64 | CRITICAL | MEDIUM |
| T3-HOM-009 | mosquito | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HOM-010 | mosquitto | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-HOM-011 | mosquitto-dev | scratch | amd64/arm64 | HIGH | HIGH |
| T3-HOM-012 | emqx | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-HOM-013 | emqx-ee | alpine | amd64/arm64 | HIGH | HIGH |
| T3-HOM-014 | vernemq | alpine | amd64/arm64 | HIGH | HIGH |
| T3-HOM-015 | node-red | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HOM-016 | node-red-admin | alpine | amd64/arm64 | HIGH | LOW |
| T3-HOM-017 | iobroker | alpine | amd64/arm64 | HIGH | HIGH |
| T3-HOM-018 | openhab | alpine | amd64/arm64 | HIGH | HIGH |
| T3-HOM-019 | openhab3 | alpine | amd64/arm64 | HIGH | HIGH |
| T3-HOM-020 | homebridge | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HOM-021 | homebridge-camera | alpine | amd64 | HIGH | LOW |
| T3-HOM-022 | homekit | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HOM-023 | esphome | alpine | amd64/arm64 | HIGH | HIGH |
| T3-HOM-024 | esphome-daemon | alpine | amd64 | HIGH | HIGH |
| T3-HOM-025 | tasmota | alpine | amd64 | MEDIUM | MEDIUM |
| T3-HOM-026 | tasmota-js | alpine | amd64 | MEDIUM | MEDIUM |
| T3-HOM-027 | espeasy | alpine | amd64 | MEDIUM | MEDIUM |
| T3-HOM-028 | espurna | alpine | amd64 | MEDIUM | MEDIUM |
| T3-HOM-029 | wled | alpine | amd64 | MEDIUM | MEDIUM |
| T3-HOM-030 | athom | alpine | amd64/arm64 | HIGH | HIGH |

#### 3.4.2 Dashboards & Overviews (20 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-DSB-001 | homepage | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-DSB-002 | homepage-config | alpine | amd64/arm64 | HIGH | LOW |
| T3-DSB-003 | homepage-sync | alpine | amd64 | HIGH | LOW |
| T3-DSB-004 | dashy | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DSB-005 | dashy-alpine | alpine | amd64/arm64 | HIGH | HIGH |
| T3-DSB-006 | flame | scratch | amd64/arm64 | HIGH | HIGH |
| T3-DSB-007 | flame-ui | scratch | amd64/arm64 | HIGH | HIGH |
| T3-DSB-008 | heimdall | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DSB-009 | heimdall-lite | scratch | amd64/arm64 | HIGH | HIGH |
| T3-DSB-010 | organizer | alpine | amd64/arm64 | HIGH | HIGH |
| T3-DSB-011 | portainer | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DSB-012 | portainer-agent | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DSB-013 | portainer-edge | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DSB-014 | yacht | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DSB-015 | cockpit | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DSB-016 | docker-clean | alpine | amd64 | HIGH | LOW |
| T3-DSB-017 | docui | alpine | amd64 | HIGH | MEDIUM |
| T3-DSB-018 | Lazydocker | alpine | amd64/arm64 | HIGH | LOW |
| T3-DSB-019 | lazydocker-ui | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-DSB-020 | docker-gc | scratch | amd64 | HIGH | LOW |

#### 3.4.3 Utility & Tool Suites (20 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-UTL-001 | it-tools | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-UTL-002 | it-tools-legacy | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-UTL-003 | cyberchef | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-UTL-004 | cyberchef-node | alpine | amd64/arm64 | HIGH | HIGH |
| T3-UTL-005 | pairdrop | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-UTL-006 | pairdrop-server | scratch | amd64/arm64 | HIGH | HIGH |
| T3-UTL-007 | privateBin | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-UTL-008 | privatebin-nginx | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-UTL-009 | hedgedoc | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-UTL-010 | hedgedoc-legacy | alpine | amd64/arm64 | HIGH | HIGH |
| T3-UTL-011 | codimd | alpine | amd64/arm64 | HIGH | HIGH |
| T3-UTL-012 | hackmd | alpine | amd64/arm64 | HIGH | HIGH |
| T3-UTL-013 | ulogger | scratch | amd64/arm64 | HIGH | HIGH |
| T3-UTL-014 | zipline | scratch | amd64/arm64 | HIGH | HIGH |
| T3-UTL-015 | transfer.sh | scratch | amd64/arm64 | HIGH | HIGH |
| T3-UTL-016 | transferhelper | scratch | amd64/arm64 | HIGH | HIGH |
| T3-UTL-017 | linguist | alpine | amd64/arm64 | HIGH | HIGH |
| T3-UTL-018 | linguist-go | scratch | amd64/arm64 | HIGH | HIGH |
| T3-UTL-019 | whoogle-search | scratch | amd64/arm64 | HIGH | HIGH |
| T3-UTL-020 | searx | alpine | amd64/arm64 | HIGH | HIGH |

### 3.5 Security & Hardening Tools (60 images)

#### 3.5.1 Vulnerability Scanning (20 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-VUL-001 | trivy | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-VUL-002 | trivy-alpine | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VUL-003 | trivy-k8s | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VUL-004 | grype | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-VUL-005 | grype-alpine | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VUL-006 | syft | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-VUL-007 | syft-alpine | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VUL-008 | snyk | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-VUL-009 | snyk-alpine | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VUL-010 | snyk-docker | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VUL-011 | snyk-monitor | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VUL-012 | dependabot | alpine | amd64/arm64 | HIGH | HIGH |
| T3-VUL-013 | npm-audit | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VUL-014 | yarn-audit | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VUL-015 | cargo-audit | scratch | amd64/arm64 | HIGH | MEDIUM |
| T3-VUL-016 | pip-audit | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VUL-017 | gem-audit | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VUL-018 | conan-audit | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-VUL-019 | composer-audit | alpine | amd64 | HIGH | MEDIUM |
| T3-VUL-020 | govulncheck | scratch | amd64/arm64 | HIGH | HIGH |

#### 3.5.2 Secrets Scanning (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-SEC-001 | trufflehog | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-SEC-002 | truffleshog | scratch | amd64/arm64 | HIGH | HIGH |
| T3-SEC-003 | truffelsh | scratch | amd64/arm64 | HIGH | HIGH |
| T3-SEC-004 | gitleaks | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-SEC-005 | git-secrets | alpine | amd64/arm64 | HIGH | LOW |
| T3-SEC-006 | repo-security | scratch | amd64/arm64 | HIGH | HIGH |
| T3-SEC-007 | gitguardian | alpine | amd64/arm64 | HIGH | HIGH |
| T3-SEC-008 | detect-secrets | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-SEC-009 | secrets-scanner | scratch | amd64/arm64 | HIGH | HIGH |
| T3-SEC-010 | secretz | alpine | amd64 | HIGH | HIGH |
| T3-SEC-011 | shh | scratch | amd64/arm64 | HIGH | HIGH |
| T3-SEC-012 | keynuker | alpine | amd64 | HIGH | HIGH |
| T3-SEC-013 | repo-supervisor | scratch | amd64/arm64 | HIGH | HIGH |
| T3-SEC-014 | gitrob | alpine | amd64/arm64 | HIGH | HIGH |
| T3-SEC-015 | ggshield | scratch | amd64/arm64 | CRITICAL | HIGH |

#### 3.5.3 Container Security (15 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-CNT-001 | hadolint | scratch | amd64/arm64 | CRITICAL | LOW |
| T3-CNT-002 | dockerfile-lint | scratch | amd64/arm64 | HIGH | LOW |
| T3-CNT-003 | docker-bench | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-CNT-004 | lynis | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-CNT-005 | r2c-bench | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-CNT-006 | trivy-iac | scratch | amd64/arm64 | HIGH | HIGH |
| T3-CNT-007 | checkov | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-CNT-008 | checkov-k8s | scratch | amd64/arm64 | HIGH | HIGH |
| T3-CNT-009 | kube-bench | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-CNT-010 | kube-hunter | scratch | amd64/arm64 | HIGH | MEDIUM |
| T3-CNT-011 | kubescape | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-CNT-012 | kubescape-operator | alpine | amd64/arm64 | HIGH | HIGH |
| T3-CNT-013 | falco | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-CNT-014 | falco-rules | alpine | amd64/arm64 | HIGH | LOW |
| T3-CNT-015 | falcosidekick | alpine | amd64/arm64 | HIGH | HIGH |

#### 3.5.4 Security Hardening (10 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-HRD-001 | openscap | alpine | amd64/arm64 | HIGH | HIGH |
| T3-HRD-002 | scap-workbench | alpine | amd64 | HIGH | HIGH |
| T3-HRD-003 | lynis | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HRD-004 | chkrootkit | alpine | amd64/arm64 | HIGH | LOW |
| T3-HRD-005 | rkhunter | alpine | amd64/arm64 | HIGH | LOW |
| T3-HRD-006 | clamav | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HRD-007 | clamav-daemon | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HRD-008 | freshclam | alpine | amd64/arm64 | HIGH | LOW |
| T3-HRD-009 | maldet | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-HRD-010 | rblake | scratch | amd64/arm64 | HIGH | HIGH |

### 3.6 DevOps & CI/CD Tools (40 images)

#### 3.6.1 Build & Package Management (20 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-BLD-001 | kaniko | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-BLD-002 | buildah | alpine | amd64/arm64 | HIGH | HIGH |
| T3-BLD-003 | buildkit | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-BLD-004 | buildx | alpine | amd64/arm64 | HIGH | MEDIUM |
| T3-BLD-005 | crane | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-BLD-006 | helm | scratch | amd64/arm64 | CRITICAL | HIGH |
| T3-BLD-007 | helmfile | scratch | amd64/arm64 | HIGH | HIGH |
| T3-BLD-008 | helmsman | scratch | amd64/arm64 | HIGH | HIGH |
| T3-BLD-009 | argo-cd | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-BLD-010 | argo-rollouts | alpine | amd64/arm64 | HIGH | HIGH |
| T3-BLD-011 | flux2 | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-BLD-012 | fluxcd-helm | alpine | amd64/arm64 | HIGH | HIGH |
| T3-BLD-013 | fluxcd-image | alpine | amd64/arm64 | HIGH | HIGH |
| T3-BLD-014 | Jenkins | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-BLD-015 | Jenkins-agent | alpine | amd64/arm64 | HIGH | HIGH |
| T3-BLD-016 | Jenkins-executor | alpine | amd64 | HIGH | HIGH |
| T3-BLD-017 | jenkins-plugin | alpine | amd64 | HIGH | MEDIUM |
| T3-BLD-018 | sbt | alpine | amd64/arm64 | HIGH | HIGH |
| T3-BLD-019 | maven | alpine | amd64/arm64 | HIGH | HIGH |
| T3-BLD-020 | gradle | alpine | amd64/arm64 | HIGH | HIGH |

#### 3.6.2 Container Orchestration (10 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-ORC-001 | k3s | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-ORC-002 | k3s-server | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ORC-003 | k3s-agent | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ORC-004 | k3d | alpine | amd64/arm64 | HIGH | HIGH |
| T3-ORC-005 | k3d-proxy | alpine | amd64 | HIGH | HIGH |
| T3-ORC-006 | kube-proxy | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-ORC-007 | kube-scheduler | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-ORC-008 | kube-controller | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-ORC-009 | kube-apiserver | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-ORC-010 | etcd-empty | scratch | amd64/arm64 | CRITICAL | HIGH |

#### 3.6.3 Observability for DevOps (10 images)

| ID | Image Name | Base Runtime | Architecture | Priority | Difficulty |
|----|-----------|-------------|-------------|-------------|----------|-----------|
| T3-OBS-001 | prometheus-operator | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-OBS-002 | prometheus-config | alpine | amd64/arm64 | HIGH | HIGH |
| T3-OBS-003 | alertmanager | alpine | amd64/arm64 | CRITICAL | HIGH |
| T3-OBS-004 | thanos-querier | alpine | amd64/arm64 | HIGH | HIGH |
| T3-OBS-005 | thanos-rule | alpine | amd64/arm64 | HIGH | HIGH |
| T3-OBS-006 | grafana-operator | alpine | amd64/arm64 | HIGH | HIGH |
| T3-OBS-007 | loki-simple | alpine | amd64/arm64 | HIGH | HIGH |
| T3-OBS-008 | promtail-agent | alpine | amd64/arm64 | HIGH | HIGH |
| T3-OBS-009 | promxy | alpine | amd64/arm64 | HIGH | HIGH |
| T3-OBS-010 | thanos-bucket | alpine | amd64/arm64 | HIGH | HIGH |

---

## Appendix A: Runtime Dependencies

These base runtimes must be built first and used as foundations for application images.

### A.1 Static Runtimes (10 images)

| ID | Runtime Name | Target | Architecture | Purpose |
|----|-------------|--------|--------------|--------|
| RT-RUST-001 | rust-static | x86_64-unknown-linux-musl | amd64 | Rust binaries |
| RT-RUST-002 | rust-static-arm | aarch64-unknown-linux-musl | arm64 | Rust binaries ARM |
| RT-GO-001 | go-static | CGO_ENABLED=0 | amd64/arm64 | Go static binaries |
| RT-GOLANG-001 | golang-alpine | standard | amd64/arm64 | Go with libc |
| RT-C-001 | static-c | musl | amd64 | C static binaries |
| RT-NODE-001 | node-alpine | alpine | amd64/arm64 | Node.js runtime |
| RT-NODE-002 | node-distroless | distroless | amd64/arm64 | Node.js minimal |
| RT-PY-001 | python-alpine | alpine | amd64/arm64 | Python runtime |
| RT-PY-002 | python-slim | debian-slim | amd64/arm64 | Python minimal |
| RT-JV-001 | openjdk-alpine | openjre | amd64/arm64 | Java runtime |

---

## Summary Statistics

| Tier | Category | Image Count |
|------|----------|------------|
| Tier 1 | Networking & Perimeter | 100 |
| Tier 1 | Databases & Persistent State | 200 |
| Tier 1 | Observability Stack | 80 |
| Tier 2 | Identity & Secret Management | 60 |
| Tier 2 | Communication & Collaboration | 80 |
| Tier 2 | Content & File Management | 60 |
| Tier 2 | Business & Finance | 50 |
| Tier 3 | Media & Asset Management | 70 |
| Tier 3 | AI & Data Science | 70 |
| Tier 3 | Automation & Web Tools | 60 |
| Tier 3 | Home & Utility | 70 |
| Tier 3 | Security & Hardening Tools | 60 |
| Tier 3 | DevOps & CI/CD Tools | 40 |
| Appendix | Runtime Dependencies | 10 |
| | **Total** | **1010** |

---

## Verification Checklist

- [ ] 1000+ images specified
- [ ] All tiers represented (Tier 1-3)
- [ ] Base runtimes defined
- [ ] Priority levels assigned
- [ ] Difficulty levels assigned
- [ ] Architecture support specified
- [ ] Metadata complete
- [ ] Traceability matrix prepared

---

## Bibliography

| ID | Source | Relevance | TQA Level |
|----|--------|-----------|-----------|
| [^1] | Docker Official Images | Base image verification | 5 |
| [^2] | Wolfi Dockerfiles | Distroless base | 4 |
| [^3] | Distroless Dockerfiles | Scratch base | 4 |
| [^4] | upstream releases | Version confirmation | 5 |
| [^5] | GitHub security advisories | CVE context | 4 |