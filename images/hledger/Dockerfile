ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.52
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/simonmichael/hledger/releases/download/${VERSION}/hledger-linux-x64.tar.gz -o /hledger.tar.gz && \
    echo "153e1e69696d5e75b2a13bf23983a0355c35999db713910615c6a536a4cd0a41  /hledger.tar.gz" | sha256sum -c ;  \
    tar -xzf /hledger.tar.gz -C /usr/local/bin/ && rm -f /hledger.tar.gz && \
    strip /usr/local/bin/hledger&& chmod +x /usr/local/bin/hledger


ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /usr/local/bin/hledger /hledger
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/hledger"]
LABEL org.opencontainers.image.title="hledger" \
      org.opencontainers.image.description="hledger container image" \
      org.opencontainers.image.version="1.52" \
      org.opencontainers.image.vendor="hledger" \
      org.opencontainers.image.source="https://github.com/simonmichael/hledger" \
      evergreen.image.tier="2" \
      evergreen.image.category="business-finance" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
