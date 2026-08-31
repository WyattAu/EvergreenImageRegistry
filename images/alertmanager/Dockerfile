ARG VERSION=0.32.1
ARG SHIM_VERSION=v2.0.0

FROM debian:bookworm-slim@sha256:abd67ffcfa541b485a3dff59865ab629aa048a6c613e639d36e7456b0b229241 AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    arch=$(case ${TARGETARCH} in amd64) echo "amd64";; arm64) echo "arm64";; *) echo "amd64";; esac) && \
    curl -fsSL "https://github.com/prometheus/alertmanager/releases/download/v${VERSION}/alertmanager-${VERSION}.linux-${arch}.tar.gz" -o /tmp/am.tar.gz && \
    tar -xzf /tmp/am.tar.gz -C /tmp && \
    cp /tmp/alertmanager-${VERSION}.linux-${arch}/alertmanager /alertmanager && \
    chmod +x /alertmanager && \
    mkdir -p /data && chmod 0777 /data

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /alertmanager /alertmanager
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /data /data

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

EXPOSE 9093 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9093"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/alertmanager"]

LABEL org.opencontainers.image.title="alertmanager" \
      org.opencontainers.image.description="Alertmanager - Go binary, scratch, non-root" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distroless="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
LABEL evergreen.security.read-only-rootfs="false"
