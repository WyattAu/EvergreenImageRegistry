# =============================================================================
# SOVEREIGN HARDENED GITBUCKET
# Constraint: debian-slim - Java runtime required for Scala/JVM application
# =============================================================================

ARG VERSION=4.43.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/gitbucket/gitbucket/releases/download/v${VERSION}/gitbucket.war" -o /tmp/gitbucket.war

FROM cgr.dev/chainguard/wolfi-base:latest

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk add --no-cache ca-certificates
RUN addgroup -S -g 65532 gitbucket && adduser -u 65532 -G gitbucket -D -h /opt/gitbucket -s /sbin/nologin gitbucket
RUN mkdir -p /opt/gitbucket /var/log/gitbucket /var/data/gitbucket && \
    chown -R 65532:65532 /opt/gitbucket /var/log/gitbucket /var/data/gitbucket
COPY --from=builder /tmp/gitbucket.war /opt/gitbucket/gitbucket.war
USER 65532:65532
ENV GITBUCKET_HOME="/var/data/gitbucket"
WORKDIR /opt/gitbucket
EXPOSE 8080
CMD ["java", "-jar", "/opt/gitbucket/gitbucket.war"]
LABEL org.opencontainers.image.title="gitbucket" \
      org.opencontainers.image.description="GitBucket - Scala-based Git platform" \
      org.opencontainers.image.version="4.43.0" \
      org.opencontainers.image.vendor="GitBucket" \
      org.opencontainers.image.source="https://github.com/gitbucket/gitbucket" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM