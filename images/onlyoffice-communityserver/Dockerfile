ARG VERSION=8.2.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg2 apt-transport-https && \
    curl -fsSL "https://download.onlyoffice.com/repo/onlyoffice.key" | gpg --dearmor -o /usr/share/keyrings/onlyoffice.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/onlyoffice.gpg] https://download.onlyoffice.com/repo/debian squeeze main" > /etc/apt/sources.list.d/onlyoffice.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends onlyoffice-documentserver && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/log/onlyoffice /var/lib/onlyoffice \
    && chown -R 65534:65534 /var/log/onlyoffice /var/lib/onlyoffice
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD ["curl", "-f", "http://localhost:80/healthcheck"]
ENTRYPOINT ["/usr/bin/ds"]
LABEL org.opencontainers.image.title="onlyoffice-communityserver" \
      org.opencontainers.image.version="8.2.2" \
      org.opencontainers.image.vendor="ONLYOFFICE" \
      org.opencontainers.image.source="https://github.com/ONLYOFFICE/DocumentServer" \
      sovereign.image.tier="2" \
      sovereign.image.category="document-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
