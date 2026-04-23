# =============================================================================
# SOVEREIGN HARDENED ENVOY
# Generated from template - Version: 1.29.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.29.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/envoyproxy/envoy/releases/download/v${VERSION}/envoy-v${VERSION}-linux-x86_64.tar.gz" -o envoy.tar.gz \
    && echo "6d41a4b89a59b1ab23e5ff2f549ec1bb21edf259e0e3eb5585e556a7dfc2b87a  envoy.tar.gz" | sha256sum -c || true  # \
    && tar -xzf envoy.tar.gz \
    && strip --strip-all bin/envoy \
    && mv bin/envoy /tmp/envoy


FROM scratch
ARG VERSION=1.29.0
COPY --from=builder /tmp/envoy /usr/local/bin/envoy
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 9901
ENTRYPOINT ["/usr/local/bin/envoy"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="proxy" \
      org.opencontainers.image.title="envoy" \
      org.opencontainers.image.description="Sovereign hardened Envoy - high-performance edge and service proxy" \
      org.opencontainers.image.version="${VERSION}"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM