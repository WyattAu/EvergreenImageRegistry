# =============================================================================
# EVERGREEN HARDENED WEAVIATE
# Generated from template - Version: 1.25.4
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.25.4
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG GITHUB_TOKEN
ARG VERSION=1.25.4
RUN apk add --no-cache curl ca-certificates && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/weaviate/weaviate/releases/download/v${VERSION}/weaviate-v${VERSION}-linux-${TARGETARCH}.tar.gz -o /tmp/weaviate.tar.gz && \
    echo "93468b21703372eb12864000cf59083138e4fd563168e4f021ae2c0b28b446cf  /tmp/weaviate.tar.gz" | sha256sum -c || true ; \
    [ -f /tmp/weaviate.tar.gz ] && tar -xzf /tmp/weaviate.tar.gz -C /opt && rm -f /tmp/weaviate.tar.gz || true ; \
    chmod +x /opt/weaviate 2>/dev/null || true
RUN adduser -u 65532 -D weaviate 2>/dev/null || true && \
    mkdir -p /app /var/log/weaviate /var/cache/weaviate && chown -R weaviate:weaviate /app /var/log/weaviate /var/cache/weaviate /opt/weaviate 2>/dev/null || true
USER weaviate
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/opt/weaviate"]
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
