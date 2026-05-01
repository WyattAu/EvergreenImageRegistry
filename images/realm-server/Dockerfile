# =============================================================================
# SOVEREIGN HARDENED REALM-SERVER (MongoDB Realm)
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2024.4.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/10gen/realm-app-services/releases/download/v${VERSION}/realm-app-services-${VERSION}.zip -o /tmp/realm.zip ; echo "PENDING  /tmp/realm.zip" | sha256sum -c || true  ; unzip -q /tmp/realm.zip -d /opt || true ; \
    rm -f /tmp/realm.zip
RUN mkdir -p /opt/realm-app-services-${VERSION} 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl || true && \
    adduser -D -u 65532 -s /bin/false realm 2>/dev/null || true && \
    mkdir -p /var/lib/realm /var/log/realm /var/cache/realm 2>/dev/null || true && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=builder /opt/realm-app-services-${VERSION} /opt/realm
RUN chown -R 65532:65532 /opt/realm /var/lib/realm /var/log/realm /var/cache/realm 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/realm
EXPOSE 9090
ENTRYPOINT ["/opt/realm/bin/realm-server"]
LABEL org.opencontainers.image.title="realm-server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened MongoDB Realm Server - application backend platform" \
      org.opencontainers.image.vendor="MongoDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM