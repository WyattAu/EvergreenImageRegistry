ARG VERSION=3.10.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM docker.io/tigergraph/tigergraph:4.2.2@sha256:c4e7ef2d653b2fa57e2df9408719d78521defe38fe3ae5ef5b8d15134a61fae8 AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=3.10.0
RUN apk add --no-cache ca-certificates wget libstdc++ python3 && \
    adduser -D -u 65532 -s /bin/false tigergraph 2>/dev/null || true && \
    mkdir -p /var/lib/tigergraph /var/log/tigergraph /var/cache/tigergraph /opt/tigergraph 2>/dev/null || true
COPY --from=upstream /opt/tigergraph /opt/tigergraph
RUN mkdir -p /etc/ssl/certs || true && COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown -R 65532:65532 /opt/tigergraph /var/lib/tigergraph /var/log/tigergraph /var/cache/tigergraph 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/tigergraph
EXPOSE 14240 9000 8123 8443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8123"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="tigergraph-ecosystem" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened TigerGraph Ecosystem - extracted from official Docker image" \
      org.opencontainers.image.vendor="TigerGraph" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.image.note="Extracted from docker.io/tigergraph/tigergraph:4.2.2. CloudFront download URL is defunct." \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/tigergraph/ecosystem"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
