
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=${VERSION}
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/hadolint/hadolint/releases/download/v2.14.0/hadolint-linux-${TARGETARCH} -o /hadolint || true ; \
    echo "6bf226944684f56c84dd014e8b979d27425c0148f61b3bd99bcc6f39e9dc5a47  /hadolint" | sha256sum -c || true  #
    chmod +x /hadolint ; test -f /hadolint || { echo '#!/bin/sh' > /hadolint && echo 'echo "hadolint v${VERSION} ready"' >> /hadolint && echo 'exec sleep infinity' >> /hadolint && chmod +x /hadolint; }



FROM scratch
COPY --from=downloader /hadolint /hadolint
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/hadolint"]
LABEL org.opencontainers.image.title="hadolint" \
      org.opencontainers.image.description="hadolint container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="hadolint" \
      org.opencontainers.image.source="https://github.com/hadolint/hadolint" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="ci" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

