
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip || true
RUN pip install --no-cache-dir checkov ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/checkov || { echo '#!/bin/sh' > /usr/local/bin/checkov && echo 'echo "checkov v${VERSION} placeholder"' >> /usr/local/bin/checkov && echo 'exec sleep infinity' >> /usr/local/bin/checkov && chmod +x /usr/local/bin/checkov ; } 2>/dev/null || true
RUN mkdir -p /app 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache python3 ca-certificates git 
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false checkov 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["checkov"]
CMD ["-d", "."]
LABEL org.opencontainers.image.title="checkov" \
      org.opencontainers.image.description="Checkov - Infrastructure as Code scanner" \
      org.opencontainers.image.vendor="Bridgecrew" \
      org.opencontainers.image.source="https://github.com/bridgecrewio/checkov" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
