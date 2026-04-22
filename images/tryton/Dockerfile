ARG VERSION=7.2.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 py3-pip python3 ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir trytond

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache python3 ca-certificates curl
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /app /var/log/app /var/cache/app \
    && chown -R 65532:65532 /app /var/log/app /var/cache/app
USER 65532:65532
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["python3", "-m", "trytond"]
LABEL org.opencontainers.image.title="tryton" \
      org.opencontainers.image.version="7.2.0" \
      org.opencontainers.image.vendor="Tryton" \
      org.opencontainers.image.source="https://github.com/tryton/tryton" \
      sovereign.image.tier="2" \
      sovereign.image.category="crm-erp" \
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