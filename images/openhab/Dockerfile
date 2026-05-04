# =============================================================================
# EVERGREEN HARDENED OPENHAB
# Generated from template - Version: 4.2.0
# Downloads OpenHAB distribution directly from GitHub releases (no upstream image).
# OpenHAB is a Java application; uses wolfi-jdk base for JDK runtime.
# =============================================================================

ARG VERSION=4.2.0
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=4.2.0
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/openhab/openhab-distro/releases/download/v${VERSION}/openhab-${VERSION}.tar.gz" -o /tmp/openhab.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/openhab.tar.gz -C /app && rm -f /tmp/openhab.tar.gz && \
    chmod +x /app/start.sh
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true && \
    apk add --no-cache java-21-default-jdk 2>/dev/null || \
    apk add --no-cache openjdk-21-jdk-headless 2>/dev/null || true && \
    adduser -u 65532 -D openhab 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /openhab
RUN mkdir -p /openhab/conf /openhab/userdata /var/log/openhab /var/cache/openhab && \
    chown -R 65532:65532 /openhab/conf /openhab/userdata /var/log/openhab /var/cache/openhab 2>/dev/null || true
USER 65532:65532
WORKDIR /openhab

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/openhab/start.sh"]
EXPOSE 8080 8443

LABEL org.opencontainers.image.title="openhab" \
      org.opencontainers.image.version="4.2.0" \
      org.opencontainers.image.vendor="OpenHAB" \
      org.opencontainers.image.source="https://github.com/openhab/openhab-distro" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.official="true"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
