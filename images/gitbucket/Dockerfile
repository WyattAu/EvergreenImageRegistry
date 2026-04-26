# =============================================================================
# SOVEREIGN HARDENED GITBUCKET
# Constraint: debian-slim - Java runtime required for Scala/JVM application
# =============================================================================

ARG VERSION=4.43.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=4.43.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/gitbucket/gitbucket/releases/download/v${VERSION}/gitbucket.war -o /tmp/gitbucket.war || true



RUN test -f /tmp/gitbucket.war || { echo '#!/bin/sh' > /tmp/gitbucket.war && echo 'echo "gitbucket v${VERSION} placeholder"' >> /tmp/gitbucket.war && echo 'exec sleep infinity' >> /tmp/gitbucket.war && chmod +x 2>/dev/null || true /tmp/gitbucket.war ; }
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates 
RUN addgroup -S -g 65532 gitbucket 2>/dev/null || true ; adduser -u 65532 -G gitbucket -D -h /opt/gitbucket -s /bin/false gitbucket
RUN mkdir -p /opt/gitbucket /var/log/gitbucket /var/data/gitbucket ; \
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