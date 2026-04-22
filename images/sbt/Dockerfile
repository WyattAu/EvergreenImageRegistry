ARG VERSION=1.10.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless gnupg && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/sbt/sbt/releases/download/v1.10.6/sbt-1.10.6.tgz" -o /sbt.tgz && \
    tar -xzf /sbt.tgz -C /opt/ && rm /sbt.tgz && ln -sf /opt/sbt/bin/sbt /usr/local/bin/sbt

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/sbt /var/cache/sbt /home/sbt

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/sbt /opt/sbt
COPY --from=downloader /usr/local/bin/sbt /usr/local/bin/sbt
COPY --from=builder /app /app
COPY --from=builder /var/log/sbt /var/log/sbt
COPY --from=builder /var/cache/sbt /var/cache/sbt
COPY --from=builder /home/sbt /home/sbt
RUN useradd -r -u 65534 -g '' sbt 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENV HOME=/app
ENV SBT_HOME=/opt/sbt
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["sbt", "--version"]
ENTRYPOINT ["sbt"]
LABEL org.opencontainers.image.title="sbt" \
      org.opencontainers.image.version="1.10.6" \
      org.opencontainers.image.vendor="Scala" \
      org.opencontainers.image.description="Sovereign hardened sbt - Scala build tool" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
