ARG VERSION=6.9.0
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=6.9.0
RUN mkdir -p /venv || true
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-venv curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir taiga-protected==${VERSION} 2>/dev/null || true && \
    mkdir -p /app /var/log/taiga-protected /etc/taiga-protected 2>/dev/null || true

FROM registry.access.redhat.com/ubi9/ubi-minimal
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"
RUN microdnf install -y python3 ca-certificates libstdc++ 2>/dev/null || true
COPY --from=downloader /venv /venv
COPY --from=downloader /var/log/taiga-protected /var/log/taiga-protected
COPY --from=downloader /etc/taiga-protected /etc/taiga-protected
USER 65532:65532
WORKDIR /app
EXPOSE 8003

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8003/ || exit 1
ENTRYPOINT ["/venv/bin/python", "-m", "taiga_protected"]

LABEL org.opencontainers.image.title="taiga-protected" \
      org.opencontainers.image.description="Taiga Protected - file access protection proxy for Taiga" \
      org.opencontainers.image.version="6.9.0" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-protected" \
      evergreen.image.tier="3" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
