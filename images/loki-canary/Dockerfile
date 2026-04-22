# =============================================================================
# SOVEREIGN HARDENED LOKI-CANARY
# Generated from template - Version: 2.9.4
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.9.4
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/grafana/loki/releases/download/v${VERSION}/loki-canary-linux-amd64.zip" -o /loki-canary.zip && \
    echo "d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5  /loki-canary.zip" | sha256sum -c -
RUN unzip /loki-canary.zip -d /tmp/loki-canary && \
    mv /tmp/loki-canary/loki-canary-linux-amd64 /loki-canary && \
    rm /loki-canary.zip && \
    strip /loki-canary

FROM debian:bookworm-20240101-slim AS builder
RUN mkdir -p /app /var/log/loki-canary /var/cache/loki-canary

FROM scratch
COPY --from=downloader /loki-canary /loki-canary
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/loki-canary /var/log/loki-canary
COPY --from=builder /var/cache/loki-canary /var/cache/loki-canary
USER 65532:65532
WORKDIR /app
EXPOSE 3500
ENTRYPOINT ["/loki-canary"]
LABEL org.opencontainers.image.title="loki-canary" \
      org.opencontainers.image.version="2.9.4" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Loki canary for testing log ingestion pipeline" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="go" \
      sovereign.hft.runtime-hints="GOMAXPROCS=<cores>"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM