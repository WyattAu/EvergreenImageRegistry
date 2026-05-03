FROM docker.io/matrixdotorg/complement@sha256:5193dd102a7cdcf93ebc6d5ac3a5f5f473ca9c189a90fb3df5bd0adb6b93ddbc AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates || true && \
    adduser -D -u 65532 complement 2>/dev/null || true && \
    mkdir -p /app /var/log/complement 2>/dev/null || true
COPY --from=upstream /complement /usr/local/bin/complement
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9004

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9004/ || exit 1
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
