FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=2.20.0
ARG TARGETARCH
RUN apk add --no-cache python3 py3-pip ca-certificates || true && \
    pip install --no-cache-dir tensorboard==${VERSION} || true && \
    addgroup -S -g 10000 tensorboard 2>/dev/null || true && \
    adduser -u 65532 -G tensorboard -D -h /app -s /bin/false tensorboard 2>/dev/null || true && \
    mkdir -p /app /app/logs /var/log/tensorboard 2>/dev/null || true && \
    chown -R 65532:65532 /app /app/logs /var/log/tensorboard 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6006

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:6006/ || exit 1
ENTRYPOINT ["tensorboard"]
CMD ["--logdir=/app/logs", "--bind_all", "--port=6006"]
LABEL org.opencontainers.image.title="tensor" \
      org.opencontainers.image.description="TensorBoard - ML experiment visualization and monitoring tool" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="TensorFlow" \
      org.opencontainers.image.source="https://github.com/tensorflow/tensorboard" \
      evergreen.image.tier="2" \
      evergreen.image.category="ml" \
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
