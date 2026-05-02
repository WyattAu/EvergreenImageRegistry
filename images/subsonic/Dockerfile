FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/airsonic-advanced/airsonic-advanced/releases/download/v10.6.0/airsonic.war" -o /app/subsonic.war

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/subsonic /var/cache/subsonic && chown -R 65532:65532 /var/log/subsonic /var/cache/subsonic 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 4040
ENTRYPOINT ["java", "-jar", "/app/subsonic.war"]
LABEL org.opencontainers.image.title="subsonic" \
      org.opencontainers.image.version="10.6.0" \
      org.opencontainers.image.vendor="Airsonic-Advanced" \
      org.opencontainers.image.source="https://github.com/airsonic-advanced/airsonic-advanced/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
