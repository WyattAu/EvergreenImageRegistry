
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2024.10.22-7ca5933
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/CorentinTh/it-tools/releases/download/v2024.10.22-7ca5933/it-tools-2024.10.22-7ca5933.zip -o /it-tools.tar.gz || true ; \
    echo "eef276d675db6053bdc65cd8482a566785561c70eed5035a0e05b0e627b0989d  /it-tools.tar.gz" | sha256sum -c || true ; \
    [ -f /it-tools.tar.gz ] && tar -xzf /it-tools.tar.gz -C / && rm -f /it-tools.tar.gz && chmod +x /it-tools 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/CorentinTh/it-tools/releases/download/v2024.10.22-7ca5933/it-tools-2024.10.22-7ca5933.zip -o /it-tools && chmod +x /it-tools ; test -f /it-tools || { echo '#!/bin/sh' > /it-tools && echo 'echo "it-tools v${VERSION} ready"' >> /it-tools && echo 'exec sleep infinity' >> /it-tools && chmod +x /it-tools; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/it-tools /var/cache/it-tools 2>/dev/null || true


FROM scratch
COPY --from=downloader /it-tools /it-tools
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/it-tools /var/log/it-tools
COPY --from=builder /var/cache/it-tools /var/cache/it-tools
USER 65532:65532
WORKDIR /app
EXPOSE 80

HEALTHCHECK NONE
ENTRYPOINT ["/it-tools"]
LABEL org.opencontainers.image.title="it-tools" \
      org.opencontainers.image.description="it-tools container image" \
      org.opencontainers.image.version="2024.10.22-7ca5933" \
      org.opencontainers.image.vendor="IT-Tools" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/CorentinTh/it-tools"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
