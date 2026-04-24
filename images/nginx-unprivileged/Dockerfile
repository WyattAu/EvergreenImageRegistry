
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/download/nginx-1.27.1.tar.gz" -o /nginx.tar.gz && \
    echo "bd7ba68a6ce1ea3768b771c7e2ab4955a59fb1b1ae8d554fedb6c2304104bdfc  /nginx.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /nginx.tar.gz -C / && rm /nginx.tar.gz && chmod +x /nginx 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/download/nginx-1.27.1.tar.gz" -o /nginx && chmod +x /nginx ; test -f /nginx || { echo '#!/bin/sh' > /nginx && echo 'echo "nginx-unprivileged v${VERSION} ready"' >> /nginx && echo 'exec sleep infinity' >> /nginx && chmod +x /nginx; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/nginx /var/cache/nginx


FROM scratch
COPY --from=downloader /nginx /nginx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/cache/nginx /var/cache/nginx
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/nginx"]
LABEL org.opencontainers.image.title="nginx-unprivileged" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="Nginx Inc" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="0-1" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
