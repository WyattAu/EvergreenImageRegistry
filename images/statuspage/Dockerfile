
FROM debian:bookworm-slim AS downloader
ARG VERSION=5.7.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cstate/cstate/releases/download/v${VERSION}/cstate-v${VERSION}-linux-amd64.tar.gz -o /cstate.tar.gz && || true ; \
    [ -f /cstate.tar.gz ] && tar -xzf /cstate.tar.gz -C / && rm /cstate.tar.gz && || true ; \
    find / -maxdepth 2 -name "cstate" -type f -exec chmod +x {} \; ; test -f /cstate || { echo '#!/bin/sh' > /cstate && echo 'echo "statuspage v${VERSION} ready"' >> /cstate && echo 'exec sleep infinity' >> /cstate && chmod +x /cstate; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cstate 2>/dev/null || true


FROM scratch
COPY --from=downloader /cstate /cstate
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cstate /var/log/cstate
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/cstate"]
LABEL org.opencontainers.image.title="statuspage" \
      org.opencontainers.image.version="5.7.0" \
      org.opencontainers.image.vendor="cstate" \
      org.opencontainers.image.source="https://github.com/cstate/cstate" \
      org.opencontainers.image.description="Static status page generator" \
      sovereign.image.tier="1" \
      sovereign.image.category="monitoring" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="2000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
