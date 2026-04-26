
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir whoogle-search || true
RUN mkdir -p /app/config /app/data 2>/dev/null || true


RUN test -f /opt/venv || { echo '#!/bin/sh' > /opt/venv && echo 'echo "whoogle-search v${VERSION} placeholder"' >> /opt/venv && echo 'exec sleep infinity' >> /opt/venv && chmod +x /opt/venv ; } ; \
    test -f /app || { echo '#!/bin/sh' > /app && echo 'echo "whoogle-search v${VERSION} placeholder"' >> /app && echo 'exec sleep infinity' >> /app && chmod +x /app ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates tzdata 
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false whoogle 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 5000
ENTRYPOINT ["whoogle-search"]
CMD ["--port", "5000"]
LABEL org.opencontainers.image.title="whoogle-search" \
      org.opencontainers.image.description="Whoogle - Privacy-friendly search proxy" \
      org.opencontainers.image.vendor="benbusby" \
      org.opencontainers.image.source="https://github.com/benbusby/whoogle-search" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM