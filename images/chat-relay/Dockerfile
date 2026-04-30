FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/matrix-org/complement/releases/download/v0.5.0/complement-linux-amd64" \
    -o /tmp/complement && \
    chmod +x /tmp/complement && \
    strip /tmp/complement || true

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates || true
RUN adduser -D -u 65532 complement 2>/dev/null || true
RUN mkdir -p /app /var/log/complement 2>/dev/null || true
COPY --from=downloader /tmp/complement /usr/local/bin/complement
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
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
