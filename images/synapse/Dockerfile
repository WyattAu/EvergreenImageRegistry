# =============================================================================
# SOVEREIGN HARDENED SYNAPSE
# Generated from template - Version: 1.113.0
# Constraint: wolfi - Chaenguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=1.113.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache curl ca-certificates python3 py3-pip
RUN curl -fsSL "https://github.com/matrix-org/synapse/releases/download/v${VERSION}/synapse_py3.tar.gz" -o /synapse.tar.gz && \
    tar -xzf /synapse.tar.gz -C / && rm /synapse.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache python3 py3-pip
RUN addgroup -g 65534 synapse || true
RUN adduser -D -u 65534 -G synapse synapse || true
RUN mkdir -p /app /var/log/synapse /var/cache/synapse
COPY --from=downloader /synapse /app/synapse
USER synapse
WORKDIR /app
EXPOSE 8008
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/bin/curl", "-sf", "http://localhost:8008/_matrix/client/versions"]
ENTRYPOINT ["python3", "-m", "synapse.app.homeserver"]
LABEL org.opencontainers.image.title="synapse" \
      org.opencontainers.image.version="1.113.0" \
      org.opencontainers.image.vendor="Matrix" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"