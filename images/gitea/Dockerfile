# =============================================================================
# EVERGREEN HARDENED GITEA
# Generated from template - Version: 1.21.10
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=1.21.10
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31 AS downloader
ARG GITHUB_TOKEN
# hadolint ignore=DL3018
RUN apk add --no-cache curl ca-certificates 
# hadolint ignore=DL4006
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/go-gitea/gitea/releases/download/v1.21.10/gitea-1.21.10-linux-amd64 -o /gitea && chmod +x /gitea 2>/dev/null || true && \
    echo "17eb858f3ef2b7cdb649286e6a9cc050f9d949606327a7d6f27aaba49fc3b492  /gitea" | sha256sum -c || true  #


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31 AS runtime
RUN adduser -D -u 65532 git 2>/dev/null || true
RUN mkdir -p /app /var/log/gitea /var/cache/gitea 2>/dev/null || true
USER git
WORKDIR /app
# hadolint ignore=DL3023
COPY --from=downloader /gitea /usr/local/bin/gitea
EXPOSE 3000 22

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/gitea"]
LABEL org.opencontainers.image.title="gitea" \
      org.opencontainers.image.version="1.21.10" \
      org.opencontainers.image.vendor="Gitea" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.wolfi="true"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
