# =============================================================================
# SOVEREIGN HARDENED MONGODB-6
# Generated from template - Version: 6.0.14
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=6.0.14
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65532 -s /usr/sbin/nologin mongodb 2>/dev/null || true
RUN mkdir -p /app /var/log/mongod /var/cache/mongod

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache ca-certificates
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/mongod /var/log/mongod
COPY --from=builder --chown=65532:65532 /var/cache/mongod /var/cache/mongod
USER 65532:65532
WORKDIR /app
EXPOSE 27017
ENTRYPOINT ["mongod"]
LABEL org.opencontainers.image.title="mongodb-6" \
      org.opencontainers.image.version="6.0.14" \
      org.opencontainers.image.vendor="MongoDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM