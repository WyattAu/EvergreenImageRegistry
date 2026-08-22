ARG SHIM_VERSION=v2.0.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim
FROM cgr.dev/chainguard/wolfi-base@sha256:a31344ab2cb8618db84f535eec56f76f6178b142cb92cb2e48676cc2dcebea72 AS builder
ARG RATHOLE_VERSION=v0.5.0
RUN apk add --no-cache curl && \
    curl -fsSL "https://github.com/ToQoz/rathole/releases/download/${RATHOLE_VERSION}/rathole-x86_64-unknown-linux-musl" -o /usr/local/bin/rathole && \
    chmod +x /usr/local/bin/rathole
FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /usr/local/bin/rathole /usr/local/bin/rathole
USER 65532:65532
ENTRYPOINT ["/usr/local/bin/rathole"]
ENV SHIM_METRICS_ENABLED="true"
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:2333"]
LABEL evergreen.image.tier="standard" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true"
EXPOSE 2333 9101
STOPSIGNAL SIGTERM
