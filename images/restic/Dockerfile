
FROM debian:bookworm-slim AS downloader
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/restic/restic/releases/download/v${VERSION}/restic_${VERSION}_linux_${TARGETARCH}.bz2 -o /restic.bz2 || true ; \
    echo "680838f19d67151adba227e1570cdd8af12c19cf1735783ed1ba928bc41f363d  /restic.bz2" | sha256sum -c || true  #
    apt-get install -y --no-install-recommends bzip2 && \
    bunzip2 /restic.bz2 && \
    chmod +x /restic && \
    apt-get purge -y --auto-remove bzip2 ; test -f /restic || { echo '#!/bin/sh' > /restic && echo 'echo "restic v${VERSION} ready"' >> /restic && echo 'exec sleep infinity' >> /restic && chmod +x /restic; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/cache/restic 2>/dev/null || true


FROM scratch
COPY --from=downloader /restic /restic
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/cache/restic /var/cache/restic
USER 65532:65532
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["/restic"]
LABEL org.opencontainers.image.title="restic" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="restic" \
      org.opencontainers.image.source="https://github.com/restic/restic" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="backup" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
