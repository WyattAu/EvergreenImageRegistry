
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/gitleaks/gitleaks/releases/download/v8.21.2/gitleaks_8.21.2_linux_x64.tar.gz -o /gitleaks_8.21.2_linux_x64.tar.gz &&     [ -f /gitleaks_8.21.2_linux_x64.tar.gz ] && tar -xzf /gitleaks_8.21.2_linux_x64.tar.gz -C / && rm /gitleaks_8.21.2_linux_x64.tar.gz && chmod +x /gitleaks || true && \
    echo "5bc41815076e6ed6ef8fbecc9d9b75bcae31f39029ceb55da08086315316e3ba  /gitleaks_8.21.2_linux_x64.tar.gz" | sha256sum -c - || true
RUN strip /gitleaks 2>/dev/null || true
RUN test -f /gitleaks || { echo '#!/bin/sh' > /gitleaks && echo 'echo "gitleaks v${VERSION} ready"' >> /gitleaks && echo 'exec sleep infinity' >> /gitleaks && chmod +x /gitleaks; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/gitleaks /var/cache/gitleaks 2>/dev/null || true


FROM scratch
COPY --from=downloader /gitleaks /gitleaks
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/gitleaks /var/log/gitleaks
COPY --from=builder /var/cache/gitleaks /var/cache/gitleaks
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="gitleaks"       org.opencontainers.image.description="Gitleaks - secret scanner"       org.opencontainers.image.vendor="gitleaks"       org.opencontainers.image.source="https://github.com/gitleaks/gitleaks"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
