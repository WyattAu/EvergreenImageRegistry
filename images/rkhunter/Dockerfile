FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        rkhunter ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin rkhunter 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["rkhunter"]
CMD ["--check", "--skip-keypress"]
LABEL org.opencontainers.image.title="rkhunter" \
      org.opencontainers.image.description="rkhunter - rootkit hunter" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM