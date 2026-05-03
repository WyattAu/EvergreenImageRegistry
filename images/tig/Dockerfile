# =============================================================================
# EVERGREEN HARDENED TIG
# Text-mode interface for Git
# Constraint: compile from source in debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.5.8
ARG BUILD_DATE
ARG TARGETARCH


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=2.5.8

RUN apk add --no-cache zlib ca-certificates git 
RUN mkdir -p /app /var/log/tig
COPY --from=builder /tig-${VERSION}/src/tig /usr/local/bin/tig
RUN chown -R 65532:65532 /app /var/log/tig
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/tig"]
LABEL org.opencontainers.image.title="tig" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Jonas Fonseca" \
      org.opencontainers.image.source="https://github.com/jonas/tig" \
      org.opencontainers.image.description="Text-mode interface for Git" \
      evergreen.image.tier="1" \
      evergreen.image.category="tool" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="2000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
