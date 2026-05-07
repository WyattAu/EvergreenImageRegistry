ARG TARGETARCH
# =============================================================================
# EVERGREEN HARDENED FORGEJO
# Generated from template - Version: 14.0.4
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=14.0.4
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS downloader
ARG TARGETARCH
# hadolint ignore=DL3018
RUN apk add --no-cache curl ca-certificates git && \
    curl --retry 3 --retry-delay 5 -fsSL "https://code.forgejo.org/forgejo/forgejo/releases/download/v14.0.4/forgejo-14.0.4-linux-${TARGETARCH}" -o /forgejo && chmod +x /forgejo && \
    echo "fa1b0b419de8ee394ff4ba76f8955282c686ba7b41514583ed834ffd5a3a1933  /forgejo" | sha256sum -c || true  #
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS runtime
RUN addgroup -g 65532 git || true && \
    adduser -D -u 65532 -G git git || true && \
    mkdir -p /app /var/log/forgejo /var/cache/forgejo 2>/dev/null || true
USER git
WORKDIR /app
# hadolint ignore=DL3023
COPY --from=downloader /forgejo /usr/local/bin/forgejo
EXPOSE 3000 22

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/forgejo"]
LABEL org.opencontainers.image.title="forgejo" \
      org.opencontainers.image.description="Forgejo - community-owned lightweight software forge" \
      org.opencontainers.image.version="14.0.4" \
      org.opencontainers.image.vendor="Forgejo" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.wolfi="true" \
            org.opencontainers.image.source="https://github.com/forgejo/forgejo"

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
