ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base
COPY --from=ghcr.io/wyattau/evergreenshim/health-shim:v2.0.0 /shim /usr/local/bin/shim
ARG VERSION=3.12
RUN apk add --no-cache python3
USER 65532:65532
WORKDIR /app
EXPOSE 9101
LABEL evergreen.entrypoint.pattern="shell"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9101"]
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "python3"]
LABEL org.opencontainers.image.title="python-slim" \
      org.opencontainers.image.source="https://github.com/python/cpython" \
      org.opencontainers.image.version="3.12" \
      org.opencontainers.image.description="Python slim base image - hardened wolfi" \
      evergreen.base.image="wolfi"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="standard"
