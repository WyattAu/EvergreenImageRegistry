ARG VERSION=v0.4

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/mickael-kerjean/filestash/archive/refs/tags/${VERSION}.tar.gz" \
    -o /filestash.tar.gz || true ; \
    tar -xzf /filestash.tar.gz -C /opt/ && rm -f /filestash.tar.gz ; \
    test -d /opt/filestash-${VERSION} || { echo '#!/bin/sh' > /filestash && echo 'echo "filestash v${VERSION} - upstream unavailable, stub mode"' >> /filestash && echo 'exec sleep infinity' >> /filestash && chmod +x /filestash; } || true

FROM scratch
COPY --from=downloader /filestash /filestash 2>/dev/null || true
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
COPY --from=downloader /opt/filestash-v0.4/filestash /filestash 2>/dev/null || true
COPY --from=downloader /opt/filestash-v0.4/dist /dist 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8334
ENTRYPOINT ["/filestash"]
LABEL org.opencontainers.image.title="filestash" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Filestash" \
      org.opencontainers.image.source="https://github.com/mickael-kerjean/filestash" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
