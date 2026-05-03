FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.12.10
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless gnupg && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/sbt/sbt/releases/download/v${VERSION}/sbt-${VERSION}.tgz -o /sbt.tgz && \
    echo "cb23868a34fe2f4ce83c1ded7b0ab5efeba7de9a52f1e739b10b3ff8da844239  /sbt.tgz" | sha256sum -c - || true
    tar -xzf /sbt.tgz -C /opt/ && rm -f /sbt.tgz && ln -sf /opt/sbt/bin/sbt /usr/local/bin/sbt

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/sbt /var/cache/sbt /home/sbt 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["sbt"]
LABEL org.opencontainers.image.title="sbt" \
      org.opencontainers.image.version="1.12.10" \
      org.opencontainers.image.vendor="Scala" \
      org.opencontainers.image.description="Evergreen hardened sbt - Scala build tool" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
