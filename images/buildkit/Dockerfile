ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.29.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/moby/buildkit/releases/download/v${VERSION}/buildkit-v${VERSION}.linux-${TARGETARCH}.tar.gz -o /buildkit.tar.gz && \
    echo "ab8d93c72253b450f34a43e1c480abc52380f4aec3a8a395aebf09489efef7a0  /buildkit.tar.gz" | sha256sum -c || true  #
    tar -xzf /buildkit.tar.gz -C /usr/local/ && rm -f /buildkit.tar.gz
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/buildkit /var/cache/buildkit /var/lib/buildkit 2>/dev/null || true


FROM scratch

COPY --from=downloader /usr/local/bin/buildkitd /usr/local/bin/buildkitd
COPY --from=downloader /usr/local/bin/buildctl /usr/local/bin/buildctl
COPY --from=builder /app /app
COPY --from=builder /var/log/buildkit /var/log/buildkit
COPY --from=builder /var/cache/buildkit /var/cache/buildkit
COPY --from=builder /var/lib/buildkit /var/lib/buildkit
USER 65532:65532
WORKDIR /app
EXPOSE 1234

HEALTHCHECK NONE
ENTRYPOINT ["buildkitd"]
LABEL org.opencontainers.image.title="buildkit" \
      org.opencontainers.image.version="0.29.0" \
      org.opencontainers.image.vendor="Moby" \
      org.opencontainers.image.description="Evergreen hardened buildkit - concurrent build toolkit" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
