FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache python3 ca-certificates
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin rblake 2>/dev/null || true && \
    mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["-c", "print('rblake: security tool placeholder')"]
LABEL org.opencontainers.image.title="rblake" \
      org.opencontainers.image.description="Placeholder - rblake" \
      sovereign.image.tier="3" \
      sovereign.image.status="placeholder" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM