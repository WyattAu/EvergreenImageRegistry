
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/aquasecurity/kube-bench/releases/download/v0.8.0/kube-bench_0.8.0_linux_${TARGETARCH}.tar.gz -o /kube-bench_0.8.0_linux_${TARGETARCH}.tar.gz &&     [ -f /kube-bench_0.8.0_linux_${TARGETARCH}.tar.gz ] && tar -xzf /kube-bench_0.8.0_linux_${TARGETARCH}.tar.gz -C / && rm -f /kube-bench_0.8.0_linux_${TARGETARCH}.tar.gz && chmod +x /kube-bench && \
    echo "8e8f083819678956b6c36623a6a0638741340397ffc209cd71a6b4907f2bb05e  /kube-bench_0.8.0_linux_${TARGETARCH}.tar.gz" | sha256sum -c && \
    strip /kube-bench 2>/dev/null && && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/kube-bench /var/cache/kube-bench 2>/dev/null || true


FROM scratch
COPY --from=downloader /kube-bench /kube-bench
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-bench /var/log/kube-bench
COPY --from=builder /var/cache/kube-bench /var/cache/kube-bench
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="kube-bench"       org.opencontainers.image.description="Kubernetes CIS benchmark"       org.opencontainers.image.vendor="aquasecurity"       org.opencontainers.image.source="https://github.com/aquasecurity/kube-bench"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="0.8.0"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/kube-bench"]
CMD ["--help"]
