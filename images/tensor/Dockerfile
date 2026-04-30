FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=2.17.0
ARG GITHUB_TOKEN
RUN apk add --no-cache python3 py3-pip ca-certificates || true
RUN pip install --no-cache-dir tensorboard==${VERSION} || true
RUN addgroup -S -g 10000 tensorboard 2>/dev/null || true && \
    adduser -u 65532 -G tensorboard -D -h /app -s /bin/false tensorboard 2>/dev/null || true
RUN mkdir -p /app /app/logs /var/log/tensorboard 2>/dev/null || true
RUN chown -R 65532:65532 /app /app/logs /var/log/tensorboard 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6006
ENTRYPOINT ["tensorboard"]
CMD ["--logdir=/app/logs", "--bind_all", "--port=6006"]
LABEL org.opencontainers.image.title="tensor" \
      org.opencontainers.image.description="TensorBoard - ML experiment visualization and monitoring tool" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="TensorFlow" \
      org.opencontainers.image.source="https://github.com/tensorflow/tensorboard" \
      sovereign.image.tier="2" \
      sovereign.image.category="ml" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM
