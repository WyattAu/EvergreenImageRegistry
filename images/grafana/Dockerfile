# =============================================================================
# SOVEREIGN HARDENED GRAFANA
# Grafana observability dashboard (builds from source)
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=11.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates tar && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-amd64.tar.gz" -o /grafana.tar.gz && \
    tar -xzf /grafana.tar.gz -C /opt && \
    rm /grafana.tar.gz && \
    ln -sf /opt/grafana-${VERSION} /opt/grafana

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates tzdata libfontconfig1 && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /opt/grafana /opt/grafana
RUN ln -sf /opt/grafana/bin/grafana-server /usr/local/bin/grafana-server && \
    groupadd -g 65534 -r grafana 2>/dev/null || true && \
    useradd -r -u 65534 -g grafana -d /opt/grafana -s /sbin/nologin grafana 2>/dev/null || true && \
    mkdir -p /var/lib/grafana /var/log/grafana /etc/grafana && \
    chown -R 65534:65534 /var/lib/grafana /var/log/grafana /etc/grafana
USER 65534:65534
WORKDIR /opt/grafana
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["grafana-server", "-v"]
ENTRYPOINT ["grafana-server"]
CMD ["--homepath=/opt/grafana", "--config=/etc/grafana/grafana.ini"]
LABEL org.opencontainers.image.title="grafana" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.source="https://github.com/grafana/grafana" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
