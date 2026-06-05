ARG VERSION=2.14.5
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /opt/tautulli && \
    mkdir -p /opt/venv || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir pyopenssl certifi && \
    git clone --branch v${VERSION} "https://github.com/Tautulli/Tautulli.git" /opt/tautulli || { echo "Binary not available - download failed" >&2; exit 1; } 2>/dev/null

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM registry.access.redhat.com/ubi9/ubi-minimal@sha256:10c773dc96763e3201275bae7865d278ca4b91db586117adec79079a2d7cdb80
COPY --from=shim /shim /shim

LABEL evergreen.base.fallback_reason="Python C extensions require glibc"

RUN dnf install -y python3 ca-certificates curl && \
    mkdir -p /opt/venv /opt/tautulli 2>/dev/null || true
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/tautulli /opt/tautulli
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /app /var/log/tautulli /var/cache/tautulli ; \
    chown -R 65532:65532 /app /var/log/tautulli /var/cache/tautulli /opt/tautulli
USER 65532:65532
WORKDIR /app
EXPOSE 8181

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8181"]

ENTRYPOINT ["/shim", "run"]
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
