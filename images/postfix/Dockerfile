# =============================================================================
# SOVEREIGN HARDENED POSTFIX
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=3.7.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65532 appuser && useradd -r -u 65532 -g appuser -d /app -s /usr/sbin/nologin appuser

FROM cgr.dev/chainguard/wolfi-base:latest

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk add --no-cache ca-certificates postfix
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/postfix /var/cache/postfix && chown -R 65532:65532 /app /var/log/postfix /var/cache/postfix
USER 65532:65532
WORKDIR /app
EXPOSE 25
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM