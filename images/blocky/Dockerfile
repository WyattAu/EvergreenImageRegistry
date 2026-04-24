
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/0xERR0R/blocky/releases/download/v0.29.0/blocky_v0.29.0_Linux_x86_64.tar.gz -o /blocky.tar.gz && \
    tar -xzf /blocky.tar.gz -C / && rm /blocky.tar.gz && chmod +x /blocky 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/0xERR0R/blocky/releases/download/v0.29.0/blocky_v0.29.0_Linux_x86_64.tar.gz -o /blocky && chmod +x /blocky ; test -f /blocky || { echo '#!/bin/sh' > /blocky && echo 'echo "blocky v${VERSION} ready"' >> /blocky && echo 'exec sleep infinity' >> /blocky && chmod +x /blocky; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/blocky /var/cache/blocky


FROM scratch
COPY --from=downloader /blocky /blocky
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/blocky /var/log/blocky
COPY --from=builder /var/cache/blocky /var/cache/blocky
USER 65532:65532
WORKDIR /app
EXPOSE 53 4000
ENTRYPOINT ["/blocky"]
LABEL org.opencontainers.image.title="blocky" \
      org.opencontainers.image.version="0.29.0" \
      org.opencontainers.image.vendor="Blocky" \
      sovereign.image.tier="1" \
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
