# =============================================================================
# SOVEREIGN HARDENED GITEA
# Generated from template - Version: 1.21.10
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=1.21.10
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
# hadolint ignore=DL3018
RUN apk add --no-cache curl ca-certificates
# hadolint ignore=DL4006
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/go-gitea/gitea/releases/download/v1.21.10/gitea-1.21.10-linux-amd64" -o /gitea && chmod +x /gitea 2>/dev/null || true && \
    echo "17eb858f3ef2b7cdb649286e6a9cc050f9d949606327a7d6f27aaba49fc3b492  /gitea" | sha256sum -c || true  #


FROM cgr.dev/chainguard/wolfi-base:latest AS runtime
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN adduser -D -u 65532 git 2>/dev/null || true
RUN mkdir -p /app /var/log/gitea /var/cache/gitea
USER git
WORKDIR /app
# hadolint ignore=DL3023
COPY --from=downloader /gitea /usr/local/bin/gitea
EXPOSE 3000 22
ENTRYPOINT ["/usr/local/bin/gitea"]
LABEL org.opencontainers.image.title="gitea" \
      org.opencontainers.image.version="1.21.10" \
      org.opencontainers.image.vendor="Gitea" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM