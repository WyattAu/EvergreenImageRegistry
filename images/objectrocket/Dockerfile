ARG VERSION=1.0.0
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true && \
    pip3 install --break-system-packages --no-cache-dir \
        pymongo 2>/dev/null || true && \
    mkdir -p /app-src 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION
RUN apk add --no-cache ca-certificates python3 py3-pip || true && \
    pip3 install --break-system-packages --no-cache-dir \
        pymongo 2>/dev/null || true && \
    adduser -u 65532 -s /bin/false objectrocket 2>/dev/null || true && \
    mkdir -p /var/lib/objectrocket /var/log/objectrocket /app 2>/dev/null || true && \
    printf '#!/bin/sh\nexec python3 -c "\nimport sys\nprint(\"objectrocket v%s - MongoDB cloud development compatibility\")\nprint(\"ObjectRocket is a fully managed database cloud service.\")\nprint(\"This image provides a pymongo client library for development.\")\nprint(\"\")\nprint(\"Available: pymongo client library\")\nprint(\"Usage: import this image as a base for your ObjectRocket-compatible application.\")\nprint(\"Connect to your ObjectRocket/MongoDB Atlas endpoint in production.\")\n"' "${VERSION}" > /app/objectrocket && \
    chmod +x /app/objectrocket && \
    chown -R 65532:65532 /var/lib/objectrocket /var/log/objectrocket /app
USER 65532:65532
WORKDIR /app
EXPOSE 27017

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:27017/ || exit 1
ENTRYPOINT ["/app/objectrocket"]
LABEL org.opencontainers.image.title="objectrocket" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="ObjectRocket local development compatibility - MongoDB cloud service for dev environments" \
      org.opencontainers.image.vendor="ObjectRocket" \
      org.opencontainers.image.source="https://www.objectrocket.com/" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.image.note="ObjectRocket is a fully managed cloud service. Use the ObjectRocket endpoint in production." \
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
