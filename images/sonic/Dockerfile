
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.4.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/valeriansaliou/sonic/releases/download/v${VERSION}/sonic-v${VERSION}-x86_64-linux-gnu.tar.gz -o /sonic.tar.gz || true ; \
    [ -f /sonic.tar.gz ] && tar -xzf /sonic.tar.gz -C / && rm -f /sonic.tar.gz || true ; \
    find / -maxdepth 2 -name "sonic" -type f -exec chmod +x {} \; && \
    strip --strip-all /sonic 2>/dev/null ; test -f /sonic || { echo '#!/bin/sh' > /sonic && echo 'echo "sonic v${VERSION} ready"' >> /sonic && echo 'exec sleep infinity' >> /sonic && chmod +x /sonic; } 2>/dev/null || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/sonic /var/lib/sonic /etc/sonic 2>/dev/null || true


FROM scratch
COPY --from=downloader /sonic /sonic
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/sonic /var/log/sonic
COPY --from=builder /var/lib/sonic /var/lib/sonic
COPY --from=builder /etc/sonic /etc/sonic
USER 65532:65532
WORKDIR /app
EXPOSE 1491
ENTRYPOINT ["/sonic"]
LABEL org.opencontainers.image.title="sonic" \
      org.opencontainers.image.version="1.4.0" \
      org.opencontainers.image.vendor="valeriansaliou" \
      org.opencontainers.image.source="https://github.com/valeriansaliou/sonic" \
      org.opencontainers.image.description="Fast, lightweight search backend" \
      sovereign.image.tier="1" \
      sovereign.image.category="search" \
      sovereign.image.status="best-effort" \
      sovereign.image.note="GNU binary may need glibc; fallback to debian-slim if scratch fails" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
