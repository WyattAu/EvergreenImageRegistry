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
        curl="7.88.1-*" \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/gitbucket/gitbucket/releases/download/v${VERSION}/gitbucket.war" -o /tmp/gitbucket.war

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless="17.*" \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd -r -g 65534 gitbucket && useradd -r -u 65534 -g gitbucket -d /opt/gitbucket -s /usr/sbin/nologin gitbucket
RUN mkdir -p /opt/gitbucket /var/log/gitbucket /var/data/gitbucket && \
    chown -R 65534:65534 /opt/gitbucket /var/log/gitbucket /var/data/gitbucket
COPY --from=builder /tmp/gitbucket.war /opt/gitbucket/gitbucket.war
USER 65534:65534
ENV GITBUCKET_HOME="/var/data/gitbucket"
WORKDIR /opt/gitbucket
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:8080/"]
CMD ["java", "-jar", "/opt/gitbucket/gitbucket.war"]
LABEL org.opencontainers.image.title="gitbucket" \
      org.opencontainers.image.description="GitBucket - Scala-based Git platform" \
      org.opencontainers.image.version="4.43.0" \
      org.opencontainers.image.vendor="GitBucket" \
      org.opencontainers.image.source="https://github.com/gitbucket/gitbucket" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
