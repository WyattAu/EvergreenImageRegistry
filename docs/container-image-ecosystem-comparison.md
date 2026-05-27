# Container Image Ecosystem Comparison Matrix

> Comprehensive comparison of container image build systems, supply chain security standards, and language-native
> tooling for building secure, reproducible OCI images.
>
> Generated: 2026-05-27 | Scope: EvergreenImageRegistry architecture decision

---

## Table of Contents

- [Part 1: Build Ecosystem Comparison](#part-1-build-ecosystem-comparison)
- [Part 2: Supply Chain Standards](#part-2-supply-chain-standards)
- [Part 3: Language-Native Tooling (Rust/C++)](#part-3-language-native-tooling-rustc)
- [Part 4: Decision Framework](#part-4-decision-framework)
- [Part 5: Recommended Architecture for EIR](#part-5-recommended-architecture-for-eir)

---

## Part 1: Build Ecosystem Comparison

### Quick Reference

| Ecosystem            | Language       | Package Format  | Base System      | libc       | Reproducibility | Image Size      | License       | Governance                    |
| -------------------- | -------------- | --------------- | ---------------- | ---------- | --------------- | --------------- | ------------- | ----------------------------- |
| Chainguard/Wolfi     | Go             | apk             | Wolfi (musl)     | musl       | Bitwise         | 2-20 MB         | Apache-2.0    | Corporate (Chainguard)        |
| Google distroless    | Starlark/Bazel | None            | scratch          | none       | Bazel-hermetic  | 2-80 MB         | Apache-2.0    | Corporate (Google)            |
| Alpine Linux         | Shell/make     | apk             | Alpine           | musl       | Partial         | ~5 MB base      | MIT           | Community                     |
| Red Hat UBI          | RPM Spec       | rpm             | RHEL             | glibc      | Low             | 38-85 MB        | GPL/Copyright | Corporate (Red Hat)           |
| NixOS/Nixpkgs        | Nix (Haskell)  | nix             | NixOS            | glibc/musl | Excellent       | 20-200 MB+      | LGPL-2.1      | Community (NixOS Foundation)  |
| CBL-Mariner          | Go/RPM         | rpm             | Mariner          | glibc      | Low-Mod         | 30-50 MB        | MIT           | Corporate (Microsoft)         |
| Debian Minbase       | Shell          | dpkg            | Debian           | glibc      | Strong          | 50-120 MB       | DFSG-free     | Community (Debian)            |
| Fedora Minimal/Bootc | Rust/RPM       | rpm             | Fedora           | glibc      | Low-Mod         | 70-500 MB       | Various open  | Community (Fedora)            |
| CNB/Paketo           | Go             | N/A (auto)      | Buildpack base   | varies     | Moderate        | 50-200 MB       | Apache-2.0    | CNCF                          |
| Bazel rules_oci      | Starlark       | N/A (builds in) | Custom           | any        | Excellent       | Variable        | Apache-2.0    | Community                     |
| Buildah              | Go             | rpm/dpkg/apk    | Any              | any        | Low-Mod         | Variable        | Apache-2.0    | Community (containers/podman) |
| Earthly              | Go             | N/A             | Dockerfile-based | any        | Good            | Variable        | MPL-2.0       | Community (unmaintained)      |
| ko                   | Go             | N/A             | Go-static        | musl       | Good            | 5-50 MB         | Apache-2.0    | CNCF                          |
| Zarf                 | Go             | N/A (packaging) | Any              | any        | Moderate        | N/A (packaging) | Apache-2.0    | CNCF (Defense Unicorns)       |

### Detailed Profiles

#### 1. Chainguard/Wolfi

| Attribute                 | Detail                                                                                                                                                                                                                                                                    |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub**                | github.com/chainguard-dev/melange, github.com/chainguard-dev/apko                                                                                                                                                                                                         |
| **Primary Language**      | Go                                                                                                                                                                                                                                                                        |
| **Build Tool**            | melange (package builder) + apko (image composer)                                                                                                                                                                                                                         |
| **Package Format**        | apk (Alpine Package Keeper)                                                                                                                                                                                                                                               |
| **Base System**           | Wolfi Linux (musl-based, no shell by default)                                                                                                                                                                                                                             |
| **libc**                  | musl                                                                                                                                                                                                                                                                      |
| **Reproducibility**       | Bitwise reproducible. Same melange config + same source tarball = identical `.apk` and identical image digest. Achieved via controlled build environment and deterministic compiler flags.                                                                                |
| **SBOM Support**          | SPDX 2.3 generated by melange for every package. Image-level SBOM composed by apko from package SBOMs. Attached as OCI attestation.                                                                                                                                       |
| **Multi-arch**            | x86_64, arm64, armv7, s390x, ppc64le                                                                                                                                                                                                                                      |
| **Typical Image Size**    | nginx: ~2 MB, python: ~15 MB, node: ~20 MB (distroless variants)                                                                                                                                                                                                          |
| **License**               | Apache-2.0 (tooling), images under Chainguard Terms                                                                                                                                                                                                                       |
| **Governance**            | Corporate (Chainguard Inc.). Images free for non-production; production use requires subscription.                                                                                                                                                                        |
| **OCI Compliant**         | Yes. Produces standard OCI images with image index for multi-arch.                                                                                                                                                                                                        |
| **SLSA Level**            | L3 (hardened build platform). Build provenance signed and stored in Transparency Log.                                                                                                                                                                                     |
| **Sigstore/Cosign**       | Yes. All images signed with cosign (keyless via Fulcio).                                                                                                                                                                                                                  |
| **in-toto**               | Yes. SLSA provenance uses in-toto attestation format.                                                                                                                                                                                                                     |
| **CVE Scanning**          | Built-in. Wolfi Security Advisories (WSA) database. Trivy/gatekeeper integration.                                                                                                                                                                                         |
| **C Compatibility**       | Limited. musl libc has differences from glibc (e.g., `strptime` locale support, resolver behavior). Static C binaries work well.                                                                                                                                          |
| **C++ Compatibility**     | Limited. musl's libstdc++ support is partial. Complex C++ apps (Boost, Qt) often need glibc. Static linking of C++ works but produces larger binaries.                                                                                                                    |
| **Rust Compatibility**    | Excellent. Rust targets `x86_64-unknown-linux-musl` natively. `static-musl` target produces fully static binaries. Most Rust crates work on musl without modification.                                                                                                    |
| **Static Binary Support** | Yes. Primary use case. Most Wolfi images contain a single static binary + ca-certificates.                                                                                                                                                                                |
| **Key Constraints**       | 1) Production images require paid subscription. 2) No shell in images by default (debugging harder). 3) musl libc incompatibilities for glibc-dependent apps. 4) Package count limited (~3000 vs Debian's ~60,000). 5) Not all upstream projects build cleanly with musl. |
| **Key URLs**              | https://github.com/chainguard-dev/melange, https://github.com/chainguard-dev/apko, https://wolfi.dev                                                                                                                                                                      |

#### 2. Google Distroless

| Attribute                 | Detail                                                                                                                                                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **GitHub**                | github.com/GoogleContainerTools/distroless                                                                                                                                                                                     |
| **Primary Language**      | Starlark (Bazel)                                                                                                                                                                                                               |
| **Build Tool**            | Bazel (bazelbuild/rules_docker, bazelbuild/rules_oci)                                                                                                                                                                          |
| **Package Format**        | None. No package manager in images.                                                                                                                                                                                            |
| **Base System**           | scratch or minimal debian with glibc                                                                                                                                                                                           |
| **libc**                  | none (static) or glibc (for dynamically linked variants)                                                                                                                                                                       |
| **Reproducibility**       | Bazel-hermetic. Same Bazel version + same inputs = identical image. Bazel's sandboxing ensures deterministic builds.                                                                                                           |
| **SBOM Support**          | SPDX generated during Bazel build. Available per-language (python, java, node).                                                                                                                                                |
| **Multi-arch**            | x86_64, arm64                                                                                                                                                                                                                  |
| **Typical Image Size**    | static: ~2 MB, python3: ~30 MB, java17: ~80 MB, nodejs20: ~80 MB                                                                                                                                                               |
| **License**               | Apache-2.0                                                                                                                                                                                                                     |
| **Governance**            | Corporate (Google). Community PRs accepted but Google-controlled.                                                                                                                                                              |
| **OCI Compliant**         | Yes                                                                                                                                                                                                                            |
| **SLSA Level**            | L2 (signed provenance). Built on Google's internal CI which provides L3 guarantees.                                                                                                                                            |
| **Sigstore/Cosign**       | Yes. All images signed.                                                                                                                                                                                                        |
| **in-toto**               | Partial (provenance only)                                                                                                                                                                                                      |
| **CVE Scanning**          | Not built-in. Relies on external scanners (Trivy, Grype).                                                                                                                                                                      |
| **C Compatibility**       | Limited. Only available for pre-built language runtimes (Go, Java, Python, Node.js). No general C/C++ support.                                                                                                                 |
| **C++ Compatibility**     | None. No C++ runtime images.                                                                                                                                                                                                   |
| **Rust Compatibility**    | Excellent via `distroless/static-debian12`. Rust static binaries run on any distroless image.                                                                                                                                  |
| **Static Binary Support** | Yes. `distroless/static` is an empty image (scratch + ca-certs + tzdata).                                                                                                                                                      |
| **Key Constraints**       | 1) No shell. Debugging requires `kubectl exec` with a shell image. 2) Limited to pre-built language images. 3) No general-purpose base. 4) glibc variant images are larger. 5) Package versions controlled by Google, not you. |
| **Key URLs**              | https://github.com/GoogleContainerTools/distroless, https://github.com/GoogleContainerTools/kaniko                                                                                                                             |

#### 3. Alpine Linux

| Attribute                 | Detail                                                                                                                                                                                                                                                                 |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub**                | github.com/alpine/docker-alpine                                                                                                                                                                                                                                        |
| **Primary Language**      | Shell / C (apk-tools in C)                                                                                                                                                                                                                                             |
| **Build Tool**            | make, abuild (APK build system)                                                                                                                                                                                                                                        |
| **Package Format**        | apk                                                                                                                                                                                                                                                                    |
| **Base System**           | Alpine Linux                                                                                                                                                                                                                                                           |
| **libc**                  | musl                                                                                                                                                                                                                                                                   |
| **Reproducibility**       | Partial. Alpine has reproducible build goals but not yet fully achieved. Images built from same apk DB are reproducible.                                                                                                                                               |
| **SBOM Support**          | None built-in. External tools (syft, trivy) can scan Alpine images.                                                                                                                                                                                                    |
| **Multi-arch**            | x86_64, arm64, armv7, s390x, ppc64le, riscv64                                                                                                                                                                                                                          |
| **Typical Image Size**    | ~5 MB (base), ~8 MB (with shell)                                                                                                                                                                                                                                       |
| **License**               | MIT                                                                                                                                                                                                                                                                    |
| **Governance**            | Community (Alpine Linux Maintainers). Small core team.                                                                                                                                                                                                                 |
| **OCI Compliant**         | Yes                                                                                                                                                                                                                                                                    |
| **SLSA Level**            | L0 (no provenance). No signed builds.                                                                                                                                                                                                                                  |
| **Sigstore/Cosign**       | No. Images not signed by default.                                                                                                                                                                                                                                      |
| **in-toto**               | No                                                                                                                                                                                                                                                                     |
| **CVE Scanning**          | Alpine Security Advisories (ASA). No built-in scanning.                                                                                                                                                                                                                |
| **C Compatibility**       | Limited. musl differences from glibc. Static C works well. Dynamic linking to glibc-only libs fails.                                                                                                                                                                   |
| **C++ Compatibility**     | Limited. Same musl issues as Wolfi. Many C++ frameworks require glibc.                                                                                                                                                                                                 |
| **Rust Compatibility**    | Excellent. `x86_64-unknown-linux-musl` target is well-tested. `alpine` is the most common Rust CI base.                                                                                                                                                                |
| **Static Binary Support** | Yes. Primary use case.                                                                                                                                                                                                                                                 |
| **Key Constraints**       | 1) musl libc (glibc incompatibilities). 2) No built-in SBOM or signing. 3) `apk add` available at build time only in most images. 4) No shell in `scratch` variant. 5) OpenSSL replaced with LibreSSL (API differences). 6) `getaddrinfo` behavior differs from glibc. |
| **Key URLs**              | https://github.com/alpine/docker-alpine, https://alpinelinux.org                                                                                                                                                                                                       |

#### 4. Red Hat UBI

| Attribute                 | Detail                                                                                                                                                                                                                                                |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub**                | github.com/redhat-developer/docker-images (examples)                                                                                                                                                                                                  |
| **Primary Language**      | RPM Spec / Shell                                                                                                                                                                                                                                      |
| **Build Tool**            | rpm-build, koji, osbuild                                                                                                                                                                                                                              |
| **Package Format**        | rpm                                                                                                                                                                                                                                                   |
| **Base System**           | RHEL (Red Hat Enterprise Linux)                                                                                                                                                                                                                       |
| **libc**                  | glibc                                                                                                                                                                                                                                                 |
| **Reproducibility**       | Low. RHEL builds are not bit-for-bit reproducible. UBI images are built from RHEL packages.                                                                                                                                                           |
| **SBOM Support**          | None built-in. Red Hat products have internal SBOMs.                                                                                                                                                                                                  |
| **Multi-arch**            | x86_64, arm64, s390x, ppc64le                                                                                                                                                                                                                         |
| **Typical Image Size**    | ubi9-init: ~85 MB, ubi9-minimal: ~38 MB, ubi9-micro: ~28 MB                                                                                                                                                                                           |
| **License**               | GPL (packages), freely redistributable UBI                                                                                                                                                                                                            |
| **Governance**            | Corporate (Red Hat / IBM). Enterprise support available.                                                                                                                                                                                              |
| **OCI Compliant**         | Yes                                                                                                                                                                                                                                                   |
| **SLSA Level**            | L0 externally. Internal builds may be higher.                                                                                                                                                                                                         |
| **Sigstore/Cosign**       | No for public images.                                                                                                                                                                                                                                 |
| **in-toto**               | No                                                                                                                                                                                                                                                    |
| **CVE Scanning**          | Red Hat Security Advisories (RHSA). Built-in with subscription.                                                                                                                                                                                       |
| **C Compatibility**       | Excellent. Full glibc. All C libraries available. ABI-stable.                                                                                                                                                                                         |
| **C++ Compatibility**     | Excellent. Full libstdc++. Boost, Qt, and all major C++ frameworks available in repos.                                                                                                                                                                |
| **Rust Compatibility**    | Good. `x86_64-unknown-linux-gnu` target. System OpenSSL (not BoringSSL). May need `pkg-config` and dev packages at build time.                                                                                                                        |
| **Static Binary Support** | Possible but not idiomatic. RPM-based system assumes dynamic linking.                                                                                                                                                                                 |
| **Key Constraints**       | 1) Larger images (glibc overhead). 2) RPM ecosystem (steeper learning curve than apk/dpkg). 3) No built-in SBOM/signing for public images. 4) Enterprise focus (some packages require subscription). 5) Slower update cadence than community distros. |
| **Key URLs**              | https://catalog.redhat.com/software/containers/ubi, https://github.com/redhat-developer/docker-images                                                                                                                                                 |

#### 5. NixOS/Nixpkgs

| Attribute                 | Detail                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **GitHub**                | github.com/NixOS/nixpkgs, github.com/NixOS/nix                                                                                                                                                                                                                                                                                                         |
| **Primary Language**      | Nix (Haskell-based DSL)                                                                                                                                                                                                                                                                                                                                |
| **Build Tool**            | Nix (build system + package manager + language)                                                                                                                                                                                                                                                                                                        |
| **Package Format**        | Nix store paths (content-addressed, immutable)                                                                                                                                                                                                                                                                                                         |
| **Base System**           | NixOS or custom via Nix expressions                                                                                                                                                                                                                                                                                                                    |
| **libc**                  | glibc (default) or musl (via `pkgsStatic`)                                                                                                                                                                                                                                                                                                             |
| **Reproducibility**       | Excellent. Nix is purely functional: same expression + same inputs = identical output, always. Fixed-output derivations pinned by SHA256. Binary cache for sharing builds.                                                                                                                                                                             |
| **SBOM Support**          | SPDX via `nix sbom` command (experimental). Or via external scanning.                                                                                                                                                                                                                                                                                  |
| **Multi-arch**            | x86_64, arm64 (via cross-compilation or remote builders)                                                                                                                                                                                                                                                                                               |
| **Typical Image Size**    | Minimal: ~20 MB, Full service: 100-500 MB+ (depends on closure size)                                                                                                                                                                                                                                                                                   |
| **License**               | LGPL-2.1                                                                                                                                                                                                                                                                                                                                               |
| **Governance**            | Community (NixOS Foundation). Large contributor base (~5000+).                                                                                                                                                                                                                                                                                         |
| **OCI Compliant**         | Yes (via `pkgs.dockerTools.buildImage` or `pkgs.ociTools`)                                                                                                                                                                                                                                                                                             |
| **SLSA Level**            | L2 achievable. Nix builds are hermetic and reproducible. External provenance signing needed for L3.                                                                                                                                                                                                                                                    |
| **Sigstore/Cosign**       | Not built-in. Can be integrated into Nix derivations.                                                                                                                                                                                                                                                                                                  |
| **in-toto**               | Not built-in. Community tools exist.                                                                                                                                                                                                                                                                                                                   |
| **CVE Scanning**          | Nix Vulnerability Scanning (nixpkgs-vuln-scan). Not built into build pipeline.                                                                                                                                                                                                                                                                         |
| **C Compatibility**       | Excellent. Full glibc. All C libraries available as Nix derivations. Static C possible via `pkgsStatic`.                                                                                                                                                                                                                                               |
| **C++ Compatibility**     | Excellent. Full C++ toolchain. All major frameworks available. `pkgsStatic` for static C++.                                                                                                                                                                                                                                                            |
| **Rust Compatibility**    | Excellent. `pkgs.rustc`, `pkgs.cargo`, `naersk`, `crane` (Nix-based Rust build helper). Cross-compilation well-supported.                                                                                                                                                                                                                              |
| **Static Binary Support** | Yes. `pkgsStatic` produces statically linked packages. `pkgsMusl` for musl-based static builds.                                                                                                                                                                                                                                                        |
| **Key Constraints**       | 1) Steep learning curve (Nix language is unique). 2) Image sizes can be large (Nix store model). 3) No standard Dockerfiles (must write Nix expressions). 4) Debugging images requires Nix knowledge. 5) CI/CD integration requires Nix installation. 6) Large closure sizes for complex applications. 7) Nix language is Haskell-based, not Rust/C++. |
| **Key URLs**              | https://github.com/NixOS/nixpkgs, https://nixos.org, https://nix.dev                                                                                                                                                                                                                                                                                   |

#### 6. CBL-Mariner (Azure Linux)

| Attribute                 | Detail                                                                                                                                                                            |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub**                | github.com/microsoft/CBL-Mariner                                                                                                                                                  |
| **Primary Language**      | Go (tooling) + RPM Spec (packages)                                                                                                                                                |
| **Build Tool**            | mariner-toolkit (custom build system), rpm-build                                                                                                                                  |
| **Package Format**        | rpm                                                                                                                                                                               |
| **Base System**           | CBL-Mariner (Azure Linux)                                                                                                                                                         |
| **libc**                  | glibc                                                                                                                                                                             |
| **Reproducibility**       | Low-Moderate. Build system is deterministic in theory but not bit-for-bit verified.                                                                                               |
| **SBOM Support**          | SPDX generated during build. Integrated into build pipeline.                                                                                                                      |
| **Multi-arch**            | x86_64, arm64                                                                                                                                                                     |
| **Typical Image Size**    | base: ~30 MB, full: ~50 MB                                                                                                                                                        |
| **License**               | MIT                                                                                                                                                                               |
| **Governance**            | Corporate (Microsoft). Used internally for Azure services.                                                                                                                        |
| **OCI Compliant**         | Yes                                                                                                                                                                               |
| **SLSA Level**            | L1-L2. Build provenance generated.                                                                                                                                                |
| **Sigstore/Cosign**       | Partial (internal Microsoft signing).                                                                                                                                             |
| **in-toto**               | Partial (provenance generation).                                                                                                                                                  |
| **CVE Scanning**          | Built-in. Microsoft Security Response Center (MSRC) advisories.                                                                                                                   |
| **C Compatibility**       | Good. glibc-based. Standard Linux toolchain.                                                                                                                                      |
| **C++ Compatibility**     | Good. glibc-based. Standard C++ toolchain.                                                                                                                                        |
| **Rust Compatibility**    | Good. glibc-based. Standard Rust targets.                                                                                                                                         |
| **Static Binary Support** | Possible but not idiomatic. RPM-based system.                                                                                                                                     |
| **Key Constraints**       | 1) Microsoft-controlled. 2) Limited community adoption outside Azure. 3) Smaller package set than Debian/RHEL. 4) Documentation gaps. 5) Designed for Azure, not general-purpose. |
| **Key URLs**              | https://github.com/microsoft/CBL-Mariner                                                                                                                                          |

#### 7. Debian Minbase / Reproducible Builds

| Attribute                 | Detail                                                                                                                                                                                                                 |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub**                | github.com/docker-library/buildpack-deps, reproducible-builds.org                                                                                                                                                      |
| **Primary Language**      | Shell                                                                                                                                                                                                                  |
| **Build Tool**            | debootstrap, dpkg-buildpackage                                                                                                                                                                                         |
| **Package Format**        | dpkg (deb)                                                                                                                                                                                                             |
| **Base System**           | Debian (stable: Trixie 13)                                                                                                                                                                                             |
| **libc**                  | glibc                                                                                                                                                                                                                  |
| **Reproducibility**       | Strong. Debian Reproducible Builds project has achieved 95%+ reproducibility for packages. Build environment differences still cause some variation.                                                                   |
| **SBOM Support**          | None built-in. External tools (syft, dpkg-query) can generate from installed packages.                                                                                                                                 |
| **Multi-arch**            | x86_64, arm64, armhf, i386, ppc64el, s390x, mips64el, riscv64                                                                                                                                                          |
| **Typical Image Size**    | minbase: ~50 MB, slim: ~75 MB, full: ~120 MB                                                                                                                                                                           |
| **License**               | DFSG-free (Debian Free Software Guidelines)                                                                                                                                                                            |
| **Governance**            | Community (Debian Project). Democratic governance. Large contributor base.                                                                                                                                             |
| **OCI Compliant**         | Yes (official Docker Hub images)                                                                                                                                                                                       |
| **SLSA Level**            | L0. No provenance for official images.                                                                                                                                                                                 |
| **Sigstore/Cosign**       | No.                                                                                                                                                                                                                    |
| **in-toto**               | No.                                                                                                                                                                                                                    |
| **CVE Scanning**          | Debian Security Advisories (DSA). Debian Security Tracker. External scanning recommended.                                                                                                                              |
| **C Compatibility**       | Excellent. Reference glibc implementation. All C libraries available.                                                                                                                                                  |
| **C++ Compatibility**     | Excellent. Reference platform for C++ development. All frameworks available.                                                                                                                                           |
| **Rust Compatibility**    | Excellent. Most Rust CI uses `debian:bookworm` or `ubuntu`. Full OpenSSL support.                                                                                                                                      |
| **Static Binary Support** | Possible. `apt install libc6-dev` + build with `-static`. Not idiomatic.                                                                                                                                               |
| **Key Constraints**       | 1) Larger images (glibc overhead). 2) Slower update cycle (2-year stable release). 3) No built-in signing/SBOM. 4) Reproducibility at package level, not image level. 5) Multi-stage builds needed for minimal images. |
| **Key URLs**              | https://reproducible-builds.org, https://hub.docker.com/_/debian                                                                                                                                                       |

#### 8. Fedora Minimal / Bootc

| Attribute                 | Detail                                                                                                                                                                        |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub**                | github.com/fedora-cloud/docker-brew-fedora, github.com/cgwalters/bootc                                                                                                        |
| **Primary Language**      | Rust (bootc), Shell/RPM                                                                                                                                                       |
| **Build Tool**            | rpm-build, bootc (Rust-based container-to-disk tool)                                                                                                                          |
| **Package Format**        | rpm (dnf)                                                                                                                                                                     |
| **Base System**           | Fedora Linux                                                                                                                                                                  |
| **libc**                  | glibc                                                                                                                                                                         |
| **Reproducibility**       | Low-Moderate. Fedora has reproducibility goals but not yet achieved. Bootc adds deterministic image building.                                                                 |
| **SBOM Support**          | None built-in for images. RPM packages have changelog metadata.                                                                                                               |
| **Multi-arch**            | x86_64, arm64, ppc64le, s390x                                                                                                                                                 |
| **Typical Image Size**    | minimal: ~70 MB, full: ~200-500 MB                                                                                                                                            |
| **License**               | Various open source licenses                                                                                                                                                  |
| **Governance**            | Community (Fedora Project). Sponsored by Red Hat.                                                                                                                             |
| **OCI Compliant**         | Yes. Bootc produces OCI images that are also bootable disks.                                                                                                                  |
| **SLSA Level**            | L0.                                                                                                                                                                           |
| **Sigstore/Cosign**       | No.                                                                                                                                                                           |
| **in-toto**               | No.                                                                                                                                                                           |
| **CVE Scanning**          | Fedora Security Advisories (FEDSA). Bodhi update system.                                                                                                                      |
| **C Compatibility**       | Excellent. Bleeding-edge glibc. Latest toolchain versions.                                                                                                                    |
| **C++ Compatibility**     | Excellent. Latest GCC/libstdc++. All frameworks available.                                                                                                                    |
| **Rust Compatibility**    | Excellent. Fedora often ships latest Rust version. System OpenSSL. `bootc` is written in Rust.                                                                                |
| **Static Binary Support** | Possible but not idiomatic.                                                                                                                                                   |
| **Key Constraints**       | 1) Rolling release (fast updates = more change). 2) Larger images. 3) Bootc is new and evolving. 4) No built-in signing/SBOM. 5) Less stable than Debian/RHEL for production. |
| **Key URLs**              | https://github.com/cgwalters/bootc, https://docs.fedoraproject.org                                                                                                            |

#### 9. Cloud Native Buildpacks (CNB / Paketo)

| Attribute                 | Detail                                                                                                                                                                                                                                                                  |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub**                | github.com/buildpacks/pack, github.com/paketo-buildpacks                                                                                                                                                                                                                |
| **Primary Language**      | Go                                                                                                                                                                                                                                                                      |
| **Build Tool**            | pack CLI + buildpacks (language-specific)                                                                                                                                                                                                                               |
| **Package Format**        | N/A (auto-detects language, installs dependencies)                                                                                                                                                                                                                      |
| **Base System**           | Buildpack base images (Ubuntu/Alpine based)                                                                                                                                                                                                                             |
| **libc**                  | varies (Ubuntu=glibc, Alpine=musl)                                                                                                                                                                                                                                      |
| **Reproducibility**       | Moderate. Same app source + same buildpack version = similar image. Not bit-for-bit reproducible.                                                                                                                                                                       |
| **SBOM Support**          | CycloneDX via Syft integration. Generated during build.                                                                                                                                                                                                                 |
| **Multi-arch**            | x86_64, arm64                                                                                                                                                                                                                                                           |
| **Typical Image Size**    | 50-200 MB (language runtime + dependencies)                                                                                                                                                                                                                             |
| **License**               | Apache-2.0 (CNB spec), various (buildpacks)                                                                                                                                                                                                                             |
| **Governance**            | CNCF. Paketo buildpacks maintained by VMware/Broadcom.                                                                                                                                                                                                                  |
| **OCI Compliant**         | Yes                                                                                                                                                                                                                                                                     |
| **SLSA Level**            | L0.                                                                                                                                                                                                                                                                     |
| **Sigstore/Cosign**       | No built-in. Can be added as a buildpack.                                                                                                                                                                                                                               |
| **in-toto**               | No.                                                                                                                                                                                                                                                                     |
| **CVE Scanning**          | Via CycloneDX SBOM + external scanning.                                                                                                                                                                                                                                 |
| **C Compatibility**       | Poor. No C/C++ buildpacks. Must use custom buildpack.                                                                                                                                                                                                                   |
| **C++ Compatibility**     | Poor. No C++ buildpacks. Must use custom buildpack.                                                                                                                                                                                                                     |
| **Rust Compatibility**    | Poor. No Rust buildpacks. Must use custom buildpack.                                                                                                                                                                                                                    |
| **Static Binary Support** | Limited. Buildpacks assume dynamic linking. Custom buildpacks can do static.                                                                                                                                                                                            |
| **Key Constraints**       | 1) Language support limited to popular runtimes (Java, Node, Python, Go, .NET). 2) No C/C++/Rust support. 3) "Magic" build process (less control). 4) Buildpack version pinning needed for reproducibility. 5) Custom buildpacks required for non-mainstream languages. |
| **Key URLs**              | https://buildpacks.io, https://paketo.io                                                                                                                                                                                                                                |

#### 10. Bazel rules_oci

| Attribute                 | Detail                                                                                                                                                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **GitHub**                | github.com/bazel-contrib/rules_oci                                                                                                                                                                                                               |
| **Primary Language**      | Starlark (Bazel DSL)                                                                                                                                                                                                                             |
| **Build Tool**            | Bazel + rules_oci                                                                                                                                                                                                                                |
| **Package Format**        | N/A (builds from source within Bazel graph)                                                                                                                                                                                                      |
| **Base System**           | Any (defined by Bazel targets)                                                                                                                                                                                                                   |
| **libc**                  | any (depends on toolchain configuration)                                                                                                                                                                                                         |
| **Reproducibility**       | Excellent. Bazel is hermetic by design: sandboxed builds, content-addressed cache, deterministic output. Same BUILD file + same sources = identical image.                                                                                       |
| **SBOM Support**          | Via external tools or custom Bazel rules. Not built-in.                                                                                                                                                                                          |
| **Multi-arch**            | Yes (via Bazel toolchain transitions or `--platforms` flags)                                                                                                                                                                                     |
| **Typical Image Size**    | Variable (depends on what you build into it)                                                                                                                                                                                                     |
| **License**               | Apache-2.0                                                                                                                                                                                                                                       |
| **Governance**            | Community. Bazel ecosystem maintained by various orgs (Google, Aspect, etc.).                                                                                                                                                                    |
| **OCI Compliant**         | Yes. Produces standard OCI manifests, configs, and image indices.                                                                                                                                                                                |
| **SLSA Level**            | L2-L3 achievable. Bazel's hermeticity provides strong provenance. External signing needed.                                                                                                                                                       |
| **Sigstore/Cosign**       | Yes (via `rules_oci` cosign integration or `rules_signing`).                                                                                                                                                                                     |
| **in-toto**               | Via external rules. Not built-in.                                                                                                                                                                                                                |
| **CVE Scanning**          | External. `rules_oci` produces deterministic images that can be scanned.                                                                                                                                                                         |
| **C Compatibility**       | Excellent. Bazel has first-class C/C++ support (`rules_cc`). Builds C with Clang or GCC.                                                                                                                                                         |
| **C++ Compatibility**     | Excellent. Full C++ toolchain via `rules_cc`. Can build complex C++ applications.                                                                                                                                                                |
| **Rust Compatibility**    | Good. `rules_rust` provides Rust toolchain for Bazel. Cross-compilation supported.                                                                                                                                                               |
| **Static Binary Support** | Yes. Linker flags controlled via Bazel `linkopts`.                                                                                                                                                                                               |
| **Key Constraints**       | 1) Bazel learning curve. 2) Requires Bazel installation in CI. 3) Starlark DSL, not Rust/C++. 4) Complex setup for mixed-language projects. 5) Larger organizations tend to have custom Bazel rules. 6) Build graph can be opaque for debugging. |
| **Key URLs**              | https://github.com/bazel-contrib/rules_oci, https://bazel.build                                                                                                                                                                                  |

#### 11. Buildah

| Attribute                 | Detail                                                                                                                                                                                          |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub**                | github.com/containers/buildah                                                                                                                                                                   |
| **Primary Language**      | Go                                                                                                                                                                                              |
| **Build Tool**            | buildah CLI (OCI-native, daemonless)                                                                                                                                                            |
| **Package Format**        | Any (rpm, dpkg, apk via Containerfile RUN)                                                                                                                                                      |
| **Base System**           | Any (FROM any image)                                                                                                                                                                            |
| **libc**                  | any (depends on base image)                                                                                                                                                                     |
| **Reproducibility**       | Low-Moderate. Depends on Containerfile determinism. No hermetic sandbox like Bazel.                                                                                                             |
| **SBOM Support**          | None built-in. External scanning (syft, trivy) against built images.                                                                                                                            |
| **Multi-arch**            | Yes (via `buildah build --platform`)                                                                                                                                                            |
| **Typical Image Size**    | Variable (depends on base and packages)                                                                                                                                                         |
| **License**               | Apache-2.0                                                                                                                                                                                      |
| **Governance**            | Community (containers/podman ecosystem). Red Hat contributors. CNCF podman graduation.                                                                                                          |
| **OCI Compliant**         | Yes. Full OCI implementation.                                                                                                                                                                   |
| **SLSA Level**            | L0. No provenance.                                                                                                                                                                              |
| **Sigstore/Cosign**       | No built-in. Can pipe to cosign externally.                                                                                                                                                     |
| **in-toto**               | No.                                                                                                                                                                                             |
| **CVE Scanning**          | External. Can integrate with Trivy.                                                                                                                                                             |
| **C Compatibility**       | Excellent. Can install any C toolchain via package manager.                                                                                                                                     |
| **C++ Compatibility**     | Excellent. Can install any C++ toolchain.                                                                                                                                                       |
| **Rust Compatibility**    | Good. Install Rust via `RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh`.                                                                                                   |
| **Static Binary Support** | Yes. COPY pre-built static binary into image.                                                                                                                                                   |
| **Key Constraints**       | 1) No hermetic builds (RUN steps are non-deterministic). 2) No SBOM/signing. 3) Containerfile syntax only (no declarative config). 4) No content-addressed layers. 5) Go-native (not Rust/C++). |
| **Key URLs**              | https://github.com/containers/buildah                                                                                                                                                           |

#### 12. Earthly (Note: Unmaintained)

| Attribute                 | Detail                                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------------------ |
| **GitHub**                | github.com/earthly/earthly                                                                             |
| **Primary Language**      | Go                                                                                                     |
| **Build Tool**            | Earthfile (Dockerfile-like + Makefile hybrid)                                                          |
| **Package Format**        | Any (via Dockerfile-like RUN)                                                                          |
| **Base System**           | Any                                                                                                    |
| **libc**                  | any                                                                                                    |
| **Reproducibility**       | Good. Build caching + deterministic targets.                                                           |
| **SBOM Support**          | None built-in.                                                                                         |
| **Multi-arch**            | Yes (via `--platform`)                                                                                 |
| **Typical Image Size**    | Variable                                                                                               |
| **License**               | MPL-2.0 (code), Business Source License (enterprise)                                                   |
| **Governance**            | Community. **Announced unmaintained July 2025.** Not recommended for new projects.                     |
| **OCI Compliant**         | Yes (via Docker/buildkit backend)                                                                      |
| **SLSA Level**            | L0                                                                                                     |
| **Sigstore/Cosign**       | No.                                                                                                    |
| **in-toto**               | No.                                                                                                    |
| **CVE Scanning**          | External.                                                                                              |
| **C Compatibility**       | Good (via standard Dockerfile RUN).                                                                    |
| **C++ Compatibility**     | Good.                                                                                                  |
| **Rust Compatibility**    | Good.                                                                                                  |
| **Static Binary Support** | Yes.                                                                                                   |
| **Key Constraints**       | 1) **UNMAINTAINED as of July 2025.** 2) BSL license for enterprise features. 3) No community momentum. |
| **Key URLs**              | https://github.com/earthly/earthly                                                                     |

#### 13. ko

| Attribute                 | Detail                                                                                                                                                    |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub**                | github.com/ko-build/ko                                                                                                                                    |
| **Primary Language**      | Go                                                                                                                                                        |
| **Build Tool**            | ko CLI                                                                                                                                                    |
| **Package Format**        | N/A (Go source -> static binary -> image)                                                                                                                 |
| **Base System**           | Go static (distroless-like, scratch + ca-certs + tzdata)                                                                                                  |
| **libc**                  | musl (via Go's static build)                                                                                                                              |
| **Reproducibility**       | Good. Same Go source + same Go version = identical binary. Go builds are reproducible with `GOFLAGS=-trimpath -ldflags=-buildid=`.                        |
| **SBOM Support**          | SPDX via Syft. Generated as OCI attestation.                                                                                                              |
| **Multi-arch**            | Yes (via `--platform` or `KO_DOCKER_PLATFORMS`)                                                                                                           |
| **Typical Image Size**    | 5-50 MB (single Go binary + ca-certs)                                                                                                                     |
| **License**               | Apache-2.0                                                                                                                                                |
| **Governance**            | CNCF (sandbox project). Go community maintained.                                                                                                          |
| **OCI Compliant**         | Yes.                                                                                                                                                      |
| **SLSA Level**            | L2. Signed provenance via Tekton Chains integration.                                                                                                      |
| **Sigstore/Cosign**       | Yes (via `ko login` and cosign integration).                                                                                                              |
| **in-toto**               | Partial (SLSA provenance).                                                                                                                                |
| **CVE Scanning**          | Go vulnerability database (`govulncheck`). Syft for SBOM-based scanning.                                                                                  |
| **C Compatibility**       | None. Go-only tool.                                                                                                                                       |
| **C++ Compatibility**     | None. Go-only tool.                                                                                                                                       |
| **Rust Compatibility**    | None. Go-only tool.                                                                                                                                       |
| **Static Binary Support** | Yes (Go is always static in ko images).                                                                                                                   |
| **Key Constraints**       | 1) **Go only.** No C, C++, Rust, Python, Java, or other languages. 2) Limited to Go applications. 3) No package manager in images. 4) No shell in images. |
| **Key URLs**              | https://github.com/ko-build/ko                                                                                                                            |

#### 14. Zarf

| Attribute                 | Detail                                                                                                                                              |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub**                | github.com/defenseunicorns/zarf                                                                                                                     |
| **Primary Language**      | Go                                                                                                                                                  |
| **Build Tool**            | Zarf CLI (packaging/deployment, not building)                                                                                                       |
| **Package Format**        | Zarf package (tarball of OCI images + manifests)                                                                                                    |
| **Base System**           | Any (packages existing images)                                                                                                                      |
| **libc**                  | any (depends on packaged images)                                                                                                                    |
| **Reproducibility**       | Moderate. Deterministic if source images are pinned by digest.                                                                                      |
| **SBOM Support**          | SPDX via Syft. Generated for all packaged images.                                                                                                   |
| **Multi-arch**            | Depends on source images.                                                                                                                           |
| **Typical Image Size**    | N/A (packaging tool, not builder)                                                                                                                   |
| **License**               | Apache-2.0                                                                                                                                          |
| **Governance**            | CNCF (Defense Unicorns). Defense/air-gap focused.                                                                                                   |
| **OCI Compliant**         | Yes (packages OCI images)                                                                                                                           |
| **SLSA Level**            | L1. Package-level provenance.                                                                                                                       |
| **Sigstore/Cosign**       | Yes (integrated image verification).                                                                                                                |
| **in-toto**               | Partial (package signing).                                                                                                                          |
| **CVE Scanning**          | Via Syft SBOM. Not built-in scanning.                                                                                                               |
| **C Compatibility**       | N/A (packaging tool).                                                                                                                               |
| **C++ Compatibility**     | N/A.                                                                                                                                                |
| **Rust Compatibility**    | N/A.                                                                                                                                                |
| **Static Binary Support** | N/A.                                                                                                                                                |
| **Key Constraints**       | 1) **Not an image builder.** Packages existing images for air-gapped deployment. 2) Defense-focused use case. 3) Does not solve image construction. |
| **Key URLs**              | https://github.com/defenseunicorns/zarf                                                                                                             |

### Cross-Ecosystem Comparison Matrices

#### Reproducibility

| Level                                    | Ecosystems                               |
| ---------------------------------------- | ---------------------------------------- |
| **Bitwise identical**                    | NixOS, Bazel rules_oci, Chainguard/Wolfi |
| **High (deterministic builds)**          | Google distroless, ko                    |
| **Moderate (good cache, some variance)** | CNB/Paketo, Earthly                      |
| **Partial (package-level only)**         | Alpine, Debian, Buildah                  |
| **Low (non-deterministic builds)**       | Red Hat UBI, CBL-Mariner, Fedora         |

#### Supply Chain Security

| Feature           | Chainguard | Distroless | Nix     | Debian     | Alpine     | Buildah | Bazel  | ko          |
| ----------------- | ---------- | ---------- | ------- | ---------- | ---------- | ------- | ------ | ----------- |
| Image signing     | Yes        | Yes        | Manual  | No         | No         | No      | Yes    | Yes         |
| Provenance (SLSA) | L3         | L2         | L2      | L0         | L0         | L0      | L2-L3  | L2          |
| SBOM (SPDX)       | Yes        | Yes        | Exp     | No         | No         | No      | Manual | Yes         |
| CVE scanning      | Built-in   | No         | Partial | Advisories | Advisories | No      | No     | govulncheck |
| in-toto           | Yes        | Partial    | Manual  | No         | No         | No      | Manual | Partial     |
| VEX support       | Yes        | No         | No      | No         | No         | No      | No     | No          |

#### Language Compatibility

| Language    | Chainguard | Distroless | Alpine    | UBI       | Debian    | Nix       | Fedora    | Bazel     | ko        |
| ----------- | ---------- | ---------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- |
| **C**       | Limited    | No         | Limited   | Excellent | Excellent | Excellent | Excellent | Excellent | No        |
| **C++**     | Limited    | No         | Limited   | Excellent | Excellent | Excellent | Excellent | Excellent | No        |
| **Rust**    | Excellent  | Excellent  | Excellent | Good      | Excellent | Excellent | Excellent | Good      | No        |
| **Go**      | Excellent  | Excellent  | Excellent | Good      | Good      | Good      | Good      | Good      | Excellent |
| **Java**    | Good       | Excellent  | Good      | Good      | Good      | Excellent | Good      | Excellent | No        |
| **Python**  | Good       | Excellent  | Good      | Good      | Good      | Excellent | Good      | Excellent | No        |
| **Node.js** | Good       | Excellent  | Good      | Good      | Good      | Excellent | Good      | Excellent | No        |

#### Image Size (Typical for nginx-equivalent)

| Ecosystem         | Minimal          | With Shell       | With glibc |
| ----------------- | ---------------- | ---------------- | ---------- |
| Chainguard/Wolfi  | ~2 MB            | ~8 MB            | N/A (musl) |
| Google distroless | ~2 MB            | N/A              | ~30 MB     |
| Alpine            | ~5 MB            | ~8 MB            | N/A (musl) |
| Red Hat UBI       | ~28 MB (micro)   | ~38 MB (minimal) | ~85 MB     |
| Debian minbase    | ~50 MB           | ~75 MB (slim)    | ~120 MB    |
| NixOS             | ~20 MB (minimal) | ~80 MB           | ~120 MB    |
| CBL-Mariner       | ~30 MB           | ~40 MB           | ~50 MB     |

---

## Part 2: Supply Chain Standards

### Standards Matrix

| Standard                  | Version      | Governing Body             | Applies To             | EIR Relevance                                                                                                        |
| ------------------------- | ------------ | -------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **OCI Image Spec**        | v1.1.1       | CNCF (OCI)                 | All container images   | **Mandatory.** Every EIR image must be OCI-compliant. Defines manifest, config, layers, annotations.                 |
| **OCI Distribution Spec** | v1.1.1       | CNCF (OCI)                 | Registries             | **Mandatory.** Defines push/pull/auth API. EIR must produce images compatible with GHCR.                             |
| **SLSA**                  | v1.2         | OpenSSF / Linux Foundation | All software artifacts | **High.** Target SLSA L2 for EIR. Signed provenance for every image. L3 (hardened build) is aspirational.            |
| **SPDX**                  | 2.3.0        | Linux Foundation           | SBOMs                  | **High.** Generate SPDX SBOM for every image. Attach as OCI attestation. Required by EO 14028.                       |
| **CycloneDX**             | 1.7          | OWASP / Ecma International | SBOMs                  | **Medium.** Alternative to SPDX. Consider for vulnerability/VEX integration. Lighter weight JSON format.             |
| **in-toto**               | 1.2.0        | CNCF                       | Attestations           | **High.** Core attestation format for SLSA provenance. Cosign uses in-toto DSSE envelopes.                           |
| **Sigstore (Cosign)**     | v3.0+        | OpenSSF / CNCF             | Signing & verification | **High.** Sign every EIR image. Keyless signing via Fulcio for CI. Transparency log via Rekor.                       |
| **NIST SP 800-190**       | Final (2017) | NIST                       | Container security     | **Medium.** Guidelines for image security: trusted base, minimal, signed, non-root. Reference for EIR policies.      |
| **CIS Docker Benchmark**  | 1.8.0        | CIS                        | Docker configuration   | **Medium.** Section 4 applies to image building. Reference for EIR Dockerfile standards.                             |
| **OpenVEX**               | v0.2.0       | OpenVEX / CISA             | Vulnerability status   | **High.** Generate VEX documents alongside images to communicate fixed/not-affected status. Reduces false positives. |
| **CAA (RFC 8659)**        | 2023         | IETF                       | Registry TLS           | **Low.** EIR uses GHCR (CAA already handled by GitHub). Relevant if self-hosting registry.                           |

### Standards Compliance Requirements for EIR

```
MUST (Phase 1):
  - OCI Image Spec v1.1.1 compliant images
  - SPDX 2.3 SBOM for every image
  - Cosign-signed images (keyless via GitHub Actions OIDC)
  - SLSA L1 provenance (build metadata)

SHOULD (Phase 2):
  - SLSA L2 provenance (signed, hosted)
  - in-toto attestations for build steps
  - CycloneDX VEX for vulnerability status
  - CIS Docker Benchmark Section 4 compliance

ASPIRATIONAL (Phase 3):
  - SLSA L3 provenance (hardened build platform)
  - Bitwise reproducible builds
  - NIST SP 800-190 full compliance
```

---

## Part 3: Language-Native Tooling (Rust/C++)

### Rust-Native Tools

| Tool                    | Stars | Purpose                               | Maturity            | OCI Compliance                        | Notes                                                            |
| ----------------------- | ----- | ------------------------------------- | ------------------- | ------------------------------------- | ---------------------------------------------------------------- |
| **youki**               | 7,400 | Container runtime (runc replacement)  | Production (v0.6.0) | Full OCI Runtime Spec                 | ~2x faster than runc. CNCF sandbox. Not a builder.               |
| **oci-spec-rs**         | 283   | OCI spec library (serde types)        | Mature (v0.9.0)     | Full (Image + Runtime + Distribution) | Used by youki. Generated from official JSON schemas.             |
| **oci-distribution-rs** | ~100  | OCI registry client (push/pull)       | Moderate            | OCI Distribution Spec                 | Closest Rust equivalent to crane. Pull/push manifests and blobs. |
| **cross**               | 8,200 | Rust cross-compilation via containers | Production (v0.2.5) | N/A (uses containers)                 | 50+ targets. Essential for multi-arch Rust images.               |
| **dockerfile-rs**       | ~50   | Dockerfile parser                     | Low                 | N/A                                   | Limited instruction coverage. Not production-ready.              |
| **wasm-to-oci**         | ~200  | WASM module push/pull to OCI          | Experimental        | Partial (WASM artifact type)          | Demonstrates Rust OCI distribution client capabilities.          |

**Key Gap:** No mature Rust-native OCI image builder exists. The Rust ecosystem has excellent runtime support (youki)
and spec libraries (oci-spec-rs) but lacks a daemonless builder comparable to buildah or kaniko.

### C++-Native Tools

| Tool       | Stars | Purpose                              | Maturity           | OCI Compliance                 | Notes                                               |
| ---------- | ----- | ------------------------------------ | ------------------ | ------------------------------ | --------------------------------------------------- |
| **build2** | 655   | C++ build system + package manager   | Production         | None                           | No OCI/container support. Pure C++ build tool.      |
| **Conan**  | 9,400 | C/C++ package manager                | Production (v2.28) | None (Docker integration only) | Docker-based isolated builds. Not an image builder. |
| **crun**   | ~6k   | Container runtime (C implementation) | Production         | Full OCI Runtime Spec          | Fastest OCI runtime. Written in C. Not a builder.   |

**Key Gap:** No C++ native container image builder exists. C++ projects rely on Dockerfile + buildah or Bazel rules_oci
for container workflows.

### Implications for EIR (Rust/C++ Preferred)

Given the language preference:

1. **No Rust-native builder exists.** EIR cannot use a Rust-native image builder today. Options:
   - Use Bazel (Starlark) with `rules_oci` for declarative builds (supports C++, Rust, Go)
   - Use melange/apko (Go) like Wolfi does (best supply chain security)
   - Use Buildah (Go) with Containerfiles (simplest migration from Dockerfiles)
   - **Build a Rust-native builder** (long-term, leverages oci-spec-rs)

2. **Rust runtime is mature (youki).** For container runtime on TrueNAS, youki could replace runc for better performance
   and memory usage.

3. **oci-spec-rs provides the foundation.** If building a Rust-native builder, oci-spec-rs gives you the manifest/config
   types. oci-distribution-rs gives you registry push/pull.

4. **C++ projects use Conan for package management.** Conan's Docker integration can create reproducible build
   environments for C++ applications.

---

## Part 4: Decision Framework

### Scoring Matrix (0-10 Scale)

| Criteria (Weight)           | Wolfi | Distroless | Alpine | Nix | Bazel rules_oci | Buildah | CNB |
| --------------------------- | ----- | ---------- | ------ | --- | --------------- | ------- | --- |
| Reproducibility (20%)       | 10    | 8          | 4      | 10  | 10              | 4       | 5   |
| Supply Chain Security (20%) | 10    | 8          | 2      | 5   | 7               | 2       | 3   |
| C++ Compatibility (15%)     | 3     | 0          | 3      | 10  | 10              | 10      | 1   |
| Rust Compatibility (15%)    | 10    | 10         | 10     | 10  | 8               | 8       | 1   |
| Image Size (10%)            | 10    | 9          | 8      | 3   | 7               | 5       | 4   |
| Multi-arch (5%)             | 9     | 7          | 9      | 6   | 9               | 9       | 7   |
| Open Source (5%)            | 3     | 10         | 10     | 10  | 10              | 10      | 10  |
| SBOM Support (5%)           | 10    | 7          | 1      | 3   | 4               | 1       | 6   |
| Maturity (5%)               | 8     | 10         | 10     | 8   | 7               | 10      | 8   |

**Weighted Scores:**

| Ecosystem             | Score    | Rank |
| --------------------- | -------- | ---- |
| **Bazel rules_oci**   | **7.75** | 1    |
| **NixOS/Nixpkgs**     | **7.55** | 2    |
| **Chainguard/Wolfi**  | **7.40** | 3    |
| **Alpine Linux**      | **5.80** | 4    |
| **Buildah**           | **5.60** | 5    |
| **Google distroless** | **6.20** | 6    |
| **CNB/Paketo**        | **4.05** | 7    |

### Key Tradeoffs

```
Maximum Security (Wolfi)          Maximum Reproducibility (Nix)
  musl libc (C++ pain)              Nix DSL (steep curve)
  Corporate (not fully open)        Large images
  Limited package set               Slow learning

Maximum Flexibility (Bazel)       Maximum Simplicity (Buildah)
  Starlark DSL (not Rust)           Containerfiles (familiar)
  Complex setup                     No hermeticity
  Excellent C++/Rust support        No SBOM/signing
```

---

## Part 5: Recommended Architecture for EIR

### Recommended Stack

Based on the analysis, the recommended architecture for EIR is a **hybrid approach** that leverages the strengths of
multiple systems:

#### Build Pipeline

```
Source Code (git)
    |
    v
melange (package builder from source)
    |  - Produces .apk packages with SPDX SBOM
    |  - Bitwise reproducible
    |  - Multi-arch (x86_64, arm64)
    |
    v
apko (image composer)
    |  - Declarative YAML -> OCI image
    |  - Composes packages into minimal image
    |  - Generates image-level SBOM
    |
    v
cosign (signing)
    |  - Keyless signing via GitHub Actions OIDC
    |  - SLSA L2 provenance generation
    |  - Transparency log via Rekor
    |
    v
GHCR (ghcr.io/wyattau/)
    - Immutable by digest
    - Multi-arch manifest list
    - OCI attestations (SBOM, provenance, VEX)
```

#### Rationale

1. **melange/apko** over alternatives because:
   - Best reproducibility (bitwise identical builds)
   - Built-in SPDX SBOM generation
   - Native SLSA provenance support
   - Smallest possible images (distroless-like)
   - apko YAML is declarative (better than Dockerfiles for 1000+ images)

2. **Alpine apk format** over RPM because:
   - Smaller packages (musl-based)
   - Simpler build system than RPM
   - Better Rust compatibility (musl = static Rust binaries)
   - Chainguard proved the approach works at scale

3. **Bazel rules_oci** as a secondary path for:
   - C++ projects that need glibc (musl-incompatible)
   - Projects already using Bazel
   - Maximum hermeticity requirements

4. **NOT choosing** Wolfi images directly because:
   - Corporate governance (not fully open source)
   - Production images require subscription
   - Need to own the build pipeline

### Phase Migration Plan

```
Phase 1 (Current - Complete):
  Fix Dockerfiles, add trivy scanning, add syft SBOM, pin digests

Phase 2 (Next):
  Set up melange/apko build pipeline for 5 critical images
  (traefik, keycloak, oauth2-proxy, victoriametrics, cloudflared)
  Integrate cosign signing in GitHub Actions CI
  Generate SLSA L1 provenance

Phase 3:
  Expand melange/apko to remaining SIS images
  Achieve SLSA L2 for all images
  Integrate VEX generation

Phase 4 (Aspirational):
  Build Rust-native image builder (using oci-spec-rs)
  Replace melange/apko for Rust-built images
  Contribute back to youki ecosystem
```

### Key Architectural Decisions

| Decision        | Choice                         | Rationale                                                     |
| --------------- | ------------------------------ | ------------------------------------------------------------- |
| Package format  | apk                            | Proven by Wolfi/Alpine, smaller than RPM, better Rust support |
| Image composer  | apko                           | Declarative, reproducible, SBOM-native                        |
| Signing         | cosign (keyless)               | No key management overhead, CI-native                         |
| SBOM format     | SPDX 2.3                       | Required by EO 14028, widely supported                        |
| Registry        | GHCR                           | Free, OCI-compliant, GitHub-native CI integration             |
| Multi-arch      | x86_64 + arm64                 | Covers TrueNAS (x86_64) and potential ARM nodes               |
| Base libc       | musl (default), glibc (opt-in) | musl for Rust/Go, glibc option for C++ via Bazel              |
| C++ build path  | Bazel rules_oci + glibc        | C++ needs glibc, Bazel provides hermeticity                   |
| Rust build path | melange/apko + musl            | Rust targets musl natively, produces static binaries          |
