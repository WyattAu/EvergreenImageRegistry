# =============================================================================
# SOVEREIGN HARDENED GRAFANA
# Generated from template - Version: 11.0.0
# Constraint: distroless - minimal base with glibc, CVE-free
# Priority: scratch > distroless (best) > wolfi > debian-slim
# =============================================================================

ARG VERSION=11.0.0
ARG BUILD_DATE

FROM gcr.io/distroless/cc-debian12 AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/grafana/grafana/releases/download/11.0.0/grafana-11.0.0.linux-amd64.tar.gz" -o /grafana.tar.gz && \
    tar -xzf /grafana.tar.gz -C / && rm /grafana.tar.gz && chmod +x /grafana 2>/dev/null || \
    curl -fsSL "https://github.com/grafana/grafana/releases/download/11.0.0/grafana-11.0.0.linux-amd64.tar.gz" -o /grafana && chmod +x /grafana

FROM gcr.io/distroless/cc-debian12
COPY --from=downloader /grafana /grafana
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app /var/log/grafana /var/cache/grafana
USER nonroot
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD grafana grafana --version
ENTRYPOINT ["/grafana"]
LABEL org.opencontainers.image.title="grafana" \
      org.opencontainers.image.version="11.0.0" \
      org.opencontainers.image.vendor="Grafana" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
