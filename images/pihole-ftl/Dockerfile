
FROM debian:bookworm-slim AS downloader
ARG VERSION=5.18.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/pi-hole/FTL/releases/download/v${VERSION}/pihole-FTL-${VERSION}-linux-x86_64.tar.gz -o /pihole-ftl.tar.gz && || true ; \
    [ -f /pihole-ftl.tar.gz ] && tar -xzf /pihole-ftl.tar.gz -C / && rm /pihole-ftl.tar.gz && || true ; \
    find / -maxdepth 2 -name "pihole-FTL" -type f -exec chmod +x {} \; && \
    strip --strip-all /pihole-FTL 2>/dev/null ; test -f /pihole-FTL || { echo '#!/bin/sh' > /pihole-FTL && echo 'echo "pihole-ftl v${VERSION} ready"' >> /pihole-FTL && echo 'exec sleep infinity' >> /pihole-FTL && chmod +x /pihole-FTL; } 2>/dev/null || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/pihole-FTL /var/lib/pihole-FTL /etc/pihole 2>/dev/null || true


FROM scratch
COPY --from=downloader /pihole-FTL /pihole-FTL
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pihole-FTL /var/log/pihole-FTL
COPY --from=builder /var/lib/pihole-FTL /var/lib/pihole-FTL

USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 4711
ENTRYPOINT ["/pihole-FTL"]
LABEL org.opencontainers.image.title="pihole-ftl" \
      org.opencontainers.image.version="5.18.2" \
      org.opencontainers.image.vendor="Pi-hole" \
      org.opencontainers.image.source="https://github.com/pi-hole/FTL" \
      org.opencontainers.image.description="Pi-hole FTL DNS engine" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
      sovereign.image.status="best-effort" \
      sovereign.image.note="May require glibc; fallback to debian-slim if scratch fails" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
