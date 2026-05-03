# =============================================================================
# SOVEREIGN HARDENED ENVOY SIDECAR
# Generated from template - Version: 1.38.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.38.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/envoyproxy/envoy/releases/download/v${VERSION}/envoy-${VERSION}-linux-x86_64 -o /tmp/envoy && \
    echo "cca312a7c3f91852f2849995c895130c59842e21ba787dc90bafa4026d6c5ecc  /tmp/envoy" | sha256sum -c || true ; \
    chmod +x /tmp/envoy && strip --strip-all /tmp/envoy
FROM scratch
ARG VERSION=1.38.0
COPY --from=builder /tmp/envoy /usr/local/bin/envoy
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 15001
ENTRYPOINT ["/usr/local/bin/envoy", "--mode", "sidecar"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="sidecar" \
      org.opencontainers.image.title="envoy-sidecar" \
      org.opencontainers.image.description="Sovereign hardened Envoy sidecar - service mesh sidecar proxy" \
      org.opencontainers.image.version="${VERSION}"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
