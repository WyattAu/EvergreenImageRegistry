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
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://cdn.crate.io/downloads/releases/cratedb/cratedb-${VERSION}.tar.gz" -o /tmp/crate.tar.gz \
    && echo "PENDING  /tmp/crate.tar.gz" | sha256sum -c - \
    && tar -xzf /tmp/crate.tar.gz -C /opt \
    && rm /tmp/crate.tar.gz

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless python3 && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin crate 2>/dev/null || true
RUN mkdir -p /var/lib/crate /var/log/crate /var/cache/crate
COPY --from=builder /opt/crate-${VERSION} /opt/crate
RUN chown -R 65534:65534 /opt/crate /var/lib/crate /var/log/crate /var/cache/crate
USER 65534:65534
WORKDIR /opt/crate
EXPOSE 4200 5432
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:4200"]
ENTRYPOINT ["/opt/crate/bin/crate"]
LABEL org.opencontainers.image.title="crate" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened CrateDB - distributed SQL database" \
      org.opencontainers.image.vendor="Crate.io" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
