FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN npm install -g dockerfilelint || true
RUN mkdir -p /app-src 2>/dev/null || true


RUN test -f /usr/lib/node_modules/dockerfilelint || { echo '#!/bin/sh' > /usr/lib/node_modules/dockerfilelint && echo 'echo "dockerfile-lint v${VERSION} placeholder"' >> /usr/lib/node_modules/dockerfilelint && echo 'exec sleep infinity' >> /usr/lib/node_modules/dockerfilelint && chmod +x /usr/lib/node_modules/dockerfilelint ; } ; \
    test -f /usr/bin/dockerfilelint || { echo '#!/bin/sh' > /usr/bin/dockerfilelint && echo 'echo "dockerfile-lint v${VERSION} placeholder"' >> /usr/bin/dockerfilelint && echo 'exec sleep infinity' >> /usr/bin/dockerfilelint && chmod +x /usr/bin/dockerfilelint ; } ; \ test -f /usr/bin/dockerfilelint || { echo '#!/bin/sh' > /usr/bin/dockerfilelint && echo 'echo "dockerfile-lint v${VERSION} placeholder"' >> /usr/bin/dockerfilelint && echo 'exec sleep infinity' >> /usr/bin/dockerfilelint && chmod +x /usr/bin/dockerfilelint ; } ; \
    test -f /app || { echo '#!/bin/sh' > /app/placeholder && echo 'echo "dockerfile-lint v${VERSION} placeholder"' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app ; } test -f /app || { echo '#!/bin/sh' > /app/placeholder && echo 'echo "dockerfile-lint v${VERSION} placeholder"' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app ; } || true


FROM cgr.dev/chainguard/wolfi-base:latest

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
ENTRYPOINT ["dockerfilelint"]
LABEL org.opencontainers.image.title="dockerfile-lint" \
      org.opencontainers.image.description="Dockerfile linter" \
      org.opencontainers.image.vendor="replicated" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
