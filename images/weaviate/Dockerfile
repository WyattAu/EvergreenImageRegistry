# =============================================================================
# EVERGREEN HARDENED WEAVIATE
# Generated from template - Version: 1.25.4
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.25.4
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=1.25.4
RUN apk add --no-cache wget ca-certificates && \
    wget -t 3 -T 10 -qO /tmp/weaviate.tar.gz "https://github.com/weaviate/weaviate/releases/download/v${VERSION}/weaviate-v${VERSION}-linux-${TARGETARCH}.tar.gz" && \
    echo "93468b21703372eb12864000cf59083138e4fd563168e4f021ae2c0b28b446cf  /tmp/weaviate.tar.gz" | sha256sum -c ; \
    [ -f /tmp/weaviate.tar.gz ] && tar -xzf /tmp/weaviate.tar.gz -C /opt && rm -f /tmp/weaviate.tar.gz ; \
    chmod +x /opt/weaviate 2>/dev/null
RUN adduser -u 65532 -D weaviate 2>/dev/null || true && \
    mkdir -p /app /var/log/weaviate /var/cache/weaviate && chown -R weaviate:weaviate /app /var/log/weaviate /var/cache/weaviate /opt/weaviate 2>/dev/null || true
USER weaviate
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="weaviate" \
      org.opencontainers.image.description="weaviate container image" \
      org.opencontainers.image.version="1.25.4" \
      org.opencontainers.image.vendor="Weaviate" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/weaviate/weaviate"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
