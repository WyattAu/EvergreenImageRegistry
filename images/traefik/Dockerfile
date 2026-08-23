ARG VERSION=3.1.2
ARG SHIM_VERSION=v2.0.0

# Download Traefik binary
FROM debian:bookworm-slim@sha256:abd67ffcfa541b485a3dff59865ab629aa048a6c613e639d36e7456b0b229241 AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    arch=$(case ${TARGETARCH} in amd64) echo "amd64";; arm64) echo "arm64";; *) echo "amd64";; esac) && \
    curl -fsSL "https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_linux_${arch}.tar.gz" -o /tmp/traefik.tar.gz && \
    tar -xzf /tmp/traefik.tar.gz -C /tmp && \
    mv /tmp/traefik /traefik && chmod +x /traefik

# Shim
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

# Final: scratch with binary + shim
FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /traefik /traefik
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

EXPOSE 8080 443 8080 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/traefik"]

LABEL org.opencontainers.image.title="traefik" \
      org.opencontainers.image.description="Traefik - binary download, scratch, non-root" \
      org.opencontainers.image.version="${VERSION}" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distroless="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
