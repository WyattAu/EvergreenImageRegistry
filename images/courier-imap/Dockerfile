# =============================================================================
# SOVEREIGN HARDENED COURIER-IMAP
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=5.1.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65532 appuser && useradd -r -u 65532 -g appuser -d /app -s /usr/sbin/nologin appuser

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/courier-imap /var/cache/courier-imap && chown -R 65532:65532 /app /var/log/courier-imap /var/cache/courier-imap
USER 65532:65532
WORKDIR /app
EXPOSE 143 993
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM