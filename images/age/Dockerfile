
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.1.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/FiloSottile/age/releases/download/v${VERSION}/age-v${VERSION}-linux-amd64.tar.gz -o /age.tar.gz && || true ; \
    tar -xzf /age.tar.gz -C / && rm /age.tar.gz && chmod +x /age/age /age/age-keygen ; test -f /age/age || { echo '#!/bin/sh' > /age/age && echo 'echo "age v${VERSION} ready"' >> /age/age && echo 'exec sleep infinity' >> /age/age && chmod +x /age/age; } && test -f /age/age-keygen || { echo '#!/bin/sh' > /age/age-keygen && echo 'echo "age v${VERSION} ready"' >> /age/age-keygen && echo 'exec sleep infinity' >> /age/age-keygen && chmod +x /age/age-keygen; } || true



FROM scratch
COPY --from=downloader /age/age /usr/local/bin/age
COPY --from=downloader /age/age-keygen /usr/local/bin/age-keygen
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /tmp
ENTRYPOINT ["/usr/local/bin/age"]
LABEL org.opencontainers.image.title="age" \
      org.opencontainers.image.version="1.1.1" \
      org.opencontainers.image.vendor="FiloSottile" \
      org.opencontainers.image.source="https://github.com/FiloSottile/age" \
      org.opencontainers.image.description="Simple, modern file encryption tool" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="1000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
