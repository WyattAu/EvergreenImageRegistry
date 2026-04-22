# =============================================================================
# SOVEREIGN HARDENED PINECONE
# Generated from template - Version: 5.4.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.4.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apk add --no-cache python3 py3-pip ca-certificates curl
RUN pip3 install --no-cache-dir --break-system-packages pinecone-client 2>/dev/null || \
    pip3 install --no-cache-dir pinecone-client
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="pinecone" \
      org.opencontainers.image.version="5.4.0" \
      org.opencontainers.image.vendor="Pinecone" \
      org.opencontainers.image.source="https://github.com/pinecone-io/pinecone-python-client" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM