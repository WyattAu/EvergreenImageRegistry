ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532















ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG TARGETARCH







ARG VERSION=2.3.0







RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/go-vikunja/vikunja/releases/download/v2.3.0/vikunja-v2.3.0-linux-${TARGETARCH}-full.zip -o /vikunja && { echo "Binary not available - download failed" >&2; exit 1; }
    echo "c37f8291698e288cd95198b52b826ffca40c3665d351041b93358e142862994d  /vikunja" | sha256sum -c  #































FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim








COPY --from=downloader /vikunja /vikunja







COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt







USER 65532:65532







WORKDIR /app







EXPOSE 3456






















HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3456"]

ENTRYPOINT ["/shim", "run"]







LABEL org.opencontainers.image.title="vikunja-api" \
      org.opencontainers.image.description="vikunja-api container image" \
      org.opencontainers.image.version="v0.24.1" \
      org.opencontainers.image.vendor="Vikunja" \
      org.opencontainers.image.source="https://github.com/go-vikunja/vikunja" \
      evergreen.image.tier="2" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms"















LABEL evergreen.base.image="scratch"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM
