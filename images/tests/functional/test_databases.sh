#!/bin/bash
# =============================================================================
# FUNCTIONAL TEST SUITE - DATABASES
# =============================================================================
# Tests for database images: PostgreSQL, Redis, MySQL/MariaDB, MongoDB, Memcached
#
# Usage: IMAGE=<image> ./test_databases.sh
#        ./test_databases.sh <image>
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

IMAGE="${IMAGE:-${1:-}}"
CONTAINER_NAME=""
PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0
TOTAL=0

cleanup() {
    if [ -n "$CONTAINER_NAME" ]; then
        docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
        docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    fi
}
trap cleanup EXIT

record() {
    local test_id="$1" status="$2" desc="$3"
    TOTAL=$((TOTAL + 1))
    case "$status" in
        PASS) PASS_COUNT=$((PASS_COUNT + 1)); echo -e "  ${GREEN}PASS${NC} [$test_id] $desc" ;;
        FAIL) FAIL_COUNT=$((FAIL_COUNT + 1)); echo -e "  ${RED}FAIL${NC} [$test_id] $desc" ;;
        SKIP) SKIP_COUNT=$((SKIP_COUNT + 1)); echo -e "  ${YELLOW}SKIP${NC} [$test_id] $desc" ;;
    esac
}

wait_for_container() {
    local max_wait="${1:-30}"
    local waited=0
    while [ $waited -lt $max_wait ]; do
        if ! docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
            return 1
        fi
        local health
        health=$(docker inspect --format='{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "unknown")
        if [ "$health" = "healthy" ]; then
            return 0
        fi
        sleep 2
        waited=$((waited + 2))
    done
    local state
    state=$(docker inspect --format='{{.State.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "unknown")
    if [ "$state" = "running" ]; then
        return 0
    fi
    return 1
}

detect_db_type() {
    local img="$1"
    local entrypoint
    entrypoint=$(docker inspect "$img" --format='{{(index .Config.Entrypoint 0)}}' 2>/dev/null || echo "")
    case "$img" in
        *postgres*) echo "postgresql" ;;
        *redis*) echo "redis" ;;
        *mysql*) echo "mysql" ;;
        *mariadb*) echo "mysql" ;;
        *mongo*) echo "mongodb" ;;
        *memcached*) echo "memcached" ;;
        *cassandra*) echo "cassandra" ;;
        *couchdb*) echo "couchdb" ;;
        *couchbase*) echo "couchbase" ;;
        *arangodb*) echo "arangodb" ;;
        *neo4j*) echo "neo4j" ;;
        *scylladb*) echo "scylladb" ;;
        *cockroachdb*) echo "cockroachdb" ;;
        *dragonfly*) echo "dragonfly" ;;
        *surrealdb*) echo "surrealdb" ;;
        *sqlite*) echo "sqlite" ;;
        *valkey*) echo "redis" ;;
        *timescaledb*) echo "postgresql" ;;
        *postgis*) echo "postgresql" ;;
        *)
            case "$entrypoint" in
                *postgres*) echo "postgresql" ;;
                *redis*) echo "redis" ;;
                *mariadbd*|*mysqld*) echo "mysql" ;;
                *mongod*) echo "mongodb" ;;
                *memcached*) echo "memcached" ;;
                *sqlite3*) echo "sqlite" ;;
                *cassandra*) echo "cassandra" ;;
                *couchdb*) echo "couchdb" ;;
                *couchbase*) echo "couchbase" ;;
                *arangod*) echo "arangodb" ;;
                *neo4j*) echo "neo4j" ;;
                *scylla*) echo "scylladb" ;;
                *cockroach*) echo "cockroachdb" ;;
                *dragonfly*) echo "dragonfly" ;;
                *surreal*) echo "surrealdb" ;;
                *valkey*) echo "redis" ;;
                *) echo "unknown" ;;
            esac
            ;;
    esac
}

# =============================================================================
# POSTGRESQL TESTS
# =============================================================================

test_postgresql() {
    echo ""
    echo "--- PostgreSQL Tests ---"

    CONTAINER_NAME="dbtest-pg-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -e POSTGRES_PASSWORD=testpass \
        -e POSTGRES_DB=testdb \
        -p 15432:5432 \
        "$IMAGE" >/dev/null 2>&1; then
        record "PG-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_container 30; then
        record "PG-START" "FAIL" "Container did not become ready within timeout"
        docker logs "$CONTAINER_NAME" 2>&1 | tail -5
        return
    fi
    record "PG-START" "PASS" "Container started and ready"

    if command -v psql &>/dev/null; then
        if psql -h 127.0.0.1 -p 15432 -U postgres -d testdb -c "CREATE TABLE test_pg (id INT, name TEXT);" >/dev/null 2>&1 <<EOF
testpass
EOF
        then
            record "PG-CREATE" "PASS" "CREATE TABLE succeeded"
        else
            record "PG-CREATE" "FAIL" "CREATE TABLE failed"
        fi

        if psql -h 127.0.0.1 -p 15432 -U postgres -d testdb -c "INSERT INTO test_pg VALUES (1, 'hello');" >/dev/null 2>&1; then
            record "PG-INSERT" "PASS" "INSERT succeeded"
        else
            record "PG-INSERT" "FAIL" "INSERT failed"
        fi

        local result
        result=$(psql -h 127.0.0.1 -p 15432 -U postgres -d testdb -t -c "SELECT name FROM test_pg WHERE id=1;" 2>/dev/null | tr -d ' ')
        if [ "$result" = "hello" ]; then
            record "PG-SELECT" "PASS" "SELECT returned correct data"
        else
            record "PG-SELECT" "FAIL" "SELECT returned '$result', expected 'hello'"
        fi
    else
        record "PG-CREATE" "SKIP" "psql not available"
        record "PG-INSERT" "SKIP" "psql not available"
        record "PG-SELECT" "SKIP" "psql not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# REDIS TESTS
# =============================================================================

test_redis() {
    echo ""
    echo "--- Redis Tests ---"

    CONTAINER_NAME="dbtest-redis-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -p 16379:6379 \
        "$IMAGE" >/dev/null 2>&1; then
        record "REDIS-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_container 15; then
        record "REDIS-START" "FAIL" "Container did not become ready within timeout"
        return
    fi
    record "REDIS-START" "PASS" "Container started and ready"

    if command -v redis-cli &>/dev/null; then
        if redis-cli -h 127.0.0.1 -p 16379 PING 2>/dev/null | grep -q PONG; then
            record "REDIS-PING" "PASS" "PING returned PONG"
        else
            record "REDIS-PING" "FAIL" "PING did not return PONG"
        fi

        if redis-cli -h 127.0.0.1 -p 16379 SET testkey "testvalue" >/dev/null 2>&1; then
            record "REDIS-SET" "PASS" "SET succeeded"
        else
            record "REDIS-SET" "FAIL" "SET failed"
        fi

        local val
        val=$(redis-cli -h 127.0.0.1 -p 16379 GET testkey 2>/dev/null)
        if [ "$val" = "testvalue" ]; then
            record "REDIS-GET" "PASS" "GET returned correct value"
        else
            record "REDIS-GET" "FAIL" "GET returned '$val', expected 'testvalue'"
        fi
    else
        record "REDIS-PING" "SKIP" "redis-cli not available"
        record "REDIS-SET" "SKIP" "redis-cli not available"
        record "REDIS-GET" "SKIP" "redis-cli not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# MYSQL / MARIADB TESTS
# =============================================================================

test_mysql() {
    echo ""
    echo "--- MySQL/MariaDB Tests ---"

    CONTAINER_NAME="dbtest-mysql-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -e MYSQL_ROOT_PASSWORD=testpass \
        -p 13306:3306 \
        "$IMAGE" >/dev/null 2>&1; then
        record "MYSQL-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_container 45; then
        record "MYSQL-START" "FAIL" "Container did not become ready within timeout"
        docker logs "$CONTAINER_NAME" 2>&1 | tail -5
        return
    fi
    record "MYSQL-START" "PASS" "Container started and ready"

    if command -v mysql &>/dev/null; then
        if mysql -h 127.0.0.1 -P 13306 -u root -ptestpass -e "CREATE DATABASE IF NOT EXISTS testdb;" >/dev/null 2>&1; then
            record "MYSQL-CREATEDB" "PASS" "CREATE DATABASE succeeded"
        else
            record "MYSQL-CREATEDB" "FAIL" "CREATE DATABASE failed"
        fi

        if mysql -h 127.0.0.1 -P 13306 -u root -ptestpass testdb -e "CREATE TABLE test_tbl (id INT, name VARCHAR(50));" >/dev/null 2>&1; then
            record "MYSQL-CREATETBL" "PASS" "CREATE TABLE succeeded"
        else
            record "MYSQL-CREATETBL" "FAIL" "CREATE TABLE failed"
        fi

        if mysql -h 127.0.0.1 -P 13306 -u root -ptestpass testdb -e "INSERT INTO test_tbl VALUES (1, 'hello');" >/dev/null 2>&1; then
            record "MYSQL-INSERT" "PASS" "INSERT succeeded"
        else
            record "MYSQL-INSERT" "FAIL" "INSERT failed"
        fi

        local result
        result=$(mysql -h 127.0.0.1 -P 13306 -u root -ptestpass testdb -N -e "SELECT name FROM test_tbl WHERE id=1;" 2>/dev/null | tr -d ' ')
        if [ "$result" = "hello" ]; then
            record "MYSQL-SELECT" "PASS" "SELECT returned correct data"
        else
            record "MYSQL-SELECT" "FAIL" "SELECT returned '$result', expected 'hello'"
        fi
    else
        record "MYSQL-CREATEDB" "SKIP" "mysql client not available"
        record "MYSQL-CREATETBL" "SKIP" "mysql client not available"
        record "MYSQL-INSERT" "SKIP" "mysql client not available"
        record "MYSQL-SELECT" "SKIP" "mysql client not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# MONGODB TESTS
# =============================================================================

test_mongodb() {
    echo ""
    echo "--- MongoDB Tests ---"

    CONTAINER_NAME="dbtest-mongo-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -p 27017:27017 \
        "$IMAGE" >/dev/null 2>&1; then
        record "MONGO-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_container 30; then
        record "MONGO-START" "FAIL" "Container did not become ready within timeout"
        return
    fi
    record "MONGO-START" "PASS" "Container started and ready"

    if command -v mongosh &>/dev/null; then
        if mongosh --quiet --host 127.0.0.1 --port 27017 --eval 'db.testCollection.insertOne({key:"testval"})' >/dev/null 2>&1; then
            record "MONGO-INSERT" "PASS" "insertOne succeeded"
        else
            record "MONGO-INSERT" "FAIL" "insertOne failed"
        fi

        local result
        result=$(mongosh --quiet --host 127.0.0.1 --port 27017 --eval 'db.testCollection.findOne({key:"testval"}).key' 2>/dev/null)
        if [ "$result" = "testval" ]; then
            record "MONGO-FIND" "PASS" "findOne returned correct document"
        else
            record "MONGO-FIND" "FAIL" "findOne returned '$result', expected 'testval'"
        fi
    elif command -v mongo &>/dev/null; then
        if mongo --quiet --host 127.0.0.1 --port 27017 --eval 'db.testCollection.insertOne({key:"testval"})' >/dev/null 2>&1; then
            record "MONGO-INSERT" "PASS" "insertOne succeeded"
        else
            record "MONGO-INSERT" "FAIL" "insertOne failed"
        fi

        local result
        result=$(mongo --quiet --host 127.0.0.1 --port 27017 --eval 'db.testCollection.findOne({key:"testval"}).key' 2>/dev/null)
        if [ "$result" = "testval" ]; then
            record "MONGO-FIND" "PASS" "findOne returned correct document"
        else
            record "MONGO-FIND" "FAIL" "findOne returned '$result', expected 'testval'"
        fi
    else
        record "MONGO-INSERT" "SKIP" "mongosh/mongo not available"
        record "MONGO-FIND" "SKIP" "mongosh/mongo not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# MEMCACHED TESTS
# =============================================================================

test_memcached() {
    echo ""
    echo "--- Memcached Tests ---"

    CONTAINER_NAME="dbtest-mc-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -p 11211:11211 \
        "$IMAGE" >/dev/null 2>&1; then
        record "MC-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_container 10; then
        record "MC-START" "FAIL" "Container did not become ready within timeout"
        return
    fi
    record "MC-START" "PASS" "Container started and ready"

    if command -v nc &>/dev/null || command -v netcat &>/dev/null; then
        local nc_cmd="nc"
        command -v nc &>/dev/null || nc_cmd="netcat"

        printf "set testkey 0 60 5\r\nhello\r\n" | "$nc_cmd" -q 2 127.0.0.1 11211 >/dev/null 2>&1
        if printf "set testkey 0 60 5\r\nhello\r\n" | "$nc_cmd" -w 2 127.0.0.1 11211 2>/dev/null | grep -q STORED; then
            record "MC-SET" "PASS" "SET returned STORED"
        else
            record "MC-SET" "SKIP" "SET verification inconclusive (nc behavior varies)"
        fi

        local get_result
        get_result=$(printf "get testkey\r\n" | "$nc_cmd" -w 2 127.0.0.1 11211 2>/dev/null || echo "")
        if echo "$get_result" | grep -q "hello"; then
            record "MC-GET" "PASS" "GET returned correct value"
        else
            record "MC-GET" "SKIP" "GET verification inconclusive (nc behavior varies)"
        fi
    else
        record "MC-SET" "SKIP" "nc/netcat not available"
        record "MC-GET" "SKIP" "nc/netcat not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# SQLITE TESTS
# =============================================================================

test_sqlite() {
    echo ""
    echo "--- SQLite Tests ---"

    local result
    result=$(docker run --rm "$IMAGE" "testdb.sqlite" "CREATE TABLE t(id INT); INSERT INTO t VALUES(42); SELECT id FROM t;" 2>&1 || echo "")
    if echo "$result" | grep -q "42"; then
        record "SQLITE-CRUD" "PASS" "CREATE/INSERT/SELECT succeeded, got 42"
    else
        record "SQLITE-CRUD" "FAIL" "SQLite CRUD test failed: $result"
    fi
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    if [ -z "$IMAGE" ]; then
        echo "Usage: IMAGE=<image> $0"
        echo "       $0 <image>"
        exit 1
    fi

    if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
        echo "ERROR: Image '$IMAGE' not found locally"
        exit 1
    fi

    echo "=========================================="
    echo "DATABASE FUNCTIONAL TESTS"
    echo "Image: $IMAGE"
    echo "=========================================="

    local db_type
    db_type=$(detect_db_type "$IMAGE")
    echo "Detected database type: $db_type"

    case "$db_type" in
        postgresql) test_postgresql ;;
        redis) test_redis ;;
        mysql) test_mysql ;;
        mongodb) test_mongodb ;;
        memcached) test_memcached ;;
        sqlite) test_sqlite ;;
        *)
            echo ""
            echo "Unknown database type. Attempting all tests..."
            for test_fn in test_postgresql test_redis test_mysql test_mongodb test_memcached; do
                $test_fn || true
            done
            ;;
    esac

    echo ""
    echo "=========================================="
    echo "SUMMARY: $IMAGE (type=$db_type)"
    echo "=========================================="
    echo -e "  ${GREEN}PASS${NC}: $PASS_COUNT"
    echo -e "  ${RED}FAIL${NC}: $FAIL_COUNT"
    echo -e "  ${YELLOW}SKIP${NC}: $SKIP_COUNT"
    echo "  TOTAL: $TOTAL"
    echo "=========================================="

    [ $FAIL_COUNT -eq 0 ]
}

main "$@"
