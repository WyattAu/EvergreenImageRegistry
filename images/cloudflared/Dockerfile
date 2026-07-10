ARG VERSION=2026.7.1
ARG SHIM_VERSION=v2.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* &&     arch=$(case ${TARGETARCH} in amd64) echo "amd64";; arm64) echo "arm64";; *) echo "amd64";; esac) &&     curl -fsSL "https://github.com/cloudflare/cloudflared/releases/download/${VERSION}/cloudflared-linux-${arch}" -o /cloudflared &&     chmod +x /cloudflared

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /cloudflared /usr/local/bin/cloudflared
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true" TUNNEL_METRICS="0.0.0.0:9101"

EXPOSE 9101
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3   CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9101"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/cloudflared"]
CMD ["tunnel", "--no-autoupdate"]

LABEL org.opencontainers.image.title="cloudflared" evergreen.image.tier="critical" evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="scratch" evergreen.security.cap-drop="ALL"
STOPSIGNAL SIGTERM
