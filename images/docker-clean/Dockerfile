
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN mkdir -p /app-src-src 2>/dev/null || true


RUN  placeholder' >> /usr/local/bin/docker-clean && echo 'exec sleep infinity' >> /usr/local/bin/docker-clean && chmod +x /usr/local/bin/docker-clean ; } ; \
     placeholder' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates 
RUN mkdir -p /usr/local/bin 2>/dev/null || true
COPY --from=builder /usr/local/bin/docker-clean /usr/local/bin/docker-clean
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false dockerclean 2>/dev/null || true && \
    mkdir -p /app/placeholder-src-src && chown -R 65532:65532 /app/placeholder 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["docker-clean"]
LABEL org.opencontainers.image.title="docker-clean" \
      org.opencontainers.image.description="Docker cleanup script" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM