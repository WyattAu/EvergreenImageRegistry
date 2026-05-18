ARG APP_UID=65532
ARG APP_GID=65532

FROM node@sha256:8ea2348b068a9544dae7317b4f3aafcdc032df1647bb7d768a05a5cad1a7683f AS builder
ARG VERSION=43.150.0
ARG TARGETARCH
RUN mkdir -p /usr/local/lib/node_modules/renovate || true
RUN npm install -g renovate@${VERSION}

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=43.150.0
RUN apk add --no-cache ca-certificates git
COPY --from=builder /usr/local/lib/node_modules/renovate /opt/renovate
COPY --from=builder /usr/local/bin/renovate /usr/local/bin/renovate
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/renovate 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["renovate"]
LABEL org.opencontainers.image.title="renovate"       org.opencontainers.image.version="43.150.0"       org.opencontainers.image.vendor="RenovateBot"       org.opencontainers.image.source="https://github.com/renovatebot/renovate"       evergreen.image.tier="2"       evergreen.image.category="automation"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="wolfi"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="30s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="30000ms" \
      org.opencontainers.image.description="renovate container image" \
evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
