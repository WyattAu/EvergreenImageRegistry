ARG VERSION=3.15.1
ARG SHIM_VERSION=v2.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    arch=$(case ${TARGETARCH} in amd64) echo "amd64";; arm64) echo "arm64";; *) echo "amd64";; esac) && \
    curl -fsSL "https://get.helm.sh/helm-v${VERSION}-linux-${arch}.tar.gz" -o /tmp/helm.tar.gz && \
    tar -xzf /tmp/helm.tar.gz -C /tmp && \
    cp /tmp/linux-${arch}/helm /helm && chmod +x /helm

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /helm /usr/local/bin/helm
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

EXPOSE 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9101"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/helm"]
CMD []

LABEL org.opencontainers.image.title="helm" \
      org.opencontainers.image.version="${VERSION}" \
      evergreen.image.tier="standard" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distroless="true"
LABEL evergreen.base.image="scratch" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true"
STOPSIGNAL SIGTERM
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
