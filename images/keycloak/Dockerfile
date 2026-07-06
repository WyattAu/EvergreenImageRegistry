FROM quay.io/keycloak/keycloak:26.0@sha256:09a381c715ab0b111835b70f2905955274843a219c6f27efb348e4d9f4086858

FROM ghcr.io/wyattau/evergreenshim/health-shim:v1.3.0 AS shim

FROM quay.io/keycloak/keycloak:26.0@sha256:09a381c715ab0b111835b70f2905955274843a219c6f27efb348e4d9f4086858
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
STOPSIGNAL SIGTERM
