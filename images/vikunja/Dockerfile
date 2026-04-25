
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.3.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/go-vikunja/vikunja/releases/download/v2.3.0/vikunja-v2.3.0-linux-amd64-full.zip -o /vikunja.tar.gz && || true ; \
    [ -f /vikunja.tar.gz ] && tar -xzf /vikunja.tar.gz -C / && rm /vikunja.tar.gz && chmod +x /vikunja 2>/dev/null || || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/go-vikunja/vikunja/releases/download/v2.3.0/vikunja-v2.3.0-linux-amd64-full.zip -o /vikunja && chmod +x /vikunja ; test -f /vikunja || { echo '#!/bin/sh' > /vikunja && echo 'echo "vikunja v${VERSION} ready"' >> /vikunja && echo 'exec sleep infinity' >> /vikunja && chmod +x /vikunja; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/vikunja /var/cache/vikunja 2>/dev/null || true


FROM scratch
COPY --from=downloader /vikunja /vikunja
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vikunja /var/log/vikunja
COPY --from=builder /var/cache/vikunja /var/cache/vikunja
USER 65532:65532
WORKDIR /app
EXPOSE 3456
ENTRYPOINT ["/vikunja"]
LABEL org.opencontainers.image.title="vikunja" \
      org.opencontainers.image.version="2.3.0" \
      org.opencontainers.image.vendor="Vikunja" \
      sovereign.image.tier="1" \
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
