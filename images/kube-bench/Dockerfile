FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/aquasecurity/kube-bench/releases/download/v0.8.0/kube-bench_0.8.0_linux_amd64.tar.gz" -o /kube-bench_0.8.0_linux_amd64.tar.gz &&     tar -xzf /kube-bench_0.8.0_linux_amd64.tar.gz -C / && rm /kube-bench_0.8.0_linux_amd64.tar.gz && chmod +x /kube-bench
RUN strip /kube-bench 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-bench /var/cache/kube-bench

FROM scratch
COPY --from=downloader /kube-bench /kube-bench
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-bench /var/log/kube-bench
COPY --from=builder /var/cache/kube-bench /var/cache/kube-bench
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="kube-bench"       org.opencontainers.image.description="Kubernetes CIS benchmark"       org.opencontainers.image.vendor="aquasecurity"       org.opencontainers.image.source="https://github.com/aquasecurity/kube-bench"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM