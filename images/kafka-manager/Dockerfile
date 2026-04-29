FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/yahoo/CMAK/releases/download/${VERSION}/cmak-${VERSION}.zip -o cmak.zip && || true
    unzip cmak.zip -d /opt/cmak && rm cmak.zip

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl 
RUN adduser -u 65532 -s /bin/false cmak 2>/dev/null || true
RUN mkdir -p /opt/cmak/logs /var/log/cmak /var/cache/cmak 2>/dev/null || true
COPY --from=builder /opt/cmak /opt/cmak
USER 65532:65532
WORKDIR /opt/cmak
EXPOSE 9000
ENTRYPOINT ["/opt/cmak/bin/cmak"]
LABEL org.opencontainers.image.title="kafka-manager" \
      org.opencontainers.image.description="Sovereign hardened CMAK (Kafka Manager) - Apache Kafka management tool" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Yahoo" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="messaging" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
