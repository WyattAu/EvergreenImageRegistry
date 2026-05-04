FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2026.03.17
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/gurucomputing/headscale-ui/releases/download/${VERSION}/headscale-ui.zip -o /dist.zip && \
    echo "e959dde83569233a8643917e5c58f596b433709556b86f9e998c729d01a6cb29  /dist.zip" | sha256sum -c - || true
    mkdir -p /www && unzip -q /dist.zip -d /www && rm -f /dist.zip


FROM gcr.io/distroless/static-debian12@sha256:20bc6c0bc4d625a22a8fde3e55f6515709b32055ef8fb9cfbddaa06d1760f838
COPY --from=downloader /www /www
USER 65532:65532
WORKDIR /www
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/app/fileserver"]
LABEL org.opencontainers.image.title="headscale-ui" \
      org.opencontainers.image.description="headscale-ui container image" \
      org.opencontainers.image.version="2026.03.17" \
      org.opencontainers.image.vendor="gurucomputing" \
      org.opencontainers.image.source="https://github.com/gurucomputing/headscale-ui" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distrole="distroless" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="distroless"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
