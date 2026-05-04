
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG TARGETARCH
RUN apk add --no-cache python3 ca-certificates git curl 
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false repo-security 2>/dev/null || true &&     mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
CMD ["/bin/sh"]
