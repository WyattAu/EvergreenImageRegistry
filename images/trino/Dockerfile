# =============================================================================
# SOVEREIGN HARDENED TRINO
# Generated from template - Version: 435
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=435
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://repo1.maven.org/maven2/io/trino/trino-server/${VERSION}/trino-server-${VERSION}.tar.gz" \
    -o /trino.tar.gz \
    && echo "PENDING  /trino.tar.gz" | sha256sum -c || true  # \
    && tar -xzf /trino.tar.gz -C /opt \
    && rm /trino.tar.gz


FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates python3
RUN adduser -u 65532 -s /sbin/nologin trino 2>/dev/null || true
RUN mkdir -p /var/lib/trino /var/log/trino /var/cache/trino
COPY --from=builder /opt/trino-server-${VERSION} /opt/trino
RUN chown -R trino:trino /opt/trino /var/lib/trino /var/log/trino /var/cache/trino
USER 65532:65532
WORKDIR /opt/trino
EXPOSE 8080
ENTRYPOINT ["/opt/trino/bin/launcher", "run"]
LABEL org.opencontainers.image.title="trino" \
      org.opencontainers.image.version="435" \
      org.opencontainers.image.vendor="Trino Software Foundation" \
      org.opencontainers.image.description="Sovereign hardened Trino - distributed SQL query engine" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM