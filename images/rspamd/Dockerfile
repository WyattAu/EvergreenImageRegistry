# =============================================================================
# SOVEREIGN HARDENED RSPAMD
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=3.7
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN groupadd -r -g 65532 appuser && useradd -r -u 65532 -g appuser -d /app -s /usr/bin/false appuser


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates rspamd || true
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/rspamd /var/cache/rspamd && chown -R 65532:65532 /app /var/log/rspamd /var/cache/rspamd 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 11333 11334
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM

ENTRYPOINT ["rspamd"]
CMD ["-F", "--no-daemon"]
