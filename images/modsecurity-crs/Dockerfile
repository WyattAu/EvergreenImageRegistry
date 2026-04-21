# =============================================================================
# SOVEREIGN HARDENED MODSECURITY-CRS
# Constraint: debian-slim - WAF ruleset with libmodsecurity
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN git clone --depth 1 --branch v${VERSION} \
    https://github.com/coreruleset/coreruleset.git /tmp/crs \
    && cp /tmp/crs/crs-setup.conf.example /tmp/crs/crs-setup.conf

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmodsecurity3 libapache2-mod-security2 ca-certificates libxml2-dev \
    libpcre3-dev libcurl4-openssl-dev libyajl-dev libgeoip-dev && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin modsec 2>/dev/null || true
RUN mkdir -p /etc/modsecurity /var/log/modsecurity /var/cache/modsecurity /var/lib/modsecurity
COPY --from=builder /tmp/crs /etc/modsecurity/crs
RUN chown -R 65534:65534 /etc/modsecurity /var/log/modsecurity /var/cache/modsecurity /var/lib/modsecurity
USER 65534:65534
WORKDIR /etc/modsecurity
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["test", "-f", "/etc/modsecurity/crs/crs-setup.conf"]
ENTRYPOINT ["/usr/sbin/apache2", "-D", "FOREGROUND"]
LABEL org.opencontainers.image.title="modsecurity-crs" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened ModSecurity CRS - OWASP Core Rule Set" \
      org.opencontainers.image.vendor="OWASP" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
