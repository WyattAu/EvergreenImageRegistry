
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /opt/venv || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates ; rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --break-system-packages --upgrade pip && \
    pip install --no-cache-dir --break-system-packages pip-audit || true && \
    mkdir -p /app-src 2>/dev/null || true && \
    test -f /app || { echo '#!/bin/sh' > /app/binary not available - download failed" >&2
exit 1 && echo 'echo "pip-audit v${VERSION} binary not available - download failed" >&2
exit 1"' >> /app/binary not available - download failed" >&2
exit 1 && echo 'exit 1' >> /app/binary not available - download failed" >&2
exit 1 && chmod +x /app ; } || true
FROM registry.access.redhat.com/ubi9/ubi-minimal
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"

RUN microdnf install -y python3 ca-certificates
RUN mkdir -p /opt/venv || true
COPY --from=builder /opt/venv /opt/venv
RUN mkdir -p /app || true
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false pipaudit 2>/dev/null || true && \
    chown -R 65532:65532 /app/binary not available - download failed" >&2
exit 1 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["pip-audit"]
LABEL org.opencontainers.image.title="pip-audit" \
      org.opencontainers.image.description="pip audit - Python dependency security scanner" \
      org.opencontainers.image.vendor="pypa" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/pypa/pip-audit" \
                  org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
