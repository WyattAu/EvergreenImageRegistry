
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --break-system-packages --upgrade pip && \
    pip install --no-cache-dir --break-system-packages detect-secrets || true
RUN mkdir -p /app-src 2>/dev/null || true


RUN test -f /app || { echo '#!/bin/sh' > /app/placeholder && echo 'echo "detect-secrets v${VERSION} placeholder"' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app ; } || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates 
RUN mkdir -p /opt 2>/dev/null || true
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false detectsecrets 2>/dev/null || true && \
    chown -R 65532:65532 /app/placeholder 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
ENTRYPOINT ["detect-secrets"]
CMD ["scan"]
LABEL org.opencontainers.image.title="detect-secrets" \
      org.opencontainers.image.description="detect-secrets - Yelp secret detection" \
      org.opencontainers.image.vendor="Yelp" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
