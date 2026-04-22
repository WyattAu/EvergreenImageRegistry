ARG VERSION=0.46.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/Stirling-Tools/Stirling-PDF/releases/download/v0.46.0/stirling-pdf-0.46.0.jar" -o /stirling-pdf-0.46.0.jar && \
    unzip -q /stirling-pdf-0.46.0.jar -d /opt/ && rm /stirling-pdf-0.46.0.jar

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/stirling-pdf-0.46.0.jar /opt/stirling-pdf
RUN mkdir -p /app /var/log/stirling-pdf \
    && chown -R 65534:65534 /app /var/log/stirling-pdf /opt/stirling-pdf
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8080"]
ENTRYPOINT ["java", "-jar", "/opt/stirling-pdf/stirling-pdf.jar"]
LABEL org.opencontainers.image.title="stirling-pdf" \
      org.opencontainers.image.version="0.46.0" \
      org.opencontainers.image.vendor="Stirling-PDF" \
      org.opencontainers.image.source="https://github.com/Stirling-Tools/Stirling-PDF" \
      sovereign.image.tier="2" \
      sovereign.image.category="document-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
