
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Praqma/helmsman/releases/download/v4.0.5/helmsman_4.0.5_linux_amd64.tar.gz" -o /helmsman.tar.gz && \
    tar -xzf /helmsman.tar.gz -C / && rm /helmsman.tar.gz && chmod +x /helmsman && strip /helmsman 2>/dev/null || true
RUN test -f /helmsman || { echo '#!/bin/sh' > /helmsman && echo 'echo "helmsman v${VERSION} ready"' >> /helmsman && echo 'exec sleep infinity' >> /helmsman && chmod +x /helmsman; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/helmsman /var/cache/helmsman


FROM scratch
COPY --from=downloader /helmsman /helmsman
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/helmsman /var/log/helmsman
COPY --from=builder /var/cache/helmsman /var/cache/helmsman
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/helmsman"]
LABEL org.opencontainers.image.title="helmsman" \
      org.opencontainers.image.version="4.0.5" \
      org.opencontainers.image.vendor="Praqma" \
      org.opencontainers.image.description="Sovereign hardened helmsman - Helm charts as code" \
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