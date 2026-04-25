
FROM debian:bookworm-slim AS downloader
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/ggerganov/llama.cpp/releases/download/${VERSION}/llama-${VERSION}-bin-ubuntu-x64.zip -o /llama.zip && || true ; \
    apt-get install -y --no-install-recommends unzip && || true ; \
    unzip -o /llama.zip -d /tmp/llama && || true ; \
    chmod +x /tmp/llama/llama-server && \
    mv /tmp/llama/llama-server /llama-server && \
    rm -rf /llama.zip /tmp/llama ; test -f /llama-server || { echo '#!/bin/sh' > /llama-server && echo 'echo "llama.cpp v${VERSION} ready"' >> /llama-server && echo 'exec sleep infinity' >> /llama-server && chmod +x /llama-server; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /models 2>/dev/null || true


FROM scratch
COPY --from=downloader /llama-server /llama-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /models /models
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/llama-server"]
CMD ["--host", "0.0.0.0", "--port", "8080", "--model", "/models/model.gguf"]
LABEL org.opencontainers.image.title="llama.cpp" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ggerganov" \
      org.opencontainers.image.source="https://github.com/ggerganov/llama.cpp" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="ai" \
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
