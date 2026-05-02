ARG VERSION=latest

FROM sqlpad/sqlpad:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates bash
COPY --from=upstream /app /app
RUN adduser -u 65532 -s /bin/false sqlpad 2>/dev/null || true && \
    chown -R 65532:65532 /app


WORKDIR /app

EXPOSE 3000
EXPOSE 9101

LABEL org.opencontainers.image.title="sqlpad" org.opencontainers.image.version="7.5.1" org.opencontainers.image.description="SQLPad - Web-based SQL Editor with Query Visualization" org.opencontainers.image.vendor="SQLPad" org.opencontainers.image.source="https://github.com/sqlpad/sqlpad" sovereign.image.tier="1" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["node", "server.js"]
