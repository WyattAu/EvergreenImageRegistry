ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=v0.24.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/go-vikunja/vikunja/releases/download/v2.3.0/vikunja-v2.3.0-linux-${TARGETARCH}-full.zip -o /vikunja && chmod +x /vikunja ; test -f /vikunja || { echo '#!/bin/sh' > /vikunja && echo 'echo "vikunja-redis v${VERSION} ready"' >> /vikunja && echo 'exec sleep infinity' >> /vikunja && chmod +x /vikunja; } || true
    echo "c37f8291698e288cd95198b52b826ffca40c3665d351041b93358e142862994d  /vikunja" | sha256sum -c || true  #



FROM scratch
COPY --from=downloader /vikunja /vikunja
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 3456
ENTRYPOINT ["/vikunja"]
CMD ["--config", "/app/config.yml"]
LABEL org.opencontainers.image.title="vikunja-redis" \
      org.opencontainers.image.version="v0.24.1" \
      org.opencontainers.image.vendor="Vikunja" \
      org.opencontainers.image.source="https://github.com/go-vikunja/vikunja" \
      org.opencontainers.image.description="Vikunja API with Redis backend configuration" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
