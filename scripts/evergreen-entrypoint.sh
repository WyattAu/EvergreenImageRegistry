#!/bin/bash
set -e

EVERGREEN_SHUTDOWN_TIMEOUT="${EVERGREEN_SHUTDOWN_TIMEOUT:-3}"
EVERGREEN_CHILD_PID=""

cleanup() {
    _sig="$1"
    _remaining="$EVERGREEN_SHUTDOWN_TIMEOUT"

    if [ -n "$EVERGREEN_CHILD_PID" ] && kill -0 "$EVERGREEN_CHILD_PID" 2>/dev/null; then
        kill "-$_sig" "$EVERGREEN_CHILD_PID" 2>/dev/null || true

        while [ "$_remaining" -gt 0 ]; do
            if ! kill -0 "$EVERGREEN_CHILD_PID" 2>/dev/null; then
                wait "$EVERGREEN_CHILD_PID" 2>/dev/null || true
                exit $?
            fi
            sleep 1
            _remaining=$((_remaining - 1))
        done

        kill -9 "$EVERGREEN_CHILD_PID" 2>/dev/null || true
        wait "$EVERGREEN_CHILD_PID" 2>/dev/null || true
        exit 143
    fi
}

trap 'cleanup TERM' TERM
trap 'cleanup INT' INT
trap 'cleanup QUIT' QUIT

reap_zombies() {
    while true; do
        wait -n 2>/dev/null && continue
        break
    done
    return 0
}

if [ $# -eq 0 ]; then
    echo "Usage: evergreen-entrypoint.sh <command> [args...]" >&2
    exit 1
fi

"$@" &
EVERGREEN_CHILD_PID=$!

reap_zombies
wait "$EVERGREEN_CHILD_PID" 2>/dev/null
_exit=$?
EVERGREEN_CHILD_PID=""
exit "$_exit"
