# =============================================================================
# EVERGREEN HARDENED SPAMASSASSIN
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=4.0.0
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN groupadd -r -g 65532 appuser && useradd -r -u 65532 -g appuser -d /app -s /usr/bin/false appuser


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates 
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/spamassassin /var/cache/spamassassin && chown -R 65532:65532 /app /var/log/spamassassin /var/cache/spamassassin 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 783
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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:783/ || exit 1

LABEL org.opencontainers.image.description="spamassassin container image" \
      org.opencontainers.image.title="SpamAssassin" \
      org.opencontainers.image.source="https://github.com/apache/spamassassin" \
            org.opencontainers.image.version="4.0.0"

ENTRYPOINT ["spamassassin"]
CMD ["-d"]
