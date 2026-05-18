ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=2.4.0
ARG TARGETARCH
RUN apk add --no-cache python3 py3-pip ca-certificates build-base || true && \
    pip install --no-cache-dir matrix-synapse==${VERSION} || true && \
    mkdir -p /etc/synapse /var/lib/synapse /var/log/synapse 2>/dev/null || true && \
    addgroup -S -g 10000 synapse 2>/dev/null || true && \
    adduser -u 65532 -G synapse -D -h /app -s /bin/false synapse 2>/dev/null || true && \
    chown -R 65532:65532 /var/lib/synapse /var/log/synapse 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8008
ENV SYNAPSE_CONFIG_PATH="/etc/synapse/homeserver.yaml"

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8008/ || exit 1
ENTRYPOINT ["synapse"]
CMD ["--config-path", "/etc/synapse/homeserver.yaml"]
LABEL org.opencontainers.image.title="chat-server" \
      org.opencontainers.image.description="Matrix homeserver (Synapse) - Python-based Matrix server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="element-hq" \
      org.opencontainers.image.source="https://github.com/element-hq/synapse" \
      evergreen.image.tier="2" \
      evergreen.image.category="chat" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
