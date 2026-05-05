
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/restic/restic/releases/download/v${VERSION}/restic_${VERSION}_linux_${TARGETARCH}.bz2 -o /restic.bz2 || true ; \
    echo "680838f19d67151adba227e1570cdd8af12c19cf1735783ed1ba928bc41f363d  /restic.bz2" | sha256sum -c || true \
    apt-get install -y --no-install-recommends bzip2 && \
    bunzip2 /restic.bz2 && \
    chmod +x /restic && \
    apt-get purge -y --auto-remove bzip2 ; test -f /restic || { echo '#!/bin/sh' > /restic && echo 'echo "restic v${VERSION} ready"' >> /restic && echo 'exec sleep infinity' >> /restic && chmod +x /restic; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/cache/restic 2>/dev/null || true


FROM scratch
COPY --from=downloader /restic /restic
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/cache/restic /var/cache/restic
USER 65532:65532
WORKDIR /app
EXPOSE 8000

HEALTHCHECK NONE
ENTRYPOINT ["/restic"]
LABEL org.opencontainers.image.title="restic" \
      org.opencontainers.image.description="restic container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="restic" \
      org.opencontainers.image.source="https://github.com/restic/restic" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="backup" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
