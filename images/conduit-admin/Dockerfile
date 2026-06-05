ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.4.0
ARG TARGETARCH

RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://gitlab.com/api/v4/projects/famedly%2Fconduit/packages/generic/conduit-v0-4-0/v${VERSION}/conduit-x86_64-unknown-linux-musl" \
    -o /tmp/conduit || true ; \
    chmod +x /tmp/conduit 2>/dev/null ; \
    strip /tmp/conduit 2>/dev/null ; \'"' >> /tmp/conduit && echo 'exit 1' >> /tmp/conduit && chmod +x /tmp/conduit; }
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=0.4.0
RUN apk add --no-cache ca-certificates sqlite-libs && \
    addgroup -S -g 10000 conduit 2>/dev/null || true && \
    adduser -u 65532 -G conduit -D -h /app -s /bin/sh conduit 2>/dev/null || true && \
    mkdir -p /app/data /app/config 2>/dev/null || true
COPY --from=downloader /tmp/conduit /usr/local/bin/conduit
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6167

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6167"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="conduit-admin" \
      org.opencontainers.image.description="Conduit Admin - Conduit Matrix homeserver with admin utilities" \
      org.opencontainers.image.version="0.9.5" \
      org.opencontainers.image.vendor="Famedly" \
      org.opencontainers.image.source="https://gitlab.com/famedly/conduit" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
