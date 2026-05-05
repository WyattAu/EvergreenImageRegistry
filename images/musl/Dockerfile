# =============================================================================
# EVERGREEN BASE - MUSL
# Minimal musl-based scratch image for statically-linked binaries.
# Uses Alpine's musl libc for C/C++ static compilation targets.
# =============================================================================


FROM cgr.dev/chainguard/static@sha256:77d8b8925dc27970ec2f48243f44c7a260d52c49cd778288e4ee97566e0cb75b

USER 65532:65532
LABEL org.opencontainers.image.title="musl" \
      org.opencontainers.image.description="Evergreen musl-based static base for C/C++ compilation targets" \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.image.category="base" \
      evergreen.image.note="Musl libc base for static binary builds. Use for Rust/C++ static targets." \
            org.opencontainers.image.source="https://github.com/openSUSE/musl" \
                  org.opencontainers.image.version="unknown"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
