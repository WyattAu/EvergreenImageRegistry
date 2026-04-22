FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache python3 ca-certificates git curl
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin repo-supervisor 2>/dev/null || true &&     mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
CMD ["-c", "print('repo-supervisor: security tool placeholder')"]

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM