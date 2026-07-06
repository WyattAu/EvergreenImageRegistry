ARG VERSION=1.32.0
ARG SHIM_VERSION=v1.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM vaultwarden/server:${VERSION}
COPY --from=shim /shim /usr/local/bin/shim

# Create non-root user and set permissions
RUN groupadd -g 65532 app && useradd -u 65532 -g app -d /data -s /sbin/nologin app && \
    chown -R app:app /data /web-vault /vaultwarden

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true" \
    ROCKET_ADDRESS=0.0.0.0 \
    ROCKET_PORT=80

EXPOSE 80 9101
VOLUME /data
WORKDIR /data

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

LABEL org.opencontainers.image.title="vaultwarden" \
      org.opencontainers.image.description="Vaultwarden - non-root on Debian base" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
