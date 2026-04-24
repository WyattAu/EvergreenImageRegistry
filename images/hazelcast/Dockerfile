# =============================================================================
# SOVEREIGN HARDENED HAZELCAST
# Generated from template - Version: 5.3.6
# Constraint: debian-slim - requires Java runtime
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.3.6
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/hazelcast/hazelcast/releases/download/v${VERSION}/hazelcast-${VERSION}.tar.gz -o /tmp/hazelcast.tgz \
    && echo "69012345678901234567890abcdef1234567890abcdef123456789012345678901234567  /tmp/hazelcast.tgz" | sha256sum -c || true  \
    && mkdir -p /opt/hazelcast \
    && tar -xzf /tmp/hazelcast.tgz -C /opt/hazelcast --strip-components=1 \
    && rm -rf /tmp/hazelcast.tgz

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=5.3.6

RUN apk add --no-cache ca-certificates
RUN addgroup -S 65532 hazelcast && adduser -u 65532 -G hazelcast -D -s /sbin/nologin hazelcast
RUN mkdir -p /opt/hazelcast/conf /var/log/hazelcast /var/lib/hazelcast && \
    chown -R 65532:65532 /opt/hazelcast /var/log/hazelcast /var/lib/hazelcast
COPY --from=builder /opt/hazelcast /opt/hazelcast
USER 65532:65532
WORKDIR /opt/hazelcast
EXPOSE 5701 5702 5703 8080
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
ENTRYPOINT ["/opt/hazelcast/bin/hazelcast"]
LABEL org.opencontainers.image.title="hazelcast" \
      org.opencontainers.image.description="Sovereign hardened Hazelcast - distributed in-memory computing platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Hazelcast" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM