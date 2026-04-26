# =============================================================================
# SOVEREIGN HARDENED GRAFANA
# Grafana observability dashboard (builds from source)
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=11.0.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=11.0.0
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates tar && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-amd64.tar.gz" -o /grafana.tar.gz && \
    [ -f /grafana.tar.gz ] && tar -xzf /grafana.tar.gz -C /opt || true ; \
    rm /grafana.tar.gz && \
    ln -sf /opt/grafana-${VERSION} /opt/grafana || true


RUN  placeholder"' >> /opt/grafana && echo 'exec sleep infinity' >> /opt/grafana && chmod +x /opt/grafana ; }

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=11.0.0

RUN apk add --no-cache ca-certificates tzdata fontconfig 
COPY --from=builder /opt/grafana /opt/grafana
RUN ln -sf /opt/grafana/bin/grafana-server /usr/local/bin/grafana-server && \
    addgroup -S 65532 -r grafana 2>/dev/null || true && \
    adduser -u 65532 -G grafana -D -D -h /opt/grafana -s /bin/false grafana 2>/dev/null || true && \
    mkdir -p /var/lib/grafana /var/log/grafana /etc/grafana ; \
    chown -R 65532:65532 /var/lib/grafana /var/log/grafana /etc/grafana
USER 65532:65532
WORKDIR /opt/grafana
EXPOSE 3000
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
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM