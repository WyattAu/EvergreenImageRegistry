# =============================================================================
# EVERGREEN HARDENED COURIER-AUTHLIB
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=0.71.4
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN groupadd -r -g 65532 appuser && useradd -r -u 65532 -g appuser -d /app -s /usr/bin/false appuser


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/courier-authlib /var/cache/courier-authlib && chown -R 65532:65532 /app /var/log/courier-authlib /var/cache/courier-authlib 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 0
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="2"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:0/ || exit 1
CMD ["/bin/sh"]
LABEL org.opencontainers.image.description="courier-authlib container image" \
      org.opencontainers.image.title="Courier Authlib" \
      org.opencontainers.image.source="https://github.com/courier-python/courier" \
            org.opencontainers.image.version="0.71.4"
