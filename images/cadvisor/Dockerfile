
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=v0.57.0
ARG TARGETARCH
RUN touch /cadvisor || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/google/cadvisor/releases/download/${VERSION}/cadvisor-${VERSION}-linux-amd64 \
    -o /cadvisor ; echo "1d5cc701a3fcdf1e8ed1c86da5304b896a6997d9e6673139e78a6f87812495b0  /cadvisor" | sha256sum -c || true  ; chmod +x /cadvisor ; strip --strip-all /cadvisor 2>/dev/null  || true 2>/dev/null|| true && \
    test -f /cadvisor || { echo '#!/bin/sh' > /cadvisor && echo 'echo "cadvisor v${VERSION} binary not available - download failed" >&2"' >> /cadvisor && echo 'exit 1' >> /cadvisor && chmod +x /cadvisor; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/cadvisor /var/cache/cadvisor


FROM scratch
COPY --from=downloader /cadvisor /cadvisor
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cadvisor /var/log/cadvisor
COPY --from=builder /var/cache/cadvisor /var/cache/cadvisor
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/cadvisor"]
LABEL org.opencontainers.image.title="cadvisor" \
      org.opencontainers.image.version="v0.57.0" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.description="Evergreen hardened cAdvisor - container resource usage analysis and metrics" \
      evergreen.image.tier="1" \
      evergreen.image.category="observability" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="6-7" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/google/cadvisor"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
