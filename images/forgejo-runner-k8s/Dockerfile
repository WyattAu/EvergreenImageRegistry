# forgejo-runner-k8s — Evergreen K8s-enabled Forgejo Actions Runner
#
# Multi-stage build:
#   1. golang:1.23 — compile act_runner with CGO + kubernetes tags
#   2. alpine:3.21  — minimal runtime with git, bash, nodejs
#
# The kubernetes executor requires CGO_ENABLED=1 and k8s.io/client-go.
# This produces a ~80MB image vs the distroless 20MB binary because
# CGO links to glibc and k8s client libraries.
#
# Usage:
#   docker build -t ghcr.io/wyattau/forgejo-runner-k8s:latest .
#   docker push ghcr.io/wyattau/forgejo-runner-k8s:latest
#
# Or just extract the binary:
#   docker build --target builder -o /tmp .
#   cp /tmp/act_runner /opt/act-runner/bin/

# ── Stage 1: Build ──────────────────────────────────────────
FROM golang:1.24-bookworm AS builder

ARG ACT_RUNNER_VERSION=v0.2.13

RUN git clone --depth 1 --branch ${ACT_RUNNER_VERSION} \
    https://gitea.com/gitea/act_runner.git /src

WORKDIR /src

# CGO_ENABLED=1 is required for k8s.io/client-go (uses cgo for auth plugins)
# -tags kubernetes enables the K8s executor
# -ldflags="-s -w" strips debug symbols (reduces binary from 60MB to 35MB)
RUN CGO_ENABLED=1 go build \
    -tags kubernetes \
    -ldflags="-s -w" \
    -o /act_runner \
    .

# ── Stage 2: Runtime ────────────────────────────────────────
# Wolfi-base provides glibc (required by CGO-linked K8s client libs).
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

# Runtime deps: git (checkout), bash (workflows), nodejs (checkout action),
# curl (cache/download actions), ca-certificates (HTTPS)
RUN apk add --no-cache \
    git \
    bash \
    nodejs \
    npm \
    curl \
    ca-certificates \
    tzdata

COPY --from=builder /act_runner /usr/local/bin/act_runner

USER 65532:65532
HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/act_runner"]
CMD ["daemon"]
