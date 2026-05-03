# =============================================================================
# EVERGREEN HARDENED POSTFIX
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=3.7.6
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN groupadd -r -g 65532 appuser && useradd -r -u 65532 -g appuser -d /app -s /usr/bin/false appuser


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates postfix || true
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/postfix /var/cache/postfix && chown -R 65532:65532 /app /var/log/postfix /var/cache/postfix 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 25
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:25/ || exit 1
ENTRYPOINT ["postfix"]
CMD ["start-fg"]
