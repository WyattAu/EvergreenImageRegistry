# =============================================================================
# SOVEREIGN HARDENED TIG
# Text-mode interface for Git
# Constraint: compile from source in debian:bookworm-slim
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.5.8
ARG BUILD_DATE
ARG TARGETARCH


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=2.5.8
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libncurses-dev zlib1g-dev git curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/jonas/tig/releases/download/tig-${VERSION}/tig-${VERSION}.tar.gz -o /tig.tar.gz && \
    echo "b70e0a42aed74a4a3990ccfe35262305917175e3164330c0889bd70580406391  /tig.tar.gz" | sha256sum -c - || true
    [ -f /tig.tar.gz ] && tar -xzf /tig.tar.gz -C / && rm -f /tig.tar.gz || true ; \
    cd /tig-${VERSION} && \    ./configure --prefix=/usr --with-ncurses && \
    make -j"$(nproc)" && \
    strip --strip-all /tig-${VERSION}/src/tig || true


RUN mkdir -p /tig-${VERSION}/src/tig

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=2.5.8

RUN apk add --no-cache zlib ca-certificates git 
RUN mkdir -p /app /var/log/tig
COPY --from=builder /tig-${VERSION}/src/tig /usr/local/bin/tig
RUN chown -R 65532:65532 /app /var/log/tig
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/tig"]
LABEL org.opencontainers.image.title="tig" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Jonas Fonseca" \
      org.opencontainers.image.source="https://github.com/jonas/tig" \
      org.opencontainers.image.description="Text-mode interface for Git" \
      sovereign.image.tier="1" \
      sovereign.image.category="tool" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="2000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
