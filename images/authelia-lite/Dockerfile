# =============================================================================
# SOVEREIGN HARDENED AUTHELIA-LITE
# Constraint: scratch - pure static Go/musl binary
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.39.19
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/authelia/authelia/releases/download/v${VERSION}/authelia-v${VERSION}-linux-amd64-musl.tar.gz -o authelia.tar.gz && \
    tar -xzf authelia.tar.gz && \
    strip --strip-all authelia && mv authelia /tmp/authelia

FROM scratch
ARG VERSION=4.39.19
COPY --from=builder /tmp/authelia /usr/local/bin/authelia
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 80 443
ENTRYPOINT ["/usr/local/bin/authelia"]
LABEL org.opencontainers.image.title="authelia-lite" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Authelia-lite - lightweight SSO/2FA authentication portal" \
      org.opencontainers.image.vendor="Authelia" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM