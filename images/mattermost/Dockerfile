# =============================================================================
# SOVEREIGN HARDENED MATTERMOST
# Mattermost team collaboration (self-hosted Slack alternative)
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=11.6.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tar && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://releases.mattermost.com/${VERSION}/mattermost-${VERSION}-linux-amd64.tar.gz" -o /mattermost.tar.gz && \
    mkdir -p /opt/mattermost && \
    tar -xzf /mattermost.tar.gz -C /opt && \
    rm /mattermost.tar.gz

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates tzdata libicu72 && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=downloader /opt/mattermost /opt/mattermost
RUN groupadd -g 65534 -r mattermost 2>/dev/null || true && \
    useradd -r -u 65534 -g mattermost -d /opt/mattermost -s /sbin/nologin mattermost 2>/dev/null || true && \
    mkdir -p /opt/mattermost/data /opt/mattermost/logs /opt/mattermost/plugins /opt/mattermost/client/plugins && \
    chown -R 65534:65534 /opt/mattermost
USER 65534:65534
WORKDIR /opt/mattermost
EXPOSE 8065
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8065/api/v4/system/ping"]
ENTRYPOINT ["/opt/mattermost/bin/mattermost"]
LABEL org.opencontainers.image.title="mattermost" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/mattermost" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="collaboration" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
