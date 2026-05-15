# FIPS Compliance Implementation Guide

This guide explains how to build FIPS 140-2 compliant images for the Evergreen Image Registry.

## Prerequisites

- Go 1.24+ (for BoringCrypto support)
- OpenSSL 3.0.x with FIPS provider module
- Docker buildx with multi-platform support
- Access to FIPS-validated cryptographic modules

## Building Go Images with BoringCrypto

BoringCrypto is the FIPS-validated cryptographic module bundled with Go's BoringSSL integration. It holds FIPS 140-2
Certificate #4140.

### Source Build Pattern

```dockerfile
FROM golang:1.24-bookworm AS builder
ARG VERSION
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}

RUN apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch "v${VERSION}" \
    https://github.com/example/project /src

RUN cd /src && \
    CGO_ENABLED=1 GOOS=linux GOARCH=${GOARCH} \
    GOEXPERIMENT=boringcrypto \
    go build -ldflags="-s -w" -o /app/binary ./cmd/binary
```

### Critical Requirements

- **CGO_ENABLED=1** is mandatory. BoringCrypto uses C code and cannot be built with `CGO_ENABLED=0`.
- **GOEXPERIMENT=boringcrypto** must be set during both build and runtime.
- The final image **cannot use `FROM scratch`**. BoringCrypto dynamically links against glibc. Use `wolfi-base` or a
  minimal glibc image instead.
- Set **GOLANG_FIPS=1** as an environment variable at runtime to activate FIPS mode.

### Runtime Verification

```bash
GOLANG_FIPS=1 /app/binary --version
# If BoringCrypto is active, the binary will refuse non-FIPS algorithms
```

### Go BoringCrypto Dockerfile Template

```dockerfile
FROM golang:1.24-bookworm AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates
RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/org/repo /src
RUN cd /src && CGO_ENABLED=1 GOEXPERIMENT=boringcrypto go build -o /binary ./cmd/binary

FROM debian:bookworm-slim
COPY --from=builder /binary /binary
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
ENV GOLANG_FIPS=1
USER 65532:65532
ENTRYPOINT ["/binary"]
```

### Images Using This Approach

| Image        | Language | Notes                                               |
| ------------ | -------- | --------------------------------------------------- |
| cosign       | Go       | Build from sigstore/cosign source                   |
| fulcio       | Go       | Build from sigstore/fulcio source                   |
| rekor        | Go       | Build from sigstore/rekor source                    |
| step-ca      | Go       | Build from smallstep/certificates source            |
| prometheus   | Go       | Build from prometheus/prometheus source             |
| alertmanager | Go       | Build from prometheus/alertmanager source           |
| loki         | Go       | Build from grafana/loki source                      |
| grafana      | Go       | Build from grafana/grafana source                   |
| traefik      | Go       | Build from traefik/traefik source                   |
| coredns      | Go       | Build from coredns/coredns source                   |
| trivy        | Go       | Build from aquasecurity/trivy source                |
| kubescape    | Go       | Build from kubescape/kubescape source               |
| dex          | Go       | Already builds from source - add BoringCrypto flags |
| cockroachdb  | Go       | Build from cockroachdb/cockroach source             |
| tidb         | Go       | Build from pingcap/tidb source                      |
| consul       | Go       | Use Enterprise FIPS or rebuild community            |

## Building C/C++ Images with OpenSSL FIPS

OpenSSL 3.0+ uses a modular provider architecture. The FIPS provider is a separate module that has been FIPS 140-2
validated (Certificate #4230).

### Installing the FIPS Provider

```dockerfile
FROM debian:bookworm-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Build OpenSSL 3.0.x with FIPS provider
RUN wget https://www.openssl.org/source/openssl-3.0.15.tar.gz && \
    tar xzf openssl-3.0.15.tar.gz && \
    cd openssl-3.0.15 && \
    ./Configure --prefix=/usr/local/ssl/fips --openssldir=/usr/local/ssl/fips \
        enable-fips && \
    make -j$(nproc) && \
    make install && \
    make install_fips && \
    cd .. && rm -rf openssl-3.0.15*
```

### Linking Against FIPS OpenSSL

```dockerfile
# Build the application linked against FIPS OpenSSL
RUN cd /src && \
    ./configure --with-ssl=/usr/local/ssl/fips && \
    make -j$(nproc) && \
    make install
```

### FIPS Configuration File

Create `/etc/ssl/fipsmodule.cnf`:

```ini
config_diagnostics = 1
openssl_conf = openssl_init

.include /usr/local/ssl/fips/fipsmodule.cnf

[openssl_init]
providers = provider_sect
alg_section = algorithm_sect

[provider_sect]
fips = fips_sect
base = base_sect
default = default_sect

[base_sect]
activate = 1

[default_sect]
activate = 1
```

### Runtime Activation

```dockerfile
FROM debian:bookworm-slim
COPY --from=builder /usr/local/ssl/fips /usr/local/ssl/fips
COPY --from=builder /etc/ssl/fipsmodule.cnf /etc/ssl/fipsmodule.cnf
ENV OPENSSL_CONF=/etc/ssl/fipsmodule.cnf
```

### Verification

```bash
openssl list -providers
# Should show:
# fips
#   name: OpenSSL FIPS Provider
#   status: active
```

### Images Using This Approach

| Image      | Language | Notes                                               |
| ---------- | -------- | --------------------------------------------------- |
| postgresql | C        | Rebuild with system OpenSSL FIPS                    |
| mysql      | C/C++    | cmake -DWITH_SSL=system linked to FIPS OpenSSL      |
| redis      | C        | make BUILD_TLS=yes with FIPS OpenSSL                |
| mongodb    | C++      | Use Enterprise FIPS or rebuild with FIPS OpenSSL    |
| valkey     | C        | Same as redis (fork)                                |
| nginx      | C        | ./configure --with-openssl pointing to FIPS build   |
| keycloak   | Java     | OpenSSL via JNI + BouncyCastle FIPS                 |
| kanidm     | Rust     | Build with OPENSSL_NO_VENDOR=1 against FIPS OpenSSL |

## Images That Can Achieve FIPS Without Code Changes

These images can be made FIPS-compliant by switching to a FIPS-enabled base image or using official FIPS binaries:

| Image          | Approach                                                                           |
| -------------- | ---------------------------------------------------------------------------------- |
| **envoy**      | Download official FIPS-validated Envoy binary (BoringSSL BoringCrypto is built-in) |
| **postgresql** | Switch wolfi package to FIPS-enabled build; configure ssl_lib                      |
| **redis**      | Switch to wolfi FIPS package or build from source                                  |
| **valkey**     | Switch to wolfi FIPS package or build from source                                  |
| **keycloak**   | Enable Quarkus native FIPS mode (`-Dquarkus.ssl.native-fips=true`)                 |

## Images That Require Upstream Changes

| Image        | Reason                                                                  | Tracking                              |
| ------------ | ----------------------------------------------------------------------- | ------------------------------------- |
| **scylladb** | No FIPS support; C++ Seastar framework with complex OpenSSL integration | github.com/scylladb/scylladb/issues   |
| **falco**    | No FIPS support; C++ userspace with kernel module dependency            | github.com/falcosecurity/falco/issues |

## Images Requiring Enterprise Edition for Certified FIPS

| Image       | Enterprise FIPS                                    | Community Alternative                     |
| ----------- | -------------------------------------------------- | ----------------------------------------- |
| **vault**   | HashiCorp Vault Enterprise FIPS build (certified)  | Rebuild with BoringCrypto (not certified) |
| **consul**  | HashiCorp Consul Enterprise FIPS build (certified) | Rebuild with BoringCrypto (not certified) |
| **mongodb** | MongoDB Enterprise FIPS build (certified)          | Rebuild from source (not certified)       |
| **nginx**   | NGINX Plus FIPS build (certified)                  | Rebuild from source (not certified)       |

## Important Caveats

1. **BoringCrypto != Certified FIPS**: Building with `GOEXPERIMENT=boringcrypto` uses the FIPS-validated module, but
   only the module itself is certified. The overall system must undergo FIPS validation for full compliance.

2. **Scratch Image Limitation**: BoringCrypto requires glibc for dynamic linking. Any image currently using
   `FROM scratch` must switch to a glibc-based image for FIPS variants, increasing image size.

3. **OpenSSL 3.x FIPS Provider**: The FIPS provider must be installed and activated via `OPENSSL_CONF`. Without the
   configuration file pointing to the FIPS module, OpenSSL will use the default (non-FIPS) provider.

4. **Go CGO Requirement**: `CGO_ENABLED=1` is non-negotiable for BoringCrypto. This means cross-compilation is more
   complex and build times are longer.

5. **FIPS 140-3 Transition**: The industry is transitioning from FIPS 140-2 to FIPS 140-3. OpenSSL 3.x FIPS provider and
   BoringCrypto are being revalidated under FIPS 140-3. Plan for this transition.

## Quick Reference

### Environment Variables

```bash
# OpenSSL FIPS
OPENSSL_CONF=/etc/ssl/fipsmodule.cnf

# Go BoringCrypto
GOLANG_FIPS=1
GOEXPERIMENT=boringcrypto

# Java (Keycloak)
JAVA_OPTS="-Dquarkus.ssl.native-fips=true"
```

### Build Flags

```bash
# Go with BoringCrypto
CGO_ENABLED=1 GOEXPERIMENT=boringcrypto go build -o binary ./cmd/binary

# OpenSSL with FIPS
./Configure --prefix=/usr/local/ssl/fips --openssldir=/usr/local/ssl/fips enable-fips

# nginx with FIPS OpenSSL
./configure --with-openssl=/usr/local/ssl/fips --with-openssl-opt=enable-fips

# Envoy with FIPS (Bazel)
bazel build --config=fips //:envoy
```
