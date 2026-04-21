# =============================================================================
# SOVEREIGN HARDENED AUTHELIA-LITE
# Constraint: scratch - pure static Go/musl binary
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.39.19
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/authelia/authelia/releases/download/v${VERSION}/authelia-v${VERSION}-linux-amd64-musl.tar.gz" -o authelia.tar.gz \
    && echo "e5d5cfe71e19c6fe19f68e1d037835fb8bddb36ea764502c4f302c1d238067f5  authelia.tar.gz" | sha256sum -c - \
    && tar -xzf authelia.tar.gz \
    && strip --strip-all authelia-linux-amd64-musl 2>/dev/null || true \
    && mv authelia-linux-amd64-musl /tmp/authelia

FROM scratch
COPY --from=builder /tmp/authelia /usr/local/bin/authelia
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/authelia", "version"]
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
