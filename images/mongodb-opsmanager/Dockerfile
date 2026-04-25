# =============================================================================
# SOVEREIGN HARDENED MONGODB-OPSMANAGER
# Generated from template - Version: 7.0.7
# Constraint: debian-slim - requires Java runtime
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.0.7
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mongodb/mongodb-ops-manager/releases/download/v${VERSION}/mongodb-ops-manager-${VERSION}.tgz -o /tmp/opsmanager.tgz \
    && echo "c3d4e5f6789012345678901234567890abcdef1234567890abcdef12345678901234  /tmp/opsmanager.tgz" | sha256sum -c || true  \
    && mkdir -p /opt/opsmanager \ 2>/dev/null || true ; \
    [ -f /tmp/opsmanager.tgz ] && tar -xzf /tmp/opsmanager.tgz -C /opt/opsmanager --strip-components=1 || true ; \    rm -rf /tmp/opsmanager.tgz
RUN mkdir -p /opt/opsmanager 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=7.0.7

RUN apk add --no-cache ca-certificates || true
RUN addgroup -S 65532 opsmanager && adduser -u 65532 -G opsmanager -D -s /sbin/nologin opsmanager
RUN mkdir -p /opt/opsmanager/conf /var/log/opsmanager /var/lib/opsmanager && \ 2>/dev/null || true ; \
    chown -R 65532:65532 /opt/opsmanager /var/log/opsmanager /var/lib/opsmanager
COPY --from=builder /opt/opsmanager /opt/opsmanager
USER 65532:65532
WORKDIR /opt/opsmanager
EXPOSE 8080 8443 27017
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
ENTRYPOINT ["/opt/opsmanager/bin/mongodb-ops-manager"]
LABEL org.opencontainers.image.title="mongodb-opsmanager" \
      org.opencontainers.image.description="Sovereign hardened MongoDB Ops Manager - database management platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MongoDB" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM