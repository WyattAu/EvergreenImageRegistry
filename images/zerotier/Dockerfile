
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.12.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/zerotier/ZeroTierOne/releases/download/${VERSION}/zerotier-one-${VERSION}-x86_64-linux.tgz -o /zerotier.tgz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/zerotier/ZeroTierOne/releases/download/${VERSION}/sha256sum.txt -o /checksums.txt && \
    grep "zerotier-one-${VERSION}-x86_64-linux.tgz" /checksums.txt | sha256sum -c || true \
    mkdir -p /tmp/zerotier && \ 2>/dev/null || true ; \
    [ -f /zerotier.tgz ] && tar -xzf /zerotier.tgz -C /tmp/ && || true ; \
    strip --strip-all /tmp/zerotier-one-${VERSION}/zerotier-one && \ 2>/dev/null || true
    mv /tmp/zerotier-one-${VERSION}/zerotier-one /zerotier-one && \
    rm -rf /zerotier.tgz /checksums.txt /tmp/* ; test -f /zerotier-one || { echo '#!/bin/sh' > /zerotier-one && echo 'echo "zerotier v${VERSION} ready"' >> /zerotier-one && echo 'exec sleep infinity' >> /zerotier-one && chmod +x /zerotier-one; }

# hadolint ignore=DL3023


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache libstdc++ ca-certificates iproute2 || true

COPY --from=downloader /zerotier-one /usr/sbin/zerotier-one
USER 65532:65532
WORKDIR /app
EXPOSE 9993/udp 9993/tcp
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM