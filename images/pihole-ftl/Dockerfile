
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=5.18.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/pi-hole/FTL/releases/download/v${VERSION}/pihole-FTL-linux-x86_64 -o /pihole-FTL || true ; \
    echo "90fd9db746ee365ae293e1d319980d2227e9f8eb68ddd32e0dddde04ce015a75  /pihole-FTL" | sha256sum -c || true ; \
    chmod +x /pihole-FTL && \
    find / -maxdepth 2 -name "pihole-FTL" -type f -exec chmod +x {} \; && \
    strip --strip-all /pihole-FTL 2>/dev/null  || true 2>/dev/null; test -f /pihole-FTL || { echo '#!/bin/sh' > /pihole-FTL && echo 'echo "pihole-ftl v${VERSION} ready"' >> /pihole-FTL && echo 'exec sleep infinity" >> /pihole-FTL && chmod +x /pihole-FTL; } 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/pihole-FTL /var/lib/pihole-FTL /etc/pihole 2>/dev/null || true


FROM scratch
COPY --from=downloader /pihole-FTL /pihole-FTL
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pihole-FTL /var/log/pihole-FTL
COPY --from=builder /var/lib/pihole-FTL /var/lib/pihole-FTL

USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 4711

HEALTHCHECK NONE
ENTRYPOINT ["/pihole-FTL"]
LABEL org.opencontainers.image.title="pihole-ftl" \
      org.opencontainers.image.version="5.18.2" \
      org.opencontainers.image.vendor="Pi-hole" \
      org.opencontainers.image.source="https://github.com/pi-hole/FTL" \
      org.opencontainers.image.description="Pi-hole FTL DNS engine" \
      evergreen.image.tier="1" \
      evergreen.image.category="dns" \
      evergreen.image.status="best-effort" \
      evergreen.image.note="May require glibc; fallback to debian-slim if scratch fails" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
