#!/usr/bin/env bash
set -eo pipefail

# Adapted from https://github.com/docker-library/mariadb/blob/master/docker-entrypoint.sh
# SPDX-License-Identifier: Apache-2.0
# Simplified for Evergreen non-root (UID 65532) wolfi-based images

mysql_log() {
    printf '%s [%s] [Entrypoint]: %s\n' "$(date --rfc-3339=seconds)" "$1" "${@:2}"
}
mysql_note() { mysql_log Note "$@"; }
mysql_warn() { mysql_log Warn "$@" >&2; }
mysql_error() { mysql_log ERROR "$@" >&2; exit 1; }

file_env() {
    local var="$1"
    local fileVar="${var}_FILE"
    local def="${2:-}"
    if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
        mysql_error "Both $var and $fileVar are set (but are exclusive)"
    fi
    local val="$def"
    if [ "${!var:-}" ]; then
        val="${!var}"
    elif [ "${!fileVar:-}" ]; then
        val="$(< "${!fileVar}")"
    fi
    export "$var"="$val"
    unset "$fileVar"
}

_is_sourced() {
    [ "${#FUNCNAME[@]}" -ge 2 ] \
        && [ "${FUNCNAME[0]}" = '_is_sourced' ] \
        && [ "${FUNCNAME[1]}" = 'source' ]
}

docker_verify_minimum_env() {
    if [ -z "$MARIADB_ROOT_PASSWORD" ] && [ -z "$MARIADB_ALLOW_EMPTY_ROOT_PASSWORD" ]; then
        mysql_error 'Database is uninitialized and password option is not specified.
    Specify MARIADB_ROOT_PASSWORD or MARIADB_ALLOW_EMPTY_ROOT_PASSWORD'
    fi
}

docker_create_db_directories() {
    mkdir -p "${DATADIR:-/var/lib/mysql}"
    mkdir -p /run/mysqld
}

docker_init_database_dir() {
    mysql_note "Initializing database files"
    mariadb-install-db \
        --datadir="${DATADIR:-/var/lib/mysql}" \
        --cross-bootstrap \
        --skip-test-db \
        --default-time-zone=SYSTEM \
        --enforce-storage-engine= \
        --skip-log-bin \
        --expire-logs-days=0 \
        --loose-innodb_buffer_pool_load_at_startup=0 \
        --loose-innodb_buffer_pool_dump_at_shutdown=0
    mysql_note "Database files initialized"
}

docker_setup_env() {
    file_env 'MARIADB_ROOT_PASSWORD'
    file_env 'MARIADB_DATABASE'
    file_env 'MARIADB_USER'
    file_env 'MARIADB_PASSWORD'
    DATADIR="${DATADIR:-/var/lib/mysql}"
    SOCKET="${SOCKET:-/run/mysqld/mysqld.sock}"
    export DATABASE_ALREADY_EXISTS=''
    if [ -d "$DATADIR/mysql" ]; then
        DATABASE_ALREADY_EXISTS='true'
    fi
}

docker_exec_client() {
    if [ -n "${MARIADB_DATABASE:-}" ]; then
        set -- --database="$MARIADB_DATABASE" "$@"
    fi
    mariadb --protocol=socket -uroot -hlocalhost --socket="$SOCKET" "$@"
}

docker_process_sql() {
    if [ '--dont-use-mysql-root-password' = "$1" ]; then
        shift
        MYSQL_PWD='' docker_exec_client "$@"
    else
        MYSQL_PWD="$MARIADB_ROOT_PASSWORD" docker_exec_client "$@"
    fi
}

docker_process_init_files() {
    [ -d /docker-entrypoint-initdb.d ] || return 0
    local f
    for f in /docker-entrypoint-initdb.d/*; do
        [ -e "$f" ] || continue
        case "$f" in
            *.sh)
                if [ -x "$f" ]; then
                    mysql_note "$0: running $f"
                    "$f"
                else
                    mysql_note "$0: sourcing $f"
                    . "$f"
                fi
                ;;
            *.sql)    mysql_note "$0: running $f"; docker_process_sql < "$f" ;;
            *.sql.gz) mysql_note "$0: running $f"; gunzip -c "$f" | docker_process_sql ;;
            *)        mysql_warn "$0: ignoring $f" ;;
        esac
    done
}

docker_temp_server_start() {
    "$@" --skip-networking --default-time-zone=SYSTEM --socket="$SOCKET" \
        --wsrep_on=OFF --expire-logs-days=0 --skip-slave-start \
        --loose-innodb_buffer_pool_load_at_startup=0 \
        --skip-ssl --ssl-cert='' --ssl-key='' --ssl-ca='' &
    declare -g MARIADB_PID=$!
    mysql_note "Waiting for server startup"
    local i
    for i in {30..0}; do
        if echo 'SELECT 1' | docker_process_sql --dont-use-mysql-root-password \
            --database=mysql --skip-ssl &> /dev/null; then
            break
        fi
        sleep 1
    done
    if [ "$i" = 0 ]; then
        mysql_error "Unable to start server"
    fi
}

docker_temp_server_stop() {
    kill "$MARIADB_PID" 2>/dev/null
    wait "$MARIADB_PID" 2>/dev/null
}

docker_sql_escape() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\'/\\\'}"
    printf '%s' "$s"
}

docker_setup_db() {
    local root_sql=""
    if [ -n "$MARIADB_ROOT_PASSWORD" ]; then
        local escaped
        escaped="$(docker_sql_escape "$MARIADB_ROOT_PASSWORD")"
        root_sql="SET PASSWORD FOR 'root'@'localhost' = PASSWORD('${escaped}');"
    fi

    local db_sql=""
    if [ -n "${MARIADB_DATABASE:-}" ]; then
        mysql_note "Creating database ${MARIADB_DATABASE}"
        db_sql="CREATE DATABASE IF NOT EXISTS \`${MARIADB_DATABASE}\`;"
    fi

    local user_sql=""
    if [ -n "${MARIADB_USER:-}" ] && [ -n "${MARIADB_PASSWORD:-}" ]; then
        mysql_note "Creating user ${MARIADB_USER}"
        local userEscaped
        userEscaped="$(docker_sql_escape "$MARIADB_PASSWORD")"
        user_sql="CREATE USER '${MARIADB_USER}'@'%' IDENTIFIED BY '${userEscaped}';"
        if [ -n "${MARIADB_DATABASE:-}" ]; then
            user_sql+=" GRANT ALL ON \`${MARIADB_DATABASE}\`.* TO '${MARIADB_USER}'@'%';"
        fi
    fi

    mysql_note "Securing system users"
    docker_process_sql --dont-use-mysql-root-password --database=mysql <<EOSQL
SET @@SESSION.SQL_LOG_BIN=0;
DROP USER IF EXISTS root@'127.0.0.1', root@'::1';
${root_sql}
${db_sql}
${user_sql}
EOSQL
}

_mysql_want_help() {
    local arg
    for arg; do
        case "$arg" in
            -'?'|--help|--print-defaults|-V|--version) return 0 ;;
        esac
    done
    return 1
}

_main() {
    if [ "${1:0:1}" = '-' ]; then
        set -- mariadbd "$@"
    fi

    if { [ "$1" = 'mariadbd' ] || [ "$1" = 'mysqld' ]; } && ! _mysql_want_help "$@"; then
        mysql_note "Entrypoint script for MariaDB Server started"
        docker_setup_env
        docker_create_db_directories

        if [ -z "$DATABASE_ALREADY_EXISTS" ]; then
            docker_verify_minimum_env
            ls /docker-entrypoint-initdb.d/ > /dev/null 2>&1 || true

            docker_init_database_dir
            mysql_note "Starting temporary server"
            docker_temp_server_start "$@"
            docker_setup_db
            docker_process_init_files
            mysql_note "Stopping temporary server"
            docker_temp_server_stop
            mysql_note "MariaDB init process done. Ready for start up."
        fi
    fi
    exec "$@"
}

if ! _is_sourced; then
    _main "$@"
fi
