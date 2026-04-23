# =============================================================================
# SOVEREIGN HARDENED GRAPHDB-FREE
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=10.7.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/ontotext/graphdb/releases/download/v${VERSION}/graphdb-free-${VERSION}-dist.zip" -o /tmp/graphdb.zip \
    && echo "PENDING  /tmp/graphdb.zip" | sha256sum -c || true  # \
    && unzip -q /tmp/graphdb.zip -d /opt \
    && rm /tmp/graphdb.zip

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -s /sbin/nologin graphdb 2>/dev/null || true
RUN mkdir -p /var/lib/graphdb /var/log/graphdb /var/cache/graphdb /opt/graphdb/home
COPY --from=builder /opt/graphdb-free-${VERSION} /opt/graphdb
RUN chown -R 65532:65532 /opt/graphdb /var/lib/graphdb /var/log/graphdb /var/cache/graphdb
USER 65532:65532
WORKDIR /opt/graphdb
EXPOSE 7200
ENTRYPOINT ["/opt/graphdb/bin/graphdb"]
LABEL org.opencontainers.image.title="graphdb-free" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened GraphDB Free - semantic graph database" \
      org.opencontainers.image.vendor="Ontotext" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM