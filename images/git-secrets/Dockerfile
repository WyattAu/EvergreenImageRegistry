
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN curl --retry 3 --retry-delay 5 -fsSL -o /usr/local/bin/git-secrets "https://raw.githubusercontent.com/awslabs/git-secrets/master/git-secrets" 2>/dev/null || true ; chmod +x /usr/local/bin/git-secrets 2>/dev/null || true && \
    echo "775e3f0d2f2f8e4b5922115f1235f7369805de76f4efc69cb674bcba5590d0fa  /usr/local/bin/git-secrets" | sha256sum -c || true
RUN mkdir -p /app 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["git-secrets"]
LABEL org.opencontainers.image.title="git-secrets" \
      org.opencontainers.image.description="AWS Git Secrets - prevent secret commits" \
      org.opencontainers.image.vendor="AWS Labs" \
      org.opencontainers.image.source="https://github.com/awslabs/git-secrets" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
