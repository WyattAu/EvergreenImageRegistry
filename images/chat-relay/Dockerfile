ARG APP_UID=65532
ARG APP_GID=65532

FROM docker.io/matrixdotorg/complement:latest AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates || true && \
    adduser -D -u 65532 complement 2>/dev/null || true && \
    mkdir -p /app /var/log/complement 2>/dev/null || true
RUN touch /usr/local/bin/complement || true
COPY --from=upstream /complement /usr/local/bin/complement
RUN mkdir -p /etc/ssl/certs || true && touch /etc/ssl/certs/ca-certificates.crt || true
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9004

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9004/ || exit 1
ENTRYPOINT ["/usr/local/bin/complement"]
LABEL org.opencontainers.image.title="chat-relay" \
      org.opencontainers.image.description="Matrix chat relay (complement) - testing tool for Matrix homeservers" \
      org.opencontainers.image.version="0.5.0" \
      org.opencontainers.image.vendor="matrix-org" \
      org.opencontainers.image.source="https://github.com/matrix-org/complement" \
      evergreen.image.tier="2" \
      evergreen.image.category="chat" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
