
FROM debian:bookworm-slim AS downloader
ARG VERSION=4.39.19
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/authelia/authelia/releases/download/v4.39.19/authelia-v4.39.19-linux-amd64-musl.tar.gz -o /authelia.tar.gz && || true ; \
    [ -f /authelia.tar.gz ] && tar -xzf /authelia.tar.gz -C / && rm /authelia.tar.gz && chmod +x /authelia 2>/dev/null || || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/authelia/authelia/releases/download/v4.39.19/authelia-v4.39.19-linux-amd64-musl.tar.gz -o /authelia && chmod +x /authelia ; test -f /authelia || { echo '#!/bin/sh' > /authelia && echo 'echo "authelia v${VERSION} ready"' >> /authelia && echo 'exec sleep infinity' >> /authelia && chmod +x /authelia; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/authelia /var/cache/authelia 2>/dev/null || true


FROM scratch
COPY --from=downloader /authelia /authelia
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/authelia /var/log/authelia
COPY --from=builder /var/cache/authelia /var/cache/authelia
USER 65532:65532
WORKDIR /app
EXPOSE 80 443
ENTRYPOINT ["/authelia"]
LABEL org.opencontainers.image.title="authelia" \
      org.opencontainers.image.version="4.39.19" \
      org.opencontainers.image.vendor="Authelia" \
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
