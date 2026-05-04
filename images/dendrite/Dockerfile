ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.13.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/element-hq/dendrite/releases/download/v${VERSION}/dendrite-monolith-linux-${TARGETARCH}" \
    -o /tmp/dendrite && \
    chmod +x /tmp/dendrite && \
    strip /tmp/dendrite
FROM scratch
COPY --from=downloader /tmp/dendrite /usr/local/bin/dendrite
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8008

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/dendrite"]
LABEL org.opencontainers.image.title="dendrite" \
      org.opencontainers.image.description="Dendrite - second-generation Matrix homeserver" \
      org.opencontainers.image.version="0.13.1" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/dendrite" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
