ARG VERSION=7.15.3
ARG SHIM_VERSION=v2.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    arch=$(case ${TARGETARCH} in amd64) echo "linux-amd64";; arm64) echo "linux-arm64";; *) echo "linux-amd64";; esac) && \
    curl -fsSL "https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v${VERSION}/oauth2-proxy-v${VERSION}.${arch}.tar.gz" -o /tmp/oauth2-proxy.tar.gz && \
    mkdir -p /tmp/oauth2-proxy && \
    tar -xzf /tmp/oauth2-proxy.tar.gz -C /tmp/oauth2-proxy && \
    find /tmp/oauth2-proxy -name oauth2-proxy -type f -exec cp {} /oauth2-proxy \; && \
    chmod +x /oauth2-proxy && \
    mkdir -p /data

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /oauth2-proxy /usr/local/bin/oauth2-proxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV OAUTH2_PROXY_HTTP_ADDRESS="0.0.0.0:4180" \
    OAUTH2_PROXY_METRICS_ADDRESS="0.0.0.0:44180"

EXPOSE 4180 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:4180"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/oauth2-proxy"]
CMD ["--help"]

LABEL org.opencontainers.image.title="oauth2-proxy" \
      org.opencontainers.image.description="OAuth2 Proxy - Go binary, scratch, non-root" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distroless="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
LABEL evergreen.security.read-only-rootfs="false"
