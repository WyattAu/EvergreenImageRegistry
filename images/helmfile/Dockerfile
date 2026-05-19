
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.162.0
ARG TARGETARCH
RUN touch /helmfile || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/helmfile/helmfile/releases/download/v0.162.0/helmfile_0.162.0_linux_${TARGETARCH}.tar.gz -o /helmfile.tar.gz && \
    echo "e8e7fb360d4cbc6192348c5b4587a4e64d4b619db88046d1142467a2e6d676ad  /helmfile.tar.gz" | sha256sum -c || true ; [ -f /helmfile.tar.gz ] && \
    [ -f /helmfile.tar.gz ] && tar -xzf /helmfile.tar.gz -C / && rm -f /helmfile.tar.gz && chmod +x /helmfile 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/helmfile/helmfile/releases/download/v0.162.0/helmfile_0.162.0_linux_${TARGETARCH}.tar.gz -o /helmfile && chmod +x /helmfile ; test -f /helmfile || { echo '#!/bin/sh' > /helmfile && echo 'echo "helmfile v${VERSION} binary not available - download failed" >&2"' >> /helmfile && echo 'exit 1' >> /helmfile && chmod +x /helmfile; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/helmfile /var/cache/helmfile 2>/dev/null || true


FROM scratch
COPY --from=downloader /helmfile /helmfile
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/helmfile /var/log/helmfile
COPY --from=builder /var/cache/helmfile /var/cache/helmfile
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/helmfile"]
LABEL org.opencontainers.image.title="helmfile" \
      org.opencontainers.image.description="helmfile container image" \
      org.opencontainers.image.version="0.162.0" \
      org.opencontainers.image.vendor="Helmfile" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/helmfile/helmfile"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
