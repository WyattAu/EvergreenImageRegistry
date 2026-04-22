FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://raw.githubusercontent.com/awslabs/git-secrets/master/git-secrets" \
    -o /usr/local/bin/git-secrets && chmod +x /usr/local/bin/git-secrets
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/bin/git-secrets /usr/local/bin/git-secrets
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin gitsecrets 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["git-secrets", "--version"] || exit 0
ENTRYPOINT ["git-secrets"]
LABEL org.opencontainers.image.title="git-secrets" \
      org.opencontainers.image.description="AWS Git Secrets - prevent secret commits" \
      org.opencontainers.image.vendor="AWS Labs" \
      org.opencontainers.image.source="https://github.com/awslabs/git-secrets" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
