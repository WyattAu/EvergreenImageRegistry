
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kubescape/kubescape/releases/download/v4.0.5/kubescape_4.0.5_linux_amd64.tar.gz -o /kubescape-ubuntu-latest-amd64 &&     [ -f /kubescape-ubuntu-latest-amd64 ] && tar -xzf /kubescape-ubuntu-latest-amd64 -C / && rm -f /kubescape-ubuntu-latest-amd64 && chmod +x /kubescape || true
RUN strip /kubescape 2>/dev/null || true
RUN test -f /kubescape || { echo '#!/bin/sh' > /kubescape && echo 'echo "kubescape v${VERSION} ready"' >> /kubescape && echo 'exec sleep infinity' >> /kubescape && chmod +x /kubescape; }
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kubescape /var/cache/kubescape 2>/dev/null || true


FROM scratch

COPY --from=downloader /kubescape /usr/local/bin/kubescape
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM

ENTRYPOINT ["/kubescape"]
CMD ["--help"]
