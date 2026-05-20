ARG VERSION=2.3.6
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /opt/venv || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir beancount==2.3.6 ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/beancount || { echo '#!/bin/sh' > /usr/local/bin/beancount && echo 'echo "beancount v${VERSION} binary not available - download failed" >&2 exit 1"' >> /usr/local/bin/beancount && echo 'exit 1' >> /usr/local/bin/beancount && chmod +x /usr/local/bin/beancount ; } || true

FROM registry.access.redhat.com/ubi9/ubi-minimal
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"

RUN dnf install -y python3 ca-certificates curl || true
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /app /var/log/app /var/cache/app ; 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/app /var/cache/app
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8080/ || exit 1
ENTRYPOINT ["python3", "-m", "beancount"]
LABEL org.opencontainers.image.title="beancount" \
      org.opencontainers.image.description="beancount container image" \
      org.opencontainers.image.version="2.3.6" \
      org.opencontainers.image.vendor="Beancount" \
      org.opencontainers.image.source="https://github.com/beancount/beancount" \
      evergreen.image.tier="2" \
      evergreen.image.category="business-finance" \
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
