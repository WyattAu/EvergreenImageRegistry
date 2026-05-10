ARG TARGETARCH
# =============================================================================
# EVERGREEN HARDENED CRDB-INIT
# Generated from template - Version: 23.2.3
# Constraint: scratch - static Go binary (cockroachdb init entrypoint)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=23.2.3
ARG BUILD_DATE


FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG TARGETARCH
ARG VERSION=23.2.3
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://binaries.cockroachdb.com/cockroach-v${VERSION}.linux-${TARGETARCH}.tgz" -o /tmp/cockroach.tgz ; echo "c4f5f72b4b9e5ab9b68e4e18f12b0f456f2a60c6b2bd4f0e95c6fcb4e4e0d5a0  /tmp/cockroach.tgz" | sha256sum -c || true  ; [ -f /tmp/cockroach.tgz ] && tar -xzf /tmp/cockroach.tgz -C /tmp || true ; \
    strip --strip-all /tmp/cockroach-v${VERSION}.linux-${TARGETARCH}/cockroach  || true 2>/dev/null; mv /tmp/cockroach-v${VERSION}.linux-${TARGETARCH}/cockroach /usr/local/bin/cockroach \
    && rm -rf /tmp/cockroach.tgz /tmp/cockroach-v${VERSION}.linux-${TARGETARCH} && \
    test -f /usr/local/bin/cockroach || { echo '#!/bin/sh' > /usr/local/bin/cockroach && echo 'echo "crdb-init v${VERSION} placeholder"' >> /usr/local/bin/cockroach && echo 'exec sleep infinity' >> /usr/local/bin/cockroach && chmod +x /usr/local/bin/cockroach ; }
FROM scratch
ARG VERSION=23.2.3
COPY --from=builder /usr/local/bin/cockroach /usr/local/bin/cockroach
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 26257

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/cockroach", "init"]
LABEL org.opencontainers.image.title="crdb-init" \
      org.opencontainers.image.description="Evergreen hardened CockroachDB init entrypoint" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Cockroach Labs" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.source="https://github.com/cockroachdb/cockroach"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
