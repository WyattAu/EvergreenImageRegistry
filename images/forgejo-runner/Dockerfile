ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=6.3.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://codeberg.org/forgejo/runner/releases/download/v${VERSION}/forgejo-runner-linux-${TARGETARCH}" \
    -o /tmp/forgejo-runner && \
    chmod +x /tmp/forgejo-runner && \
    strip /tmp/forgejo-runner || true
FROM scratch
COPY --from=downloader /tmp/forgejo-runner /usr/local/bin/forgejo-runner
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8088

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/forgejo-runner"]
CMD ["daemon"]
LABEL org.opencontainers.image.title="forgejo-runner" \
      org.opencontainers.image.description="Forgejo Act Runner - CI/CD runner for Forgejo" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Forgejo" \
      org.opencontainers.image.source="https://codeberg.org/forgejo/runner" \
      evergreen.image.tier="2" \
      evergreen.image.category="ci" \
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
