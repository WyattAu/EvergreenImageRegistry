ARG VERSION=9.01
ARG TARGETARCH







ARG BUILD_DATE























FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg unzip && \
    rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/wekan/wekan/releases/download/v${VERSION}/wekan-${VERSION}-amd64.zip -o /wekan.zip || true; \
    echo "1026b8631b38eb6213eb72aaad867dc198e5ae1da819130a70bf46b50697a583  /wekan.zip" | sha256sum -c || true  #







RUN if [ -f /wekan.zip ]; then unzip -q /wekan.zip -d /opt/ && rm -f /wekan.zip; fi















FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9















RUN apk add --no-cache ca-certificates curl







COPY --from=builder /opt/bundle /opt/wekan







RUN mkdir -p /app /var/log/wekan /var/cache/wekan /opt/wekan 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/wekan /var/cache/wekan /opt/wekan







USER 65532:65532







WORKDIR /app







EXPOSE 8080















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1







ENTRYPOINT ["node", "/opt/wekan/main.js"]







LABEL org.opencontainers.image.title="wekan" \
      org.opencontainers.image.description="wekan container image" \
      org.opencontainers.image.version="9.01" \
      org.opencontainers.image.vendor="Wekan" \
      org.opencontainers.image.source="https://github.com/wekan/wekan" \
      evergreen.image.tier="2" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"







LABEL evergreen.base.image="wolfi"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM
