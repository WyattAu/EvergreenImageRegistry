
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN printf '#!/bin/sh\nset -e\necho "=== Docker Clean ==="\ndocker system prune -af --volumes 2>/dev/null || true\ndocker builder prune -af 2>/dev/null || true\necho "=== Docker Clean Complete ==="\n' > /usr/local/bin/docker-clean && \
    chmod +x /usr/local/bin/docker-clean
RUN mkdir -p /app


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates
COPY --from=builder /usr/local/bin/docker-clean /usr/local/bin/docker-clean
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin dockerclean 2>/dev/null || true && \
    mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["docker-clean"]
LABEL org.opencontainers.image.title="docker-clean" \
      org.opencontainers.image.description="Docker cleanup script" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM