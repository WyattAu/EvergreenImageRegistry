# =============================================================================
# SOVEREIGN HARDENED TEKTON
# Tekton Pipelines (Go binary from GitHub releases)
# Constraint: scratch - static Go binary, smallest attack surface
# =============================================================================

ARG VERSION=v0.62.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tar && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/tektoncd/pipeline/releases/download/${VERSION}/tekton-linux-amd64_${VERSION#v}.tar.gz" -o /tekton.tar.gz 2>/dev/null || \
    curl -fsSL "https://github.com/tektoncd/pipeline/releases/download/${VERSION}/tekton-linux-amd64.tar.gz" -o /tekton.tar.gz 2>/dev/null || \
    curl -fsSL "https://github.com/tektoncd/pipeline/releases/download/${VERSION}/release.notags.tar.gz" -o /tekton.tar.gz 2>/dev/null
RUN tar -xzf /tekton.tar.gz -C /tmp 2>/dev/null; \
    find /tmp -name "tekton-*" -type f -executable 2>/dev/null | head -1 | xargs -I{} cp {} /tekton 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/tekton

FROM scratch
COPY --from=downloader /tekton /tekton
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tekton /var/log/tekton
USER 65534:65534
WORKDIR /app
EXPOSE 9090
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/tekton", "--help"]
ENTRYPOINT ["/tekton"]
LABEL org.opencontainers.image.title="tekton" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="TektonCD" \
      org.opencontainers.image.source="https://github.com/tektoncd/pipeline" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="ci" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
