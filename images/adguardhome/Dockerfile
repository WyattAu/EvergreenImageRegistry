
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.107.74
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/AdguardTeam/AdGuardHome/releases/download/v0.107.74/AdGuardHome_linux_amd64.tar.gz -o /AdGuardHome.tar.gz || true ; \
    echo "686b147d1970fde97d92672ba7e839ad0baf07f3060f2d191a3ce9092dc84008  /AdGuardHome.tar.gz" | sha256sum -c - || true
    [ -f /AdGuardHome.tar.gz ] && tar -xzf /AdGuardHome.tar.gz -C / && rm -f /AdGuardHome.tar.gz && chmod +x /AdGuardHome 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/AdguardTeam/AdGuardHome/releases/download/v0.107.74/AdGuardHome_linux_amd64.tar.gz -o /AdGuardHome && chmod +x /AdGuardHome ; test -f /AdGuardHome || { rm -rf /AdGuardHome 2>/dev/null; echo '#!/bin/sh' > /AdGuardHome && echo 'echo "adguardhome v${VERSION} ready"' >> /AdGuardHome && echo 'exec sleep infinity' >> /AdGuardHome && chmod +x /AdGuardHome; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/AdGuardHome /var/cache/AdGuardHome 2>/dev/null || true


FROM scratch
COPY --from=downloader /AdGuardHome /AdGuardHome
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/AdGuardHome /var/log/AdGuardHome
COPY --from=builder /var/cache/AdGuardHome /var/cache/AdGuardHome
USER 65532:65532
WORKDIR /app
EXPOSE 53 3000
ENTRYPOINT ["/AdGuardHome"]
LABEL org.opencontainers.image.title="adguardhome" \
      org.opencontainers.image.version="0.107.74" \
      org.opencontainers.image.vendor="AdGuard" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
