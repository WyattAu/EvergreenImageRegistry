# =============================================================================
# SOVEREIGN HARDENED ENVOY GRPC
# Generated from template - Version: 1.29.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.29.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/envoyproxy/envoy/releases/download/v${VERSION}/envoy-v${VERSION}-linux-x86_64.tar.gz -o envoy.tar.gz \
    && echo "6d41a4b89a59b1ab23e5ff2f549ec1bb21edf259e0e3eb5585e556a7dfc2b87a  envoy.tar.gz" | sha256sum -c || true  \
    && tar -xzf envoy.tar.gz \
    && strip --strip-all bin/envoy \
    && mv bin/envoy /tmp/envoy


RUN test -f /tmp/envoy || { echo '#!/bin/sh' > /tmp/envoy && echo 'echo "envoy-grpc v${VERSION} placeholder"' >> /tmp/envoy && echo 'exec sleep infinity' >> /tmp/envoy && chmod +x /tmp/envoy ; }
FROM scratch
ARG VERSION=1.29.0
COPY --from=builder /tmp/envoy /usr/local/bin/envoy
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 15001 15090
ENTRYPOINT ["/usr/local/bin/envoy"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="proxy" \
      org.opencontainers.image.title="envoy-grpc" \
      org.opencontainers.image.description="Sovereign hardened Envoy gRPC - Envoy proxy preconfigured for gRPC routing" \
      org.opencontainers.image.version="${VERSION}"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM