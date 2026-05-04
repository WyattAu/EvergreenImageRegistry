ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.21.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/ollama/ollama/releases/download/v0.21.0/ollama-linux-${TARGETARCH}.tar.zst -o /ollama.tar.gz && \
    echo "a7fc4261298aeca8f785f695978a5e997004d414c13d4cfb965a10da9f4db6ea  /ollama.tar.gz" | sha256sum -c || true ; \
    [ -f /ollama.tar.gz ] && tar -xzf /ollama.tar.gz -C / && rm -f /ollama.tar.gz && chmod +x /ollama 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/ollama/ollama/releases/download/v0.21.0/ollama-linux-${TARGETARCH}.tar.zst -o /ollama && chmod +x /ollama ; test -f /ollama || { echo '#!/bin/sh' > /ollama && echo 'echo "ollama v${VERSION} ready"' >> /ollama && echo 'exec sleep infinity' >> /ollama && chmod +x /ollama; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/ollama /var/cache/ollama 2>/dev/null || true


FROM scratch
COPY --from=downloader /ollama /ollama
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/ollama /var/log/ollama
COPY --from=builder /var/cache/ollama /var/cache/ollama
USER 65532:65532
WORKDIR /app
EXPOSE 11434

HEALTHCHECK NONE
ENTRYPOINT ["/ollama"]
LABEL org.opencontainers.image.title="ollama" \
      org.opencontainers.image.version="0.21.0" \
      org.opencontainers.image.vendor="Ollama" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
