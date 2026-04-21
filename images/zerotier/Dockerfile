# =============================================================================
# SOVEREIGN HARDENED ZEROTIER
# ZeroTier virtual network layer 2 overlay
# Constraint: debian-slim - C++ binary requires glibc, libstdc++, libgcc
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.12.2
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/zerotier/ZeroTierOne/releases/download/${VERSION}/zerotier-one-${VERSION}-x86_64-linux.tgz" -o /zerotier.tgz && \
    curl -fsSL "https://github.com/zerotier/ZeroTierOne/releases/download/${VERSION}/sha256sum.txt" -o /checksums.txt && \
    grep "zerotier-one-${VERSION}-x86_64-linux.tgz" /checksums.txt | sha256sum -c - && \
    mkdir -p /tmp/zerotier && \
    tar -xzf /zerotier.tgz -C /tmp/ && \
    strip --strip-all /tmp/zerotier-one-${VERSION}/zerotier-one && \
    mv /tmp/zerotier-one-${VERSION}/zerotier-one /zerotier-one && \
    rm -rf /zerotier.tgz /checksums.txt /tmp/*

# hadolint ignore=DL3023
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libstdc++6 libgcc-s1 ca-certificates iproute2 && rm -rf /var/lib/apt/lists/* && \
    groupadd -g 65534 zerotier && useradd -u 65534 -g zerotier -s /usr/sbin/nologin -d /app zerotier && \
    mkdir -p /app/var/lib/zerotier-one && chown -R 65534:65534 /app

COPY --from=downloader /zerotier-one /usr/sbin/zerotier-one
USER 65534:65534
WORKDIR /app
EXPOSE 9993/udp 9993/tcp
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/sbin/zerotier-one", "-version"]
ENTRYPOINT ["/usr/sbin/zerotier-one"]
CMD ["-p9993"]
LABEL org.opencontainers.image.title="zerotier" \
      org.opencontainers.image.version="1.12.2" \
      org.opencontainers.image.vendor="ZeroTier" \
      org.opencontainers.image.source="https://github.com/zerotier/ZeroTierOne" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distrole="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
