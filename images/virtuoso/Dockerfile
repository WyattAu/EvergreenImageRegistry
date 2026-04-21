# =============================================================================
# SOVEREIGN HARDENED VIRTUOSO
# Constraint: debian-slim - native package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.2.12
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg2 && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://virtuoso.openlinksw.com/data/virtuoso_abikey.asc" | gpg --dearmor -o /usr/share/keyrings/virtuoso-keyring.gpg 2>/dev/null || true \
    && echo "deb [signed-by=/usr/share/keyrings/virtuoso-keyring.gpg] https://packages.virtuoso.opensourcedatabases.org/virtuoso/deb bookworm main" > /etc/apt/sources.list.d/virtuoso.list 2>/dev/null || true

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    virtuoso-opensource virtuoso-opensource-7 ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin virtuoso 2>/dev/null || true
RUN mkdir -p /var/lib/virtuoso /var/log/virtuoso /var/cache/virtuoso
RUN chown -R 65534:65534 /var/lib/virtuoso /var/log/virtuoso /var/cache/virtuoso
USER 65534:65534
WORKDIR /var/lib/virtuoso
EXPOSE 1111 8890
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8890/sparql"]
ENTRYPOINT ["virtuoso-t", "-f", "-c", "/etc/virtuoso/virtuoso.ini"]
LABEL org.opencontainers.image.title="virtuoso" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Virtuoso - universal RDF/graph database" \
      org.opencontainers.image.vendor="OpenLink Software" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
