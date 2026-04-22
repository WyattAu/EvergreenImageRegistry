ARG VERSION=18.12.11
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/apache/ofbiz-framework/releases/download/release-18.12.11/apache-ofbiz-18.12.11.zip" -o /apache-ofbiz-18.12.11.zip && \
    unzip -q /apache-ofbiz-18.12.11.zip -d /opt/ && rm /apache-ofbiz-18.12.11.zip

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/apache-ofbiz-18.12.11 /opt/apache-ofbiz
RUN mkdir -p /app /var/log/apache-ofbiz \
    && chown -R 65534:65534 /app /var/log/apache-ofbiz /opt/apache-ofbiz
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8080"]
ENTRYPOINT ["java", "-jar", "/opt/apache-ofbiz/apache-ofbiz-18.12.11"]
LABEL org.opencontainers.image.title="apache-ofbiz" \
      org.opencontainers.image.version="18.12.11" \
      org.opencontainers.image.vendor="Apache OFBiz" \
      org.opencontainers.image.source="https://github.com/apache/ofbiz-framework" \
      sovereign.image.tier="2" \
      sovereign.image.category="crm-erp" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
