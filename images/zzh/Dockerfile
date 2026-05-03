
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates 
RUN pip install --break-system-packages --no-cache-dir zigpy 2>/dev/null || true
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false zzh 2>/dev/null || true
RUN mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
