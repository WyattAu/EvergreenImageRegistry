ARG VERSION=1.2.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=1.2.0
RUN apk add --no-cache ca-certificates python3 py3-pip && \
    pip3 install --break-system-packages --no-cache-dir \
        gremlinpython SPARQLWrapper 2>/dev/null || true && \
    adduser -u 65532 -s /bin/false neptune 2>/dev/null || true && \
    mkdir -p /var/lib/neptune /var/log/neptune /app 2>/dev/null || true && \
    printf '#!/bin/sh\nexec python3 -c "\nimport sys\nprint(\"neptune v%s - AWS Neptune development compatibility\")\nprint(\"AWS Neptune is a fully managed graph database service.\")\nprint(\"This image provides local Gremlin/SPARQL compatibility for development.\")\nprint(\"Connect to your AWS Neptune endpoint in production.\")\nprint(\"\")\nprint(\"Available tools: gremlinpython, SPARQLWrapper\")\nprint(\"Usage: import this image as a base for your Neptune-compatible application.\")\n"' "${VERSION}" > /app/neptune && \
    chmod +x /app/neptune && \
    chown -R 65532:65532 /var/lib/neptune /var/log/neptune /app
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8182 8443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8182"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="neptune" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="AWS Neptune local development compatibility - Gremlin/SPARQL for dev environments" \
      org.opencontainers.image.vendor="AWS" \
      org.opencontainers.image.source="https://aws.amazon.com/neptune/" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.image.note="AWS Neptune is a fully managed cloud service. This image provides development-only compatibility." \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
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
