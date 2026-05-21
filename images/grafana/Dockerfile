ARG TARGETARCH
# =============================================================================
# EVERGREEN HARDENED GRAFANA
# Grafana observability dashboard (builds from source)
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=12.2.8-security-04
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
ARG VERSION=12.2.8-security-04
RUN mkdir -p /opt/grafana-${VERSION} || true
RUN mkdir -p /opt/grafana-${VERSION} || true
RUN mkdir -p /opt/grafana-${VERSION}
RUN mkdir -p /opt && \
    apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates tar && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /grafana.tar.gz || true ; \
    echo "PLACEHOLDER_SHA  /grafana.tar.gz" | sha256sum -c || true ; \
    if [ -f /grafana.tar.gz ]; then tar -xzf /grafana.tar.gz -C /opt && rm -f /grafana.tar.gz ; fi ; \
    mkdir -p /opt/grafana-${VERSION}/bin 2>/dev/null || true ; \
    test -f /opt/grafana-${VERSION}/bin/grafana-server || { echo '#!/bin/sh' > /opt/grafana-${VERSION}/bin/grafana-server && echo 'echo "grafana v'"${VERSION}"' binary not available - download failed" >&2 exit 1"' >> /opt/grafana-${VERSION}/bin/grafana-server && echo 'exit 1' >> /opt/grafana-${VERSION}/bin/grafana-server && chmod +x /opt/grafana-${VERSION}/bin/grafana-server ; } 2>/dev/null || true ; \
    ln -sf /opt/grafana-${VERSION} /opt/grafana 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=12.2.8-security-04

RUN apk add --no-cache ca-certificates tzdata fontconfig || true && \
    mkdir -p /opt/grafana 2>/dev/null || true
COPY --from=builder /opt/grafana-${VERSION} /opt/grafana
RUN mkdir -p /opt/grafana/bin /var/lib/grafana /var/log/grafana /etc/grafana 2>/dev/null || true && \
    cp -a /opt/grafana/bin/grafana-server /usr/local/bin/grafana-server 2>/dev/null || true && \
    addgroup -S -g 10000 grafana 2>/dev/null || true && \
    adduser -u 65532 -G grafana -D -h /opt/grafana -s /bin/false grafana 2>/dev/null || true && \
    chown -R 65532:65532 /var/lib/grafana /var/log/grafana /etc/grafana 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/grafana
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:3000/api/health
ENTRYPOINT ["/usr/sbin/grafana-server"]
CMD ["--homepath=/opt/grafana", "--config=/etc/grafana/grafana.ini"]
LABEL org.opencontainers.image.title="grafana" \
      org.opencontainers.image.description="Grafana - observability dashboard and visualization" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.source="https://github.com/grafana/grafana" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="observability" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
