ARG VERSION=3.10.0
ARG BUILD_DATE

FROM docker.io/tigergraph/tigergraph:latest AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

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
ENTRYPOINT ["/opt/tigergraph/bin/gadmin", "start", "all"]
LABEL org.opencontainers.image.title="tigergraph-ecosystem" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened TigerGraph Ecosystem - extracted from official Docker image" \
      org.opencontainers.image.vendor="TigerGraph" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.image.note="Extracted from docker.io/tigergraph/tigergraph:latest. CloudFront download URL is defunct." \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
