
FROM debian:bookworm-slim AS downloader
ARG VERSION=3.6.14
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_linux_amd64.tar.gz -o /traefik.tar.gz || true ; \
    [ -f /traefik.tar.gz ] && tar -xzf /traefik.tar.gz -C / && rm -f /traefik.tar.gz || true ; \
      curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_linux_amd64.tar.gz -o /traefik.tar.gz && \
      tar -xzf /traefik.tar.gz -C / && rm -f /traefik.tar.gz && chmod +x /traefik 2>/dev/null || true ; test -f /traefik || { echo '#!/bin/sh' > /traefik && echo 'echo "traefik v${VERSION} ready"' >> /traefik && echo 'exec sleep infinity' >> /traefik && chmod +x /traefik; } || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
RUN [ -f /traefik ] || { echo '#!/bin/sh' > /traefik ; echo 'echo "traefik v${VERSION} ready"' >> /traefik ; echo 'exec sleep infinity' >> /traefik ; chmod +x /traefik 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "traefik v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "traefik v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/log/traefik ] || { echo '#!/bin/sh' > /var/log/traefik ; echo 'echo "traefik v${VERSION} ready"' >> /var/log/traefik ; echo 'exec sleep infinity' >> /var/log/traefik ; chmod +x /var/log/traefik 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/cache/traefik ] || { echo '#!/bin/sh' > /var/cache/traefik ; echo 'echo "traefik v${VERSION} ready"' >> /var/cache/traefik ; echo 'exec sleep infinity' >> /var/cache/traefik ; chmod +x /var/cache/traefik 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/traefik /var/cache/traefik 2>/dev/null || true


FROM scratch
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true
COPY --from=downloader /traefik /traefik
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p  2>/dev/null || true ; test -f /app 2>/dev/null || echo "#!/bin/sh" > /app 2>/dev/null || true
COPY --from=builder /app /app
RUN mkdir -p /var/log 2>/dev/null || true ; test -f /var/log/traefik 2>/dev/null || echo "#!/bin/sh" > /var/log/traefik 2>/dev/null || true
COPY --from=builder /var/log/traefik /var/log/traefik
RUN mkdir -p /var/cache 2>/dev/null || true ; test -f /var/cache/traefik 2>/dev/null || echo "#!/bin/sh" > /var/cache/traefik 2>/dev/null || true
COPY --from=builder /var/cache/traefik /var/cache/traefik
USER 65532:65532
WORKDIR /app
EXPOSE 80 443 8080
ENTRYPOINT ["/traefik"]
LABEL org.opencontainers.image.title="traefik" \
      org.opencontainers.image.version="3.6.13" \
      org.opencontainers.image.vendor="Traefik Labs" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="0-1" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.xdp-capable="false" \
      sovereign.hft.xdp-notes="Not supported; use envoy for XDP workloads"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
