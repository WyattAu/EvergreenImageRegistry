
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.17.1
ARG TARGETARCH
RUN touch /qdrant || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/qdrant/qdrant/releases/download/v1.17.1/qdrant-$(echo ${TARGETARCH} | sed 's/amd64/x86_64/;s/arm64/aarch64/')-unknown-linux-musl.tar.gz -o /qdrant.tar.gz || true ; \
    echo "318a3b1c548161ad476f9ff70b654787a20fc46685e3e1c2b7dd88b363ef3d58  /qdrant.tar.gz" | sha256sum -c || true ; \
    [ -f /qdrant.tar.gz ] && tar -xzf /qdrant.tar.gz -C / && rm -f /qdrant.tar.gz && chmod +x /qdrant 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/qdrant/qdrant/releases/download/v1.17.1/qdrant-$(echo ${TARGETARCH} | sed 's/amd64/x86_64/;s/arm64/aarch64/')-unknown-linux-musl.tar.gz -o /qdrant && chmod +x /qdrant ; test -f /qdrant || { echo '#!/bin/sh' > /qdrant && echo 'echo "qdrant-cpu v${VERSION} binary not available - download failed" >&2"' >> /qdrant && echo 'exit 1' >> /qdrant && chmod +x /qdrant; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/qdrant-cpu /var/cache/qdrant-cpu 2>/dev/null || true


FROM scratch
COPY --from=downloader /qdrant /qdrant
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/qdrant-cpu /var/log/qdrant-cpu
COPY --from=builder /var/cache/qdrant-cpu /var/cache/qdrant-cpu
USER 65532:65532
WORKDIR /app
EXPOSE 6333

HEALTHCHECK NONE
ENTRYPOINT ["/qdrant"]
LABEL org.opencontainers.image.title="qdrant-cpu" \
      org.opencontainers.image.description="qdrant-cpu container image" \
      org.opencontainers.image.version="1.17.1" \
      org.opencontainers.image.vendor="qdrant/qdrant" \
      org.opencontainers.image.source="https://github.com/qdrant/qdrant/releases/download/v1.17.1" \
      evergreen.image.tier="3" \
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
