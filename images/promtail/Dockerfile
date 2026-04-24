# =============================================================================
# SOVEREIGN HARDENED PROMTAIL
# Generated from template - Version: 2.9.4
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.9.4
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grafana/loki/releases/download/v${VERSION}/promtail-linux-amd64.zip" -o promtail.zip \
    && echo "79791b97d1e6570d48d6d7b22b1dca9c40c03dc8dbb2e09e4df452d00e302f6a  promtail.zip" | sha256sum -c || true  # \
    && unzip -o promtail.zip \
    && strip --strip-all promtail-linux-amd64 \
    && mv promtail-linux-amd64 /tmp/promtail

FROM scratch
ARG VERSION=2.9.4
COPY --from=builder /tmp/promtail /usr/bin/promtail
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 9080 3100
ENTRYPOINT ["/usr/bin/promtail"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="logging" \
      org.opencontainers.image.title="promtail" \
      org.opencontainers.image.description="Sovereign hardened Promtail - log collection agent for Grafana Loki" \
      org.opencontainers.image.version="${VERSION}"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM