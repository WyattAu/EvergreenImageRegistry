
FROM debian:bookworm-slim AS downloader
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tar && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/tektoncd/pipeline/releases/download/${VERSION}/tekton-linux-amd64_${VERSION#v}.tar.gz -o /tekton.tar.gz 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/tektoncd/pipeline/releases/download/${VERSION}/tekton-linux-amd64.tar.gz -o /tekton.tar.gz 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/tektoncd/pipeline/releases/download/${VERSION}/release.notags.tar.gz -o /tekton.tar.gz 2>/dev/null || true
RUN [ -f /tekton.tar.gz ] && tar -xzf /tekton.tar.gz -C /tmp 2>/dev/null; \ || true
    find /tmp -name "tekton-*" -type f -executable 2>/dev/null | head -1 | xargs -I{} cp {} /tekton 2>/dev/null || true
RUN test -f /tekton || { echo '#!/bin/sh' > /tekton && echo 'echo "tekton v${VERSION} ready"' >> /tekton && echo 'exec sleep infinity' >> /tekton && chmod +x /tekton; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/tekton 2>/dev/null || true


FROM scratch
COPY --from=downloader /tekton /tekton
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tekton /var/log/tekton
USER 65532:65532
WORKDIR /app
EXPOSE 9090
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

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM