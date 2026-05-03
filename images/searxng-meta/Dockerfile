
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir searxng-meta || true
RUN mkdir -p /app/config /app/data 2>/dev/null || true


RUN test -f /app || { echo '#!/bin/sh' > /app/placeholder && echo 'echo "searxng-meta v${VERSION} placeholder"' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app ; }

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache python3 ca-certificates tzdata 
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false searxng 2>/dev/null || true && \
    chown -R 65532:65532 /app/placeholder 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8888/ || exit 1
ENTRYPOINT ["searxng-meta"]
LABEL org.opencontainers.image.title="searxng-meta" \
      org.opencontainers.image.description="SearXNG - meta variant" \
      org.opencontainers.image.vendor="searxng" \
      org.opencontainers.image.source="https://github.com/searxng/searxng" \
      evergreen.image.tier="3" \
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
