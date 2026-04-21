# =============================================================================
# SOVEREIGN HARDENED TELEGRAF
# Generated from template - Version: 1.30.3
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.30.3
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://dl.influxdata.com/telegraf/releases/telegraf-${VERSION}_linux_amd64.tar.gz" -o telegraf.tar.gz \
    && echo "1b5bf21b8f28b84be0db2b5a86e2c0bfed3a5656f06fc8c8f1c33c50b8c6afba  telegraf.tar.gz" | sha256sum -c - \
    && tar -xzf telegraf.tar.gz \
    && strip --strip-all usr/bin/telegraf \
    && mv usr/bin/telegraf /tmp/telegraf

FROM scratch
COPY --from=builder /tmp/telegraf /usr/bin/telegraf
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
EXPOSE 8125 8092 8094
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/bin/telegraf", "--version"]
ENTRYPOINT ["/usr/bin/telegraf"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="monitoring" \
      org.opencontainers.image.title="telegraf" \
      org.opencontainers.image.description="Sovereign hardened Telegraf - metrics collection agent by InfluxData" \
      org.opencontainers.image.version="${VERSION}"
