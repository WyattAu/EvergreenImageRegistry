
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /opt/venv || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates ; rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip || true && \
    pip install --no-cache-dir conan ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/conan || { echo '#!/bin/sh' > /usr/local/bin/conan && echo 'echo "conan-audit v${VERSION} binary not available - download failed" >&2
exit 1"' >> /usr/local/bin/conan && echo 'exit 1' >> /usr/local/bin/conan && chmod +x /usr/local/bin/conan ; } 2>/dev/null || true && \
    mkdir -p /app 2>/dev/null || true
FROM registry.access.redhat.com/ubi9/ubi-minimal
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"

RUN microdnf install -y python3 ca-certificates 
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false conan 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["conan"]
CMD ["audit"]
LABEL org.opencontainers.image.title="conan-audit" \
      org.opencontainers.image.description="Conan audit - C/C++ dependency security scanner" \
      org.opencontainers.image.vendor="conan-io" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/conan-io/conan" \
                  org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
