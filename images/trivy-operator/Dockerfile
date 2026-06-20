







ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG VERSION=0.30.1







ARG TARGETARCH







RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/aquasecurity/trivy-operator/releases/download/v${VERSION}/trivy_operator_Linux_${TARGETARCH}.tar.gz -o /trivy-operator.tar.gz ; \
    echo "03aad0222b59bd5bfacc00505d01cdc41bed83fb0321ecc644e0d4680bd2f3dd  /trivy-operator.tar.gz" | sha256sum -c; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/aquasecurity/trivy-operator/releases/download/v${VERSION}/trivy_operator_Linux_${TARGETARCH}.tar.gz.sig -o /trivy-operator.sig && \
    [ -f /trivy-operator.tar.gz ] && tar -xzf /trivy-operator.tar.gz -C /tmp/ ; \
    strip --strip-all /tmp/trivy-operator 2>/dev/null&& \
    mv /tmp/trivy-operator /trivy-operator && \
    rm -rf /trivy-operator.tar.gz /trivy-operator.sig /tmp/* && { echo "Binary not available - download failed" >&2; exit 1; }































ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim







COPY --from=downloader /trivy-operator /trivy-operator







COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt







USER 65532:65532







WORKDIR /app















HEALTHCHECK NONE







ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/trivy-operator"]







LABEL org.opencontainers.image.title="trivy-operator" \
      org.opencontainers.image.description="trivy-operator container image" \
      org.opencontainers.image.version="0.30.1" \
      org.opencontainers.image.vendor="Aqua Security" \
      org.opencontainers.image.source="https://github.com/aquasecurity/trivy-operator" \
      evergreen.image.tier="2" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"















LABEL evergreen.base.image="scratch"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM
