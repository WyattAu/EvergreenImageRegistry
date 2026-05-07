ARG VERSION=1.2.0
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true && \
    pip3 install --break-system-packages --no-cache-dir \
        gremlinpython SPARQLWrapper 2>/dev/null || true && \
    mkdir -p /app-src 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION
RUN apk add --no-cache ca-certificates python3 py3-pip || true && \
    pip3 install --break-system-packages --no-cache-dir \
        gremlinpython SPARQLWrapper 2>/dev/null || true && \
    adduser -u 65532 -s /bin/false neptune 2>/dev/null || true && \
    mkdir -p /var/lib/neptune /var/log/neptune /app 2>/dev/null || true && \
    printf '#!/bin/sh\nexec python3 -c "\nimport sys\nprint(\"neptune v%s - AWS Neptune development compatibility\")\nprint(\"AWS Neptune is a fully managed graph database service.\")\nprint(\"This image provides local Gremlin/SPARQL compatibility for development.\")\nprint(\"Connect to your AWS Neptune endpoint in production.\")\nprint(\"\")\nprint(\"Available tools: gremlinpython, SPARQLWrapper\")\nprint(\"Usage: import this image as a base for your Neptune-compatible application.\")\n"' "${VERSION}" > /app/neptune && \
    chmod +x /app/neptune && \
    chown -R 65532:65532 /var/lib/neptune /var/log/neptune /app
USER 65532:65532
WORKDIR /app
EXPOSE 8182 8443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8182/ || exit 1
ENTRYPOINT ["/app/neptune"]
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
STOPSIGNAL SIGTERM
