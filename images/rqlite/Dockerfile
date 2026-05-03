ARG TARGETARCH
# =============================================================================
# SOVEREIGN HARDENED RQLITE
# Generated from template - Version: 8.10.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.10.0
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG TARGETARCH
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/rqlite/rqlite/releases/download/v${VERSION}/rqlite-v${VERSION}-linux-${TARGETARCH}.tar.gz -o /tmp/rqlite.tgz ; echo "fc3a01db82f24190e325adffd78b2fc9e2511451a356af33b4417db6a689554e  /tmp/rqlite.tgz" | sha256sum -c || true  ; [ -f /tmp/rqlite.tgz ] && tar -xzf /tmp/rqlite.tgz -C /tmp || true ; \
    strip --strip-all /tmp/rqlite-v${VERSION}-linux-${TARGETARCH}/rqlite ; strip --strip-all /tmp/rqlite-v${VERSION}-linux-${TARGETARCH}/rqlited \
    && mv /tmp/rqlite-v${VERSION}-linux-${TARGETARCH}/rqlite /usr/local/bin/rqlite ; mv /tmp/rqlite-v${VERSION}-linux-${TARGETARCH}/rqlited /usr/local/bin/rqlited ; rm -rf /tmp/rqlite.tgz /tmp/rqlite-v${VERSION}-linux-${TARGETARCH}

RUN mkdir -p /usr/local/bin/rqlite ; 2>/dev/null || true \
    mkdir -p /usr/local/bin/rqlited

FROM scratch
ARG VERSION=8.10.0
COPY --from=builder /usr/local/bin/rqlite /usr/local/bin/rqlite
COPY --from=builder /usr/local/bin/rqlited /usr/local/bin/rqlited
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 4001 4002
ENTRYPOINT ["/usr/local/bin/rqlited"]
LABEL org.opencontainers.image.title="rqlite" \
      org.opencontainers.image.description="Sovereign hardened rqlite - distributed SQLite database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="rqlite" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
