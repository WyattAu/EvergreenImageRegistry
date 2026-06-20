ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532















FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG TARGETARCH







RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/aquasecurity/trivy/releases/download/v0.70.0/trivy_0.70.0_Linux-64bit.tar.gz -o /trivy_0.58.2_linux-${TARGETARCH}.tar.gz &&     [ -f /trivy_0.58.2_linux-${TARGETARCH}.tar.gz ] && tar -xzf /trivy_0.58.2_linux-${TARGETARCH}.tar.gz -C / && rm -f /trivy_0.58.2_linux-${TARGETARCH}.tar.gz && chmod +x /trivy; \
    echo "8b4376d5d6befe5c24d503f10ff136d9e0c49f9127a4279fd110b727929a5aa9  /trivy_0.58.2_linux-${TARGETARCH}.tar.gz" | sha256sum -c  #







RUN strip /trivy 2>/dev/null \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true && \
    [ -f /trivy ] || { echo '#!/bin/sh' > /trivy ; echo 'echo "trivy-iac v${VERSION} binary not available - download failed" >&2"' >> /trivy ; echo 'exit 1' >> /trivy ; chmod +x /trivy 2>/dev/null ; } 2>/dev/null && \
    [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "trivy-iac v${VERSION} binary not available - download failed" >&2"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exit 1' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null ; } 2>/dev/null && \
    [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "trivy-iac v${VERSION} binary not available - download failed" >&2"' >> /app ; echo 'exit 1' >> /app ; chmod +x /app 2>/dev/null ; } 2>/dev/null







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







ARG TARGETARCH







RUN mkdir -p /app /var/log/trivy-iac /var/cache/trivy-iac 2>/dev/null || true























ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim















COPY --from=downloader /trivy /usr/local/bin/trivy







COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt







COPY --from=builder /app /app







USER 65532:65532







WORKDIR /app







LABEL evergreen.base.image="scratch"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"







LABEL evergreen.image.tier="2"















EXPOSE 9101







STOPSIGNAL SIGTERM















HEALTHCHECK NONE















LABEL org.opencontainers.image.description="trivy-iac container image" \
      org.opencontainers.image.title="Trivy IaC" \
      org.opencontainers.image.source="https://github.com/aquasecurity/trivy" \
            org.opencontainers.image.version="0.70.0"















ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/trivy"]







CMD ["--help"]
