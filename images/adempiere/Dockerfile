ARG VERSION=3.9.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/adempiere/adempiere/releases/download/release-3.9.4/Adempiere_394.tar.gz" -o /Adempiere_394.tar.gz && \
    unzip -q /Adempiere_394.tar.gz -d /opt/ && rm /Adempiere_394.tar.gz

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/Adempiere_394 /opt/adempiere
RUN mkdir -p /app /var/log/adempiere \
    && chown -R 65534:65534 /app /var/log/adempiere /opt/adempiere
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8080"]
ENTRYPOINT ["java", "-jar", "/opt/adempiere/Adempiere"]
LABEL org.opencontainers.image.title="adempiere" \
      org.opencontainers.image.version="3.9.4" \
      org.opencontainers.image.vendor="Adempiere" \
      org.opencontainers.image.source="https://github.com/adempiere/adempiere" \
      sovereign.image.tier="2" \
      sovereign.image.category="crm-erp" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
