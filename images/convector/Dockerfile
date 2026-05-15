FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=1.0.0
ARG TARGETARCH
RUN apk add --no-cache nodejs-20 npm ca-certificates || true && \
    npm install -g @worldsibu/convector-platform@${VERSION} 2>/dev/null || true && \
    addgroup -S -g 10000 convector 2>/dev/null || true && \
    adduser -u 65532 -G convector -D -h /app -s /bin/false convector 2>/dev/null || true && \
    mkdir -p /app /var/log/convector 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/convector 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV NODE_ENV="production"
EXPOSE 8008

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8008/ || exit 1
ENTRYPOINT ["node"]
CMD []
LABEL org.opencontainers.image.title="convector" \
      org.opencontainers.image.description="Convector - smart contract framework tools" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="worldsibu" \
      org.opencontainers.image.source="https://github.com/worldsibu/convector-platform" \
      evergreen.image.tier="3" \
      evergreen.image.category="blockchain" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
