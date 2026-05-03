FROM node:22-alpine AS builder
ARG VERSION=43.160.6
RUN npm install -g renovate@${VERSION}

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION
ARG TARGETARCH
RUN apk add --no-cache ca-certificates git
COPY --from=builder /usr/local/lib/node_modules/renovate /opt/renovate
COPY --from=builder /usr/local/bin/renovate /usr/local/bin/renovate
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/renovate 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["renovate"]
LABEL org.opencontainers.image.title="renovate"       org.opencontainers.image.version="43.160.6"       org.opencontainers.image.vendor="RenovateBot"       org.opencontainers.image.source="https://github.com/renovatebot/renovate"       evergreen.image.tier="2"       evergreen.image.category="automation"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="wolfi"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="30s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
