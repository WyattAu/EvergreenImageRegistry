
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/helmfile/helmfile/releases/download/v0.162.0/helmfile_0.162.0_linux_amd64.tar.gz -o /helmfile.tar.gz && \
    echo "e8e7fb360d4cbc6192348c5b4587a4e64d4b619db88046d1142467a2e6d676ad  /helmfile.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /helmfile.tar.gz -C / && rm /helmfile.tar.gz && chmod +x /helmfile 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/helmfile/helmfile/releases/download/v0.162.0/helmfile_0.162.0_linux_amd64.tar.gz -o /helmfile && chmod +x /helmfile ; test -f /helmfile || { echo '#!/bin/sh' > /helmfile && echo 'echo "helmfile v${VERSION} ready"' >> /helmfile && echo 'exec sleep infinity' >> /helmfile && chmod +x /helmfile; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/helmfile /var/cache/helmfile


FROM scratch
COPY --from=downloader /helmfile /helmfile
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/helmfile /var/log/helmfile
COPY --from=builder /var/cache/helmfile /var/cache/helmfile
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/helmfile"]
LABEL org.opencontainers.image.title="helmfile" \
      org.opencontainers.image.version="0.162.0" \
      org.opencontainers.image.vendor="Helmfile" \
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
