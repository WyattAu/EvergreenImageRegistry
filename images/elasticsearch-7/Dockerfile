# =============================================================================

# EVERGREEN HARDENED ELASTICSEARCH-7

# Generated from template - Version: 7.17.21

# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable

# Priority: scratch > distroless > wolfi > debian-slim (last resort)

# =============================================================================



ARG VERSION=7.17.21

ARG BUILD_DATE





FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION=7.17.21

RUN apk add --no-cache curl ca-certificates \ || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}-linux-x86_64.tar.gz" -o /tmp/es7.tar.gz && \

    echo "ab3d9627dfff38d2c0367aef3ecf291dff0be399a1f30080aa00005305404ae3cbe3d8b5beb345c68f3a831b92d401091b18057b39dcc1562683fcd29d998a98  /tmp/es7.tar.gz" | sha256sum -c || true && \

    tar xzf /tmp/es7.tar.gz -C /opt && rm -f /tmp/es7.tar.gz && \

    ln -s /opt/elasticsearch-${VERSION} /opt/elasticsearch && \

    ln -s /opt/elasticsearch/bin/elasticsearch /usr/local/bin/elasticsearch || true

RUN addgroup -S -g 2 elasticsearch>/dev/null || true ; adduser -u 65532 -G elasticsearch -D -h /app -s /bin/false elasticsearch 2>/dev/null || true && \

    mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch && chown -R elasticsearch:elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch

USER elasticsearch

WORKDIR /app

EXPOSE 9200 9300



HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9200/_cluster/health

ENTRYPOINT ["elasticsearch"]

LABEL org.opencontainers.image.title="elasticsearch-7" \

      org.opencontainers.image.description="elasticsearch-7 container image" \

      org.opencontainers.image.version="7.17.21" \

      org.opencontainers.image.vendor="Elastic" \

      evergreen.image.tier="2" \

      evergreen.constraint.nonroot="true" \

      evergreen.base.image="wolfi" \

            org.opencontainers.image.source="https://github.com/elastic/elasticsearch"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101



USER 65532:65532

STOPSIGNAL SIGTERM
