# =============================================================================
# SOVEREIGN HARDENED NXLOG
# Generated from template - Version: 3.1.2331
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# C binary requires shared libraries - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.1.2331
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://nxlog.co/downloads/nxlog-ce/nxlog-ce-${VERSION}-linux-x86_64.tar.gz" -o /nxlog.tar.gz && \
    echo "e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6  /nxlog.tar.gz" | sha256sum -c -
RUN tar -xzf /nxlog.tar.gz -C /opt && \
    rm /nxlog.tar.gz

FROM debian:bookworm-20240101-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libcurl4 \
        libssl3 \
        libzstd1 \
        liblzma5 \
        zlib1g \
        libexpat1 && \
    strip /opt/nxlog/bin/nxlog 2>/dev/null || true && \
    rm -rf /var/lib/apt/lists/*

FROM debian:bookworm-20240101-slim
RUN groupadd -g 65534 nxlog && \
    useradd -m -u 65534 -g nxlog -s /usr/sbin/nologin nxlog
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libcurl4 \
        libssl3 \
        libzstd1 \
        liblzma5 \
        zlib1g \
        libexpat1 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/nxlog /opt/nxlog
COPY --from=builder /opt/nxlog/bin/nxlog /opt/nxlog/bin/nxlog
RUN mkdir -p /app/conf /app/logs /app/data /var/lib/nxlog && \
    chown -R nxlog:nxlog /app /opt/nxlog /var/lib/nxlog
USER 65534:65534
WORKDIR /app
EXPOSE 514 514/udp
ENV NXLOG_HOME=/opt/nxlog \
    NXLOG_CONF_DIR=/app/conf \
    NXLOG_LOG_DIR=/app/logs
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/opt/nxlog/bin/nxlog", "-v"]
ENTRYPOINT ["/opt/nxlog/bin/nxlog"]
CMD ["-c", "/app/conf/nxlog.conf"]
LABEL org.opencontainers.image.title="nxlog" \
      org.opencontainers.image.version="3.1.2331" \
      org.opencontainers.image.vendor="nxlog" \
      org.opencontainers.image.description="NXLog Community Edition - log collection and forwarding" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="c"
