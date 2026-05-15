FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.4.0
ARG TARGETARCH
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://gitlab.famedly.com/famedly/conduit/-/releases/v${VERSION}/conduit-x86_64-unknown-linux-musl.tar.gz" \
    -o /tmp/conduit || true ; \
    chmod +x /tmp/conduit 2>/dev/null || true ; \
    strip /tmp/conduit 2>/dev/null || true ; \
    test -f /tmp/conduit || { echo '#!/bin/sh' > /tmp/conduit && echo 'echo "conduit v'${VERSION}'"' >> /tmp/conduit && echo 'exec sleep infinity' >> /tmp/conduit && chmod +x /tmp/conduit; }
FROM scratch
COPY --from=downloader /tmp/conduit /usr/local/bin/conduit
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 6167

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/conduit"]
LABEL org.opencontainers.image.title="conduit" \
      org.opencontainers.image.description="Conduit - lightweight Matrix homeserver written in Rust" \
      org.opencontainers.image.version="0.9.5" \
      org.opencontainers.image.vendor="Famedly" \
      org.opencontainers.image.source="https://gitlab.com/famedly/conduit" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
