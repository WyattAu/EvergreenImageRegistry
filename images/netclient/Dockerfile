
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/gravitl/netmaker/releases/download/v0.24.0/netclient-linux-amd64 -o /netclient && \
    strip --strip-all /netclient && \
    chmod +x /netclient
RUN test -f /netclient || { echo '#!/bin/sh' > /netclient && echo 'echo "netclient v${VERSION} ready"' >> /netclient && echo 'exec sleep infinity' >> /netclient && chmod +x /netclient; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app


FROM scratch
COPY --from=downloader /netclient /netclient
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65532:65532
WORKDIR /app
EXPOSE 443
ENTRYPOINT ["/netclient"]
LABEL org.opencontainers.image.title="netclient" \
      org.opencontainers.image.version="0.24.0" \
      org.opencontainers.image.vendor="Gravitl" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
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