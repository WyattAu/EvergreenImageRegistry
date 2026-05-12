# Evergreen Image Registry

Hardened container images for production: 998 images built non-root, distroless, and fully auditable.

[![Build](https://img.shields.io/github/actions/workflow/status/WyattAu/EvergreenImageRegistry/build.yml?branch=main&style=flat-square&label=CI)](https://github.com/WyattAu/EvergreenImageRegistry/actions/workflows/build.yml)
[![Nightly Scan](https://img.shields.io/github/actions/workflow/status/WyattAu/EvergreenImageRegistry/nightly-scan.yml?branch=main&style=flat-square&label=Nightly%20Scan)](https://github.com/WyattAu/EvergreenImageRegistry/actions/workflows/nightly-scan.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg?style=flat-square)](LICENSE)
[![Images: 998](https://img.shields.io/badge/images-998-green.svg?style=flat-square)](docs/catalog/index.html)
[![SBOM Coverage: 100%](https://img.shields.io/badge/SBOM-998%2F998%20SPDX%202.3-brightgreen.svg?style=flat-square)](docs/standards.md)

Evergreen provides a long-term home for open-source container images that vendors have abandoned or moved behind paywalls. Every image adheres to a strict set of [Image Standards](docs/standards.md) -- non-root execution, distroless bases, mandatory healthchecks, and reproducible builds. Images are built for environments where failure is not an option: trading floors, air-gapped networks, and regulated infrastructure.

## Quick Start

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/redis:7.2

docker run -d \
  --name redis \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  ghcr.io/wyattau/evergreenimageregistry/redis:7.2
```

All images are published to `ghcr.io/wyattau/evergreenimageregistry/<image>:<version>`. Pin by digest for production:

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/redis@sha256:<digest>
```

## Security Guarantees

| Hardening Control              | Coverage        | Standard Reference         |
|-------------------------------|-----------------|----------------------------|
| Non-root execution            | 99.5% (993/998) | CIS 5.2.1                  |
| HEALTHCHECK instruction       | 100% (998/998)  | Docker best practice       |
| SBOM (SPDX 2.3)              | 100% (998/998)  | NIST SP 800-218            |
| Digest-pinned final stages    | 100% (998/998)  | Supply chain integrity     |
| All-stage FROM digest pinning | 75.3% (1522/2020) | Supply chain integrity  |
| CAP\_DROP ALL documented      | 100%            | CIS 5.3.1                  |
| no-new-privileges documented  | 100%            | CIS 5.3.2                  |
| Multi-stage builds            | 100%            | Attack surface reduction   |
| SOURCE\_DATE\_EPOCH           | 100%            | Reproducible builds        |
| No hardcoded secrets          | 100%            | NIST SP 800-190             |

All images use distroless or wolfi-base final stages. Build tools, compilers, and package managers are never present in the runtime image.

## Image Catalog

Browse the full catalog at [docs/catalog/index.html](docs/catalog/index.html) -- 998 images across 16 categories:

| Category            | Count | Category            | Count |
|---------------------|-------|---------------------|-------|
| Database            | 118   | Monitoring          | 55    |
| Networking          | 112   | CI/CD               | 55    |
| Security            | 109   | Media               | 50    |
| Web App             | 83    | Operator            | 28    |
| Other               | 312   | Tool                | 25    |
|                     |       | Home Automation     | 16    |
|                     |       | Storage             | 15    |
|                     |       | Identity            | 7     |
|                     |       | Container Runtime   | 7     |
|                     |       | Observability       | 5     |
|                     |       | Messaging           | 1     |

## Multi-Arch Support

322 images publish multi-architecture manifests (`linux/amd64`, `linux/arm64`). To pull the correct image for your platform:

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/nginx:1.27
docker buildx imagetools inspect ghcr.io/wyattau/evergreenimageregistry/nginx:1.27
```

Use `--platform` to force a specific architecture:

```bash
docker pull --platform linux/arm64 ghcr.io/wyattau/evergreenimageregistry/nginx:1.27
```

## evergreenctl

`evergreenctl` is the registry management toolchain, written in Rust. It handles image verification, drift detection, Dockerfile generation, and audit operations.

```bash
cd evergreenctl && cargo build --release

evergreenctl audit images/           # Check for stubs and placeholders
evergreenctl verify images/redis/    # Verify checksums
evergreenctl drift images/nginx/     # Detect manifest vs. Dockerfile drift
evergreenctl generate images/postgres/  # Generate Dockerfile from manifest.toml
```

See [evergreenctl/](evergreenctl/) for the full source and command reference.

## Compliance

Reference material for regulated environments:

| Framework | Location | Description |
|-----------|----------|-------------|
| FIPS      | [compliance/fips/](compliance/fips/) | FIPS image matrix and implementation guide |
| CIS       | [compliance/cis/](compliance/cis/) | CIS benchmark scan scripts |
| STIG      | [compliance/stig/](compliance/stig/) | DISA STIG check scripts |
| ATO       | [compliance/ato/](compliance/ato/) | Controls mapping, SSP, POA&M, and risk evidence |

## Architecture

All images follow a layered base hierarchy designed for minimal attack surface:

```
scratch (static binaries)
  > wolfi-base (Chainguard Wolfi -- glibc + CA certs)
    > distroless (Google Distroless -- language-specific runtimes)
```

- **scratch** -- Used for compiled Go, Rust, and C binaries with no runtime dependencies.
- **wolfi** -- Minimal base with glibc, TLS certificates, and timezone data. Used when libc is required.
- **distroless** -- Language-specific runtime bases (Java, Python, Node). Used for interpreted or JVM applications.

Multi-stage builds ensure the final image contains only the application binary and its direct runtime dependencies. No shells, no package managers, no build artifacts.

## Contributing

See [docs/contributing_guide.md](docs/contributing_guide.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

The Dockerfiles, scripts, and tooling in this repository are licensed under the [Apache-2.0](LICENSE) license. Upstream software packaged in the images retains its original license.
