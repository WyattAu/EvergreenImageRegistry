
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/anchore/syft/releases/download/v1.11.0/syft_1.11.0_linux_${TARGETARCH}.tar.gz -o /syft_1.11.0_linux_${TARGETARCH}.tar.gz &&     [ -f /syft_1.11.0_linux_${TARGETARCH}.tar.gz ] && tar -xzf /syft_1.11.0_linux_${TARGETARCH}.tar.gz -C / && rm -f /syft_1.11.0_linux_${TARGETARCH}.tar.gz && chmod +x /syft && \
    echo "0a61e5ef09f88562a35b6ec5dd27fa77f19c8611c26e58d527c4da191736b472  /syft_1.11.0_linux_${TARGETARCH}.tar.gz" | sha256sum -c && \
    strip /syft 2>/dev/null && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/syft-alpine /var/cache/syft-alpine 2>/dev/null || true


FROM scratch
COPY --from=downloader /syft /syft
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/syft-alpine /var/log/syft-alpine
COPY --from=builder /var/cache/syft-alpine /var/cache/syft-alpine
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="syft-alpine"       org.opencontainers.image.description="Syft - SBOM scanner (no Alpine)"       org.opencontainers.image.vendor="Anchore"       org.opencontainers.image.source="https://github.com/anchore/syft"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="1.11.0"

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
ENTRYPOINT ["/syft"]
CMD ["--help"]
