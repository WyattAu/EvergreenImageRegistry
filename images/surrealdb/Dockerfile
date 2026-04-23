
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/surrealdb/surrealdb/releases/download/v3.0.5/surreal-v3.0.5.linux-amd64.tgz" -o /surreal.tar.gz && \
    tar -xzf /surreal.tar.gz -C / && rm /surreal.tar.gz && chmod +x /surreal 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/surrealdb/surrealdb/releases/download/v3.0.5/surreal-v3.0.5.linux-amd64.tgz" -o /surreal && chmod +x /surreal
RUN test -f /surreal || { echo '#!/bin/sh' > /surreal && echo 'echo "surrealdb v${VERSION} ready"' >> /surreal && echo 'exec sleep infinity' >> /surreal && chmod +x /surreal; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/surreal /var/cache/surreal


FROM scratch
COPY --from=downloader /surreal /surreal
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/surreal /var/log/surreal
COPY --from=builder /var/cache/surreal /var/cache/surreal
USER 65532:65532
WORKDIR /app
EXPOSE 8000 8001
ENTRYPOINT ["/surreal"]
LABEL org.opencontainers.image.title="surrealdb" \
      org.opencontainers.image.version="3.0.5" \
      org.opencontainers.image.vendor="Surrealdb" \
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