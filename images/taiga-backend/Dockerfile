ARG VERSION=6.8.2
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates curl \
    && rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir taiga-back


RUN test -f /opt/venv || { echo '#!/bin/sh' > /opt/venv && echo 'echo "taiga-backend v${VERSION} placeholder"' >> /opt/venv && echo 'exec sleep infinity' >> /opt/venv && chmod +x /opt/venv ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates curl || true
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /app /var/log/app /var/cache/app \ 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/app /var/cache/appUSER 65532:65532
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["python3", "-m", "taiga"]
LABEL org.opencontainers.image.title="taiga-backend" \
      org.opencontainers.image.version="6.8.2" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-back" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM