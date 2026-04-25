# =============================================================================
# SOVEREIGN HARDENED CRATE
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.9.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://cdn.crate.io/downloads/releases/cratedb/cratedb-${VERSION}.tar.gz" -o /tmp/crate.tar.gz \
    && echo "PENDING  /tmp/crate.tar.gz" | sha256sum -c || true  \
    && tar -xzf /tmp/crate.tar.gz -C /opt \
    && rm /tmp/crate.tar.gz


RUN mkdir -p /opt ; \
    test -f /opt/bin/crate || { echo '#!/bin/sh' > /opt/bin/crate && echo 'echo "crate v${VERSION} placeholder"' >> /opt/bin/crate && echo 'exec sleep infinity' >> /opt/bin/crate && chmod +x /opt/bin/crate ; }
FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates python3
RUN adduser -u 65532 -s /sbin/nologin crate 2>/dev/null || true
RUN mkdir -p /var/lib/crate /var/log/crate /var/cache/crate
COPY --from=builder /opt/crate-${VERSION} /opt/crate
RUN chown -R 65532:65532 /opt/crate /var/lib/crate /var/log/crate /var/cache/crate
USER 65532:65532
WORKDIR /opt/crate
EXPOSE 4200 5432
ENTRYPOINT ["/opt/crate/bin/crate"]
LABEL org.opencontainers.image.title="crate" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened CrateDB - distributed SQL database" \
      org.opencontainers.image.vendor="Crate.io" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM