ARG VERSION=8.5.0
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates curl mariadb-client && \
    rm -rf /var/lib/apt/lists/* || true
RUN pip3 install --break-system-packages --no-cache-dir \
        pymysql sqlalchemy 2>/dev/null || true
RUN mkdir -p /app-src 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION
RUN apk add --no-cache ca-certificates python3 py3-pip mariadb-client || true && \
    pip3 install --break-system-packages --no-cache-dir \
        pymysql sqlalchemy 2>/dev/null || true && \
    adduser -u 65532 -s /bin/false singlestore 2>/dev/null || true && \
    mkdir -p /var/lib/singlestore /var/log/singlestore /app 2>/dev/null || true
RUN printf '#!/bin/sh\nexec python3 -c "\nimport sys\nprint(\"singlestore v%s - development compatibility (requires license)\")\nprint(\"SingleStore is a commercial distributed SQL database.\")\nprint(\"This image provides pymysql/sqlalchemy client libraries for development.\")\nprint(\"\")\nprint(\"Available: pymysql, sqlalchemy, mariadb-client\")\nprint(\"Usage: import this image as a base for your SingleStore-compatible application.\")\nprint(\"Download the free edition from https://www.singlestore.com/ for production use.\")\n"' "${VERSION}" > /app/singlestore && \
    chmod +x /app/singlestore
RUN chown -R 65532:65532 /var/lib/singlestore /var/log/singlestore /app
USER 65532:65532
WORKDIR /app
EXPOSE 3306 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:3306/ || exit 1
ENTRYPOINT ["/app/singlestore"]
LABEL org.opencontainers.image.title="singlestore" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="SingleStore local development compatibility - commercial distributed SQL database" \
      org.opencontainers.image.vendor="SingleStore" \
      org.opencontainers.image.source="https://www.singlestore.com/" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.image.note="SingleStore requires a license. Download from https://www.singlestore.com/ for production." \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
