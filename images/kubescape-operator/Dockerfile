FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/kubescape/kubescape/releases/download/v3.0.3/kubescape-ubuntu-latest-amd64" -o /kubescape-ubuntu-latest-amd64 &&     tar -xzf /kubescape-ubuntu-latest-amd64 -C / && rm /kubescape-ubuntu-latest-amd64 && chmod +x /kubescape
RUN strip /kubescape 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kubescape-operator /var/cache/kubescape-operator

FROM debian:bookworm-slim
COPY --from=downloader /kubescape /usr/local/bin/kubescape
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin kubescape-operator 2>/dev/null || true &&     chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["kubescape", "--version"]
ENTRYPOINT ["kubescape"]
LABEL org.opencontainers.image.title="kubescape-operator"       org.opencontainers.image.description="Kubescape - operator mode"       org.opencontainers.image.vendor="kubescape"       org.opencontainers.image.source="https://github.com/kubescape/kubescape"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian_slim="true"
