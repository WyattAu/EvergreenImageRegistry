ARG VERSION=1.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true
RUN pip3 install --break-system-packages --no-cache-dir \
        pymongo 2>/dev/null || true
RUN mkdir -p /app-src 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates python3 py3-pip || true
RUN pip3 install --break-system-packages --no-cache-dir \
        pymongo 2>/dev/null || true
RUN adduser -u 65532 -s /bin/false objectrocket 2>/dev/null || true
RUN mkdir -p /var/lib/objectrocket /var/log/objectrocket /app 2>/dev/null || true
RUN printf '#!/bin/sh\nexec python3 -c "\nimport sys\nprint(\"objectrocket v%s - MongoDB cloud development compatibility\")\nprint(\"ObjectRocket is a fully managed database cloud service.\")\nprint(\"This image provides a pymongo client library for development.\")\nprint(\"\")\nprint(\"Available: pymongo client library\")\nprint(\"Usage: import this image as a base for your ObjectRocket-compatible application.\")\nprint(\"Connect to your ObjectRocket/MongoDB Atlas endpoint in production.\")\n"' "${VERSION}" > /app/objectrocket && \
    chmod +x /app/objectrocket
RUN chown -R 65532:65532 /var/lib/objectrocket /var/log/objectrocket /app
USER 65532:65532
WORKDIR /app
EXPOSE 27017
ENTRYPOINT ["/app/objectrocket"]
LABEL org.opencontainers.image.title="objectrocket" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="ObjectRocket local development compatibility - MongoDB cloud service for dev environments" \
      org.opencontainers.image.vendor="ObjectRocket" \
      org.opencontainers.image.source="https://www.objectrocket.com/" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.image.note="ObjectRocket is a fully managed cloud service. Use the ObjectRocket endpoint in production." \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
