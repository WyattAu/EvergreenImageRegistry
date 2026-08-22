# =============================================================================
# Evergreen Operator — Container Image
# =============================================================================
# Builds the Kubernetes operator binary and packages it into a minimal image.
# Multi-stage build for security and size optimization.
# =============================================================================

FROM golang:1.23-bookworm AS builder

WORKDIR /workspace

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source
COPY main.go ./
COPY controllers/ ./controllers/
COPY api/ ./api/

# Build with FIPS BoringCrypto support
RUN CGO_ENABLED=1 GOEXPERIMENT=boringcrypto go build -ldflags="-s -w" -o manager main.go

# Runtime image — distroless for security
FROM gcr.io/distroless/static:nonroot

WORKDIR /

COPY --from=builder /workspace/manager .

USER 65532:65532

ENTRYPOINT ["/manager"]

LABEL org.opencontainers.image.title="evergreen-operator" \
      org.opencontainers.image.description="Kubernetes operator for Evergreen Image Registry" \
      org.opencontainers.image.vendor="Evergreen Image Registry" \
      org.opencontainers.image.source="https://github.com/WyattAu/EvergreenImageRegistry" \
      org.opencontainers.image.licenses="Apache-2.0"
