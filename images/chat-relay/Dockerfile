FROM docker.io/matrixdotorg/complement:latest AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates || true && \
    adduser -D -u 65532 complement 2>/dev/null || true && \
    mkdir -p /app /var/log/complement 2>/dev/null || true
COPY --from=upstream /complement /usr/local/bin/complement
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9004
ENTRYPOINT ["/usr/local/bin/complement"]
LABEL org.opencontainers.image.title="chat-relay" \
      org.opencontainers.image.description="Matrix chat relay (complement) - testing tool for Matrix homeservers" \
      org.opencontainers.image.version="0.5.0" \
      org.opencontainers.image.vendor="matrix-org" \
      org.opencontainers.image.source="https://github.com/matrix-org/complement" \
      sovereign.image.tier="2" \
      sovereign.image.category="chat" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="tcp"
EXPOSE 9101
STOPSIGNAL SIGTERM
