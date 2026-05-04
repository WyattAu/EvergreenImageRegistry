ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.9.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/gotify/server/releases/download/v${VERSION}/gotify-linux-${TARGETARCH}" \
    -o /tmp/gotify && \
    chmod +x /tmp/gotify && \
    strip /tmp/gotify || true
FROM scratch
COPY --from=downloader /tmp/gotify /usr/local/bin/gotify
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/gotify"]
LABEL org.opencontainers.image.title="gotify" \
      org.opencontainers.image.description="Gotify - simple push notification server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Gotify" \
      org.opencontainers.image.source="https://github.com/gotify/server" \
      evergreen.image.tier="2" \
      evergreen.image.category="notifications" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
