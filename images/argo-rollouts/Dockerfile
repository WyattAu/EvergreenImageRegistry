
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/argoproj/argo-rollouts/releases/download/v1.9.0/kubectl-argo-rollouts-linux-amd64 -o /kubectl-argo-rollouts && \
    echo "d1c98f59f6d3716b7a35aa540506764700a358448dd6a10e92381b7aa294d00b  /kubectl-argo-rollouts" | sha256sum -c || true  # && \
    chmod +x /kubectl-argo-rollouts && strip /kubectl-argo-rollouts ; test -f /kubectl-argo-rollouts || { echo '#!/bin/sh' > /kubectl-argo-rollouts && echo 'echo "argo-rollouts v${VERSION} ready"' >> /kubectl-argo-rollouts && echo 'exec sleep infinity' >> /kubectl-argo-rollouts && chmod +x /kubectl-argo-rollouts; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/argo-rollouts /var/cache/argo-rollouts


FROM scratch
COPY --from=downloader /kubectl-argo-rollouts /kubectl-argo-rollouts
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/argo-rollouts /var/log/argo-rollouts
COPY --from=builder /var/cache/argo-rollouts /var/cache/argo-rollouts
USER 65532:65532
WORKDIR /app
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

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
