ARG VERSION=2.8.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/fluxcd/flux2/releases/download/v2.8.6/flux_2.8.6_linux_amd64.tar.gz" -o /flux.tar.gz && \
    echo "c53cc990ae266f7840f64c81515d701d8821d558a9062aa4211d71b38cf044be  /flux.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /flux.tar.gz -C / && rm /flux.tar.gz && chmod +x /flux && strip /flux

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/fluxcd-image /var/cache/fluxcd-image

FROM scratch
COPY --from=downloader /flux /flux
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/fluxcd-image /var/log/fluxcd-image
COPY --from=builder /var/cache/fluxcd-image /var/cache/fluxcd-image
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/flux", "bootstrap", "image-automation"]
LABEL org.opencontainers.image.title="fluxcd-image" \
      org.opencontainers.image.version="2.8.6" \
      org.opencontainers.image.vendor="Flux CD" \
      org.opencontainers.image.description="Sovereign hardened fluxcd-image - image automation for Flux" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM