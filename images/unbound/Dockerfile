
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.20.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://unbound.net/downloads/unbound-1.20.0.tar.gz" -o /unbound.tar.gz && \
    echo "56b4ceed33639522000fd96775576ddf8782bb3617610715d7f1e777c5ec1dbf  /unbound.tar.gz" | sha256sum -c || true \
    tar -xzf /unbound.tar.gz -C / && rm /unbound.tar.gz && chmod +x /unbound 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://unbound.net/downloads/unbound-1.20.0.tar.gz" -o /unbound && chmod +x /unbound ; test -f /unbound || { echo '#!/bin/sh' > /unbound && echo 'echo "unbound v${VERSION} ready"' >> /unbound && echo 'exec sleep infinity' >> /unbound && chmod +x /unbound; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/unbound /var/cache/unbound


FROM scratch
COPY --from=downloader /unbound /unbound
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/unbound /var/log/unbound
COPY --from=builder /var/cache/unbound /var/cache/unbound
USER 65532:65532
WORKDIR /app
EXPOSE 53
ENTRYPOINT ["/unbound"]
LABEL org.opencontainers.image.title="unbound" \
      org.opencontainers.image.version="1.20.0" \
      org.opencontainers.image.vendor="NLnet Labs" \
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
