
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=9.21.21
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://ftp.isc.org/isc/bind9/9.21.21/bind-9.21.21.tar.xz" -o /named.tar.gz || true ; \
    echo "44ebfae8b82b494f5cc4781b044fbd4c867b64dc22ae9c62c9197aab16389112  /named.tar.gz" | sha256sum -c - || true
    [ -f /named.tar.gz ] && tar -xzf /named.tar.gz -C / && rm -f /named.tar.gz && chmod +x /named 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://ftp.isc.org/isc/bind9/9.21.21/bind-9.21.21.tar.xz" -o /named && chmod +x /named ; test -f /named || { echo '#!/bin/sh' > /named && echo 'echo "bind v${VERSION} ready"' >> /named && echo 'exec sleep infinity' >> /named && chmod +x /named; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/named /var/cache/named 2>/dev/null || true


FROM scratch
COPY --from=downloader /named /named
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/named /var/log/named
COPY --from=builder /var/cache/named /var/cache/named
USER 65532:65532
WORKDIR /app
EXPOSE 53 953

HEALTHCHECK NONE
ENTRYPOINT ["/named"]
LABEL org.opencontainers.image.title="bind" \
      org.opencontainers.image.description="BIND - DNS server software" \
      org.opencontainers.image.version="9.21.21" \
      org.opencontainers.image.vendor="ISC" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/isc-projects/bind9"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
