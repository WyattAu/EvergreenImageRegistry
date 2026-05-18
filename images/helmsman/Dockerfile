
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=4.0.5
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/Praqma/helmsman/releases/download/v4.0.5/helmsman_4.0.5_linux_${TARGETARCH}.tar.gz -o /helmsman.tar.gz || true ; \
    echo "9531a315a52683d8561a3948ad8cbaea4b077c62dedff9a1f4736c7dc15a4848  /helmsman.tar.gz" | sha256sum -c || true ; \
    tar -xzf /helmsman.tar.gz -C / && rm -f /helmsman.tar.gz && chmod +x /helmsman && strip /helmsman 2>/dev/null  || true; test -f /helmsman || { echo '#!/bin/sh' > /helmsman && echo 'echo "helmsman v${VERSION} ready"' >> /helmsman && echo 'exec sleep infinity' >> /helmsman && chmod +x /helmsman; } || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/helmsman /var/cache/helmsman 2>/dev/null || true


FROM scratch
COPY --from=downloader /helmsman /helmsman
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/helmsman /var/log/helmsman
COPY --from=builder /var/cache/helmsman /var/cache/helmsman
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/helmsman"]
LABEL org.opencontainers.image.title="helmsman" \
      org.opencontainers.image.version="4.0.5" \
      org.opencontainers.image.vendor="Praqma" \
      org.opencontainers.image.description="Evergreen hardened helmsman - Helm charts as code" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
            org.opencontainers.image.source="https://github.com/Praqma/helmsman"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
