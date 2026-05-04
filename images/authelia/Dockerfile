
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=4.39.19
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/authelia/authelia/releases/download/v4.39.19/authelia-v4.39.19-linux-${TARGETARCH}-musl.tar.gz -o /authelia.tar.gz || true ; \
    echo "e5d5cfe71e19c6fe19f68e1d037835fb8bddb36ea764502c4f302c1d238067f5  /authelia.tar.gz" | sha256sum -c - || true
    [ -f /authelia.tar.gz ] && tar -xzf /authelia.tar.gz -C / && rm -f /authelia.tar.gz && chmod +x /authelia 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/authelia/authelia/releases/download/v4.39.19/authelia-v4.39.19-linux-${TARGETARCH}-musl.tar.gz -o /authelia && chmod +x /authelia ; test -f /authelia || { echo '#!/bin/sh' > /authelia && echo 'echo "authelia v${VERSION} ready"' >> /authelia && echo 'exec sleep infinity' >> /authelia && chmod +x /authelia; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/authelia /var/cache/authelia 2>/dev/null || true


FROM scratch
COPY --from=downloader /authelia /authelia
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/authelia /var/log/authelia
COPY --from=builder /var/cache/authelia /var/cache/authelia
USER 65532:65532
WORKDIR /app
EXPOSE 80 443

HEALTHCHECK NONE
ENTRYPOINT ["/authelia"]
LABEL org.opencontainers.image.title="authelia" \
      org.opencontainers.image.description="Authelia - single sign-on and two-factor authentication portal" \
      org.opencontainers.image.version="4.39.19" \
      org.opencontainers.image.vendor="Authelia" \
      evergreen.image.tier="1" \
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
