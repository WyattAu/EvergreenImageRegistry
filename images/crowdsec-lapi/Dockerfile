ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader

ARG VERSION=1.7.7
ARG TARGETARCH

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates binutils && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/crowdsecurity/crowdsec/releases/download/v${VERSION}/crowdsec-release.tgz" \
    -o /crowdsec-release.tgz && \
    tar -xzf /crowdsec-release.tgz -C /tmp/ && \
    cp /tmp/crowdsec-v${VERSION}/cmd/crowdsec/crowdsec /crowdsec && \
    chmod +x /crowdsec && \
    strip --strip-all /crowdsec 2>/dev/null&& \
    rm -rf /crowdsec-release.tgz /tmp/crowdsec-v${VERSION}

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim


COPY --from=downloader /crowdsec /crowdsec

COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

WORKDIR /app

EXPOSE 8080 6060




HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]

CMD ["-c", "/crowdsec", "--", "-c /app/config.yaml -lapi"]

LABEL org.opencontainers.image.title="crowdsec-lapi"       org.opencontainers.image.version="1.7.7"       org.opencontainers.image.vendor="CrowdSecurity"       org.opencontainers.image.source="https://github.com/crowdsecurity/crowdsec"       evergreen.image.tier="1"       evergreen.image.category="security"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms" \
org.opencontainers.image.description="crowdsec-lapi container image" \
evergreen.base.image="scratch"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
