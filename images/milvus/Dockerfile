# =============================================================================
# SOVEREIGN HARDENED MILVUS
# Generated from template - Version: 2.4.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.4.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG GITHUB_TOKEN
ARG VERSION=2.4.0
RUN apk add --no-cache curl ca-certificates
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/milvus-io/milvus/releases/download/v${VERSION}/milvus-standalone_${VERSION}_linux_amd64.tar.gz" -o /tmp/milvus.tar.gz && \
    tar -xzf /tmp/milvus.tar.gz -C /opt && rm /tmp/milvus.tar.gz && \
    chmod +x /opt/milvus/bin/milvus 2>/dev/null || true
RUN adduser -u 65532 -D milvus 2>/dev/null || true
RUN mkdir -p /app /var/log/milvus /var/cache/milvus && chown -R milvus:milvus /app /var/log/milvus /var/cache/milvus /opt/milvus 2>/dev/null || true
USER milvus
WORKDIR /app
EXPOSE 19530
ENTRYPOINT ["/opt/milvus/bin/milvus"]
LABEL org.opencontainers.image.title="milvus" \
      org.opencontainers.image.version="2.4.0" \
      org.opencontainers.image.vendor="Milvus" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM