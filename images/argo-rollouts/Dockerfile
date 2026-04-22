ARG VERSION=v1.9.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/argoproj/argo-rollouts/releases/download/v1.9.0/kubectl-argo-rollouts-linux-amd64" -o /kubectl-argo-rollouts && \
    echo "d1c98f59f6d3716b7a35aa540506764700a358448dd6a10e92381b7aa294d00b  /kubectl-argo-rollouts" | sha256sum -c - && \
    chmod +x /kubectl-argo-rollouts && strip /kubectl-argo-rollouts

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/argo-rollouts /var/cache/argo-rollouts

FROM scratch
COPY --from=downloader /kubectl-argo-rollouts /kubectl-argo-rollouts
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/argo-rollouts /var/log/argo-rollouts
COPY --from=builder /var/cache/argo-rollouts /var/cache/argo-rollouts
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/kubectl-argo-rollouts", "version"]
ENTRYPOINT ["/kubectl-argo-rollouts"]
LABEL org.opencontainers.image.title="argo-rollouts" \
      org.opencontainers.image.version="1.9.0" \
      org.opencontainers.image.vendor="Argo Project" \
      org.opencontainers.image.description="Sovereign hardened argo-rollouts - progressive delivery" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"
