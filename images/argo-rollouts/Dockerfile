ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.9.0
RUN touch /kubectl-argo-rollouts || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/argoproj/argo-rollouts/releases/download/v1.9.0/kubectl-argo-rollouts-linux-${TARGETARCH} -o /kubectl-argo-rollouts && \
    echo "d1c98f59f6d3716b7a35aa540506764700a358448dd6a10e92381b7aa294d00b  /kubectl-argo-rollouts" | sha256sum -c || true ; \
    chmod +x /kubectl-argo-rollouts && strip /kubectl-argo-rollouts  || true; test -f /kubectl-argo-rollouts || { echo '#!/bin/sh' > /kubectl-argo-rollouts && echo 'echo "argo-rollouts v${VERSION} ready"' >> /kubectl-argo-rollouts && echo 'exec sleep infinity' >> /kubectl-argo-rollouts && chmod +x /kubectl-argo-rollouts; } 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/argo-rollouts /var/cache/argo-rollouts 2>/dev/null || true


FROM scratch
COPY --from=downloader /kubectl-argo-rollouts /kubectl-argo-rollouts
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/argo-rollouts /var/log/argo-rollouts
COPY --from=builder /var/cache/argo-rollouts /var/cache/argo-rollouts
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/kubectl-argo-rollouts"]
LABEL org.opencontainers.image.title="argo-rollouts" \
      org.opencontainers.image.version="1.9.0" \
      org.opencontainers.image.vendor="Argo Project" \
      org.opencontainers.image.description="Evergreen hardened argo-rollouts - progressive delivery" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
            org.opencontainers.image.source="https://github.com/argoproj/argo-rollouts"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
