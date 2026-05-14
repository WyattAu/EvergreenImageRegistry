FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=3.12
ARG TARGETARCH
RUN apk add --no-cache python3 2>/dev/null || true
USER 65532:65532
EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["sleep", "infinity"]
LABEL org.opencontainers.image.title="python-slim" \
      org.opencontainers.image.source="https://github.com/python/cpython" \
            org.opencontainers.image.version="3.12" \
      org.opencontainers.image.description="python-slim container image" \
evergreen.base.image="wolfi"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="0"
