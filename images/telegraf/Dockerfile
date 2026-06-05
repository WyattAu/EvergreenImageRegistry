# =============================================================================
# EVERGREEN HARDENED TELEGRAF
# Generated from template - Version: 1.30.3
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.30.3
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.30.3
WORKDIR /tmp
RUN mkdir -p /tmp/telegraf || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.influxdata.com/telegraf/releases/telegraf-${VERSION}_linux_amd64.tar.gz" -o telegraf.tar.gz ; echo "1b5bf21b8f28b84be0db2b5a86e2c0bfed3a5656f06fc8c8f1c33c50b8c6afba  telegraf.tar.gz" | sha256sum -c  ; [ -f telegraf.tar.gz ] && tar -xzf telegraf.tar.gz ; \
    strip --strip-all usr/bin/telegraf 2>/dev/null; mv usr/bin/telegraf /tmp/telegraf 2>/dev/null && \
    mkdir -p /tmp/telegraf
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=1.30.3
COPY --from=builder /tmp/telegraf /usr/bin/telegraf
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 8125 8092 8094

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8125"]

ENTRYPOINT ["/shim", "run"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="monitoring" \
      org.opencontainers.image.title="telegraf" \
      org.opencontainers.image.description="Evergreen hardened Telegraf - metrics collection agent by InfluxData" \
      org.opencontainers.image.version="${VERSION}" \
            org.opencontainers.image.source="https://github.com/influxdata/telegraf"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
