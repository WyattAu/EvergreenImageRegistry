# =============================================================================
# SOVEREIGN HARDENED FORGEJO
# Generated from template - Version: 14.0.4
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=14.0.4
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:20240415 AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
# hadolint ignore=DL3018
RUN apk add --no-cache curl ca-certificates git
# hadolint ignore=DL4006
RUN curl -fsSL "https://code.forgejo.org/forgejo/forgejo/releases/download/v14.0.4/forgejo-14.0.4-linux-amd64" -o /forgejo && chmod +x /forgejo && \
    echo "fa1b0b419de8ee394ff4ba76f8955282c686ba7b41514583ed834ffd5a3a1933  /forgejo" | sha256sum -c -

FROM cgr.dev/chainguard/wolfi-base:20240415 AS runtime
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN addgroup -g 65534 git || true
RUN adduser -D -u 65534 -G git git || true
RUN mkdir -p /app /var/log/forgejo /var/cache/forgejo
USER git
WORKDIR /app
# hadolint ignore=DL3023
COPY --from=downloader /forgejo /usr/local/bin/forgejo
EXPOSE 3000 22
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/local/bin/forgejo --version
ENTRYPOINT ["/usr/local/bin/forgejo"]
LABEL org.opencontainers.image.title="forgejo" \
      org.opencontainers.image.version="14.0.4" \
      org.opencontainers.image.vendor="Forgejo" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
