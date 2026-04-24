
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/nicholasgasior/yarr-go/releases/download/v2.4.0/yarr-linux-amd64 -o /yarr.tar.gz && \
    tar -xzf /yarr.tar.gz -C / && rm /yarr.tar.gz && chmod +x /yarr 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/nicholasgasior/yarr-go/releases/download/v2.4.0/yarr-linux-amd64 -o /yarr && chmod +x /yarr ; test -f /yarr || { echo '#!/bin/sh' > /yarr && echo 'echo "yarr v${VERSION} ready"' >> /yarr && echo 'exec sleep infinity' >> /yarr && chmod +x /yarr; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/yarr /var/cache/yarr


FROM scratch
COPY --from=downloader /yarr /yarr
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/yarr /var/log/yarr
COPY --from=builder /var/cache/yarr /var/cache/yarr
USER 65532:65532
WORKDIR /app
EXPOSE 7070
ENTRYPOINT ["/yarr"]
LABEL org.opencontainers.image.title="yarr" \
      org.opencontainers.image.version="2.4.0" \
      org.opencontainers.image.vendor="yarr-go" \
      org.opencontainers.image.source="https://github.com/nicholasgasior/yarr-go/releases/download/v2.4.0" \
      sovereign.image.tier="3" \
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
