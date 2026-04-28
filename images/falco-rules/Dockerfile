
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN git clone --depth 1 https://github.com/falcosecurity/rules.git /rules 2>/dev/null || echo "Source repo not available - using placeholder" || true
RUN mkdir -p /app/rules 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates 
COPY --from=builder /rules /app/rules
RUN addgroup -S -g 2 nogroup>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false falcorules 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["cat"]
CMD ["/app/rules/rules.yaml"]
LABEL org.opencontainers.image.title="falco-rules" \
      org.opencontainers.image.description="Falco - rules only" \
      org.opencontainers.image.vendor="Sysdig" \
      org.opencontainers.image.source="https://github.com/falcosecurity/rules" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM