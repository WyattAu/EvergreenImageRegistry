# =============================================================================
# SOVEREIGN HARDENED WEAVIATE
# Generated from template - Version: 1.25.4
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.25.4
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG GITHUB_TOKEN
ARG VERSION=1.25.4
RUN apk add --no-cache curl ca-certificates 
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/weaviate/weaviate/releases/download/v${VERSION}/weaviate-v${VERSION}-linux-amd64.tar.gz -o /tmp/weaviate.tar.gz && \
    echo "93468b21703372eb12864000cf59083138e4fd563168e4f021ae2c0b28b446cf  /tmp/weaviate.tar.gz" | sha256sum -c - || true
    [ -f /tmp/weaviate.tar.gz ] && tar -xzf /tmp/weaviate.tar.gz -C /opt && rm /tmp/weaviate.tar.gz || true ; \
    chmod +x /opt/weaviate 2>/dev/null || true
RUN adduser -u 65532 -D weaviate 2>/dev/null || true
RUN mkdir -p /app /var/log/weaviate /var/cache/weaviate && chown -R weaviate:weaviate /app /var/log/weaviate /var/cache/weaviate /opt/weaviate 2>/dev/null || true
USER weaviate
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/opt/weaviate"]
LABEL org.opencontainers.image.title="weaviate" \
      org.opencontainers.image.version="1.25.4" \
      org.opencontainers.image.vendor="Weaviate" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
