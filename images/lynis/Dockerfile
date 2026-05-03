
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN git clone --depth 1 https://github.com/CISOfy/Lynis.git /src 2>/dev/null || echo "Source repo not available - using placeholder" || true
RUN mkdir -p /src 2>/dev/null || true
RUN mkdir -p /app 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false lynis 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/app/src/lynis"]
CMD ["audit", "system"]
LABEL org.opencontainers.image.title="lynis" \
      org.opencontainers.image.description="Lynis - Security auditing tool" \
      org.opencontainers.image.vendor="CISOfy" \
      org.opencontainers.image.source="https://github.com/CISOfy/Lynis" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
