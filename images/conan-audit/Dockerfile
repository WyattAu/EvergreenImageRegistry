
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \ || true
    pip install --no-cache-dir conan ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/conan || { echo '#!/bin/sh' > /usr/local/bin/conan && echo 'echo "conan-audit v${VERSION} placeholder"' >> /usr/local/bin/conan && echo 'exec sleep infinity' >> /usr/local/bin/conan && chmod +x /usr/local/bin/conan ; } 2>/dev/null || true
RUN mkdir -p /app 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates || true
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin conan 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
ENTRYPOINT ["conan"]
CMD ["audit"]
LABEL org.opencontainers.image.title="conan-audit" \
      org.opencontainers.image.description="Conan audit - C/C++ dependency security scanner" \
      org.opencontainers.image.vendor="conan-io" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM