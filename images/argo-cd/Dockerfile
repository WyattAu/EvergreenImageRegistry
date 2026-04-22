ARG VERSION=v3.3.8
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/argoproj/argo-cd/releases/download/v3.3.8/argocd-linux-amd64" -o /argocd && \
    echo "11070d2502c5a51523f78388e23ddefb9151bd33f2faab955cde78a9c0d492e6  /argocd" | sha256sum -c - && \
    chmod +x /argocd && strip /argocd 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/argocd /var/cache/argocd /home/argocd

FROM scratch
COPY --from=downloader /argocd /argocd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/argocd /var/log/argocd
COPY --from=builder /var/cache/argocd /var/cache/argocd
COPY --from=builder /home/argocd /home/argocd
USER 65534:65534
WORKDIR /app
ENV HOME=/app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/argocd", "version"]
ENTRYPOINT ["/argocd"]
LABEL org.opencontainers.image.title="argo-cd" \
      org.opencontainers.image.version="3.3.8" \
      org.opencontainers.image.vendor="Argo Project" \
      org.opencontainers.image.description="Sovereign hardened argo-cd - GitOps CD tool" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
