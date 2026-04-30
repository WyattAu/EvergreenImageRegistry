FROM debian:bookworm-slim AS downloader
ARG VERSION=2.6.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/gotify/server/releases/download/v${VERSION}/gotify-linux-amd64" \
    -o /tmp/gotify && \
    chmod +x /tmp/gotify && \
    strip /tmp/gotify || true

FROM scratch
COPY --from=downloader /tmp/gotify /usr/local/bin/gotify
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/gotify"]
LABEL org.opencontainers.image.title="gotify" \
      org.opencontainers.image.description="Gotify - simple push notification server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Gotify" \
      org.opencontainers.image.source="https://github.com/gotify/server" \
      sovereign.image.tier="2" \
      sovereign.image.category="notifications" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM
