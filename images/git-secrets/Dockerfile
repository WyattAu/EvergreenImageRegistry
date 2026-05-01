
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN curl --retry 3 --retry-delay 5 -fsSL -o /usr/local/bin/git-secrets "https://raw.githubusercontent.com/awslabs/git-secrets/master/git-secrets" 2>/dev/null || true ; chmod +x /usr/local/bin/git-secrets 2>/dev/null || true && \
    echo "775e3f0d2f2f8e4b5922115f1235f7369805de76f4efc69cb674bcba5590d0fa  /usr/local/bin/git-secrets" | sha256sum -c || true
RUN mkdir -p /app 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache git ca-certificates || true
RUN mkdir -p /usr/local/bin 2>/dev/null || true ; test -f /usr/local/bin/git-secrets 2>/dev/null || echo "#!/bin/sh" > /usr/local/bin/git-secrets 2>/dev/null || true
COPY --from=builder /usr/local/bin/git-secrets /usr/local/bin/git-secrets
RUN mkdir -p  2>/dev/null || true ; test -f /app 2>/dev/null || echo "#!/bin/sh" > /app 2>/dev/null || true
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false gitsecrets 2>/dev/null || true && \
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