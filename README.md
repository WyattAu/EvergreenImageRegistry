# Evergreen Image Registry

Hardened container images for production, with inventory and coverage metrics generated from the active image tree.

[![Build](https://img.shields.io/github/actions/workflow/status/WyattAu/EvergreenImageRegistry/build.yml?branch=main&style=flat-square&label=CI)](https://github.com/WyattAu/EvergreenImageRegistry/actions/workflows/build.yml)
[![Nightly Scan](https://img.shields.io/github/actions/workflow/status/WyattAu/EvergreenImageRegistry/nightly-scan.yml?branch=main&style=flat-square&label=Nightly%20Scan)](https://github.com/WyattAu/EvergreenImageRegistry/actions/workflows/nightly-scan.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg?style=flat-square)](LICENSE)
[![Image catalog](https://img.shields.io/badge/image%20catalog-generated-green.svg?style=flat-square)](docs/catalog/index.html)
[![SBOM coverage](https://img.shields.io/badge/SBOM%20coverage-generated-brightgreen.svg?style=flat-square)](docs/standards.md)

Evergreen provides a long-term home for open-source container images that vendors have abandoned or moved behind
paywalls. Images target a strict set of [Image Standards](docs/standards.md), including non-root execution, minimal runtime
bases, healthchecks where supported, and reproducible-build controls. Coverage is measured by generated reports; these
artifacts are not a substitute for deployment-specific verification.

## Quick Start

<!-- AUTO_IMAGE_LIST_START -->
<!-- AUTO_IMAGE_LIST_END -->

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

| Hardening Control             | Coverage          | Standard Reference       |
| ----------------------------- | ----------------- | ------------------------ |
| Non-root execution            | Generated         | CIS 4.5.1                |
| HEALTHCHECK instruction       | Generated         | Docker best practice     |
| SBOM (SPDX 2.3)               | Generated         | NIST SP 800-218          |
| Digest-pinned final stages    | Generated         | Supply chain integrity   |
| Critical-tier FROM pinning    | Blocking in CI    | Supply chain integrity   |
| Standard-tier FROM pinning    | Tracked debt      | Supply chain integrity   |
| CAP_DROP ALL documented       | Policy target     | CIS 4.5.3                |
| no-new-privileges documented  | Policy target     | CIS 4.5.1                |
| Multi-stage builds            | Generated         | Attack surface reduction |
| SOURCE_DATE_EPOCH             | Build control     | Reproducible builds      |
| No hardcoded secrets          | Generated         | NIST SP 800-53 SC-12     |

Images are intended to use approved minimal final stages. Build tools, compilers, and package managers should be
excluded from runtime images; the validation pipeline remains the authoritative source for coverage.

## Image Catalog

Browse the full catalog at [docs/catalog/index.html](docs/catalog/index.html). The catalog generator derives the
current image count and categories from active image directories:

| Category   | Count | Category          | Count |
| ---------- | ----- | ----------------- | ----- |
| Database   | 118   | Monitoring        | 55    |
| Networking | 112   | CI/CD             | 55    |
| Security   | 109   | Media             | 50    |
| Web App    | 83    | Operator          | 28    |
| Other      | 312   | Tool              | 25    |
|            |       | Home Automation   | 16    |
|            |       | Storage           | 15    |
|            |       | Identity          | 7     |
|            |       | Container Runtime | 7     |
|            |       | Observability     | 5     |
|            |       | Messaging         | 1     |

## Multi-Arch Support

31 images declare multi-architecture support via `ARG TARGETARCH` (`linux/amd64`, `linux/arm64`). To pull the correct
image for your platform:

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/nginx:1.27
docker buildx imagetools inspect ghcr.io/wyattau/evergreenimageregistry/nginx:1.27
```

Use `--platform` to force a specific architecture:

```bash
docker pull --platform linux/arm64 ghcr.io/wyattau/evergreenimageregistry/nginx:1.27
```

## evergreenctl

`evergreenctl` is the registry management toolchain, written in Rust. It handles image verification, drift detection,
Dockerfile generation, and audit operations.

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

| Framework | Location                             | Description                                     |
| --------- | ------------------------------------ | ----------------------------------------------- |
| FIPS      | [compliance/fips/](compliance/fips/) | FIPS image matrix and implementation guide      |
| CIS       | [compliance/cis/](compliance/cis/)   | CIS benchmark scan scripts                      |
| STIG      | [compliance/stig/](compliance/stig/) | DISA STIG check scripts                         |
| ATO       | [compliance/ato/](compliance/ato/)   | Controls mapping, SSP, POA&M, and risk evidence |

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

Multi-stage builds ensure the final image contains only the application binary and its direct runtime dependencies. No
shells, no package managers, no build artifacts.

## Contributing

See [docs/contributing_guide.md](docs/contributing_guide.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

The Dockerfiles, scripts, and tooling in this repository are licensed under the [Apache-2.0](LICENSE) license. Upstream
software packaged in the images retains its original license.
