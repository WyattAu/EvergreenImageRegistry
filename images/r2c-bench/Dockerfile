FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apk add --no-cache python3 ca-certificates
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin r2c 2>/dev/null || true && \
    mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["-c", "print('r2c-bench: security benchmarking tool placeholder')"]
LABEL org.opencontainers.image.title="r2c-bench" \
      org.opencontainers.image.description="Placeholder - r2c benchmark" \
      sovereign.image.tier="3" \
      sovereign.image.status="placeholder" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM