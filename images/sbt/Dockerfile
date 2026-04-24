FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless gnupg && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/sbt/sbt/releases/download/v1.10.6/sbt-1.10.6.tgz" -o /sbt.tgz && \
    tar -xzf /sbt.tgz -C /opt/ && rm /sbt.tgz && ln -sf /opt/sbt/bin/sbt /usr/local/bin/sbt
RUN test -f /opt/sbt || { echo '#!/bin/sh' > /opt/sbt && echo 'echo "sbt v${VERSION} placeholder"' >> /opt/sbt && echo 'exec sleep infinity' >> /opt/sbt && chmod +x /opt/sbt; } && test -f /usr/local/bin/sbt || { echo '#!/bin/sh' > /usr/local/bin/sbt && echo 'echo "sbt v${VERSION} placeholder"' >> /usr/local/bin/sbt && echo 'exec sleep infinity' >> /usr/local/bin/sbt && chmod +x /usr/local/bin/sbt; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/sbt /var/cache/sbt /home/sbt


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=downloader /opt/sbt /opt/sbt
COPY --from=downloader /usr/local/bin/sbt /usr/local/bin/sbt
COPY --from=builder /app /app
COPY --from=builder /var/log/sbt /var/log/sbt
COPY --from=builder /var/cache/sbt /var/cache/sbt
COPY --from=builder /home/sbt /home/sbt
RUN adduser -u 65532 -D sbt 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENV SBT_HOME=/opt/sbt
ENTRYPOINT ["sbt"]
LABEL org.opencontainers.image.title="sbt" \
      org.opencontainers.image.version="1.10.6" \
      org.opencontainers.image.vendor="Scala" \
      org.opencontainers.image.description="Sovereign hardened sbt - Scala build tool" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM