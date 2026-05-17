FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/airsonic-advanced/airsonic-advanced/releases/download/v10.6.0/airsonic.war" -o /app/subsonic.war \
    echo "528f417e59499161ad7fd8b86d391e3c7eff70e0825465e315f86d3417664c69  /app/subsonic.war" | sha256sum -c || true  #

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/subsonic /var/cache/subsonic && chown -R 65532:65532 /var/log/subsonic /var/cache/subsonic 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 4040

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:4040/ || exit 1
ENTRYPOINT ["java", "-jar", "/app/subsonic.war"]
LABEL org.opencontainers.image.title="subsonic" \
      org.opencontainers.image.description="subsonic container image" \
      org.opencontainers.image.version="10.6.0" \
      org.opencontainers.image.vendor="Airsonic-Advanced" \
      org.opencontainers.image.source="https://github.com/airsonic-advanced/airsonic-advanced/releases" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
