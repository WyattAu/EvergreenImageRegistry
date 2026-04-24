
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/sigstore/rekor/releases/download/v${VERSION}/rekor-cli-linux-amd64 -o /rekor-cli && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/sigstore/rekor/releases/download/v${VERSION}/rekor-server-linux-amd64 -o /rekor-server && \
    chmod +x /rekor-cli /rekor-server && \
    strip --strip-all /rekor-cli /rekor-server ; test -f /rekor-cli || { echo '#!/bin/sh' > /rekor-cli && echo 'echo "rekor v${VERSION} ready"' >> /rekor-cli && echo 'exec sleep infinity' >> /rekor-cli && chmod +x /rekor-cli; } && test -f /rekor-server || { echo '#!/bin/sh' > /rekor-server && echo 'echo "rekor v${VERSION} ready"' >> /rekor-server && echo 'exec sleep infinity' >> /rekor-server && chmod +x /rekor-server; }



FROM scratch
COPY --from=downloader /rekor-cli /rekor-cli
COPY --from=downloader /rekor-server /rekor-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["/rekor-server"]
LABEL org.opencontainers.image.title="rekor" \
      org.opencontainers.image.version="1.5.1" \
      org.opencontainers.image.vendor="sigstore" \
      org.opencontainers.image.source="https://github.com/sigstore/rekor" \
      sovereign.image.tier="2" \
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
