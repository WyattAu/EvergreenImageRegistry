FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apk add --no-cache python3 py3-pip ca-certificates
RUN pip install --break-system-packages --no-cache-dir zigpy 2>/dev/null || true
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin homekit 2>/dev/null || true
RUN mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM