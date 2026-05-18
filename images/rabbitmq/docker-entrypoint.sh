#!/usr/bin/env bash
set -euo pipefail

# Adapted from https://github.com/docker-library/rabbitmq/blob/master/docker-entrypoint.sh
# SPDX-License-Identifier: Apache-2.0
# Simplified for Evergreen non-root (UID 65532) wolfi-based images

deprecatedEnvVars=(
    RABBITMQ_DEFAULT_PASS_FILE
    RABBITMQ_DEFAULT_USER_FILE
    RABBITMQ_MANAGEMENT_SSL_CACERTFILE
    RABBITMQ_MANAGEMENT_SSL_CERTFILE
    RABBITMQ_MANAGEMENT_SSL_DEPTH
    RABBITMQ_MANAGEMENT_SSL_FAIL_IF_NO_PEER_CERT
    RABBITMQ_MANAGEMENT_SSL_KEYFILE
    RABBITMQ_MANAGEMENT_SSL_VERIFY
    RABBITMQ_SSL_CACERTFILE
    RABBITMQ_SSL_CERTFILE
    RABBITMQ_SSL_DEPTH
    RABBITMQ_SSL_FAIL_IF_NO_PEER_CERT
    RABBITMQ_SSL_KEYFILE
    RABBITMQ_SSL_VERIFY
    RABBITMQ_VM_MEMORY_HIGH_WATERMARK
)

hasOldEnv=
for old in "${deprecatedEnvVars[@]}"; do
    if [ -n "${!old:-}" ]; then
        echo >&2 "error: $old is set but deprecated"
        hasOldEnv=1
    fi
done

if [ -n "$hasOldEnv" ]; then
    echo >&2 'error: deprecated environment variables detected'
    echo >&2 'Please use a configuration file instead: https://www.rabbitmq.com/configure.html'
    exit 1
fi

if [ -z "${RABBITMQ_USE_LONGNAME:-}" ] && [ "$(hostname)" != "$(hostname -s)" ]; then
    : "${RABBITMQ_USE_LONGNAME:=true}"
fi

exec "$@"
