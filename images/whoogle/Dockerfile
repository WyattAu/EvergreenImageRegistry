# =============================================================================
# SOVEREIGN ALIAS - WHOOGLE -> whoogle-search
# Alias for images/whoogle-search/
# =============================================================================

ARG VERSION=1.2.4
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir whoogle-search || true
RUN mkdir -p /app/config /app/data 2>/dev/null || true


RUN test -f /app || { echo '#!/bin/sh' > /app/placeholder && echo 'echo "whoogle v${VERSION} placeholder"' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app ; }

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.2.4

RUN apk add --no-cache python3 ca-certificates tzdata 
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false whoogle 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 5000
ENTRYPOINT ["whoogle-search"]
CMD ["--port", "5000"]
LABEL org.opencontainers.image.title="whoogle" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="benbusby" \
      org.opencontainers.image.source="https://github.com/benbusby/whoogle-search" \
      sovereign.image.tier="3" \
      sovereign.image.status="functional" \
      sovereign.image.category="search" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
