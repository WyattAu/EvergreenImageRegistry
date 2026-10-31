# Yellow Paper: Container Hardening Benchmarks: Industry Analysis
This Yellow Paper benchmarks the container image hardening practices of four major projects; Chainguard Wolfi, Bitnami,
Google Distroless, and Red Hat UBI; to extract actionable patterns for the EvergreenImageRegistry.
**Recommendation for EvergreenImageRegistry:** Adopt the Chainguard/Wolfi model as the primary pattern; declarative
`:latest-glibc`. **[DEPRECATED: Alpine references; see deprecation notice above; use Wolfi/glibc variants.]**
Wolfi uses **apk** (Alpine Package Keeper) as its package manager **[DEPRECATED: Alpine-origin tooling; see deprecation
- **Build tool:** `melange`; builds `.apk` packages from declarative YAML pipelines
- **Image assembler:** `apko`; bundles APKs into OCI images via declarative YAML manifests
- **Nightly full rebuilds** from latest upstream source; this is the primary CVE mitigation mechanism
- **Production (distroless):** No shell, no package manager; smallest attack surface
- `tdnf` (Tiny DNF) package manager; fast, lightweight
- `/bitnami/{app}`; application installation directory
- `/bitnami/{app}/data`; persistent data (often a volume)
- `/bitnami/{app}/conf`; configuration files (often mounted)
Bitnami uses a **libentrypoint.sh** pattern; a shared entrypoint script library that handles:
- **VEX statements:** Commercial feature; vulnerability triage with VEX, KEV (Known Exploited Vulnerabilities), and
Bitnami provides **first-class Helm chart support**; this is a major differentiator:
- `:nonroot`; runs as `nobody` (UID 65534)
- `:debug`; includes busybox shell for debugging
- `:debug-nonroot`; debug + non-root
- **Bazel**; primary build system (not Dockerfiles)
- No nightly full rebuilds; updates are triggered by Debian security releases
- No shell-based signal handling; the application must handle signals directly
- `microdnf`; stripped-down dnf with fewer dependencies
- NOT default; runs as root by default
- NOT every CVE requires action; VEX provides context
   shell. This is the correct pattern; secure by default, debuggable when needed.
| [^1]  | Chainguard Images GitHub; github.com/chainguard-images               | Primary research source                    | 5   |
| [^2]  | Chainguard Academy; edu.chainguard.dev                               | Documentation and best practices           | 5   |
| [^3]  | Bitnami Containers GitHub; github.com/bitnami/containers             | Primary research source                    | 5   |
| [^4]  | Google Distroless GitHub; github.com/GoogleContainerTools/distroless | Primary research source                    | 5   |
| [^5]  | Red Hat UBI; catalog.redhat.com                                      | Enterprise reference                       | 4   |
| [^6]  | Wolfi OS; github.com/wolfi-dev                                       | Base distribution details                  | 5   |
| [^7]  | apko; github.com/chainguard-dev/apko                                 | Build tool reference                       | 5   |
| [^8]  | melange; github.com/chainguard-dev/melange                           | Package build reference                    | 5   |