#!/usr/bin/env bash
set -Eeo pipefail

# Adapted from https://github.com/docker-library/postgres/blob/master/docker-entrypoint.sh
# SPDX-License-Identifier: Apache-2.0
# Simplified for Evergreen non-root (UID 65532) wolfi-based images

file_env() {
    local var="$1"
    local fileVar="${var}_FILE"
    local def="${2:-}"
    if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
        printf >&2 'error: both %s and %s are set (but are exclusive)\n' "$var" "$fileVar"
        exit 1
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

docker_create_db_directories() {
    mkdir -p "$PGDATA"
    chmod 700 "$PGDATA" 2>/dev/null || :
    mkdir -p /var/run/postgresql 2>/dev/null || :
    chmod 3775 /var/run/postgresql 2>/dev/null || :
}

docker_init_database_dir() {
    local pwfile
    pwfile="$(mktemp)"
    printf '%s\n' "$POSTGRES_PASSWORD" > "$pwfile"
    initdb --username="$POSTGRES_USER" --pwfile="$pwfile" ${POSTGRES_INITDB_ARGS:-} "$@"
    rm -f "$pwfile"
}

docker_verify_minimum_env() {
    if [ -z "$POSTGRES_PASSWORD" ] && [ 'trust' != "${POSTGRES_HOST_AUTH_METHOD:-}" ]; then
        cat >&2 <<'EOE'
Error: POSTGRES_PASSWORD not set and POSTGRES_HOST_AUTH_METHOD is not "trust".
       Specify POSTGRES_PASSWORD for the superuser, e.g.:
       docker run -e POSTGRES_PASSWORD=secret ...
EOE
        exit 1
    fi
    if [ 'trust' = "${POSTGRES_HOST_AUTH_METHOD:-}" ]; then
        cat >&2 <<'EOWARN'
WARNING: POSTGRES_HOST_AUTH_METHOD is "trust" - passwordless access enabled.
EOWARN
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
                    printf '%s: running %s\n' "$0" "$f"
                    "$f"
                else
                    printf '%s: sourcing %s\n' "$0" "$f"
                    . "$f"
                fi
                ;;
            *.sql)    printf '%s: running %s\n' "$0" "$f"; docker_process_sql -f "$f" ;;
            *.sql.gz) printf '%s: running %s\n' "$0" "$f"; gunzip -c "$f" | docker_process_sql ;;
            *)        printf '%s: ignoring %s\n' "$0" "$f" ;;
        esac
    done
}

docker_process_sql() {
    local psql_args=( -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --no-password --no-psqlrc )
    if [ -n "${POSTGRES_DB:-}" ]; then
        psql_args+=( --dbname "$POSTGRES_DB" )
    fi
    PGHOST= PGHOSTADDR= psql "${psql_args[@]}" "$@"
}

docker_setup_db() {
    local dbAlreadyExists
    dbAlreadyExists="$(
        POSTGRES_DB= docker_process_sql --dbname postgres --set db="$POSTGRES_DB" --tuples-only <<'EOSQL'
            SELECT 1 FROM pg_database WHERE datname = :'db' ;
EOSQL
    )"
    if [ -z "$dbAlreadyExists" ]; then
        POSTGRES_DB= docker_process_sql --dbname postgres --set db="$POSTGRES_DB" <<'EOSQL'
            CREATE DATABASE :"db" ;
EOSQL
    fi
}

docker_setup_env() {
    file_env 'POSTGRES_PASSWORD'
    file_env 'POSTGRES_USER' 'postgres'
    file_env 'POSTGRES_DB' "$POSTGRES_USER"
    file_env 'POSTGRES_INITDB_ARGS'
    : "${POSTGRES_HOST_AUTH_METHOD:=}"
    export DATABASE_ALREADY_EXISTS=''
    if [ -s "$PGDATA/PG_VERSION" ]; then
        DATABASE_ALREADY_EXISTS='true'
    fi
}

pg_setup_hba_conf() {
    if [ "$1" = 'postgres' ]; then shift; fi
    local auth
    auth="$(postgres -C password_encryption "$@")"
    : "${POSTGRES_HOST_AUTH_METHOD:=$auth}"
    {
        printf '\n'
        [ 'trust' = "$POSTGRES_HOST_AUTH_METHOD" ] && printf '# WARNING: trust auth enabled\n'
        printf 'host all all all %s\n' "$POSTGRES_HOST_AUTH_METHOD"
    } >> "$PGDATA/pg_hba.conf"
}

docker_temp_server_start() {
    if [ "$1" = 'postgres' ]; then shift; fi
    NOTIFY_SOCKET= \
    PGUSER="${PGUSER:-$POSTGRES_USER}" \
    pg_ctl -D "$PGDATA" -o "-c listen_addresses='' -p ${PGPORT:-5432}" -w start
}

docker_temp_server_stop() {
    PGUSER="${PGUSER:-postgres}" \
    pg_ctl -D "$PGDATA" -m fast -w stop
}

_pg_want_help() {
    local arg
    for arg; do
        case "$arg" in
            -'?'|--help|--describe-config|-V|--version) return 0 ;;
        esac
    done
    return 1
}

_main() {
    if [ "${1:0:1}" = '-' ]; then
        set -- postgres "$@"
    fi

    if [ "$1" = 'postgres' ] && ! _pg_want_help "$@"; then
        docker_setup_env
        docker_create_db_directories

        if [ -z "$DATABASE_ALREADY_EXISTS" ]; then
            docker_verify_minimum_env
            ls /docker-entrypoint-initdb.d/ > /dev/null 2>&1 || true

            docker_init_database_dir "$@"
            pg_setup_hba_conf "$@"
            export PGPASSWORD="${PGPASSWORD:-$POSTGRES_PASSWORD}"

            docker_temp_server_start "$@"
            docker_setup_db
            docker_process_init_files
            docker_temp_server_stop

            unset PGPASSWORD
            echo
            echo 'PostgreSQL init process complete; ready for start up.'
            echo
        else
            echo
            echo 'PostgreSQL Database directory appears to contain a database; Skipping initialization'
            echo
        fi
    fi

    exec "$@"
}

if ! _is_sourced; then
    _main "$@"
fi
