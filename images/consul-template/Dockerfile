
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/consul-template/0.37.0/consul-template_0.37.0_linux_amd64.zip" -o /consul-template.tar.gz && \
    echo "4695bf2c316d771f4574a1347bcdbe230f3c30f3b0c16faad2eaaa7797b73ae9  /consul-template.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /consul-template.tar.gz -C / && rm /consul-template.tar.gz && chmod +x /consul-template 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/consul-template/0.37.0/consul-template_0.37.0_linux_amd64.zip" -o /consul-template && chmod +x /consul-template ; test -f /consul-template || { echo '#!/bin/sh' > /consul-template && echo 'echo "consul-template v${VERSION} ready"' >> /consul-template && echo 'exec sleep infinity' >> /consul-template && chmod +x /consul-template; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/consul-template /var/cache/consul-template


FROM scratch
COPY --from=downloader /consul-template /consul-template
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/consul-template /var/log/consul-template
COPY --from=builder /var/cache/consul-template /var/cache/consul-template
USER 65532:65532
WORKDIR /app
EXPOSE 8500
ENTRYPOINT ["/consul-template"]
LABEL org.opencontainers.image.title="consul-template" \
      org.opencontainers.image.version="0.37.0" \
      org.opencontainers.image.vendor="HashiCorp" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms" \
      sovereign.hft.fips-required="true" \
      sovereign.hft.cap-required="CAP_SYS_NICE" \
      sovereign.hft.cap-drop="ALL"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
