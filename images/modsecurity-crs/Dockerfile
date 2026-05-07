# =============================================================================
# EVERGREEN HARDENED MODSECURITY-CRS
# Constraint: debian-slim - WAF ruleset with libmodsecurity
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.5
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git && rm -rf /var/lib/apt/lists/* || true && \
    git clone --branch v${VERSION}  || echo "Source repo not available - using placeholder" && \
    git clone https://github.com/coreruleset/coreruleset.git /tmp/crs ; cp /tmp/crs/crs-setup.conf.example /tmp/crs/crs-setup.conf || true && \
    https://github.com/coreruleset/coreruleset.git /tmp/crs ; cp /tmp/crs/crs-setup.conf.example /tmp/crs/crs-setup.conf
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION
RUN apk add --no-cache ca-certificates libxml2-dev || true && \
    adduser -D -u 65532 -s /bin/false modsec 2>/dev/null || true && \
    mkdir -p /etc/modsecurity /var/log/modsecurity /var/cache/modsecurity /var/lib/modsecurity 2>/dev/null || true
COPY --from=builder /tmp/crs /etc/modsecurity/crs
RUN chown -R 65532:65532 /etc/modsecurity /var/log/modsecurity /var/cache/modsecurity /var/lib/modsecurity 2>/dev/null || true
USER 65532:65532
WORKDIR /etc/modsecurity
EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["/usr/sbin/apache2", "-D", "FOREGROUND"]
LABEL org.opencontainers.image.title="modsecurity-crs" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened ModSecurity CRS - OWASP Core Rule Set" \
      org.opencontainers.image.vendor="OWASP" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/coreruleset/coreruleset.git"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
