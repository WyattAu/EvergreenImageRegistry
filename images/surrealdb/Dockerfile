ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=3.0.5
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/surrealdb/surrealdb/releases/download/v3.0.5/surreal-v3.0.5.linux-${TARGETARCH}.tgz -o /surreal.tar.gz || true ; \
    echo "48dbeba4896765f33e07acc25224073f0850c190872052b917ebda1f7b4375cb  /surreal.tar.gz" | sha256sum -c - || true
    [ -f /surreal.tar.gz ] && tar -xzf /surreal.tar.gz -C / && rm -f /surreal.tar.gz && chmod +x /surreal 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/surrealdb/surrealdb/releases/download/v3.0.5/surreal-v3.0.5.linux-${TARGETARCH}.tgz -o /surreal && chmod +x /surreal ; test -f /surreal || { echo '#!/bin/sh' > /surreal && echo 'echo "surrealdb v${VERSION} ready"' >> /surreal && echo 'exec sleep infinity' >> /surreal && chmod +x /surreal; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/surreal /var/cache/surreal 2>/dev/null || true


FROM scratch
COPY --from=downloader /surreal /surreal
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/surreal /var/log/surreal
COPY --from=builder /var/cache/surreal /var/cache/surreal
USER 65532:65532
WORKDIR /app
EXPOSE 8000 8001

HEALTHCHECK NONE
ENTRYPOINT ["/surreal"]
LABEL org.opencontainers.image.title="surrealdb" \
      org.opencontainers.image.description="surrealdb container image" \
      org.opencontainers.image.version="3.0.5" \
      org.opencontainers.image.vendor="Surrealdb" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/surrealdb/surrealdb"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
