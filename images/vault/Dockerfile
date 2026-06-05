
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.18.1
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/vault/${VERSION}/vault_${VERSION}_linux_${TARGETARCH}.zip" -o /vault.zip && \
    echo "d6486e4644cbeefa841ff6a41e39b68a5129c329bd2e271b29368948ff9ddfc4  /vault.zip" | sha256sum -c && \
    unzip -o /vault.zip -d / && rm -f /vault.zip && chmod +x /vault || \
    { echo "ERROR: vault binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/vault /var/cache/vault 2>/dev/null || true

FROM ghcr.io/wyattau/evergreenshim/health-shim:v0.1.0 AS shim

FROM scratch
COPY --from=downloader /vault /vault
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vault /var/log/vault
COPY --from=builder /var/cache/vault /var/cache/vault
COPY --from=shim /shim /shim
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8200 8201 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8200"]

ENTRYPOINT ["/shim", "run"]
CMD ["-c", "/vault", "server", "-dev"]
LABEL org.opencontainers.image.title="vault" \
      org.opencontainers.image.description="Vault - secrets management and data protection by HashiCorp" \
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
LABEL evergreen.health.type="http"
LABEL evergreen.health.endpoint="/livez"
LABEL evergreen.health.listen="0.0.0.0:9101"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
