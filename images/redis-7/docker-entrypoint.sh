#!/bin/sh
set -e

# Adapted from https://github.com/docker-library/redis/blob/master/docker-entrypoint.sh
# SPDX-License-Identifier: Apache-2.0
# Simplified for Evergreen non-root (UID 65532) wolfi-based images

if [ "${1#-}" != "$1" ] || [ "${1%.conf}" != "$1" ]; then
    set -- redis-server "$@"
fi

um="$(umask)"
if [ "$um" = '0022' ]; then
    umask 0077
fi

exec "$@"
