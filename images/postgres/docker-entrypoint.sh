#!/bin/sh
set -e

if [ ! -f "$PGDATA/PG_VERSION" ]; then
    echo "Initializing database..."
    initdb -D "$PGDATA" --auth=trust --encoding=UTF8 --locale=C.UTF-8
fi

# Create database and user via postgres --single if env vars are set
if [ -n "$POSTGRES_DB" ] && [ -n "$POSTGRES_USER" ]; then
    DB_EXISTS=$(postgres --single -D "$PGDATA" postgres 2>/dev/null | grep -c "database \"$POSTGRES_DB\"" || true)
    if [ "$DB_EXISTS" -eq 0 ]; then
        printf 'CREATE DATABASE "%s";\n' "$POSTGRES_DB" | postgres --single -D "$PGDATA" postgres 2>/dev/null || true
    fi

    USER_EXISTS=$(postgres --single -D "$PGDATA" postgres 2>/dev/null | grep -c "role \"$POSTGRES_USER\"" || true)
    if [ "$USER_EXISTS" -eq 0 ]; then
        PWD_SQL=""
        if [ -n "$POSTGRES_PASSWORD" ]; then
            PWD_SQL="PASSWORD '$POSTGRES_PASSWORD'"
        fi
        printf 'CREATE ROLE "%s" WITH LOGIN SUPERUSER %s;\n' "$POSTGRES_USER" "$PWD_SQL" | postgres --single -D "$PGDATA" postgres 2>/dev/null || true
    fi
fi

exec postgres -D "$PGDATA" -c listen_addresses="*"
