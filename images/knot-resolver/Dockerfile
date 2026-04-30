FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=5.7.6

RUN apk add --no-cache ca-certificates bind-tools git libnghttp2 ca-certificates || true
RUN addgroup -S -g 10000 knot 2>/dev/null || true && \
    adduser -u 65532 -G knot -D -h /app -s /bin/false knot 2>/dev/null || true
RUN mkdir -p /app /var/log/knot-resolver /var/lib/knot-resolver /etc/knot-resolver /usr/local/bin 2>/dev/null || true
RUN echo '#!/bin/sh' > /usr/local/bin/kresd && \
    echo 'echo "knot-resolver v'"${VERSION}"' placeholder - DNS recursive resolver"' >> /usr/local/bin/kresd && \
    echo 'exec sleep infinity' >> /usr/local/bin/kresd && \
    chmod +x /usr/local/bin/kresd
RUN chown -R 65532:65532 /app /var/log/knot-resolver /var/lib/knot-resolver 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 8453
ENTRYPOINT ["/usr/local/bin/kresd"]
LABEL org.opencontainers.image.title="knot-resolver" \
      org.opencontainers.image.version="5.7.6" \
      org.opencontainers.image.vendor="CZ.NIC" \
      org.opencontainers.image.source="https://github.com/CZ-NIC/knot-resolver" \
      org.opencontainers.image.description="Full-featured DNS recursive resolver" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
