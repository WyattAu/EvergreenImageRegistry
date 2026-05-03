ARG TARGETARCH
FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=0.13.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/element-hq/dendrite/releases/download/v${VERSION}/dendrite-monolith-linux-${TARGETARCH}" \
    -o /tmp/dendrite && \
    chmod +x /tmp/dendrite && \
    strip /tmp/dendrite

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=0.13.1
RUN apk add --no-cache ca-certificates || true
RUN addgroup -S -g 10000 dendrite 2>/dev/null || true && \
    adduser -u 65532 -G dendrite -D -h /app -s /bin/false dendrite 2>/dev/null || true
COPY --from=downloader /tmp/dendrite /usr/local/bin/dendrite
RUN mkdir -p /app 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8008
ENTRYPOINT ["/usr/local/bin/dendrite"]
CMD ["--config=/app/dendrite.yaml"]
LABEL org.opencontainers.image.title="dendrite-pot" \
      org.opencontainers.image.description="Dendrite POT - Polylith OUTBOX Trusted worker for Dendrite" \
      org.opencontainers.image.version="0.13.1" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/dendrite" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
