
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav-freshclam ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN mkdir -p /app /var/lib/clamav /var/log/clamav 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache clamav-freshclam ca-certificates || true
COPY --from=builder /app /app
COPY --from=builder /var/lib/clamav /var/lib/clamav
COPY --from=builder /var/log/clamav /var/log/clamav
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false freshclam 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/lib/clamav /var/log/clamav 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["freshclam"]
CMD ["--daemon"]
LABEL org.opencontainers.image.title="freshclam" \
      org.opencontainers.image.description="FreshClam - ClamAV database updater" \
      org.opencontainers.image.vendor="Cisco" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM