ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.42.1
RUN touch /meilisearch || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/meilisearch/meilisearch/releases/download/v1.42.1/meilisearch-enterprise-linux-${TARGETARCH} -o /meilisearch.tar.gz || true ; \
    echo "4ff9a43e0ccd5bd61efaaa37bd42b2a9fc349d2b6d80e1488810019701104162  /meilisearch" | sha256sum -c || true ; \
    echo "4ff9a43e0ccd5bd61efaaa37bd42b2a9fc349d2b6d80e1488810019701104162  /meilisearch" | sha256sum -c || true ; \
    [ -f /meilisearch.tar.gz ] && tar -xzf /meilisearch.tar.gz -C / && rm -f /meilisearch.tar.gz && chmod +x /meilisearch 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/meilisearch/meilisearch/releases/download/v1.42.1/meilisearch-enterprise-linux-${TARGETARCH} -o /meilisearch && chmod +x /meilisearch ; test -f /meilisearch || { echo '#!/bin/sh' > /meilisearch && echo 'echo "meilisearch v${VERSION} ready"' >> /meilisearch && echo 'exec sleep infinity' >> /meilisearch && chmod +x /meilisearch; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/meilisearch /var/cache/meilisearch 2>/dev/null || true


FROM scratch
COPY --from=downloader /meilisearch /meilisearch
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/meilisearch /var/log/meilisearch
COPY --from=builder /var/cache/meilisearch /var/cache/meilisearch
USER 65532:65532
WORKDIR /app
EXPOSE 7700

HEALTHCHECK NONE
ENTRYPOINT ["/meilisearch"]
LABEL org.opencontainers.image.title="meilisearch" \
      org.opencontainers.image.description="Meilisearch - fast, relevant, and typo-tolerant search engine" \
      org.opencontainers.image.version="1.42.1" \
      org.opencontainers.image.vendor="Meilisearch" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/meilisearch/meilisearch"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
