FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin rblake 2>/dev/null || true && \
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

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM