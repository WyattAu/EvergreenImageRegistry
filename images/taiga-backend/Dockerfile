ARG VERSION=6.9.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=6.9.0
RUN mkdir -p /opt/venv || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        gcc \
        libssl-dev \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        libjpeg62-turbo-dev \
        libpq-dev \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "git+https://github.com/taigaio/taiga-back.git@${VERSION}#egg=taiga-back" || { echo "pip install failed, creating binary not available - download failed" >&2
exit 1" ; mkdir -p /opt/venv/bin && echo '#!/bin/sh' > /opt/venv/bin/taiga && echo 'echo "taiga-back v'"${VERSION}"' binary not available - download failed" >&2
exit 1"' >> /opt/venv/bin/taiga && echo 'exit 1' >> /opt/venv/bin/taiga && chmod +x /opt/venv/bin/taiga ; }

FROM registry.access.redhat.com/ubi9/ubi-minimal
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"

ARG VERSION=6.9.0
RUN microdnf install -y python3 ca-certificates curl && \
    mkdir -p /app && \
    chown -R 65532:65532 /app 2>/dev/null || true
COPY --from=downloader /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
USER 65532:65532
WORKDIR /app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8000/api/v1/ || exit 1
ENTRYPOINT ["python", "-m", "taiga"]
LABEL org.opencontainers.image.title="taiga-backend" \
      org.opencontainers.image.description="Taiga Backend - Django backend for Taiga project management" \
      org.opencontainers.image.version="6.9.0" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-back" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
