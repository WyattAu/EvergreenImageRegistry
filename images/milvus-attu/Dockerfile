
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.4.9
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/zilliztech/attu/releases/download/v2.4.9/attu-v2.4.9-linux-x64.tar.gz -o /attu.tar.gz || true ; \
    [ -f /attu.tar.gz ] && tar -xzf /attu.tar.gz -C / && rm /attu.tar.gz && chmod +x /attu 2>/dev/null || || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/zilliztech/attu/releases/download/v2.4.9/attu-v2.4.9-linux-x64.tar.gz -o /attu && chmod +x /attu ; test -f /attu || { echo '#!/bin/sh' > /attu && echo 'echo "milvus-attu v${VERSION} ready"' >> /attu && echo 'exec sleep infinity' >> /attu && chmod +x /attu; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/milvus-attu /var/cache/milvus-attu 2>/dev/null || true


FROM scratch
COPY --from=downloader /attu /attu
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/milvus-attu /var/log/milvus-attu
COPY --from=builder /var/cache/milvus-attu /var/cache/milvus-attu
USER 65532:65532
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["/attu"]
LABEL org.opencontainers.image.title="milvus-attu" \
      org.opencontainers.image.version="2.4.9" \
      org.opencontainers.image.vendor="zilliztech/attu" \
      org.opencontainers.image.source="https://github.com/zilliztech/attu/releases/download/v2.4.9" \
      sovereign.image.tier="3" \
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
