ARG VERSION=0.46.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Stirling-Tools/Stirling-PDF/releases/download/v0.46.0/stirling-pdf-0.46.0.jar" -o /stirling-pdf-0.46.0.jar && \
    unzip -q /stirling-pdf-0.46.0.jar -d /opt/ && rm /stirling-pdf-0.46.0.jar


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /opt/stirling-pdf-0.46.0.jar /opt/stirling-pdf-core
RUN mkdir -p /app /var/log/stirling-pdf-core \
    && chown -R 65532:65532 /app /var/log/stirling-pdf-core /opt/stirling-pdf-core
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/opt/stirling-pdf-core/stirling-pdf.jar"]
LABEL org.opencontainers.image.title="stirling-pdf-core" \
      org.opencontainers.image.version="0.46.0" \
      org.opencontainers.image.vendor="Stirling-PDF" \
      org.opencontainers.image.source="https://github.com/Stirling-Tools/Stirling-PDF" \
      sovereign.image.tier="2" \
      sovereign.image.category="document-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM