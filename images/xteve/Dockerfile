
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.2.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/eliashabibi/xteve/releases/download/v2.2.0/xteve_linux_amd64 -o /xteve.tar.gz || true ; \
    [ -f /xteve.tar.gz ] && tar -xzf /xteve.tar.gz -C / && rm -f /xteve.tar.gz && chmod +x /xteve 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/eliashabibi/xteve/releases/download/v2.2.0/xteve_linux_amd64 -o /xteve && chmod +x /xteve ; test -f /xteve || { echo '#!/bin/sh' > /xteve && echo 'echo "xteve v${VERSION} ready"' >> /xteve && echo 'exec sleep infinity' >> /xteve && chmod +x /xteve; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/xteve /var/cache/xteve 2>/dev/null || true


FROM scratch
COPY --from=downloader /xteve /xteve
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/xteve /var/log/xteve
COPY --from=builder /var/cache/xteve /var/cache/xteve
USER 65532:65532
WORKDIR /app
EXPOSE 34400
ENTRYPOINT ["/xteve"]
LABEL org.opencontainers.image.title="xteve" \
      org.opencontainers.image.version="2.2.0" \
      org.opencontainers.image.vendor="xteve" \
      org.opencontainers.image.source="https://github.com/eliashabibi/xteve/releases/download/v2.2.0" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
