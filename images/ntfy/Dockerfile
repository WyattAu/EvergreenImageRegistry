ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.11.0
ARG TARGETARCH
RUN mkdir -p /usr/local/bin/ntfy || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/binwiederhier/ntfy/releases/download/v${VERSION}/ntfy_${VERSION}_linux_${TARGETARCH}.tar.gz" \
    -o /tmp/ntfy.tar.gz && \
    case ${TARGETARCH} in \
        amd64) EXPECTED_SHA="61722868e2ace31f736e2b9be8ada1b42d0c2e62d0e785252fdaf482b0a677ed" ;; \
        arm64) EXPECTED_SHA="02f742c5dd00906a28ebed3d1cb1e1aeb551ebe7789271ee3d28ae2dcc876e4c" ;; \
        *) EXPECTED_SHA="" ;; \
    esac && \
    echo "${EXPECTED_SHA}  /tmp/ntfy.tar.gz" | sha256sum -c && \
    tar -xzf /tmp/ntfy.tar.gz -C /tmp && \
    mv /tmp/ntfy /usr/local/bin/ntfy && \
    chmod +x /usr/local/bin/ntfy && \
    strip /usr/local/bin/ntfy
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /usr/local/bin/ntfy /usr/local/bin/ntfy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/shim", "run"]
CMD ["-c", "/usr/local/bin/ntfy", "--", "serve"]
LABEL org.opencontainers.image.title="ntfy" \
      org.opencontainers.image.description="ntfy - push notification service" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ntfy" \
      org.opencontainers.image.source="https://github.com/binwiederhier/ntfy" \
      evergreen.image.tier="2" \
      evergreen.image.category="notifications" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
