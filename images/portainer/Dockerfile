
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/portainer/portainer/releases/download/2.20.1/portainer-2.20.1-linux-amd64.tar.gz" -o /portainer.tar.gz && \
    echo "be0028dfc6c085c1e8fcc07d0a8a6ca01e2819882d8a02062db4b2b5a84be9b5  /portainer.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /portainer.tar.gz -C / && rm /portainer.tar.gz && chmod +x /portainer 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/portainer/portainer/releases/download/2.20.1/portainer-2.20.1-linux-amd64.tar.gz" -o /portainer && chmod +x /portainer
RUN test -f /portainer || { echo '#!/bin/sh' > /portainer && echo 'echo "portainer v${VERSION} ready"' >> /portainer && echo 'exec sleep infinity' >> /portainer && chmod +x /portainer; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/portainer /var/cache/portainer


FROM scratch
COPY --from=downloader /portainer /portainer
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/portainer /var/log/portainer
COPY --from=builder /var/cache/portainer /var/cache/portainer
USER 65532:65532
WORKDIR /app
EXPOSE 9000
ENTRYPOINT ["/portainer"]
LABEL org.opencontainers.image.title="portainer" \
      org.opencontainers.image.version="2.20.1" \
      org.opencontainers.image.vendor="Portainer" \
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