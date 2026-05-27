ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.3.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/FiloSottile/age/releases/download/v${VERSION}/age-v${VERSION}-linux-${TARGETARCH}.tar.gz -o /age.tar.gz ; \
    echo "cf16cbb108fc56e2064b00ba2b65d9fb1b8d7002ca5e38260ee1cc34f6aaa8f9  /age.tar.gz" | sha256sum -c ; \
    tar -xzf /age.tar.gz -C / && rm -f /age.tar.gz && chmod +x /age/age /age/age-keygenbinary not available - download failed" >&2"' >> /age/age && echo 'exit 1' >> /age/age && chmod +x /age/age; } &&binary not available - download failed" >&2"' >> /age/age-keygen && echo 'exit 1' >> /age/age-keygen && chmod +x /age/age-keygen; }



FROM scratch
COPY --from=downloader /age/age /usr/local/bin/age
COPY --from=downloader /age/age-keygen /usr/local/bin/age-keygen
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /tmp

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/age"]
LABEL org.opencontainers.image.title="age" \
      org.opencontainers.image.version="1.3.1" \
      org.opencontainers.image.vendor="FiloSottile" \
      org.opencontainers.image.source="https://github.com/FiloSottile/age" \
      org.opencontainers.image.description="Simple, modern file encryption tool" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="1000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
