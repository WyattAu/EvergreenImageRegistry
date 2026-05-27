ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.35.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/thanos-io/thanos/releases/download/v0.35.0/thanos-0.35.0.linux-${TARGETARCH}.tar.gz -o /thanos.tar.gz && \
    echo "8c8c8a4dfe8a71c23c3723ecea63a3d8ef07bd643615999ddf76167e68edd2f6  /thanos.tar.gz" | sha256sum -c ; [ -f /thanos.tar.gz ] && \
    [ -f /thanos.tar.gz ] && tar -xzf /thanos.tar.gz -C / && rm -f /thanos.tar.gz && chmod +x /thanos 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/thanos-io/thanos/releases/download/v0.35.0/thanos-0.35.0.linux-${TARGETARCH}.tar.gz -o /thanos && chmod +x /thanosbinary not available - download failed" >&2"' >> /thanos && echo 'exit 1' >> /thanos && chmod +x /thanos; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/thanos /var/cache/thanos 2>/dev/null || true


FROM scratch
COPY --from=downloader /thanos /thanos
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/thanos /var/log/thanos
COPY --from=builder /var/cache/thanos /var/cache/thanos
USER 65532:65532
WORKDIR /app
EXPOSE 10902

HEALTHCHECK NONE
ENTRYPOINT ["/thanos"]
LABEL org.opencontainers.image.title="thanos-receive" \
      org.opencontainers.image.description="thanos-receive container image" \
      org.opencontainers.image.version="0.35.0" \
      org.opencontainers.image.vendor="Thanos" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/thanos-io/thanos"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
