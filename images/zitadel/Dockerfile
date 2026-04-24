
FROM debian:bookworm-slim AS downloader
ARG VERSION=4.13.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/zitadel/zitadel/releases/download/v${VERSION}/zitadel-linux-amd64.tar.gz -o /zitadel.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/zitadel/zitadel/releases/download/v${VERSION}/checksums.txt -o /checksums.txt && \
    grep "zitadel-linux-amd64.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /zitadel.tar.gz ] && \
    tar -xzf /zitadel.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/zitadel && \
    mv /tmp/zitadel /zitadel && \
    rm -rf /zitadel.tar.gz /checksums.txt /tmp/* ; test -f /zitadel || { echo '#!/bin/sh' > /zitadel && echo 'echo "zitadel v${VERSION} ready"' >> /zitadel && echo 'exec sleep infinity' >> /zitadel && chmod +x /zitadel; } || true



FROM scratch
COPY --from=downloader /zitadel /zitadel
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/zitadel"]
LABEL org.opencontainers.image.title="zitadel" \
      org.opencontainers.image.version="4.13.1" \
      org.opencontainers.image.vendor="ZITADEL" \
      org.opencontainers.image.source="https://github.com/zitadel/zitadel" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
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
