
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.8.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/anchore/syft/releases/download/v1.8.0/syft_1.8.0_linux_${TARGETARCH}.tar.gz -o /syft.tar.gz ; \
    echo "b487ee715e715e960f0d327b49ed9f5926b82bfa2f7283942f9631c41e7c0545  /syft.tar.gz" | sha256sum -c ; \
    [ -f /syft.tar.gz ] && tar -xzf /syft.tar.gz -C / && rm -f /syft.tar.gz && chmod +x /syft 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/anchore/syft/releases/download/v1.8.0/syft_1.8.0_linux_${TARGETARCH}.tar.gz -o /syft && { echo "Binary not available - download failed" >&2; exit 1; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/syft /var/cache/syft 2>/dev/null || true


FROM scratch
COPY --from=downloader /syft /syft
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/syft /var/log/syft
COPY --from=builder /var/cache/syft /var/cache/syft
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/syft"]
LABEL org.opencontainers.image.title="syft" \
      org.opencontainers.image.description="syft container image" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Anchore" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/anchore/syft"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
