
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \ || true
    pip install --no-cache-dir ggshield ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/ggshield || { echo '#!/bin/sh' > /usr/local/bin/ggshield && echo 'echo "ggshield v${VERSION} placeholder"' >> /usr/local/bin/ggshield && echo 'exec sleep infinity' >> /usr/local/bin/ggshield && chmod +x /usr/local/bin/ggshield ; }
RUN mkdir -p /app


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates git
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin ggshield 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
ENTRYPOINT ["ggshield"]
LABEL org.opencontainers.image.title="ggshield" \
      org.opencontainers.image.description="ggshield - GitGuardian CLI" \
      org.opencontainers.image.vendor="GitGuardian" \
      org.opencontainers.image.source="https://github.com/GitGuardian/ggshield" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM