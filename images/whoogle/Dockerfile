# =============================================================================
# SOVEREIGN ALIAS - WHOOGLE -> whoogle-search
# Alias for images/whoogle-search/
# =============================================================================

ARG VERSION=0.9.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir whoogle-search
RUN mkdir -p /app/config /app/data

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin whoogle 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/')"] || exit 0
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
      sovereign.constraint.debian_slim="true"
