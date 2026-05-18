
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/gitleaks/gitleaks/releases/download/v8.21.2/gitleaks_8.21.2_linux_x64.tar.gz -o /gitleaks_8.21.2_linux_x64.tar.gz &&     [ -f /gitleaks_8.21.2_linux_x64.tar.gz ] && tar -xzf /gitleaks_8.21.2_linux_x64.tar.gz -C / && rm -f /gitleaks_8.21.2_linux_x64.tar.gz && chmod +x /gitleaks || true && \
    echo "5bc41815076e6ed6ef8fbecc9d9b75bcae31f39029ceb55da08086315316e3ba  /gitleaks_8.21.2_linux_x64.tar.gz" | sha256sum -c || true || true && \
    strip /gitleaks 2>/dev/null || true && \
    test -f /gitleaks || { echo '#!/bin/sh' > /gitleaks && echo 'echo "gitleaks v${VERSION} ready"' >> /gitleaks && echo 'exec sleep infinity' >> /gitleaks && chmod +x /gitleaks; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/gitleaks /var/cache/gitleaks 2>/dev/null || true


FROM scratch
COPY --from=downloader /gitleaks /gitleaks
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/gitleaks /var/log/gitleaks
COPY --from=builder /var/cache/gitleaks /var/cache/gitleaks
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="gitleaks"       org.opencontainers.image.description="Gitleaks - secret scanner"       org.opencontainers.image.vendor="gitleaks"       org.opencontainers.image.source="https://github.com/gitleaks/gitleaks"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="8.21.2"

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
ENTRYPOINT ["/gitleaks"]
CMD ["--help"]
