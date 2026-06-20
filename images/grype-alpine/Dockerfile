
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/anchore/grype/releases/download/v0.80.0/grype_0.80.0_linux_${TARGETARCH}.tar.gz -o /grype_0.80.0_linux_${TARGETARCH}.tar.gz &&     [ -f /grype_0.80.0_linux_${TARGETARCH}.tar.gz ] && tar -xzf /grype_0.80.0_linux_${TARGETARCH}.tar.gz -C / && rm -f /grype_0.80.0_linux_${TARGETARCH}.tar.gz && chmod +x /grype && \
    echo "a86a90074129cb72b47476f6ac3959eab95fba71f095521f5c8e58152463bd24  /grype_0.80.0_linux_${TARGETARCH}.tar.gz" | sha256sum -c && \
    strip /grype 2>/dev/null && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/grype-alpine /var/cache/grype-alpine 2>/dev/null || true


ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /grype /grype
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/grype-alpine /var/log/grype-alpine
COPY --from=builder /var/cache/grype-alpine /var/cache/grype-alpine
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="grype-alpine"       org.opencontainers.image.description="Grype - vulnerability scanner (no Alpine)"       org.opencontainers.image.vendor="Anchore"       org.opencontainers.image.source="https://github.com/anchore/grype"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="0.80.0"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/grype"]
CMD ["--help"]
