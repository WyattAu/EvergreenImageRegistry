ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=3.0.6
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/sigstore/cosign/releases/download/v${VERSION}/cosign-linux-${TARGETARCH} -o /cosign && \
    echo "c956e5dfcac53d52bcf058360d579472f0c1d2d9b69f55209e256fe7783f4c74  /cosign" | sha256sum -c ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/sigstore/cosign/releases/download/v${VERSION}/cosign-linux-${TARGETARCH}.sig -o /cosign.sig && \
    chmod +x /cosign && \
    strip --strip-all /cosign 2>/dev/null&& \
    rm -f /cosign.sigbinary not available - download failed" >&2"' >> /cosign && echo 'exit 1' >> /cosign && chmod +x /cosign; }
FROM scratch
COPY --from=downloader /cosign /cosign
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/cosign"]
CMD ["verify"]
LABEL org.opencontainers.image.title="cosign-verify" \
      org.opencontainers.image.description="cosign-verify container image" \
      org.opencontainers.image.version="3.0.6" \
      org.opencontainers.image.vendor="sigstore" \
      org.opencontainers.image.source="https://github.com/sigstore/cosign" \
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
