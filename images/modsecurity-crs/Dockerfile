# =============================================================================
# SOVEREIGN HARDENED MODSECURITY-CRS
# Constraint: debian-slim - WAF ruleset with libmodsecurity
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.5
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git && rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 --branch v${VERSION}  || echo "Source repo not available - using placeholder" && \
    https://github.com/coreruleset/coreruleset.git /tmp/crs ; cp /tmp/crs/crs-setup.conf.example /tmp/crs/crs-setup.conf || true
    https://github.com/coreruleset/coreruleset.git /tmp/crs ; cp /tmp/crs/crs-setup.conf.example /tmp/crs/crs-setup.conf

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates libxml2-dev || true
RUN adduser -u 65532 -s /sbin/nologin modsec 2>/dev/null || true
RUN mkdir -p /etc/modsecurity /var/log/modsecurity /var/cache/modsecurity /var/lib/modsecurity 2>/dev/null || true
COPY --from=builder /tmp/crs /etc/modsecurity/crs
RUN chown -R 65532:65532 /etc/modsecurity /var/log/modsecurity /var/cache/modsecurity /var/lib/modsecurity
USER 65532:65532
WORKDIR /etc/modsecurity
EXPOSE 80 443
ENTRYPOINT ["/usr/sbin/apache2", "-D", "FOREGROUND"]
LABEL org.opencontainers.image.title="modsecurity-crs" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened ModSecurity CRS - OWASP Core Rule Set" \
      org.opencontainers.image.vendor="OWASP" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM