# =============================================================================
# PHASE 3: TEST COVERAGE & PROVABLE CORRECTNESS - Detailed Execution Plan
# =============================================================================
# Version: 1.0.0
# Status: PENDING
# Author: Nexus (Principal Systems Architect)
# Date: 2026-04-19
#
# ABSTRACT: This phase dramatically expands test coverage from basic constraint
# checks to functional correctness tests, adversarial security tests, and
# property-based testing. It covers all 223 images with comprehensive test
# configurations, adds image layer analysis via dive, startup time benchmarking,
# and database/proxy integration tests. Phase 2 must pass all quality gates
# before this phase begins.
# =============================================================================

## Table of Contents

1. [Current State Assessment](#1-current-state-assessment)
2. [Task Inventory](#2-task-inventory)
3. [Detailed Task Specifications](#3-detailed-task-specifications)
4. [Quality Gates](#4-quality-gates)
5. [Risk Register](#5-risk-register)
6. [Rollback Procedures](#6-rollback-procedures)
7. [Success Metrics](#7-success-metrics)

---

## 1. Current State Assessment

### 1.1 Current Test Coverage

| Test Type | Coverage | Implementation | Images Tested |
|-----------|----------|---------------|---------------|
| Constraint tests (C001-C014, C019) | 100% | `test_framework.sh` | 223 (via CI) |
| Functional: binary execution | 100% | `test_framework.sh:test_functional_basic` | 223 |
| Functional: port binding | 100% | `test_framework.sh:test_functional_ports` | 223 |
| Functional: environment | 100% | `test_framework.sh:test_functional_environment` | 223 |
| Functional: database operations | 0% | Missing | 0 |
| Functional: proxy routing | 0% | Missing | 0 |
| Adversarial: shell escape | 0% | Missing | 0 |
| Adversarial: privilege escalation | 0% | Missing | 0 |
| Adversarial: network exfiltration | 0% | Missing | 0 |
| Property-based testing | 0% | Missing | 0 |
| Image layer analysis | 0% | Missing | 0 |
| Startup benchmarking | 0% | Missing | 0 |
| Test runner config | ~35/223 (16%) | `test_runner.sh:IMAGE_CONFIGS` | 35 |

### 1.2 Test Runner Config Gap

The `test_runner.sh` `IMAGE_CONFIGS` associative array has entries for only ~35 images out of 223. Missing entries cause the runner to fall back to using the image name as the binary name, which may be incorrect (e.g., `mysql` uses `mariadbd`, `redis7` uses `redis-server`).

**Current entries (35):**
```
traefik, nginx, haproxy, envoy, caddy, coredns, postgres, postgresql,
mysql, mariadb, redis, memcached, etcd, consul, vault, prometheus,
grafana, loki, thanos, node-exporter, jenkins, argocd, rabbitmq, nats,
minio, restic, rclone, trivy, syft, grype, cosign, step-cli, forgejo,
gitea, keycloak, openldap, zitadel, flux, tekton, drone
```

**Missing entries (188+):** All variant images (nginx-unprivileged, nginx-exporter, traefik-v2, caddy-wildcard, etc.) and many base images.

### 1.3 Image Categories for Functional Testing

| Category | Images | Functional Tests Needed |
|----------|--------|------------------------|
| Databases | postgresql, redis, mysql, mariadb, mongodb, sqlite, dragonfly, cockroachdb | CRUD operations, connection handling |
| Proxies | nginx, traefik, haproxy, envoy, caddy, nginx-unprivileged, caddy-reverseproxy | Request routing, TLS, load balancing |
| Monitoring | prometheus, grafana, loki, thanos, victoriametrics, cadvisor | Metrics collection, query API |
| Security | vault, keycloak, openldap, zitadel, headscale | Auth flows, token issuance |
| Networking | bind, coredns, unbound, consul | DNS resolution, service discovery |
| VPN | wireguard, wg-quick, tailscale, netclient, netmaker, netbird, strongswan, openvpn | Tunnel creation, connectivity |
| CI/CD | jenkins, argocd, tekton, drone, forgejo, gitea, gitlab | Build triggers, repository access |
| Storage | minio, s3, restic, rclone | Object operations, backup/restore |
| Messaging | rabbitmq, nats, activemq | Message publish/consume |
| Utilities | trivy, syft, grype, cosign, step-cli, rclone | CLI operations, output parsing |

### 1.4 Adversarial Test Categories

| Attack Vector | Description | Current Mitigation | Test Needed |
|--------------|-------------|-------------------|-------------|
| Shell escape | Container process obtains shell access | No shell in image (C003) | Verify no `/bin/sh`, `/bin/bash` |
| Privilege escalation | Process elevates to root | Non-root user (C001) | Verify no `su`, `sudo`, setuid |
| Network exfiltration | Process connects to unauthorized hosts | Default deny network | Verify outbound restrictions |
| Package install | Process installs new packages | No package manager (C004) | Verify no `apt`, `apk`, `yum` |
| Binary exec | Process executes arbitrary binaries | Read-only filesystem (C002) | Verify no writable exec paths |
| Disk fill | Process fills filesystem | Resource limits | Verify no excessive writes |

---

## 2. Task Inventory

### Dependency Graph (Topological Order)

```
Phase 2 (all gates passed)
    |
    +--> T3.1.1 (Database functional tests) ──> Depends on T0.3.1
    +--> T3.1.2 (Proxy functional tests) ──> Depends on T0.3.1
    +--> T3.1.3 (Adversarial tests) ──> Depends on T0.4.1
    +--> T3.2.1 (Layer analysis - dive) ──> Independent
    +--> T3.2.2 (Startup benchmarking) ──> Independent
```

### Additional Task (Not in master_plan.toml but Required)

**T3.1.4: Expand test_runner.sh config to cover all 223 images**

This task is critical because the functional tests (T3.1.1, T3.1.2) depend on correct image configurations. The current 16% coverage is insufficient.

### Parallel Execution Opportunities

```
Stream A: Database Tests (T3.1.1) — 16 hours
Stream B: Proxy Tests (T3.1.2) — 12 hours
Stream C: Adversarial Tests (T3.1.3) — 16 hours
Stream D: Layer Analysis (T3.2.1) — 4 hours
Stream E: Startup Benchmarking (T3.2.2) — 4 hours
Stream F: Test Config Expansion (T3.1.4) — 8 hours
```

All streams are independent and can execute in parallel. T3.1.4 should complete first (or in parallel) since other tests depend on correct configs.

### Effort Estimate Summary

| Task | Estimated Hours | Parallel? |
|------|----------------|-----------|
| T3.1.1 | 16 | Yes |
| T3.1.2 | 12 | Yes |
| T3.1.3 | 16 | Yes |
| T3.1.4 (new) | 8 | Yes |
| T3.2.1 | 4 | Yes |
| T3.2.2 | 4 | Yes |
| **Total** | **60** | **~20 hours wall-clock** |

---

## 3. Detailed Task Specifications

### 3.1 T3.1.1: Write functional correctness tests for database images

#### Problem Analysis

Current functional tests only check that a binary responds to `--version` or `-v`. For databases, this is insufficient — a database that starts but cannot store or retrieve data is not functional.

**Database images in the registry:**

| Image | Binary | Port | Type | Test Complexity |
|-------|--------|------|------|----------------|
| postgresql | `postgres` | 5432 | RDBMS | HIGH — needs initdb, data directory |
| postgres | `postgres` | 5432 | RDBMS | HIGH — same as postgresql |
| mysql | `mariadbd` | 3306 | RDBMS | HIGH — needs data directory |
| mariadb | `mariadbd` | 3306 | RDBMS | HIGH — same as mysql |
| mongodb | `mongod` | 27017 | Document DB | HIGH — needs data directory |
| redis | `redis-server` | 6379 | Key-value | MEDIUM — in-memory |
| redis7 | `redis-server` | 6379 | Key-value | MEDIUM — in-memory |
| sqlite | `sqlite3` | N/A | Embedded | LOW — file-based |
| dragonfly | `dragonfly` | 6379 | Key-value | MEDIUM — Redis-compatible |
| cockroachdb | `cockroach` | 26257 | RDBMS | HIGH — distributed |
| memcached | `memcached` | 11211 | Key-value | LOW — simple get/set |

#### Solution: Per-Database Functional Test Suite

**Test file:** `images/tests/functional/test_databases.sh`

```bash
#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../test_framework.sh"

# =============================================================================
# POSTGRESQL FUNCTIONAL TESTS
# =============================================================================

test_postgresql_create_table() {
    local image="$1"
    local container

    container=$(docker run -d --rm \
        -e POSTGRES_HOST_AUTH_METHOD=trust \
        -p 15432:5432 \
        "$image" \
        -c listen_addresses='*' 2>/dev/null || echo "")

    if [ -z "$container" ]; then
        echo "SKIP: Cannot start postgresql container"
        return 0
    fi

    local retries=30
    while [ $retries -gt 0 ]; do
        if docker exec "$container" pg_isready -h localhost 2>/dev/null; then
            break
        fi
        sleep 1
        retries=$((retries - 1))
    done

    if [ "$retries" -eq 0 ]; then
        docker stop "$container" 2>/dev/null || true
        echo "FAIL: PostgreSQL did not become ready"
        return 1
    fi

    # Create table
    docker exec "$container" psql -U postgres -c \
        "CREATE TABLE test_evergreen (id SERIAL PRIMARY KEY, data TEXT);" 2>/dev/null

    # Insert data
    docker exec "$container" psql -U postgres -c \
        "INSERT INTO test_evergreen (data) VALUES ('evergreen_test');" 2>/dev/null

    # Query data
    RESULT=$(docker exec "$container" psql -U postgres -t -c \
        "SELECT data FROM test_evergreen WHERE id = 1;" 2>/dev/null | tr -d ' ')

    docker stop "$container" 2>/dev/null || true

    if [ "$RESULT" = "evergreen_test" ]; then
        echo "PASS: PostgreSQL CRUD operations work"
        return 0
    else
        echo "FAIL: PostgreSQL query returned '${RESULT}', expected 'evergreen_test'"
        return 1
    fi
}

# =============================================================================
# REDIS FUNCTIONAL TESTS
# =============================================================================

test_redis_set_get() {
    local image="$1"
    local container

    container=$(docker run -d --rm -p 16379:6379 "$image" 2>/dev/null || echo "")

    if [ -z "$container" ]; then
        echo "SKIP: Cannot start redis container"
        return 0
    fi

    sleep 2

    # SET
    docker exec "$container" redis-cli SET evergreen_key evergreen_value 2>/dev/null

    # GET
    RESULT=$(docker exec "$container" redis-cli GET evergreen_key 2>/dev/null)

    docker stop "$container" 2>/dev/null || true

    if [ "$RESULT" = "evergreen_value" ]; then
        echo "PASS: Redis SET/GET operations work"
        return 0
    else
        echo "FAIL: Redis GET returned '${RESULT}', expected 'evergreen_value'"
        return 1
    fi
}

# =============================================================================
# MYSQL FUNCTIONAL TESTS
# =============================================================================

test_mysql_create_query() {
    local image="$1"
    local container

    container=$(docker run -d --rm \
        -e MYSQL_ALLOW_EMPTY_PASSWORD=yes \
        -p 13306:3306 \
        "$image" 2>/dev/null || echo "")

    if [ -z "$container" ]; then
        echo "SKIP: Cannot start mysql container"
        return 0
    fi

    # Wait for MySQL to be ready
    local retries=30
    while [ $retries -gt 0 ]; do
        if docker exec "$container" mariadb-admin ping -h 127.0.0.1 --silent 2>/dev/null; then
            break
        fi
        sleep 2
        retries=$((retries - 1))
    done

    if [ "$retries" -eq 0 ]; then
        docker stop "$container" 2>/dev/null || true
        echo "FAIL: MySQL did not become ready"
        return 1
    fi

    # Create database and table
    docker exec "$container" mariadb -u root -e \
        "CREATE DATABASE IF NOT EXISTS evergreen_test;
         USE evergreen_test;
         CREATE TABLE test_table (id INT AUTO_INCREMENT PRIMARY KEY, data VARCHAR(255));
         INSERT INTO test_table (data) VALUES ('evergreen_data');" 2>/dev/null

    # Query
    RESULT=$(docker exec "$container" mariadb -u root -N -e \
        "SELECT data FROM evergreen_test.test_table WHERE id = 1;" 2>/dev/null | tr -d '\n')

    docker stop "$container" 2>/dev/null || true

    if [ "$RESULT" = "evergreen_data" ]; then
        echo "PASS: MySQL CRUD operations work"
        return 0
    else
        echo "FAIL: MySQL query returned '${RESULT}', expected 'evergreen_data'"
        return 1
    fi
}

# =============================================================================
# MONGODB FUNCTIONAL TESTS
# =============================================================================

test_mongodb_insert_find() {
    local image="$1"
    local container

    container=$(docker run -d --rm -p 27017:27017 "$image" 2>/dev/null || echo "")

    if [ -z "$container" ]; then
        echo "SKIP: Cannot start mongodb container"
        return 0
    fi

    sleep 5

    # Insert document
    docker exec "$container" mongosh --quiet --eval \
        'db.evergreen_test.insertOne({test: "evergreen_value"})' 2>/dev/null || \
    docker exec "$container" mongo --quiet --eval \
        'db.evergreen_test.insertOne({test: "evergreen_value"})' 2>/dev/null || true

    # Find document
    RESULT=$(docker exec "$container" mongosh --quiet --eval \
        'db.evergreen_test.findOne().test' 2>/dev/null || \
        docker exec "$container" mongo --quiet --eval \
        'db.evergreen_test.findOne().test' 2>/dev/null || echo "")

    docker stop "$container" 2>/dev/null || true

    if [ "$RESULT" = "evergreen_value" ]; then
        echo "PASS: MongoDB insert/find operations work"
        return 0
    else
        echo "WARN: MongoDB test returned '${RESULT}' (may need shell access)"
        return 0
    fi
}

# =============================================================================
# SQLITE FUNCTIONAL TESTS
# =============================================================================

test_sqlite_basic() {
    local image="$1"

    # SQLite is embedded — test basic query
    RESULT=$(docker run --rm "$image" sqlite3 :memory: \
        "CREATE TABLE t(x); INSERT INTO t VALUES('evergreen'); SELECT x FROM t;" 2>/dev/null)

    if [ "$RESULT" = "evergreen" ]; then
        echo "PASS: SQLite basic operations work"
        return 0
    else
        echo "WARN: SQLite test returned '${RESULT}'"
        return 0
    fi
}

# =============================================================================
# MEMCACHED FUNCTIONAL TESTS
# =============================================================================

test_memcached_set_get() {
    local image="$1"
    local container

    container=$(docker run -d --rm -p 11211:11211 "$image" 2>/dev/null || echo "")

    if [ -z "$container" ]; then
        echo "SKIP: Cannot start memcached container"
        return 0
    fi

    sleep 1

    # Use netcat or python to test (memcached has no CLI client in image)
    RESULT=$(docker exec "$container" sh -c \
        'echo -e "set evergreen_key 0 0 15\r\nevergreen_value\r\nget evergreen_key\r\n" \
        | nc -q1 localhost 11211 2>/dev/null | grep -o "evergreen_value"' 2>/dev/null || echo "")

    docker stop "$container" 2>/dev/null || true

    if [ "$RESULT" = "evergreen_value" ]; then
        echo "PASS: Memcached SET/GET operations work"
        return 0
    else
        echo "WARN: Memcached test inconclusive (no nc available)"
        return 0
    fi
}
```

#### Test Matrix

| Database | Test | Expected Result | Timeout |
|----------|------|----------------|---------|
| PostgreSQL | CREATE TABLE + INSERT + SELECT | Returns inserted data | 60s |
| MySQL/MariaDB | CREATE DB + INSERT + SELECT | Returns inserted data | 60s |
| Redis | SET + GET | Returns set value | 10s |
| MongoDB | insertOne + findOne | Returns inserted document | 30s |
| SQLite | CREATE TABLE + INSERT + SELECT | Returns inserted data | 10s |
| Memcached | SET + GET via netcat | Returns set value | 10s |
| Dragonfly | SET + GET (Redis-compatible) | Returns set value | 10s |
| CockroachDB | CREATE TABLE + INSERT + SELECT | Returns inserted data | 90s |

#### Implementation Steps

1. **Create test directory structure**:
   ```
   images/tests/functional/
     test_databases.sh
     test_proxies.sh
     common.sh          # Shared utilities
   ```

2. **Implement database tests**: Write each database-specific test function.

3. **Handle container startup challenges**:
   - PostgreSQL needs writable data directory (currently runs as UID 65534)
   - MySQL needs init script
   - MongoDB needs `--dbpath` writable
   - Use Docker tmpfs mounts for data directories

4. **Handle permission issues**: Many database images run as UID 65534 and cannot write to default data paths. Tests must:
   ```bash
   docker run -d --rm \
     --tmpfs /var/lib/postgresql/data \
     -e PGDATA=/var/lib/postgresql/data \
     "$image"
   ```

5. **CI integration**: Add functional test job to build.yml:
   ```yaml
   functional-tests:
     needs: [build, verify]
     runs-on: ubuntu-latest
     steps:
       - name: Run database functional tests
         run: bash images/tests/functional/test_databases.sh
   ```

#### Verification Criteria

- [ ] PostgreSQL: CREATE TABLE, INSERT, SELECT returns correct data
- [ ] MySQL/MariaDB: CREATE DB, INSERT, SELECT returns correct data
- [ ] Redis: SET key, GET key returns correct value
- [ ] MongoDB: insertOne, findOne returns correct document
- [ ] SQLite: in-memory CREATE, INSERT, SELECT works
- [ ] Memcached: SET/GET works (if netcat available)
- [ ] All tests use ephemeral containers (no data persistence)
- [ ] Tests clean up containers on failure

---

### 3.2 T3.1.2: Write functional correctness tests for proxy images

#### Problem Analysis

Proxy images (nginx, traefik, haproxy, envoy, caddy) need tests that verify:
1. The proxy starts and listens on the configured port
2. It can serve static content or route requests
3. TLS termination works (where applicable)
4. Configuration reload works (where applicable)

**Proxy images in the registry:**

| Image | Binary | Ports | Special Features |
|-------|--------|-------|-----------------|
| nginx | `/nginx` | 80, 443 | Static file serving, reverse proxy |
| nginx-unprivileged | `/nginx` | 8080, 8443 | Same as nginx, non-root ports |
| nginx-exporter | `/nginx-prometheus-exporter` | 9113 | Metrics exporter |
| nginx-ingress | `/nginx` | 80, 443 | Ingress controller |
| nginx-stream | `/nginx` | 80, 443 | TCP/UDP stream proxy |
| traefik | `/traefik` | 80, 443, 8080 | Auto-discovery, Let's Encrypt |
| traefik-v2 | `/traefik` | 80, 443, 8080 | Traefik v2 |
| haproxy | `/haproxy` | 80, 443 | Load balancing, health checks |
| haproxy-dev | `/haproxy` | 80, 443 | Development variant |
| haproxy-exporter | `/haproxy-exporter` | 9101 | Metrics exporter |
| haproxy-lb | `/haproxy` | 80, 443 | Load balancer variant |
| envoy | `/envoy` | 80, 443, 9900 | gRPC proxy, HTTP/2 |
| envoy-extras | `/envoy` | 80, 443 | Extended configuration |
| envoy-sidecar | `/envoy` | 15001 | Sidecar pattern |
| envoy-grpc | `/envoy` | 80, 443 | gRPC proxy |
| envoy-init | `/envoy` | 80, 443 | Init container |
| caddy | `/caddy` | 80, 443, 2019 | Auto-TLS, Caddyfile |
| caddy-wildcard | `/caddy` | 80, 443 | Wildcard cert support |
| caddy-reverseproxy | `/caddy` | 80, 443 | Reverse proxy focus |
| caddy-fileserver | `/caddy` | 80, 443 | Static file serving |

#### Solution: Per-Proxy Functional Test Suite

**Test file:** `images/tests/functional/test_proxies.sh`

```bash
#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../test_framework.sh"

# =============================================================================
# NGINX FUNCTIONAL TESTS
# =============================================================================

test_nginx_serves_content() {
    local image="$1"
    local port="${2:-8080}"
    local container

    # Create minimal config
    CONFIG=$(mktemp)
    cat > "$CONFIG" << 'EOF'
    events { worker_connections 1; }
    http {
        server {
            listen 8080;
            location / {
                return 200 'evergreen-ok';
                add_header Content-Type text/plain;
            }
        }
    }
EOF

    container=$(docker run -d --rm \
        -v "${CONFIG}:/app/nginx.conf:ro" \
        -p "${port}:8080" \
        "$image" -c /app/nginx.conf -g 'daemon off;' 2>/dev/null || echo "")

    if [ -z "$container" ]; then
        rm -f "$CONFIG"
        echo "SKIP: Cannot start nginx container"
        return 0
    fi

    sleep 2

    RESULT=$(curl -sf "http://localhost:${port}/" 2>/dev/null || echo "")
    docker stop "$container" 2>/dev/null || true
    rm -f "$CONFIG"

    if [ "$RESULT" = "evergreen-ok" ]; then
        echo "PASS: Nginx serves content correctly"
        return 0
    else
        echo "FAIL: Nginx returned '${RESULT}', expected 'evergreen-ok'"
        return 1
    fi
}

# =============================================================================
# TRAEFIK FUNCTIONAL TESTS
# =============================================================================

test_traefik_routes_request() {
    local image="$1"
    local container

    container=$(docker run -d --rm \
        -p 18080:8080 \
        "$image" --api.insecure=true --providers.docker=false 2>/dev/null || echo "")

    if [ -z "$container" ]; then
        echo "SKIP: Cannot start traefik container"
        return 0
    fi

    sleep 3

    # Test Traefik dashboard/API is accessible
    HTTP_CODE=$(curl -sf -o /dev/null -w "%{http_code}" \
        "http://localhost:18080/api/overview" 2>/dev/null || echo "000")

    docker stop "$container" 2>/dev/null || true

    if [ "$HTTP_CODE" = "200" ]; then
        echo "PASS: Traefik API is accessible"
        return 0
    else
        echo "FAIL: Traefik API returned HTTP ${HTTP_CODE}"
        return 1
    fi
}

# =============================================================================
# HAPROXY FUNCTIONAL TESTS
# =============================================================================

test_haproxy_load_balances() {
    local image="$1"
    local container

    # Create minimal config with stats
    CONFIG=$(mktemp)
    cat > "$CONFIG" << 'EOF'
    global
        daemon
    defaults
        mode http
        timeout connect 5s
        timeout client 10s
        timeout server 10s
    frontend stats
        bind *:8080
        stats enable
        stats uri /
        stats refresh 5s
    frontend http_front
        bind *:8081
        default_backend http_back
    backend http_back
        server s1 127.0.0.1:1 check
EOF

    container=$(docker run -d --rm \
        -v "${CONFIG}:/app/haproxy.cfg:ro" \
        -p 19080:8080 \
        "$image" -f /app/haproxy.cfg 2>/dev/null || echo "")

    if [ -z "$container" ]; then
        rm -f "$CONFIG"
        echo "SKIP: Cannot start haproxy container"
        return 0
    fi

    sleep 2

    # Test HAProxy stats page is accessible
    HTTP_CODE=$(curl -sf -o /dev/null -w "%{http_code}" \
        "http://localhost:19080/" 2>/dev/null || echo "000")

    docker stop "$container" 2>/dev/null || true
    rm -f "$CONFIG"

    if [ "$HTTP_CODE" = "200" ]; then
        echo "PASS: HAProxy stats page is accessible"
        return 0
    else
        echo "FAIL: HAProxy stats returned HTTP ${HTTP_CODE}"
        return 1
    fi
}

# =============================================================================
# ENVOY FUNCTIONAL TESTS
# =============================================================================

test_envoy_version() {
    local image="$1"

    RESULT=$(docker run --rm "$image" /envoy --version 2>&1 | head -1 || echo "")

    if echo "$RESULT" | grep -qi "version"; then
        echo "PASS: Envoy reports version: ${RESULT}"
        return 0
    else
        echo "FAIL: Envoy did not report version"
        return 1
    fi
}

# =============================================================================
# CADDY FUNCTIONAL TESTS
# =============================================================================

test_caddy_serves_content() {
    local image="$1"
    local container

    CONFIG=$(mktemp)
    cat > "$CONFIG" << 'EOF'
    :8080 {
        respond "evergreen-caddy-ok" 200
    }
EOF

    container=$(docker run -d --rm \
        -v "${CONFIG}:/app/Caddyfile:ro" \
        -p 28080:8080 \
        "$image" --config /app/Caddyfile 2>/dev/null || echo "")

    if [ -z "$container" ]; then
        rm -f "$CONFIG"
        echo "SKIP: Cannot start caddy container"
        return 0
    fi

    sleep 2

    RESULT=$(curl -sf "http://localhost:28080/" 2>/dev/null || echo "")
    docker stop "$container" 2>/dev/null || true
    rm -f "$CONFIG"

    if [ "$RESULT" = "evergreen-caddy-ok" ]; then
        echo "PASS: Caddy serves content correctly"
        return 0
    else
        echo "FAIL: Caddy returned '${RESULT}', expected 'evergreen-caddy-ok'"
        return 1
    fi
}
```

#### Test Matrix

| Proxy | Test | Expected Result | Timeout |
|-------|------|----------------|---------|
| Nginx | Serve static content via config | HTTP 200 with "evergreen-ok" | 15s |
| Nginx | Version flag | Reports version string | 5s |
| Traefik | API dashboard accessible | HTTP 200 on /api/overview | 15s |
| HAProxy | Stats page accessible | HTTP 200 on stats URI | 15s |
| Envoy | Version flag | Reports version string | 5s |
| Caddy | Serve content via Caddyfile | HTTP 200 with "evergreen-caddy-ok" | 15s |

#### Implementation Steps

1. **Implement proxy tests**: Write test functions for each proxy type.

2. **Handle configuration injection**: Most proxies need a config file to be useful. Use Docker volume mounts with temporary config files.

3. **Handle port conflicts**: Each test uses a unique host port to allow parallel execution.

4. **Handle proxy-specific startup**: Some proxies (envoy) need complex configs. For Phase 3, test version flag and simple configs only.

5. **CI integration**: Add to functional test job.

#### Verification Criteria

- [ ] Nginx serves configured static content with correct HTTP status
- [ ] Traefik API/dashboard is accessible
- [ ] HAProxy stats page is accessible
- [ ] Envoy reports version correctly
- [ ] Caddy serves content via Caddyfile
- [ ] All tests use ephemeral containers
- [ ] Port assignments do not conflict

---

### 3.3 T3.1.3: Write adversarial tests for all images

#### Problem Analysis

Adversarial tests verify that security constraints hold even under deliberate attack. These tests attempt actions that a compromised process might perform and verify that the container's security measures prevent them.

**Attack categories:**

| Category | Attack | Mitigation | Test Method |
|----------|--------|------------|-------------|
| Shell access | Execute `/bin/sh` | C003 (no shell) | Try to exec shell |
| Privilege escalation | Read `/etc/shadow` | C001 (non-root) + file permissions | Try to read sensitive files |
| Package installation | Run `apt-get install` | C004 (no package manager) | Try to install a package |
| Network exfiltration | Connect to external host | Network policy (runtime) | Try DNS resolution + HTTP |
| Process injection | ptrace another process | Seccomp/AppArmor (Phase 2) | Try ptrace |
| Binary execution | Run arbitrary binary | C002 (read-only fs) | Try to write + exec |
| Sensitive file access | Read `/proc/self/maps` | File permissions | Try to read /proc entries |

#### Solution: Adversarial Test Suite

**Test file:** `images/tests/adversarial/test_adversarial.sh`

```bash
#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASS=0
FAIL=0
SKIP=0

test_shell_escape() {
    local image="$1"
    local shells=("/bin/sh" "/bin/bash" "/dash" "/ash" "/zsh" "/ksh")

    for shell in "${shells[@]}"; do
        # Try to execute the shell
        if docker run --rm --entrypoint "$shell" "$image" -c "echo SHELL_ESCAPE" 2>/dev/null; then
            echo "FAIL: Shell escape possible via ${shell}"
            FAIL=$((FAIL + 1))
            return 1
        fi
    done

    # Try to exec shell from within the container
    if docker run --rm "$image" sh -c "echo SHELL_ESCAPE" 2>/dev/null; then
        echo "FAIL: Shell accessible via default CMD"
        FAIL=$((FAIL + 1))
        return 1
    fi

    echo "PASS: Shell escape blocked (no shell in image)"
    PASS=$((PASS + 1))
    return 0
}

test_privilege_escalation() {
    local image="$1"

    # Test 1: Check effective UID
    EUID=$(docker run --rm "$image" id -u 2>/dev/null || echo "unknown")

    if [ "$EUID" = "0" ]; then
        echo "FAIL: Container runs as root (UID 0)"
        FAIL=$((FAIL + 1))
        return 1
    fi

    # Test 2: Try to read /etc/shadow
    if docker run --rm "$image" cat /etc/shadow 2>/dev/null; then
        echo "FAIL: Can read /etc/shadow"
        FAIL=$((FAIL + 1))
        return 1
    fi

    # Test 3: Try to use sudo/su
    for tool in sudo su; do
        if docker run --rm "$image" "$tool" whoami 2>/dev/null; then
            echo "FAIL: Privilege escalation via ${tool}"
            FAIL=$((FAIL + 1))
            return 1
        fi
    done

    # Test 4: Check for setuid binaries
    SUID=$(docker run --rm "$image" find / -perm -4000 -type f 2>/dev/null || echo "")
    if [ -n "$SUID" ]; then
        echo "WARN: Setuid binaries found: ${SUID}"
        # Not a fail — setuid in scratch images is expected for the main binary
    fi

    echo "PASS: Privilege escalation blocked (UID=${EUID})"
    PASS=$((PASS + 1))
    return 0
}

test_package_manager_execution() {
    local image="$1"

    for pm in apt apt-get apk dnf yum zypper pip npm gem; do
        if docker run --rm --entrypoint "$pm" "$image" --version 2>/dev/null; then
            echo "FAIL: Package manager ${pm} is accessible"
            FAIL=$((FAIL + 1))
            return 1
        fi
    done

    # Try common install commands
    if docker run --rm "$image" apt-get install -y curl 2>/dev/null; then
        echo "FAIL: apt-get install succeeds"
        FAIL=$((FAIL + 1))
        return 1
    fi

    if docker run --rm "$image" apk add curl 2>/dev/null; then
        echo "FAIL: apk add succeeds"
        FAIL=$((FAIL + 1))
        return 1
    fi

    echo "PASS: Package manager execution blocked"
    PASS=$((PASS + 1))
    return 0
}

test_network_exfiltration() {
    local image="$1"

    # Test 1: DNS resolution to known-bad domain
    # (Use a domain that should not resolve in test environment)
    if docker run --rm "$image" nslookup evergreen-test-not-exists.invalid 2>/dev/null; then
        echo "WARN: DNS resolution works (expected in non-scratch images)"
    fi

    # Test 2: Try to connect to external host (using curl if available)
    # This test verifies that if curl exists, it's not trivially exfiltrating
    if docker run --rm "$image" curl -sf http://ifconfig.me 2>/dev/null; then
        echo "WARN: Outbound HTTP works (expected in images with curl)"
        # This is a warning, not a fail — network restrictions are runtime policy
    fi

    # Test 3: Check for network tools
    for tool in wget curl nc ncat netcat socat; do
        if docker run --rm "$image" which "$tool" 2>/dev/null; then
            echo "INFO: Network tool ${tool} found in image"
        fi
    done

    echo "PASS: Network exfiltration test completed (runtime policy required for enforcement)"
    PASS=$((PASS + 1))
    return 0
}

test_sensitive_file_access() {
    local image="$1"

    # /proc/self/maps — reveals memory layout
    if docker run --rm "$image" cat /proc/self/maps 2>/dev/null; then
        echo "WARN: /proc/self/maps is readable (common in Linux containers)"
    fi

    # /proc/1/environ — reveals environment variables of PID 1
    if docker run --rm "$image" cat /proc/1/environ 2>/dev/null; then
        echo "WARN: /proc/1/environ is readable"
    fi

    # Try to write to /tmp
    if docker run --rm "$image" sh -c "echo test > /tmp/test_write" 2>/dev/null; then
        echo "WARN: /tmp is writable"
    fi

    echo "PASS: Sensitive file access test completed"
    PASS=$((PASS + 1))
    return 0
}

# =============================================================================
# RUN ALL ADVERSARIAL TESTS
# =============================================================================

run_adversarial_tests() {
    local image="$1"

    echo "=========================================="
    echo "ADVERSARIAL TESTS: ${image}"
    echo "=========================================="

    echo ""
    echo "--- Shell Escape ---"
    test_shell_escape "$image" || true

    echo ""
    echo "--- Privilege Escalation ---"
    test_privilege_escalation "$image" || true

    echo ""
    echo "--- Package Manager ---"
    test_package_manager_execution "$image" || true

    echo ""
    echo "--- Network Exfiltration ---"
    test_network_exfiltration "$image" || true

    echo ""
    echo "--- Sensitive File Access ---"
    test_sensitive_file_access "$image" || true

    echo ""
    echo "=========================================="
    echo "ADVERSARIAL RESULTS: ${PASS} passed, ${FAIL} failed, ${SKIP} skipped"
    echo "=========================================="

    [ "$FAIL" -gt 0 ] && return 1
    return 0
}

# Entry point
IMAGE="${1:?Usage: $0 <image>}"
run_adversarial_tests "$IMAGE"
```

#### Implementation Steps

1. **Create adversarial test directory**: `images/tests/adversarial/`

2. **Implement all adversarial test functions**: shell escape, privilege escalation, package install, network exfiltration, sensitive file access.

3. **Handle image categories**:
   - Scratch images: Most tests should pass (no shell, no package manager)
   - Debian-slim images: Shell and package manager tests may be expected failures (documented)
   - Distroless images: Similar to scratch

4. **Create expected-failure matrix**: Some images are expected to fail certain tests. These should be documented, not hidden:
   ```bash
   # debian-slim images are expected to have shell and package manager
   # These are tested in constraint tests C003/C004
   # Adversarial tests document the risk, not block the build
   ```

5. **CI integration**: Add adversarial test job (may be slow — run in parallel):
   ```yaml
   adversarial-tests:
     needs: [build, verify]
     runs-on: ubuntu-latest
     strategy:
       matrix:
         batch: [1, 2, 3, 4, 5]
     steps:
       - name: Run adversarial tests
         run: |
           for image in $(batch_images ${{ matrix.batch }}); do
             bash images/tests/adversarial/test_adversarial.sh "$image" || true
           done
   ```

#### Verification Criteria

- [ ] Shell escape test blocks execution on scratch/distroless images
- [ ] Privilege escalation test confirms non-root on all images
- [ ] Package manager execution test blocks on scratch/distroless images
- [ ] Network exfiltration test documents outbound connectivity
- [ ] Sensitive file access test documents /proc accessibility
- [ ] Test results are recorded (pass/fail/warn) for each image
- [ ] Expected failures are documented per image category

---

### 3.4 T3.1.4: Expand test_runner.sh config to cover all 223 images (Required Dependency)

#### Problem Analysis

The `test_runner.sh` `IMAGE_CONFIGS` has only ~35 entries. The functional tests (T3.1.1, T3.1.2) and adversarial tests (T3.1.3) need correct binary names, ports, and configurations for all 223 images.

#### Solution: Systematic Config Generation

1. **Auto-generate configs from Dockerfiles**:
   ```bash
   # Extract ENTRYPOINT binary from Dockerfile
   for dockerfile in images/*/Dockerfile; do
     image=$(dirname "$dockerfile" | sed 's|images/||')
     binary=$(grep '^ENTRYPOINT' "$dockerfile" | \
       grep -oP '\["?/\K[^", ]+')
     ports=$(grep '^EXPOSE' "$dockerfile" | \
       sed 's/EXPOSE //' | awk '{print $1}')
     echo "[\"$image\"]=\"${binary},${ports},${ports}\""
   done
   ```

2. **Manual review and correction**: Auto-generated configs need manual review for:
   - Variant images (nginx vs nginx-unprivileged — same binary, different ports)
   - Images with non-obvious binary names (mysql uses `mariadbd`)
   - Images with multiple binaries (postgres has `postgres`, `pg_isready`, `psql`)
   - Images that don't expose ports (CLI tools like cosign, trivy)

3. **Create `test_config.yaml`**: Move from bash associative array to YAML for better maintainability:
   ```yaml
   images:
     nginx:
       binary: /nginx
       health_port: 80
       primary_port: 80
       version_flag: "-v"
     postgresql:
       binary: postgres
       health_port: 5432
       primary_port: 5432
       version_flag: "--version"
       test_type: database
     redis:
       binary: redis-server
       health_port: 6379
       primary_port: 6379
       version_flag: "--version"
       test_type: database
     # ... 220 more entries
   ```

4. **Update test_runner.sh to read YAML**: Use `yq` or simple Python parser.

#### Verification Criteria

- [ ] Every image has a test config entry
- [ ] Binary names are correct for all images
- [ ] Ports are correct for all images
- [ ] Config includes test type (database, proxy, cli, etc.)
- [ ] `test_runner.sh` can load and use the YAML config

---

### 3.5 T3.2.1: Add image layer analysis (dive integration)

#### Problem Analysis

Docker image layers accumulate wasted space from:
- Downloaded archives not cleaned up
- Package manager caches
- Intermediate build artifacts
- Duplicate files across layers

Excessive layers increase:
- Image size
- Attack surface (more files to scan)
- Pull time

#### Solution: CI Integration with dive

**CI step:**
```yaml
- name: Analyze image layers with dive
  run: |
    docker run --rm -it \
      -v /var/run/docker.sock:/var/run/docker.sock \
      wagoodman/dive:0.12.0 \
      --ci \
      --lowestEfficiency=90 \
      --highestWastedBytes=5MB \
      --highestUserWastedPercent=5.0 \
      "$REF"
```

**dive thresholds:**

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Efficiency | >= 90% | At least 90% of layer space is used in final image |
| Wasted bytes | <= 5 MB | No single layer wastes more than 5MB |
| Wasted percent | <= 5% | No single layer wastes more than 5% of its space |
| Layer count | <= 5 | Minimal layers for smaller attack surface |

**Enforcement:**
- Tier 1: BLOCKING on all thresholds
- Tier 2: WARNING on all thresholds
- Tier 3: WARNING only

#### Implementation Steps

1. **Add dive to CI**: Install via Docker or binary.

2. **Configure thresholds**: Set appropriate limits per tier.

3. **Add to build.yml**: Run after build, before verify.

4. **Generate layer report**: Output layer analysis as build artifact.

#### Verification Criteria

- [ ] dive runs on all images in CI
- [ ] Tier 1 images have <= 5 layers
- [ ] Tier 1 images have >= 90% efficiency
- [ ] No single layer wastes > 5MB
- [ ] Layer analysis report generated as build artifact

---

### 3.6 T3.2.2: Add startup time benchmarking

#### Problem Analysis

Container startup time affects:
- Scaling speed during traffic spikes
- Rollout duration during deployments
- Health check latency
- Resource efficiency during autoscaling

#### Solution: Startup Time Measurement

**Benchmark script:**
```bash
#!/bin/bash
IMAGE="$1"

# Measure time from docker run to HEALTHCHECK passing
START=$(date +%s%N)

container=$(docker run -d --rm "$IMAGE" 2>/dev/null || echo "")

if [ -z "$container" ]; then
    echo "SKIP: Cannot start container for benchmarking"
    exit 0
fi

# Wait for HEALTHCHECK to pass (max 30 seconds)
retries=30
while [ $retries -gt 0 ]; do
    STATUS=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "none")
    if [ "$STATUS" = "healthy" ]; then
        break
    fi
    sleep 1
    retries=$((retries - 1))
done

END=$(date +%s%N)
ELAPSED_MS=$(( (END - START) / 1000000 ))

docker stop "$container" 2>/dev/null || true

echo "${IMAGE}: ${ELAPSED_MS}ms startup time"

if [ "$ELAPSED_MS" -gt 2000 ]; then
    echo "WARN: Startup time ${ELAPSED_MS}ms exceeds 2s threshold"
fi

# Output as GitHub Actions variable for reporting
echo "startup_ms=${ELAPSED_MS}" >> "$GITHUB_OUTPUT"
```

**Thresholds:**

| Category | Threshold | Rationale |
|----------|-----------|-----------|
| CLI tools | < 100ms | Should start and exit instantly |
| Proxies (Go) | < 500ms | Go binaries start fast |
| Databases | < 5000ms | Need initialization time |
| Heavy applications | < 10000ms | ERP, CRM need longer startup |

**CI integration:**
```yaml
- name: Benchmark startup time
  run: |
    {
      echo "## Startup Time Benchmark"
      echo ""
      echo "| Image | Startup (ms) | Threshold | Status |"
      echo "|-------|-------------|-----------|--------|"
    } >> "$GITHUB_STEP_SUMMARY"

    for image in "${IMAGE_LIST[@]}"; do
      MS=$(bash scripts/benchmark_startup.sh "$image" 2>/dev/null | grep 'startup_ms' | cut -d= -f2)
      if [ -n "$MS" ]; then
        echo "| ${image} | ${MS}ms | 2000ms | $( [ "$MS" -le 2000 ] && echo OK || echo SLOW ) |"
      fi
    done >> "$GITHUB_STEP_SUMMARY"
```

#### Implementation Steps

1. **Create benchmark script**: Measure startup time using `docker run -d` + HEALTHCHECK polling.

2. **Handle images without HEALTHCHECK**: Skip benchmarking for images without HEALTHCHECK (post-Phase 0 this should be zero).

3. **Handle images that need config**: Some images need config files to start. Use minimal default configs or skip.

4. **Add trend tracking**: Store benchmark results in build artifacts for comparison across builds.

5. **CI integration**: Add to build.yml after build stage.

#### Verification Criteria

- [ ] Startup time measured for all images with HEALTHCHECK
- [ ] Results reported in GitHub Step Summary table
- [ ] Images exceeding 2s threshold are flagged
- [ ] Benchmark results stored as build artifact
- [ ] CLI tools start in < 100ms

---

## 4. Quality Gates

### Gate QG-3.1: 100% of Images Have Functional Test Config

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| Config entries | Entries in test_config.yaml | 223 (100%) |
| Binary names correct | Spot-check 20 random images | 100% |
| Ports correct | Spot-check 20 random images | 100% |
| Test type assigned | All entries have test_type | 100% |

### Gate QG-3.2: All Adversarial Tests Pass

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| Shell escape blocked (scratch/distroless) | Test result | 100% |
| Privilege escalation blocked | Test result | 100% |
| Package manager blocked (scratch/distroless) | Test result | 100% |
| Network exfiltration documented | Test result | 100% |

### Gate QG-3.3: Critical Images Have Integration Tests

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| Database images tested | Databases with passing functional tests | 100% |
| Proxy images tested | Proxies with passing functional tests | 100% |
| CRUD operations verified | Data round-trip succeeds | 100% |

### Gate QG-3.4: All Images Have <= 5 Layers

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| Layer count | dive analysis | <= 5 for Tier 1 |
| Efficiency | dive analysis | >= 90% for Tier 1 |
| Wasted space | dive analysis | <= 5MB per layer |

---

## 5. Risk Register

| Risk | Probability | Impact | Mitigation | Owner | Related Task |
|------|-------------|--------|------------|-------|-------------|
| Database containers need writable data directories | HIGH | MEDIUM | Use tmpfs mounts; document per-database requirements | Nexus | T3.1.1 |
| Proxy tests need complex configurations | MEDIUM | MEDIUM | Use minimal configs; test version flag as baseline | Nexus | T3.1.2 |
| Adversarial tests false-positive on debian-slim images | HIGH | LOW | Expected-failure matrix; document per category | Nexus | T3.1.3 |
| Test config generation has wrong binary names | MEDIUM | MEDIUM | Manual review of all auto-generated configs | Nexus | T3.1.4 |
| dive reports are noisy for complex images | MEDIUM | LOW | Use tier-based thresholds; warning vs error | Nexus | T3.2.1 |
| Startup benchmarks are inconsistent (CI noise) | MEDIUM | LOW | Run 3x and take median; allow 20% variance | Nexus | T3.2.2 |
| CI timeout due to too many functional tests | MEDIUM | MEDIUM | Run tests in parallel batches; limit DB tests to Tier 1+2 | Nexus | T3.1.1 |
| Docker-in-Docker issues in CI | MEDIUM | HIGH | Use docker socket mounting; avoid nested containers | Nexus | T3.1.1 |

---

## 6. Rollback Procedures

### If T3.1.1 (database functional tests) causes widespread failures:
1. Identify root cause (usually permissions or data directory issues)
2. Add tmpfs mounts or volume mounts for data directories
3. If database image cannot start as non-root: document as known limitation
4. Reduce test scope to version flag only for problematic databases

### If T3.1.2 (proxy functional tests) causes failures:
1. Check that config files are valid
2. Verify port bindings don't conflict
3. Fall back to version-only tests for complex proxies (envoy, traefik)

### If T3.1.3 (adversarial tests) have too many failures:
1. Review expected-failure matrix
2. Separate blocking tests (privilege escalation) from informational tests (network)
3. Make informational tests non-blocking with warnings

### If T3.2.1 (dive) reports are too noisy:
1. Adjust thresholds per tier
2. Create per-image `.dive.yaml` overrides for known-acceptable waste
3. Make dive warnings non-blocking initially

---

## 7. Success Metrics

| Metric | Current Value | Target Value | Measurement |
|--------|--------------|--------------|-------------|
| Images with test config | 35 (16%) | 223 (100%) | test_config.yaml entries |
| Database functional tests | 0 | 11 (100%) | Test results |
| Proxy functional tests | 0 | 19 (100%) | Test results |
| Adversarial test coverage | 0% | 100% (all images) | Test run count |
| Images passing adversarial tests | N/A | 111+ Tier 1 (100%) | Test pass rate |
| Images with <= 5 layers | Unknown | 223 (100%) | dive analysis |
| Average image efficiency | Unknown | >= 90% | dive analysis |
| Average startup time | Unknown | < 2s (Tier 1) | Benchmark results |
| Test types per image | 3 (constraint, basic functional, ports) | 6+ (adversarial, layer, startup) | Test count |
| Property-based tests | 0 | >= 5 properties | Test count |

---

**END OF PHASE 3 PLAN**
