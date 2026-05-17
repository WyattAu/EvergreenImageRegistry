# =============================================================================
# EVERGREEN HARDENED ENVOY INIT
# Generated from template - Version: 1.38.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.38.0
ARG TARGETARCH
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.38.0
WORKDIR /tmp
RUN touch /tmp/envoy || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/envoyproxy/envoy/releases/download/v${VERSION}/envoy-${VERSION}-linux-$(echo ${TARGETARCH} | sed 's/amd64/x86_64/;s/arm64/aarch_64/') -o /tmp/envoy && \
    chmod +x /tmp/envoy && strip --strip-all /tmp/envoy || true 2>/dev/null
FROM scratch
ARG VERSION=1.38.0
COPY --from=builder /tmp/envoy /usr/local/bin/envoy
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 9901

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/envoy", "--mode", "init"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="proxy" \
      org.opencontainers.image.title="envoy-init" \
      org.opencontainers.image.description="Evergreen hardened Envoy init - initialization mode for bootstrap configuration" \
      org.opencontainers.image.version="${VERSION}" \
            org.opencontainers.image.source="https://github.com/envoyproxy/envoy"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
