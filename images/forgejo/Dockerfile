ARG VERSION=v15.0.4
ARG SHIM_VERSION=v2.0.0

FROM debian:bookworm-slim@sha256:abd67ffcfa541b485a3dff59865ab629aa048a6c613e639d36e7456b0b229241 AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates xz-utils git && rm -rf /var/lib/apt/lists/* &&     arch=$(case ${TARGETARCH} in amd64) echo "linux-amd64";; arm64) echo "linux-arm64";; *) echo "linux-amd64";; esac) &&     curl -fsSL "https://codeberg.org/forgejo/forgejo/releases/download/${VERSION}/forgejo-${VERSION#v}-${arch}.xz" -o /tmp/forgejo.xz &&     xz -d /tmp/forgejo.xz &&     cp /tmp/forgejo /forgejo && chmod +x /forgejo

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM debian:bookworm-slim@sha256:abd67ffcfa541b485a3dff59865ab629aa048a6c613e639d36e7456b0b229241 AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /forgejo /usr/local/bin/forgejo

ENV FORGEJO_WORK_DIR=/data/gitea FORGEJO_CUSTOM=/data/gitea     SHIM_METRICS_ENABLED="true"

EXPOSE 3000 22 9101
VOLUME /data

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3   CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/forgejo web"]
CMD []

LABEL org.opencontainers.image.title="forgejo" evergreen.image.tier="critical" evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="scratch" evergreen.security.cap-drop="ALL"
STOPSIGNAL SIGTERM
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
