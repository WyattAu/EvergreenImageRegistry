
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://raw.githubusercontent.com/awslabs/git-secrets/master/git-secrets" \
    -o /usr/local/bin/git-secrets && chmod +x /usr/local/bin/git-secrets
RUN mkdir -p /app


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache git ca-certificates
COPY --from=builder /usr/local/bin/git-secrets /usr/local/bin/git-secrets
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin gitsecrets 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["git-secrets"]
LABEL org.opencontainers.image.title="git-secrets" \
      org.opencontainers.image.description="AWS Git Secrets - prevent secret commits" \
      org.opencontainers.image.vendor="AWS Labs" \
      org.opencontainers.image.source="https://github.com/awslabs/git-secrets" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM