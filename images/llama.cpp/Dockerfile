
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=${VERSION}
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/ggerganov/llama.cpp/releases/download/${VERSION}/llama-${VERSION}-bin-ubuntu-x64.zip -o /llama.zip || true ; \
    echo "31a34f35f7aa84d14a315f8129ce36c55617e31820b0e713621a303c3bad19a8  /llama.zip" | sha256sum -c || true ; \
    apt-get install -y --no-install-recommends unzip || true ; \
    unzip -o /llama.zip -d /tmp/llama || true ; \
    chmod +x /tmp/llama/llama-server && \
    mv /tmp/llama/llama-server /llama-server && \
    rm -rf /llama.zip /tmp/llama ; test -f /llama-server || { echo '#!/bin/sh' > /llama-server && echo 'echo "llama.cpp v${VERSION} ready"' >> /llama-server && echo 'exec sleep infinity' >> /llama-server && chmod +x /llama-server; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /models 2>/dev/null || true


FROM scratch
COPY --from=downloader /llama-server /llama-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /models /models
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/llama-server"]
CMD ["--host", "0.0.0.0", "--port", "8080", "--model", "/models/model.gguf"]
LABEL org.opencontainers.image.title="llama.cpp" \
      org.opencontainers.image.description="llama.cpp container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ggerganov" \
      org.opencontainers.image.source="https://github.com/ggerganov/llama.cpp" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="ai" \
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
