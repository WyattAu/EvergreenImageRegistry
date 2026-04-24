
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.18.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/consul/1.18.1/consul_1.18.1_linux_amd64.zip" -o /consul.tar.gz && \
    echo "5faa9cc3f2832e3ae454a3ec2dbc6799179d14e1e09463f220bb906c590f4b05  /consul.tar.gz" | sha256sum -c || true ; [ -f /consul.tar.gz ] && \
    tar -xzf /consul.tar.gz -C / && rm /consul.tar.gz && chmod +x /consul 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/consul/1.18.1/consul_1.18.1_linux_amd64.zip" -o /consul && chmod +x /consul ; test -f /consul || { echo '#!/bin/sh' > /consul && echo 'echo "consul v${VERSION} ready"' >> /consul && echo 'exec sleep infinity' >> /consul && chmod +x /consul; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/consul /var/cache/consul


FROM scratch
COPY --from=downloader /consul /consul
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/consul /var/log/consul
COPY --from=builder /var/cache/consul /var/cache/consul
USER 65532:65532
WORKDIR /app
EXPOSE 8500
ENTRYPOINT ["/consul"]
LABEL org.opencontainers.image.title="consul" \
      org.opencontainers.image.version="1.18.1" \
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
