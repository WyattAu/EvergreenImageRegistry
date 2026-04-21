# =============================================================================
# SOVEREIGN HARDENED FIREBIRD
# Constraint: debian-slim - native database package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.5
ARG BUILD_DATE

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    firebird4.0-server firebird4.0-utils ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin firebird 2>/dev/null || true
RUN mkdir -p /var/lib/firebird /var/log/firebird /var/cache/firebird
RUN chown -R 65534:65534 /var/lib/firebird /var/log/firebird /var/cache/firebird
USER 65534:65534
WORKDIR /var/lib/firebird
EXPOSE 3050
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["gsutil", "-z", "localhost:/var/lib/firebird/test.fdb"]
ENTRYPOINT ["firebird"]
LABEL org.opencontainers.image.title="firebird" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Firebird - SQL relational database" \
      org.opencontainers.image.vendor="FirebirdSQL" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
