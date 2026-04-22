ARG VERSION=24.04.10.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg2 apt-transport-https && \
    curl -fsSL "https://www.collaboraoffice.com/downloads/collabora-office/code/debian/" | grep -oP 'https://[^"]+Release.key' | head -1 | xargs -r curl -fsSL | gpg --dearmor -o /usr/share/keyrings/collabora.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/collabora.gpg] https://www.collabora.com/downloads/collabora-office/code/debian/ /" > /etc/apt/sources.list.d/collabora.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends collabora-online-code-brand && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/log/collabora /etc/loolwsd \
    && chown -R 65534:65534 /var/log/collabora /etc/loolwsd
USER 65534:65534
WORKDIR /app
EXPOSE 9980
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:9980/hosting/discovery"]
ENTRYPOINT ["/usr/bin/loolwsd"]
LABEL org.opencontainers.image.title="collabora-online" \
      org.opencontainers.image.version="24.04.10.2" \
      org.opencontainers.image.vendor="Collabora" \
      org.opencontainers.image.source="https://github.com/CollaboraOnline/online" \
      sovereign.image.tier="2" \
      sovereign.image.category="document-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
