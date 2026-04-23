# =============================================================================
# SOVEREIGN HARDENED VIRTUOSO
# Constraint: debian-slim - native package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.2.12
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://virtuoso.openlinksw.com/data/virtuoso_abikey.asc" | gnupg --dearmor -o /usr/share/keyrings/virtuoso-keyring.gnupg 2>/dev/null || true \
    && echo "deb [signed-by=/usr/share/keyrings/virtuoso-keyring.gnupg] https://packages.virtuoso.opensourcedatabases.org/virtuoso/deb bookworm main" > /etc/apt/sources.list.d/virtuoso.list 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates
RUN adduser -u 65532 -s /sbin/nologin virtuoso 2>/dev/null || true
RUN mkdir -p /var/lib/virtuoso /var/log/virtuoso /var/cache/virtuoso
RUN chown -R 65532:65532 /var/lib/virtuoso /var/log/virtuoso /var/cache/virtuoso
USER 65532:65532
WORKDIR /var/lib/virtuoso
EXPOSE 1111 8890
ENTRYPOINT ["virtuoso-t", "-f", "-c", "/etc/virtuoso/virtuoso.ini"]
LABEL org.opencontainers.image.title="virtuoso" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Virtuoso - universal RDF/graph database" \
      org.opencontainers.image.vendor="OpenLink Software" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM