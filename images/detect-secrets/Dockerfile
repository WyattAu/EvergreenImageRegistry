
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3-venv python3 ca-certificates ; rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --break-system-packages --upgrade pip && \
    pip install --no-cache-dir --break-system-packages detect-secrets || true && \
    mkdir -p /app-src 2>/dev/null || true && \
    test -f /app || { echo '#!/bin/sh' > /app/placeholder && echo 'echo "detect-secrets v${VERSION} placeholder"' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app ; } || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache python3 ca-certificates && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false detectsecrets 2>/dev/null || true && \
    chown -R 65532:65532 /app/placeholder 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["detect-secrets"]
CMD ["scan"]
LABEL org.opencontainers.image.title="detect-secrets" \
      org.opencontainers.image.description="detect-secrets - Yelp secret detection" \
      org.opencontainers.image.vendor="Yelp" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/Yelp/detect-secrets" \
                  org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
