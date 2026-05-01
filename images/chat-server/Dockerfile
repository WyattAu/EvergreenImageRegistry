FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=2.4.0
ARG GITHUB_TOKEN
RUN apk add --no-cache python3 py3-pip ca-certificates build-base || true && \
    pip install --no-cache-dir matrix-synapse==${VERSION} || true && \
    mkdir -p /etc/synapse /var/lib/synapse /var/log/synapse 2>/dev/null || true
RUN addgroup -S -g 10000 synapse 2>/dev/null || true && \
    adduser -u 65532 -G synapse -D -h /app -s /bin/false synapse 2>/dev/null || true && \
    chown -R 65532:65532 /var/lib/synapse /var/log/synapse 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8008
ENV SYNAPSE_CONFIG_PATH="/etc/synapse/homeserver.yaml"
ENTRYPOINT ["synapse"]
CMD ["--config-path", "/etc/synapse/homeserver.yaml"]
LABEL org.opencontainers.image.title="chat-server" \
      org.opencontainers.image.description="Matrix homeserver (Synapse) - Python-based Matrix server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="element-hq" \
      org.opencontainers.image.source="https://github.com/element-hq/synapse" \
      sovereign.image.tier="2" \
      sovereign.image.category="chat" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM
