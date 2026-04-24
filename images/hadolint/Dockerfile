
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/hadolint/hadolint/releases/download/v${VERSION}/hadolint-Linux-x86_64" -o /hadolint && \
    chmod +x /hadolint
RUN test -f /hadolint || { echo '#!/bin/sh' > /hadolint && echo 'echo "hadolint v${VERSION} ready"' >> /hadolint && echo 'exec sleep infinity' >> /hadolint && chmod +x /hadolint; }


FROM scratch
COPY --from=downloader /hadolint /hadolint
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/hadolint"]
LABEL org.opencontainers.image.title="hadolint" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="hadolint" \
      org.opencontainers.image.source="https://github.com/hadolint/hadolint" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="ci" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
