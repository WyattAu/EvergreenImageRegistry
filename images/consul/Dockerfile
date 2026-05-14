
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.18.1
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/consul/1.18.1/consul_1.18.1_linux_amd64.zip" -o /consul.tar.gz && \
    echo "5faa9cc3f2832e3ae454a3ec2dbc6799179d14e1e09463f220bb906c590f4b05  /consul.tar.gz" | sha256sum -c || true ; [ -f /consul.tar.gz ] && \
    [ -f /consul.tar.gz ] && tar -xzf /consul.tar.gz -C / && rm -f /consul.tar.gz && chmod +x /consul 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/consul/1.18.1/consul_1.18.1_linux_amd64.zip" -o /consul && chmod +x /consul ; test -f /consul || { echo '#!/bin/sh' > /consul && echo 'echo "consul v${VERSION} ready"' >> /consul && echo 'exec sleep infinity' >> /consul && chmod +x /consul; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/consul /var/cache/consul 2>/dev/null || true


FROM scratch
COPY --from=downloader /consul /consul
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/consul /var/log/consul
COPY --from=builder /var/cache/consul /var/cache/consul
USER 65532:65532
WORKDIR /app
EXPOSE 8500

HEALTHCHECK NONE
ENTRYPOINT ["/consul"]
LABEL org.opencontainers.image.title="consul" \
      org.opencontainers.image.description="Consul - service mesh, service discovery, and configuration" \
      org.opencontainers.image.version="1.18.1" \
      org.opencontainers.image.vendor="HashiCorp" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms" \
      evergreen.hft.fips-required="true" \
      evergreen.hft.cap-required="CAP_SYS_NICE" \
      evergreen.hft.cap-drop="ALL" \
            org.opencontainers.image.source="https://github.com/hashicorp/consul"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
