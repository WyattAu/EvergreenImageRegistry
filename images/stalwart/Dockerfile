ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.16.2
ARG TARGETARCH
RUN mkdir -p /usr/local/bin/stalwart || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    TARGETVARIANT=$(case "${TARGETARCH}" in amd64) echo "x86_64";; arm64) echo "aarch64";; esac) && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/stalwartlabs/stalwart/releases/download/v${VERSION}/stalwart-${TARGETVARIANT}-unknown-linux-musl.tar.gz" \
    -o /tmp/stalwart.tar.gz && \
    tar -xzf /tmp/stalwart.tar.gz -C /tmp && \
    mv /tmp/stalwart /usr/local/bin/stalwart && \
    chmod +x /usr/local/bin/stalwart && \
    strip /usr/local/bin/stalwart || true
FROM scratch
COPY --from=downloader /usr/local/bin/stalwart /usr/local/bin/stalwart
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 25 143 465 587 993

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/stalwart"]
CMD ["mail"]
LABEL org.opencontainers.image.title="stalwart" \
      org.opencontainers.image.description="Stalwart Mail Server - all-in-one mail server written in Rust" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="stalwartlabs" \
      org.opencontainers.image.source="https://github.com/stalwartlabs/stalwart" \
      evergreen.image.tier="2" \
      evergreen.image.category="email" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
