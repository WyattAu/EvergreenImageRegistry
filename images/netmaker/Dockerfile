ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.5.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/gravitl/netmaker/releases/download/v1.5.1/netmaker-linux-${TARGETARCH} -o /netmaker.tar.gz ; \
    echo "4bd005147ae3679fc012c2db7f86e0e74c48cda5c648831b1af20d05d633ba84  /netmaker.tar.gz" | sha256sum -c ; \
    [ -f /netmaker.tar.gz ] && tar -xzf /netmaker.tar.gz -C / && rm -f /netmaker.tar.gz && chmod +x /netmaker 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/gravitl/netmaker/releases/download/v1.5.1/netmaker-linux-${TARGETARCH} -o /netmaker && { echo "Binary not available - download failed" >&2; exit 1; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/netmaker /var/cache/netmaker 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /netmaker /netmaker
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/netmaker /var/log/netmaker
COPY --from=builder /var/cache/netmaker /var/cache/netmaker
USER 65532:65532
WORKDIR /app
EXPOSE 443 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:443"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="netmaker" \
      org.opencontainers.image.description="netmaker container image" \
      org.opencontainers.image.version="1.5.1" \
      org.opencontainers.image.vendor="NetMaker" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/gravitl/netmaker"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
