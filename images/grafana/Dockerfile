ARG VERSION=11.2.0
ARG SHIM_VERSION=v2.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    arch=$(case ${TARGETARCH} in amd64) echo "amd64";; arm64) echo "arm64";; *) echo "amd64";; esac) && \
    curl -fsSL "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-${arch}.tar.gz" -o /tmp/grafana.tar.gz && \
    tar -xzf /tmp/grafana.tar.gz -C /tmp && \
    mkdir -p /gf/bin /gf/conf /gf/public /var/lib/grafana /var/log/grafana /etc/grafana && \
    cp /tmp/grafana-v${VERSION}/bin/grafana /gf/bin/ && \
    cp /tmp/grafana-v${VERSION}/bin/grafana-server /gf/bin/ && \
    cp /tmp/grafana-v${VERSION}/bin/grafana-cli /gf/bin/ && \
    cp -r /tmp/grafana-v${VERSION}/conf/* /gf/conf/ && \
    cp -r /tmp/grafana-v${VERSION}/public/* /gf/public/ && \
    chmod -R 0777 /gf /var/lib/grafana /var/log/grafana /etc/grafana

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /gf /usr/share/grafana
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /var/lib/grafana /var/lib/grafana
COPY --from=downloader /var/log/grafana /var/log/grafana

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true" \
    GF_PATHS_DATA=/var/lib/grafana \
    GF_PATHS_LOGS=/var/log/grafana \
    GF_PATHS_HOME=/usr/share/grafana \
    GF_SECURITY_ADMIN_PASSWORD=admin \
    PATH="/usr/share/grafana/bin:${PATH}"

EXPOSE 3000 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/share/grafana/bin/grafana server --homepath=/usr/share/grafana"]

LABEL org.opencontainers.image.title="grafana" \
      org.opencontainers.image.description="Grafana - binary extraction, scratch, non-root" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distroless="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
