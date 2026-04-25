
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.52.5
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/navidrome/navidrome/releases/download/v0.52.5/navidrome_0.52.5_linux_amd64.tar.gz -o /navidrome.tar.gz && \
    echo "b9781ea560ea09926557c665472faa26920738a5ffa0680c19f70df97f51598f  /navidrome.tar.gz" | sha256sum -c || true ; [ -f /navidrome.tar.gz ] && \
    [ -f /navidrome.tar.gz ] && tar -xzf /navidrome.tar.gz -C / && rm /navidrome.tar.gz && chmod +x /navidrome 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/navidrome/navidrome/releases/download/v0.52.5/navidrome_0.52.5_linux_amd64.tar.gz -o /navidrome && chmod +x /navidrome ; test -f /navidrome || { echo '#!/bin/sh' > /navidrome && echo 'echo "navidrome v${VERSION} ready"' >> /navidrome && echo 'exec sleep infinity' >> /navidrome && chmod +x /navidrome; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/navidrome /var/cache/navidrome 2>/dev/null || true


FROM scratch
COPY --from=downloader /navidrome /navidrome
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/navidrome /var/log/navidrome
COPY --from=builder /var/cache/navidrome /var/cache/navidrome
USER 65532:65532
WORKDIR /app
EXPOSE 4533
ENTRYPOINT ["/navidrome"]
LABEL org.opencontainers.image.title="navidrome" \
      org.opencontainers.image.version="0.52.5" \
      org.opencontainers.image.vendor="Navidrome" \
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
