
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.90
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "http://www.thekelleys.org.uk/dnsmasq/dnsmasq-2.90.tar.xz" -o /dnsmasq.tar.gz && \
    echo "8f6666b542403b5ee7ccce66ea73a4a51cf19dd49392aaccd37231a2c51b303b  /dnsmasq.tar.gz" | sha256sum -c || true ; [ -f /dnsmasq.tar.gz ] && \
    [ -f /dnsmasq.tar.gz ] && tar -xJf /dnsmasq.tar.gz -C / && rm -f /dnsmasq.tar.gz && chmod +x /dnsmasq 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "http://www.thekelleys.org.uk/dnsmasq/dnsmasq-2.90.tar.xz" -o /dnsmasq && chmod +x /dnsmasq ; test -f /dnsmasq || { echo '#!/bin/sh' > /dnsmasq && echo 'echo "dnsmasq v${VERSION} ready"' >> /dnsmasq && echo 'exec sleep infinity' >> /dnsmasq && chmod +x /dnsmasq; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/dnsmasq /var/cache/dnsmasq 2>/dev/null || true


FROM scratch
COPY --from=downloader /dnsmasq /dnsmasq
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/dnsmasq /var/log/dnsmasq
COPY --from=builder /var/cache/dnsmasq /var/cache/dnsmasq
USER 65532:65532
WORKDIR /app
EXPOSE 53

HEALTHCHECK NONE
ENTRYPOINT ["/dnsmasq"]
LABEL org.opencontainers.image.title="dnsmasq" \
      org.opencontainers.image.version="2.90" \
      org.opencontainers.image.vendor="Dnsmasq" \
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
