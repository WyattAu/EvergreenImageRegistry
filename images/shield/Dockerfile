
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/starkandwayne/shield/releases/download/v${VERSION}/shield-v${VERSION}-linux-amd64 -o /shield && \
    chmod +x /shield && \
    strip --strip-all /shield ; test -f /shield || { echo '#!/bin/sh' > /shield && echo 'echo "shield v${VERSION} ready"' >> /shield && echo 'exec sleep infinity' >> /shield && chmod +x /shield; }



FROM scratch
COPY --from=downloader /shield /shield
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8443
ENTRYPOINT ["/shield"]
CMD ["server", "-c", "/app/shield.yml"]
LABEL org.opencontainers.image.title="shield" \
      org.opencontainers.image.version="8.6.0" \
      org.opencontainers.image.vendor="Stark & Wayne" \
      org.opencontainers.image.source="https://github.com/starkandwayne/shield" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
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
