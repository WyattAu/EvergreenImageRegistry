FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN printf '#!/bin/sh\nset -e\necho "=== Docker Clean ==="\ndocker system prune -af --volumes 2>/dev/null || true\ndocker builder prune -af 2>/dev/null || true\necho "=== Docker Clean Complete ==="\n' > /usr/local/bin/docker-clean && \
    chmod +x /usr/local/bin/docker-clean
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/bin/docker-clean /usr/local/bin/docker-clean
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin dockerclean 2>/dev/null || true && \
    mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["test", "-x", "/usr/local/bin/docker-clean"]
ENTRYPOINT ["docker-clean"]
LABEL org.opencontainers.image.title="docker-clean" \
      org.opencontainers.image.description="Docker cleanup script" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
