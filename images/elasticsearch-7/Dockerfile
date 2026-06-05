# =============================================================================







# EVERGREEN HARDENED ELASTICSEARCH-7







# Generated from template - Version: 7.17.21







# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable







# Priority: scratch > distroless > wolfi > debian-slim (last resort)







# =============================================================================















ARG VERSION=7.17.21
ARG TARGETARCH







ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532























ARG SHIM_VERSION=v0.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim








ARG VERSION=7.17.21







RUN apk add --no-cache wget ca-certificates && \
    wget -t 3 -T 10 -qO /tmp/es7.tar.gz "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}-linux-x86_64.tar.gz" && \
    echo "e38938059bac6020de17be3a8804a25e55f40a5adc2edf2eda3e23897a2545e2  /tmp/es7.tar.gz" | sha256sum -c && \
    tar xzf /tmp/es7.tar.gz -C /opt && rm -f /tmp/es7.tar.gz && \
    ln -s /opt/elasticsearch-${VERSION} /opt/elasticsearch && \
    ln -s /opt/elasticsearch/bin/elasticsearch /usr/local/bin/elasticsearch || true







RUN addgroup -S -g 2 elasticsearch 2>/dev/null || true ; adduser -u 65532 -G elasticsearch -D -h /app -s /bin/false elasticsearch 2>/dev/null || true && \
    mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch && chown -R elasticsearch:elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch







USER elasticsearch







WORKDIR /app







EXPOSE 9200 9300






















HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9200"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]







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
