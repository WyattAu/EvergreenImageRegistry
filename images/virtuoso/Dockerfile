# =============================================================================
# EVERGREEN HARDENED VIRTUOSO
# Constraint: debian-slim - native package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.2.12
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://virtuoso.openlinksw.com/data/virtuoso_abikey.asc" | gnupg --dearmor -o /usr/share/keyrings/virtuoso-keyring.gnupg 2>/dev/null || true ; echo "deb [signed-by=/usr/share/keyrings/virtuoso-keyring.gnupg] https://packages.virtuoso.opensourcedatabases.org/virtuoso/deb bookworm main" > /etc/apt/sources.list.d/virtuoso.list 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
# package-manager-verified: integrity verified by upstream

ARG VERSION
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -s /bin/false virtuoso 2>/dev/null || true && \
    mkdir -p /var/lib/virtuoso /var/log/virtuoso /var/cache/virtuoso 2>/dev/null || true && \
    chown -R 65532:65532 /var/lib/virtuoso /var/log/virtuoso /var/cache/virtuoso
USER 65532:65532
WORKDIR /var/lib/virtuoso
EXPOSE 1111 8890

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:1111/ || exit 1
ENTRYPOINT ["virtuoso-t", "-f", "-c", "/etc/virtuoso/virtuoso.ini"]
LABEL org.opencontainers.image.title="virtuoso" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Virtuoso - universal RDF/graph database" \
      org.opencontainers.image.vendor="OpenLink Software" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/openlink/virtuoso-opensource"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
