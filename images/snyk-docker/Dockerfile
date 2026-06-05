
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/snyk/snyk/releases/download/v1.1295.0/snyk-linux -o /snyk-docker && chmod +x /snyk-docker && strip /snyk-docker && { echo "Binary not available - download failed" >&2; exit 1; }
    echo "ee7382115d7a4f1fee05a70e3af7db4dbd07f6c54f1adb76fce534ac607c0372  /snyk-docker" | sha256sum -c && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/snyk-docker /var/cache/snyk-docker 2>/dev/null || true


FROM scratch

COPY --from=downloader /snyk-docker /usr/local/bin/snyk-docker
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65532:65532
WORKDIR /app
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="2"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE

LABEL org.opencontainers.image.description="snyk-docker container image" \
      org.opencontainers.image.title="Snyk Docker" \
      org.opencontainers.image.source="https://github.com/snyk/snyk" \
            org.opencontainers.image.version="1.1295.0"

ENTRYPOINT ["/snyk-docker"]
CMD ["--help"]
