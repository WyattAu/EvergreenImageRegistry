ARG VERSION=26.6.2

FROM quay.io/keycloak/keycloak:${VERSION}

FROM ghcr.io/wyattau/evergreenshim/health-shim:v1.3.0 AS shim

FROM quay.io/keycloak/keycloak:${VERSION}
USER 0
COPY --from=shim /shim /usr/local/bin/shim
USER 1000

ENV SHIM_METRICS_ENABLED="true"     KC_HTTP_ENABLED="true"     KC_HOSTNAME_STRICT="false"

EXPOSE 8080 9101

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5   CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

LABEL org.opencontainers.image.title="keycloak"       org.opencontainers.image.description="Keycloak - upstream repack with health shim, non-root"       evergreen.image.tier="critical"       evergreen.constraint.nonroot="true"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
LABEL evergreen.entrypoint.pattern="chainguard-repack"
STOPSIGNAL SIGTERM
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
