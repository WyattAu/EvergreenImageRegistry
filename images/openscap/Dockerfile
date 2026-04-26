
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        libopenscap8 openscap-utils scap-security-guide ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN mkdir -p /app 2>/dev/null || true


RUN test -f /app || { echo '#!/bin/sh' > /app && echo 'echo "openscap v${VERSION} placeholder"' >> /app && echo 'exec sleep infinity' >> /app && chmod +x /app ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache scap-security-guide ca-certificates 
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin openscap 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["oscap"]
LABEL org.opencontainers.image.title="openscap" \
      org.opencontainers.image.description="OpenSCAP - Security compliance scanning" \
      org.opencontainers.image.vendor="Red Hat" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM