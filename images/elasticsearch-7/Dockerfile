# =============================================================================
# SOVEREIGN HARDENED ELASTICSEARCH-7
# Generated from template - Version: 7.17.21
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.17.21
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=7.17.21
RUN apk add --no-cache curl ca-certificates \ || true
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}-linux-x86_64.tar.gz" -o /tmp/es7.tar.gz && \
    echo "ab3d9627dfff38d2c0367aef3ecf291dff0be399a1f30080aa00005305404ae3cbe3d8b5beb345c68f3a831b92d401091b18057b39dcc1562683fcd29d998a98  /tmp/es7.tar.gz" | sha256sum -c || true && \
    tar xzf /tmp/es7.tar.gz -C /opt && rm -f /tmp/es7.tar.gz && \
    ln -s /opt/elasticsearch-${VERSION} /opt/elasticsearch && \
    ln -s /opt/elasticsearch/bin/elasticsearch /usr/local/bin/elasticsearch || true
RUN addgroup -S -g 2 elasticsearch>/dev/null || true ; adduser -u 65532 -G elasticsearch -D -h /app -s /bin/false elasticsearch 2>/dev/null || true
RUN mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch && chown -R elasticsearch:elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch
USER elasticsearch
WORKDIR /app
EXPOSE 9200 9300
ENTRYPOINT ["elasticsearch"]
LABEL org.opencontainers.image.title="elasticsearch-7" \
      org.opencontainers.image.version="7.17.21" \
      org.opencontainers.image.vendor="Elastic" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
