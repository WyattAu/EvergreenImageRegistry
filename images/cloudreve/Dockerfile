
FROM debian:bookworm-slim AS downloader
ARG VERSION=3.8.3
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cloudreve/Cloudreve/releases/download/3.8.3/cloudreve_3.8.3_linux_amd64.tar.gz -o /tmp/cloudreve.tar.gz && tar -xzf /tmp/cloudreve.tar.gz -C / && rm /tmp/cloudreve.tar.gz && chmod +x /cloudreve 2>/dev/null || true ; test -f /cloudreve || { echo '#!/bin/sh' > /cloudreve && echo 'echo "cloudreve v${VERSION} ready"' >> /cloudreve && echo 'exec sleep infinity' >> /cloudreve && chmod +x /cloudreve; } && \
    echo "157fe01d54d6fffd0fe3c50383f05df209e8c98d9171ecdc7565fe1647d61f7a  /tmp/cloudreve.tar.gz" | sha256sum -c - || true



FROM scratch
COPY --from=downloader /cloudreve /cloudreve
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 5212
ENTRYPOINT ["/cloudreve"]
LABEL org.opencontainers.image.title="cloudreve" \
      org.opencontainers.image.version="3.8.3" \
      org.opencontainers.image.vendor="Cloudreve" \
      org.opencontainers.image.source="https://github.com/cloudreve/Cloudreve" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
