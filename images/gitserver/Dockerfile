ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
ARG VERSION=1.26.1
RUN mkdir -p /opt/gitserver || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates xz-utils && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL "https://dl.gitea.io/gitea/${VERSION}/gitea-${VERSION}-linux-${TARGETARCH}.xz" -o /gitea.xz 2>/dev/null ; \
    echo "92090a3f74bfc537a30d598ba45180c5b7da3064b4d17e3cd95f388da85cf4d3  /gitea.xz" | sha256sum -c ; \
    mkdir -p /opt/gitserver && if [ -f /gitea.xz ]; then tar -xJf /gitea.xz -C /opt/gitserver --strip-components=1 2>/dev/null ; rm -f /gitea.xz 2>/dev/null ; fi && \
    echo "324ffd2cc85d567ecd821ad3e19de4abe1c7f94a082b382c1453d4ca7bcf2a7b  /opt/gitserver/gitea" | sha256sum -c
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=builder /opt/gitserver /opt/gitserver
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 80 22

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="gitserver" \
      org.opencontainers.image.version="1.26.1" \
      org.opencontainers.image.vendor="Gitea" \
      org.opencontainers.image.source="https://github.com/go-gitea/gitea" \
      org.opencontainers.image.description="GitServer - lightweight git HTTP server" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
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
