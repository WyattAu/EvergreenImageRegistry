FROM debian:bookworm-slim AS downloader
ARG VERSION=2.10.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates dpkg && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Stirling-Tools/Stirling-PDF/releases/download/v${VERSION}/Stirling-PDF-linux-x86_64.deb -o /stirling-pdf.deb && \
    dpkg -i /stirling-pdf.deb && rm /stirling-pdf.deb


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 
COPY --from=downloader /opt/stirling-pdf /opt/stirling-pdf
RUN mkdir -p /app /var/log/stirling-pdf && \
    chown -R 65532:65532 /app /var/log/stirling-pdf /opt/stirling-pdf
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/opt/stirling-pdf/stirling-pdf"]
LABEL org.opencontainers.image.title="stirling-pdf" \
      org.opencontainers.image.version="2.10.0" \
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
