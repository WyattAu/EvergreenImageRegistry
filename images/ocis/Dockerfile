# =============================================================================
# EVERGREEN HARDENED OCIS
# Wolfi-base with init wrapper
# =============================================================================
ARG VERSION=8.0.4
ARG SHIM_VERSION=v1.1.0

FROM --platform=linux/amd64 cgr.dev/chainguard/wolfi-base@sha256:0b5fd36c9f36ecc95bf6dbe049fe0a211410e1ba8a9801db0fbe25c7561d81c1 AS downloader
ARG VERSION
RUN apk add --no-cache wget ca-certificates && \
    wget -q "https://github.com/owncloud/ocis/releases/download/v${VERSION}/ocis-${VERSION}-linux-amd64" -O /ocis && \
    chmod +x /ocis

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM --platform=linux/amd64 cgr.dev/chainguard/wolfi-base@sha256:0b5fd36c9f36ecc95bf6dbe049fe0a211410e1ba8a9801db0fbe25c7561d81c1
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim
RUN apk add --no-cache bash ca-certificates && \
    adduser -u 65532 -D ocis 2>/dev/null || true && \
    mkdir -p /etc/ocis /var/lib/ocis && \
    chown -R 65532:65532 /etc/ocis /var/lib/ocis
COPY --from=downloader /ocis /usr/local/bin/ocis
RUN chmod +x /usr/local/bin/ocis

# Create init wrapper script
RUN printf '#!/bin/sh\nexport OCIS_CONFIG_DIR=/etc/ocis\nif [ ! -f /etc/ocis/ocis.yaml ]; then\n  /usr/local/bin/ocis init\nfi\nexec /usr/local/bin/ocis "$@"\n' > /usr/local/bin/ocis-wrapper.sh && \
    chmod +x /usr/local/bin/ocis-wrapper.sh

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true" OCIS_CONFIG_DIR=/etc/ocis
WORKDIR /
EXPOSE 9200 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9200"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/ocis-wrapper.sh"]
CMD ["server"]
LABEL org.opencontainers.image.title="ocis" \
      org.opencontainers.image.description="ownCloud Infinite Scale - collaboration platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ownCloud" \
      org.opencontainers.image.source="https://github.com/owncloud/ocis"
LABEL evergreen.base.image="wolfi" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
