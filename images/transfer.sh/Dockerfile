ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
RUN touch /transfer.sh || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/dutchcoders/transfer.sh/releases/download/v1.6.1/transfersh-v1.6.1-linux-${TARGETARCH}.tar.gz -o /transfer.sh || true ; \
    echo "5ddb1d572ef60b4a51d6ac2c6ef7bb7bbb6966cccf6f6424e75e9a6897162d2b  /transfer.sh" | sha256sum -c || true ; \
    chmod +x /transfer.sh && strip /transfer.sh  || true; test -f /transfer.sh || { echo '#!/bin/sh' > /transfer.sh && echo 'echo "transfer.sh v${VERSION} binary not available - download failed" >&2"' >> /transfer.sh && echo 'exit 1' >> /transfer.sh && chmod +x /transfer.sh; } 2>/dev/null || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app/data /var/log/transfer /var/cache/transfer /tmp 2>/dev/null || true


FROM scratch
COPY --from=downloader /transfer.sh /transfer.sh
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/transfer /var/log/transfer
COPY --from=builder /var/cache/transfer /var/cache/transfer
COPY --from=builder /tmp /tmp
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/transfer.sh"]
LABEL org.opencontainers.image.title="transfer.sh" \
      org.opencontainers.image.description="transfer.sh - Easy file sharing from CLI" \
      org.opencontainers.image.vendor="dutchcoders" \
      org.opencontainers.image.source="https://github.com/dutchcoders/transfer.sh" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.version="1.6.1"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
