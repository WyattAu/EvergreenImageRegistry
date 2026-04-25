# =============================================================================
# SOVEREIGN HARDENED FIREBIRD
# Constraint: debian-slim - native database package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.5
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates || true
RUN adduser -u 65532 -s /sbin/nologin firebird 2>/dev/null || true
RUN mkdir -p /var/lib/firebird /var/log/firebird /var/cache/firebird 2>/dev/null || true
RUN chown -R 65532:65532 /var/lib/firebird /var/log/firebird /var/cache/firebird
USER 65532:65532
WORKDIR /var/lib/firebird
EXPOSE 3050
ENTRYPOINT ["firebird"]
LABEL org.opencontainers.image.title="firebird" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Firebird - SQL relational database" \
      org.opencontainers.image.vendor="FirebirdSQL" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM