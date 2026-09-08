ARG SHIM_VERSION=v2.0.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim
FROM cgr.dev/chainguard/wolfi-base@sha256:a31344ab2cb8618db84f535eec56f76f6178b142cb92cb2e48676cc2dcebea72 AS builder
ARG RATHOLE_VERSION=v0.4.8
RUN apk add --no-cache curl unzip && \
    curl -fsSL --retry 3 "https://github.com/rapiz1/rathole/releases/download/${RATHOLE_VERSION}/rathole-x86_64-unknown-linux-musl.zip" -o /tmp/rathole.zip && \
    unzip -o /tmp/rathole.zip -d /tmp && \
    mkdir -p /usr/local/bin && \
    mv /tmp/rathole /usr/local/bin/rathole && \
    chmod +x /usr/local/bin/rathole
FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /usr/local/bin/rathole /usr/local/bin/rathole
USER 65532:65532
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/rathole"]
ENV SHIM_METRICS_ENABLED="true"
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:2333"]
LABEL evergreen.image.tier="standard" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true"
EXPOSE 2333 9101
STOPSIGNAL SIGTERM
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
