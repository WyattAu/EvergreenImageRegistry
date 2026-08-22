ARG SHIM_VERSION=v2.0.0
ARG FRP_VERSION=0.61.1

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:a31344ab2cb8618db84f535eec56f76f6178b142cb92cb2e48676cc2dcebea72 AS builder
ARG FRP_VERSION
RUN apk add --no-cache curl tar && \
    curl -fsSL "https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_linux_amd64.tar.gz" | \
    tar xz -C /tmp && \
    cp /tmp/frp_${FRP_VERSION}_linux_amd64/frps /usr/local/bin/frps

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /usr/local/bin/frps /usr/local/bin/frps
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532

ENTRYPOINT ["/usr/local/bin/frps"]

ENV SHIM_METRICS_ENABLED="true"
EXPOSE 7000 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:7000"]

LABEL evergreen.image.tier="standard" \
      evergreen.entrypoint.pattern="repack-upstream-init" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true"
STOPSIGNAL SIGTERM
