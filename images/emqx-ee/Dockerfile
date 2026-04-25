
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* || true

RUN mkdir -p /app /opt/emqx/data /opt/emqx/log 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl procps || true
COPY --from=builder /app /app
COPY --from=builder /opt/emqx /opt/emqx
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /opt/emqx -s /sbin/nologin emqx 2>/dev/null || true && \
    chown -R 65532:65532 /opt/emqx /app 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/emqx
EXPOSE 1883 8083 8084 8883 18083
ENTRYPOINT ["echo"]
CMD ["emqx-ee: Enterprise edition requires license. Place emqx binary in /opt/emqx/bin/"]
LABEL org.opencontainers.image.title="emqx-ee" \
      org.opencontainers.image.description="EMQX Enterprise - requires license" \
      org.opencontainers.image.vendor="EMQ" \
      org.opencontainers.image.source="https://github.com/emqx/emqx" \
      sovereign.image.tier="3" \
      sovereign.image.status="license-required" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM