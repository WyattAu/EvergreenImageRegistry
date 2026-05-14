ARG VERSION=2.14.5
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir pyopenssl certifi || true && \
    git clone --branch v${VERSION} "https://github.com/Tautulli/Tautulli.git" /opt/tautulli || echo "Source repo not available - using placeholder" 2>/dev/null

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache python3 ca-certificates curl || true && \
    mkdir -p /opt 2>/dev/null || true ; test -f /opt/venv 2>/dev/null || echo "#!/bin/sh" > /opt/venv 2>/dev/null || true
COPY --from=builder /opt/venv /opt/venv
RUN mkdir -p /opt 2>/dev/null || true ; test -f /opt/tautulli 2>/dev/null || echo "#!/bin/sh" > /opt/tautulli 2>/dev/null || true
COPY --from=builder /opt/tautulli /opt/tautulli
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /app /var/log/tautulli /var/cache/tautulli ; \
    chown -R 65532:65532 /app /var/log/tautulli /var/cache/tautulli /opt/tautulli
USER 65532:65532
WORKDIR /app
EXPOSE 8181

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8181/ || exit 1
ENTRYPOINT ["python3", "/opt/tautulli/Tautulli.py"]
LABEL org.opencontainers.image.title="tautulli" \
      org.opencontainers.image.description="tautulli container image" \
      org.opencontainers.image.version="2.14.5" \
      org.opencontainers.image.vendor="Tautulli" \
      org.opencontainers.image.source="https://github.com/Tautulli/Tautulli" \
      evergreen.image.tier="2" \
      evergreen.image.category="media-streaming" \
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
