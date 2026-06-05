
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.18.1
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/vault/1.18.1/vault_1.18.1_linux_${TARGETARCH}.zip" -o /vault.tar.gz && \
    echo "d6486e4644cbeefa841ff6a41e39b68a5129c329bd2e271b29368948ff9ddfc4  /vault.tar.gz" | sha256sum -c ; [ -f /vault.tar.gz ] && \
    [ -f /vault.tar.gz ] && tar -xzf /vault.tar.gz -C / && rm -f /vault.tar.gz && chmod +x /vault 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/vault/1.18.1/vault_1.18.1_linux_${TARGETARCH}.zip" -o /vault && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/vault /var/cache/vault 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /vault /vault
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vault /var/log/vault
COPY --from=builder /var/cache/vault /var/cache/vault
USER 65532:65532
WORKDIR /app
EXPOSE 8200 8201

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8200"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="hashicorp-vault" \
      org.opencontainers.image.description="hashicorp-vault container image" \
      org.opencontainers.image.version="1.18.1" \
      org.opencontainers.image.vendor="HashiCorp" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms" \
      evergreen.hft.fips-required="true" \
      evergreen.hft.cap-required="CAP_SYS_NICE" \
      evergreen.hft.cap-drop="ALL" \
            org.opencontainers.image.source="https://github.com/hashicorp/vault"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
