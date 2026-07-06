ARG VERSION=1.32.0
ARG SHIM_VERSION=v1.2.0

FROM vaultwarden/server:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

# Use Debian (same as upstream) to ensure shared lib compatibility
FROM debian:bookworm-slim
COPY --from=shim /shim /usr/local/bin/shim

RUN apt-get update && apt-get install -y --no-install-recommends libssl3 ca-certificates libmariadb3 libpq5 && rm -rf /var/lib/apt/lists/* && mkdir -p /data && groupadd -g 65532 app && useradd -u 65532 -g app -d /data -s /usr/sbin/nologin app && \
    chown -R app:app /data

COPY --from=upstream /vaultwarden /vaultwarden
COPY --from=upstream /web-vault /web-vault
RUN chmod +x /vaultwarden

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true" \
    ROCKET_ADDRESS=0.0.0.0 \
    ROCKET_PORT=80 \
    DATA_FOLDER=/data

EXPOSE 80 9101
VOLUME /data
WORKDIR /data

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

LABEL org.opencontainers.image.title="vaultwarden" \
      org.opencontainers.image.description="Vaultwarden - non-root on Debian" \
      org.opencontainers.image.version="${VERSION}" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="debian-slim"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
