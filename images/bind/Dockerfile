
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=9.21.21
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://ftp.isc.org/isc/bind9/9.21.21/bind-9.21.21.tar.xz" -o /named.tar.gz ; \
    echo "44ebfae8b82b494f5cc4781b044fbd4c867b64dc22ae9c62c9197aab16389112  /named.tar.gz" | sha256sum -c ; \
    [ -f /named.tar.gz ] && tar -xzf /named.tar.gz -C / && rm -f /named.tar.gz && chmod +x /named 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://ftp.isc.org/isc/bind9/9.21.21/bind-9.21.21.tar.xz" -o /named || { echo "Binary not available - download failed" >&2; exit 1; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/named /var/cache/named 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim

COPY --from=downloader /named /named
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/named /var/log/named
COPY --from=builder /var/cache/named /var/cache/named
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 53 953

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:53"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/named"]
LABEL org.opencontainers.image.title="bind" \
      org.opencontainers.image.description="BIND - DNS server software" \
      org.opencontainers.image.version="9.21.21" \
      org.opencontainers.image.vendor="ISC" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/isc-projects/bind9"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
