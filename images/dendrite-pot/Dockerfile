ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.13.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/element-hq/dendrite/releases/download/v${VERSION}/dendrite-monolith-linux-${TARGETARCH}" \
    -o /tmp/dendrite && \
    chmod +x /tmp/dendrite && \
    strip /tmp/dendrite
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=0.13.1
RUN apk add --no-cache ca-certificates || true && \
    addgroup -S -g 10000 dendrite 2>/dev/null || true && \
    adduser -u 65532 -G dendrite -D -h /app -s /bin/false dendrite 2>/dev/null || true
COPY --from=downloader /tmp/dendrite /usr/local/bin/dendrite
RUN mkdir -p /app 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8008

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8008/ || exit 1
ENTRYPOINT ["/usr/local/bin/dendrite"]
CMD ["--config=/app/dendrite.yaml"]
LABEL org.opencontainers.image.title="dendrite-pot" \
      org.opencontainers.image.description="Dendrite POT - Polylith OUTBOX Trusted worker for Dendrite" \
      org.opencontainers.image.version="0.13.1" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/dendrite" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
