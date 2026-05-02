FROM node:22-alpine AS builder
ARG VERSION=43.160.6
RUN npm install -g renovate@${VERSION}

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates git
COPY --from=builder /usr/local/lib/node_modules/renovate /opt/renovate
COPY --from=builder /usr/local/bin/renovate /usr/local/bin/renovate
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/renovate 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["renovate"]
LABEL org.opencontainers.image.title="renovatebot"       org.opencontainers.image.version="43.160.6"       org.opencontainers.image.vendor="RenovateBot"       org.opencontainers.image.source="https://github.com/renovatebot/renovate"       sovereign.image.tier="2"       sovereign.image.category="automation"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.base="wolfi"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="30s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
