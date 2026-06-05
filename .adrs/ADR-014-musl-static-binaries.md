# Architecture Decision Record: Musl Static Binaries

## ADR-014: Musl Static Binaries

### Status

ACCEPTED

### Date

2026-06-05

### Author

Evergreen Image Registry Team

### Context

Shim binaries must run in `FROM scratch` and `FROM cgr.dev/chainguard/wolfi-base` images. These images have no glibc, no
dynamic linker, and no shared libraries. Statically linked binaries are the only option for scratch images.

The registry's base image hierarchy is:

```
scratch (static binaries: Go, Rust, C)
  → wolfi-base (Chainguard: glibc + CA certs)
    → distroless (Google: language-specific runtimes)
```

BANNED for final stage: debian-slim, alpine, ubuntu, centos.

### Decision

Build all shim binaries with musl static linking using the `x86_64-unknown-linux-musl` and `aarch64-unknown-linux-musl`
targets.

**Build command:**

```bash
# x86_64
cargo build --release --target x86_64-unknown-linux-musl

# aarch64
cargo build --release --target aarch64-unknown-linux-musl
```

**Cargo.toml configuration:**

```toml
[profile.release]
opt-level = "z"      # Optimize for size
lto = true           # Link-time optimization
codegen-units = 1    # Single codegen unit for better optimization
panic = "abort"      # No unwind tables
strip = true         # Strip debug symbols

[profile.release.build-override]
opt-level = 3        # Build scripts optimized for speed
```

**Binary size budget:**

| Component            | Size           |
| -------------------- | -------------- |
| Tokio runtime        | ~100KB         |
| Axum HTTP            | ~50KB          |
| Prometheus client    | ~30KB          |
| Application logic    | ~20KB          |
| **Total (stripped)** | **~200-300KB** |

**Dockerfile integration:**

```dockerfile
FROM rust:1.75-bookworm AS builder
ARG TARGETARCH
RUN target-triple=$(case $TARGETARCH in amd64) echo x86_64-unknown-linux-musl;; arm64) echo aarch64-unknown-linux-musl;; esac) && \
    rustup target add $target-triple && \
    cargo build --release --target $target-triple

FROM scratch
COPY --from=builder /app/target/$target-triple/release/health-shim /app/health-shim
```

### Consequences

**Positive:**

- No glibc dependency — runs in scratch and wolfi
- Single binary — no dynamic linking, no shared libraries
- Predictable behavior across all base images
- Smaller attack surface — no dynamic linker vulnerabilities

**Negative:**

- Slightly larger binaries than glibc-linked equivalents (~10-20%)
- musl has different behavior than glibc in some edge cases (e.g., DNS resolution, locale)
- Cross-compilation requires musl toolchain setup

**Risks:**

- musl DNS resolution is synchronous and may block the async runtime (mitigated by using `trust-dns` resolver)
- Some crate dependencies may not compile cleanly for musl (mitigated by testing in CI)
- Binary size may exceed budget if dependencies grow (mitigated by periodic audits)

### Build Verification

```bash
# Verify static linking
file target/x86_64-unknown-linux-musl/release/health-shim
# Output: ELF 64-bit LSB executable, x86-64, statically linked

# Verify no dynamic dependencies
ldd target/x86_64-unknown-linux-musl/release/health-shim
# Output: not a dynamic executable

# Verify binary size
ls -lh target/x86_64-unknown-linux-musl/release/health-shim
# Output: ~200-300KB
```

### Related ADRs

- ADR-010: Scratch-Based Images with Embedded Health-Shim
- ADR-009: Rust Health-Shim as Entrypoint

### Related Standards

| Standard             | Relevance                     |
| -------------------- | ----------------------------- |
| CIS Docker Benchmark | 4.1 - Container health checks |
| NIST SP 800-190      | 3.2 - Container monitoring    |
| OpenMetrics 1.0.0    | Metrics format                |
