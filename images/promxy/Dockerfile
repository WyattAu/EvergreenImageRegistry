ARG VERSION=0.0.93
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.0.93
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/jacksontj/promxy/releases/download/v${VERSION}/promxy-v${VERSION}-linux-${TARGETARCH}" \
    -o /promxy && chmod +x /promxy && strip /promxy || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/promxy /var/cache/promxy /etc/promxy 2>/dev/null || true

FROM scratch
COPY --from=downloader /promxy /promxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/promxy /var/log/promxy
COPY --from=builder /var/cache/promxy /var/cache/promxy
COPY --from=builder /etc/promxy /etc/promxy
USER 65532:65532
WORKDIR /app
EXPOSE 8082

HEALTHCHECK NONE
ENTRYPOINT ["/promxy"]
LABEL org.opencontainers.image.title="promxy" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="prymitive" \
      org.opencontainers.image.description="Evergreen hardened promxy - Prometheus proxy" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
            org.opencontainers.image.source="https://github.com/jacksontj/promxy"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
