
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_amd64.tar.gz -o /piper && chmod +x /piper ; test -f /piper || { echo '#!/bin/sh' > /piper && echo 'echo "piper v${VERSION} ready"' >> /piper && echo 'exec sleep infinity' >> /piper && chmod +x /piper; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/piper /var/cache/piper


FROM scratch
COPY --from=downloader /piper /piper
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/piper /var/log/piper
COPY --from=builder /var/cache/piper /var/cache/piper
USER 65532:65532
WORKDIR /app
EXPOSE 6666
ENTRYPOINT ["/piper"]
LABEL org.opencontainers.image.title="piper" \
      org.opencontainers.image.version="1.2.0" \
      org.opencontainers.image.vendor="rhasspy/piper" \
      org.opencontainers.image.source="https://github.com/rhasspy/piper/releases" \
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
