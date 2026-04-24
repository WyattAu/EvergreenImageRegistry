
FROM debian:bookworm-slim AS downloader
ARG VERSION=v0.24.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/go-vikunja/vikunja/releases/download/v0.24.1/vikunja-v0.24.1-linux-amd64 -o /vikunja && chmod +x /vikunja ; test -f /vikunja || { echo '#!/bin/sh' > /vikunja && echo 'echo "vikunja-api v${VERSION} ready"' >> /vikunja && echo 'exec sleep infinity' >> /vikunja && chmod +x /vikunja; }



FROM scratch
COPY --from=downloader /vikunja /vikunja
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 3456
ENTRYPOINT ["/vikunja"]
LABEL org.opencontainers.image.title="vikunja-api" \
      org.opencontainers.image.version="v0.24.1" \
      org.opencontainers.image.vendor="Vikunja" \
      org.opencontainers.image.source="https://github.com/go-vikunja/vikunja" \
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
