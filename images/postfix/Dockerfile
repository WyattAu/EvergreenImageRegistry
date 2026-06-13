# =============================================================================
# EVERGREEN HARDENED POSTFIX
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=3.7.6
ARG BUILD_DATE

ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN groupadd -r -g 65532 appuser && useradd -r -u 65532 -g appuser -d /app -s /usr/bin/false appuser


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates postfix
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/postfix /var/cache/postfix && chown -R 65532:65532 /app /var/log/postfix /var/cache/postfix 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 25
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="2"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM


LABEL org.opencontainers.image.description="postfix container image" \
      org.opencontainers.image.title="Postfix" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://github.com/VernonDGodfrey/postfix" \
            org.opencontainers.image.version="3.7.6"

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:25"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "postfix", "--", "start-fg"]
