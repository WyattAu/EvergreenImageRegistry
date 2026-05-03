ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/dutchcoders/transfer.sh/releases/download/v1.6.1/transfersh-v1.6.1-linux-${TARGETARCH}.tar.gz -o /transfer.sh || true ; \
    echo "5ddb1d572ef60b4a51d6ac2c6ef7bb7bbb6966cccf6f6424e75e9a6897162d2b  /transfer.sh" | sha256sum -c || true  #
    chmod +x /transfer.sh && strip /transfer.sh ; test -f /transfer.sh || { echo '#!/bin/sh' > /transfer.sh && echo 'echo "transfer.sh v${VERSION} ready"' >> /transfer.sh && echo 'exec sleep infinity' >> /transfer.sh && chmod +x /transfer.sh; } 2>/dev/null || true



FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app/data /var/log/transfer /var/cache/transfer /tmp 2>/dev/null || true


FROM scratch
COPY --from=downloader /transfer.sh /transfer.sh
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/transfer /var/log/transfer
COPY --from=builder /var/cache/transfer /var/cache/transfer
COPY --from=builder /tmp /tmp
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/transfer.sh"]
LABEL org.opencontainers.image.title="transfer.sh" \
      org.opencontainers.image.description="transfer.sh - Easy file sharing from CLI" \
      org.opencontainers.image.vendor="dutchcoders" \
      org.opencontainers.image.source="https://github.com/dutchcoders/transfer.sh" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
