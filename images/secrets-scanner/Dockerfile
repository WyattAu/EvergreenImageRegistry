FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends         python3 ca-certificates git curl     && rm -rf /var/lib/apt/lists/*
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin secrets-scanner 2>/dev/null || true &&     mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1     CMD ["python3", "-c", "print('ok')"]
ENTRYPOINT ["python3"]
CMD ["-c", "print('secrets-scanner: security tool placeholder')"]
LABEL org.opencontainers.image.title="secrets-scanner"       org.opencontainers.image.description="Placeholder - secrets-scanner"       sovereign.image.tier="3"       sovereign.image.status="placeholder"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian_slim="true"
