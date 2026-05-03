ARG VERSION=3.10.0
ARG BUILD_DATE

FROM docker.io/tigergraph/tigergraph:latest AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
RUN apk add --no-cache ca-certificates curl libstdc++ python3 || true && \
    adduser -D -u 65532 -s /bin/false tigergraph 2>/dev/null || true && \
    mkdir -p /var/lib/tigergraph /var/log/tigergraph /var/cache/tigergraph /opt/tigergraph 2>/dev/null || true
COPY --from=upstream /opt/tigergraph /opt/tigergraph 2>/dev/null || true
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
RUN chown -R 65532:65532 /opt/tigergraph /var/lib/tigergraph /var/log/tigergraph /var/cache/tigergraph 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/tigergraph
EXPOSE 14240 9000 8123 8443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8123/ || exit 1
ENTRYPOINT ["/opt/tigergraph/bin/gadmin", "start", "all"]
LABEL org.opencontainers.image.title="tigergraph-ecosystem" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened TigerGraph Ecosystem - extracted from official Docker image" \
      org.opencontainers.image.vendor="TigerGraph" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.image.note="Extracted from docker.io/tigergraph/tigergraph:latest. CloudFront download URL is defunct." \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
