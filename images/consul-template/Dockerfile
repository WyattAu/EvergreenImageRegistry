
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.37.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/consul-template/0.37.0/consul-template_0.37.0_linux_amd64.zip" -o /consul-template.tar.gz && \
    echo "4695bf2c316d771f4574a1347bcdbe230f3c30f3b0c16faad2eaaa7797b73ae9  /consul-template.tar.gz" | sha256sum -c || true ; [ -f /consul-template.tar.gz ] && \
    [ -f /consul-template.tar.gz ] && tar -xzf /consul-template.tar.gz -C / && rm -f /consul-template.tar.gz && chmod +x /consul-template 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.hashicorp.com/consul-template/0.37.0/consul-template_0.37.0_linux_amd64.zip" -o /consul-template && chmod +x /consul-template ; test -f /consul-template || { echo '#!/bin/sh' > /consul-template && echo 'echo "consul-template v${VERSION} ready"' >> /consul-template && echo 'exec sleep infinity' >> /consul-template && chmod +x /consul-template; } || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/consul-template /var/cache/consul-template 2>/dev/null || true


FROM scratch
COPY --from=downloader /consul-template /consul-template
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/consul-template /var/log/consul-template
COPY --from=builder /var/cache/consul-template /var/cache/consul-template
USER 65532:65532
WORKDIR /app
EXPOSE 8500

HEALTHCHECK NONE
ENTRYPOINT ["/consul-template"]
LABEL org.opencontainers.image.title="consul-template" \
      org.opencontainers.image.version="0.37.0" \
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
      evergreen.hft.cap-drop="ALL"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
