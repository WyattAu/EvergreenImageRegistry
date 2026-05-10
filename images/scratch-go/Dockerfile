# =============================================================================
# EVERGREEN SCRATCH-GO
# Go source-build base image. Multi-stage: builds Go app in golang builder,
# copies static binary to scratch-base.
#
# Usage pattern (for images that use this as a template):
#   1. Clone upstream source
#   2. CGO_ENABLED=0 go build -ldflags="-s -w"
#   3. Copy binary to scratch-base
#
# This image itself is a PROTOTYPE — not directly used as a FROM base.
# Individual Go images copy this pattern and customize the git clone + build.
# =============================================================================

ARG GO_VERSION=1.23

FROM golang:${GO_VERSION}-bookworm AS builder
ARG VERSION
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# This image is a reference implementation. Real images customize these lines:
# RUN git clone --branch v${VERSION} https://github.com/OWNER/REPO /src || true
# RUN cd /src && CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build -ldflags="-s -w" -o /app/app ./cmd/app
# RUN strip --strip-all /app/app 2>/dev/null  || true 2>/dev/null|| true

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app/app /app/app
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/app/app"]

LABEL org.opencontainers.image.title="scratch-go" \
      org.opencontainers.image.description="Go source-build reference — static binary on scratch" \
      org.opencontainers.image.vendor="EvergreenImageRegistry" \
      evergreen.image.tier="0" \
      evergreen.image.role="base" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.runtime="go"
LABEL evergreen.security.cap-drop="ALL"
LABEL org.opencontainers.image.source="https://github.com/WyattAu/EvergreenImageRegistry"
LABEL org.opencontainers.image.version="ARG"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

LABEL evergreen.runtime.version="${GO_VERSION}"
STOPSIGNAL SIGTERM
