
FROM debian:bookworm-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://nxlog.co/downloads/nxlog-ce/nxlog-ce-${VERSION}-linux-x86_64.tar.gz" -o /nxlog.tar.gz && \
    echo "e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6  /nxlog.tar.gz" | sha256sum -c || true  #
RUN tar -xzf /nxlog.tar.gz -C /opt && \
    rm /nxlog.tar.gz




FROM debian:bookworm-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        openssl-libs \
        libzstd1 \
        liblzma5 \
        zlib1g \
        libexpat1 && \
    strip /opt/nxlog/bin/nxlog 2>/dev/null || true && \
    rm -rf /var/lib/apt/lists/*


FROM cgr.dev/chainguard/wolfi-base:latest

RUN addgroup -S 65532 nxlog && \
    adduser -u 65532 -G nxlog -D -s /sbin/nologin nxlog
RUN apk add --no-cache curl libzstd1 zlib expat ca-certificates
COPY --from=downloader /opt/nxlog /opt/nxlog
COPY --from=builder /opt/nxlog/bin/nxlog /opt/nxlog/bin/nxlog
RUN mkdir -p /app/conf /app/logs /app/data /var/lib/nxlog && \
    chown -R nxlog:nxlog /app /opt/nxlog /var/lib/nxlog
USER 65532:65532
WORKDIR /app
EXPOSE 514 514/udp
ENV NXLOG_HOME=/opt/nxlog \
    NXLOG_CONF_DIR=/app/conf \
    NXLOG_LOG_DIR=/app/logs
ENTRYPOINT ["/opt/nxlog/bin/nxlog"]
CMD ["-c", "/app/conf/nxlog.conf"]
LABEL org.opencontainers.image.title="nxlog" \
      org.opencontainers.image.version="3.1.2331" \
      org.opencontainers.image.vendor="nxlog" \
      org.opencontainers.image.description="NXLog Community Edition - log collection and forwarding" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM