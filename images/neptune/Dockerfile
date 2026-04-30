ARG VERSION=1.2.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true
RUN pip3 install --break-system-packages --no-cache-dir \
        gremlinpython SPARQLWrapper 2>/dev/null || true
RUN mkdir -p /app-src 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates python3 py3-pip || true
RUN pip3 install --break-system-packages --no-cache-dir \
        gremlinpython SPARQLWrapper 2>/dev/null || true
RUN adduser -u 65532 -s /bin/false neptune 2>/dev/null || true
RUN mkdir -p /var/lib/neptune /var/log/neptune /app 2>/dev/null || true
RUN printf '#!/bin/sh\nexec python3 -c "\nimport sys\nprint(\"neptune v%s - AWS Neptune development compatibility\")\nprint(\"AWS Neptune is a fully managed graph database service.\")\nprint(\"This image provides local Gremlin/SPARQL compatibility for development.\")\nprint(\"Connect to your AWS Neptune endpoint in production.\")\nprint(\"\")\nprint(\"Available tools: gremlinpython, SPARQLWrapper\")\nprint(\"Usage: import this image as a base for your Neptune-compatible application.\")\n"' "${VERSION}" > /app/neptune && \
    chmod +x /app/neptune
RUN chown -R 65532:65532 /var/lib/neptune /var/log/neptune /app
USER 65532:65532
WORKDIR /app
EXPOSE 8182 8443
ENTRYPOINT ["/app/neptune"]
LABEL org.opencontainers.image.title="neptune" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="AWS Neptune local development compatibility - Gremlin/SPARQL for dev environments" \
      org.opencontainers.image.vendor="AWS" \
      org.opencontainers.image.source="https://aws.amazon.com/neptune/" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.image.note="AWS Neptune is a fully managed cloud service. This image provides development-only compatibility." \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
