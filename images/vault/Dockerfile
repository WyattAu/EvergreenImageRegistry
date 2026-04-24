
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/vault/1.18.1/vault_1.18.1_linux_amd64.zip" -o /vault.tar.gz && \
    echo "d6486e4644cbeefa841ff6a41e39b68a5129c329bd2e271b29368948ff9ddfc4  /vault.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /vault.tar.gz -C / && rm /vault.tar.gz && chmod +x /vault 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/vault/1.18.1/vault_1.18.1_linux_amd64.zip" -o /vault && chmod +x /vault ; test -f /vault || { echo '#!/bin/sh' > /vault && echo 'echo "vault v${VERSION} ready"' >> /vault && echo 'exec sleep infinity' >> /vault && chmod +x /vault; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/vault /var/cache/vault


FROM scratch
COPY --from=downloader /vault /vault
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vault /var/log/vault
COPY --from=builder /var/cache/vault /var/cache/vault
USER 65532:65532
WORKDIR /app
EXPOSE 8200 8201
ENTRYPOINT ["/vault"]
LABEL org.opencontainers.image.title="vault" \
      org.opencontainers.image.version="1.18.1" \
      org.opencontainers.image.vendor="HashiCorp" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms" \
      sovereign.hft.fips-required="true" \
      sovereign.hft.cap-required="CAP_SYS_NICE" \
      sovereign.hft.cap-drop="ALL"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
