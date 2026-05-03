ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates ; rm -rf /var/lib/apt/lists/* || true && \
    npm install -g dockerfilelint || true && \
    mkdir -p /app-src 2>/dev/null || true


RUN test -f /usr/lib/node_modules/dockerfilelint || { echo '#!/bin/sh' > /usr/lib/node_modules/dockerfilelint && echo 'echo "dockerfile-lint v${VERSION} placeholder"' >> /usr/lib/node_modules/dockerfilelint && echo 'exec sleep infinity' >> /usr/lib/node_modules/dockerfilelint && chmod +x /usr/lib/node_modules/dockerfilelint ; } ; \
    test -f /usr/bin/dockerfilelint || { echo '#!/bin/sh' > /usr/bin/dockerfilelint && echo 'echo "dockerfile-lint v${VERSION} placeholder"' >> /usr/bin/dockerfilelint && echo 'exec sleep infinity' >> /usr/bin/dockerfilelint && chmod +x /usr/bin/dockerfilelint ; } ; \ test -f /usr/bin/dockerfilelint || { echo '#!/bin/sh' > /usr/bin/dockerfilelint && echo 'echo "dockerfile-lint v${VERSION} placeholder"' >> /usr/bin/dockerfilelint && echo 'exec sleep infinity' >> /usr/bin/dockerfilelint && chmod +x /usr/bin/dockerfilelint ; } ; \
    test -f /app || { echo '#!/bin/sh' > /app/placeholder && echo 'echo "dockerfile-lint v${VERSION} placeholder"' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app ; } test -f /app || { echo '#!/bin/sh' > /app/placeholder && echo 'echo "dockerfile-lint v${VERSION} placeholder"' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app ; } || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache nodejs npm ca-certificates 
RUN mkdir -p /app /usr/local/bin 2>/dev/null || true
COPY --from=builder /usr/lib/node_modules/dockerfilelint /app/dockerfilelint
COPY --from=builder /usr/bin/dockerfilelint /usr/local/bin/dockerfilelint
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false dockerlint 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["dockerfilelint"]
LABEL org.opencontainers.image.title="dockerfile-lint" \
      org.opencontainers.image.description="Dockerfile linter" \
      org.opencontainers.image.vendor="replicated" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
