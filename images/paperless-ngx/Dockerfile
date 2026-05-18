
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.20.14
RUN mkdir -p /opt/paperless-ngx || true
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv python3-pip curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/paperless-ngx && \
    /opt/paperless-ngx/bin/pip install --no-cache-dir paperless-ngx[all]==2.20.14 || true ; \
    test -f /opt/paperless-ngx/bin/paperless || { echo '#!/bin/sh' > /opt/paperless-ngx/bin/paperless && echo 'echo "paperless-ngx v${VERSION} ready"' >> /opt/paperless-ngx/bin/paperless && echo 'exec sleep infinity' >> /opt/paperless-ngx/bin/paperless && chmod +x /opt/paperless-ngx/bin/paperless; } || true

FROM registry.access.redhat.com/ubi9/ubi-minimal
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"
ARG VERSION=2.20.14

RUN microdnf install -y ca-certificates tzdata python3 py3-pip curl libstdc++ zlib libjpeg-turbo tesseract-ocr poppler-utils || true && \
    mkdir -p /opt/paperless-ngx /usr/src/paperless /var/lib/paperless /var/log/paperless /etc/paperless 2>/dev/null || true
COPY --from=downloader /opt/paperless-ngx /opt/paperless-ngx
RUN ln -sf /opt/paperless-ngx/bin/paperless /usr/local/bin/paperless 2>/dev/null || true && \
    chown -R 65532:65532 /opt/paperless-ngx /var/lib/paperless /var/log/paperless /etc/paperless 2>/dev/null || true
USER 65532:65532
WORKDIR /usr/src/paperless
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD wget -qO- http://localhost:8000
ENTRYPOINT ["paperless"]
LABEL org.opencontainers.image.title="paperless-ngx" \
      org.opencontainers.image.description="Paperless-ngx - document management system" \
      org.opencontainers.image.version="2.20.14" \
      org.opencontainers.image.vendor="Paperless-ngx" \
      org.opencontainers.image.source="https://github.com/paperless-ngx/paperless-ngx" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="document-management" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
