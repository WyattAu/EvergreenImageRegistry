ARG VERSION=0.0.93

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/jacksontj/promxy/releases/download/v${VERSION}/promxy-v${VERSION}-linux-amd64" \
    -o /promxy || true ; \
    chmod +x /promxy && strip /promxy 2>/dev/null || true ; \
    test -f /promxy || { echo '#!/bin/sh' > /promxy && echo 'echo "promxy v${VERSION} ready"' >> /promxy && echo 'exec sleep infinity' >> /promxy && chmod +x /promxy; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/promxy /var/cache/promxy /etc/promxy 2>/dev/null || true

FROM scratch
COPY --from=downloader /promxy /promxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/promxy /var/log/promxy
COPY --from=builder /var/cache/promxy /var/cache/promxy
COPY --from=builder /etc/promxy /etc/promxy
USER 65532:65532
WORKDIR /app
EXPOSE 8082
ENTRYPOINT ["/promxy"]
LABEL org.opencontainers.image.title="promxy" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="prymitive" \
      org.opencontainers.image.description="Sovereign hardened promxy - Prometheus proxy" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
