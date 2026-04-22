FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache curl ca-certificates
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin transfer 2>/dev/null || true && \
    mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["echo"]
CMD ["transferhelper: transfer file helper utility"]
LABEL org.opencontainers.image.title="transferhelper" \
      org.opencontainers.image.description="Placeholder - Transfer helper utility" \
      sovereign.image.tier="3" \
      sovereign.image.status="placeholder" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM