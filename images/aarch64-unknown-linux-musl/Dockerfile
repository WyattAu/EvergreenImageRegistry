
FROM scratch
USER 65532:65532
LABEL org.opencontainers.image.title="aarch64-unknown-linux-musl" \
      org.opencontainers.image.description="Sovereign hardened aarch64-unknown-linux-musl - ARM64 musl static base" \
      sovereign.image.tier="3" \
      sovereign.image.note="Placeholder base image for ARM64 musl static binaries. Extend with application binaries."

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
