# Evergreen Image Registry: Official Image Standards

## 1. Introduction

This document defines the official standards that every image published under the Evergreen Image Registry project MUST
adhere to. These standards are not optional guidelines; they are the foundation of our commitment to providing the
community with secure, minimal, reliable, and production-ready container images.

The purpose of these standards is to build a high degree of trust. When a user pulls an image from this registry, they
can be confident that it was built with security, performance, and usability as its primary design goals.

For clarity and to remove ambiguity, this document uses keywords as defined in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) (e.g., MUST, SHOULD, MUST NOT).

## 2. Pillar I: Security & Minimalism

This pillar is the core philosophy of the project. The primary goal is to minimize the attack surface of every image.

### 2.1. Distroless-First Principle

Images MUST use a "distroless" base image where a suitable one exists. If a distroless base is not technically feasible
for the application, a minimal base like wolfi (Chainguard) MUST be used. Standard distribution images (e.g., `ubuntu`,
`debian:slim`) are not acceptable for the final stage.

- Why: This is the most effective way to reduce the attack surface. No shells, package managers, or unnecessary
  utilities means fewer potential vulnerabilities and exploits.

### 2.2. Non-Root Execution

All application processes inside the container MUST run as a non-root user. A dedicated, unprivileged user and group
MUST be created in the `Dockerfile`.

- Why: This adheres to the Principle of Least Privilege. If an attacker compromises the application, they will not have
  root privileges within the container, severely limiting their ability to escalate an attack.

### 2.3. Mandatory Multi-Stage Builds

Every `Dockerfile` MUST be a multi-stage build. The final runtime image MUST NOT contain any build tools, compilers,
development headers, source code, or package managers.

- Why: This practice ensures the final image contains only the application and its direct runtime dependencies,
  drastically reducing size and potential vulnerabilities.

### 2.4. No Hardcoded Secrets

Images MUST NOT contain any secrets, including passwords, API keys, certificates, or tokens, in any layer. All secrets
MUST be injectable at runtime via environment variables or Docker secrets.

- Why: Hardcoding secrets is a critical security vulnerability that exposes sensitive information to anyone with access
  to the image.

### 2.5. Vulnerability Scanning

All images MUST be successfully scanned for critical and high-severity CVEs as part of the CI/CD pipeline before being
published. The pipeline SHOULD fail if new vulnerabilities of this severity are detected in a pull request.

- Why: This provides a continuous, automated check to prevent known vulnerabilities from being shipped.

## 3. Pillar II: Reliability & Production-Readiness

Images must be stable, performant, and behave predictably in orchestrated environments.

### 3.1. Mandatory Health Probes

Every image MUST provide a health check mechanism. Images with HTTP endpoints MUST expose `/livez` and `/readyz` probes
on port 9101 (via the health-shim sidecar or natively). Images built `FROM scratch` or `distroless` that lack a shell
MUST use `HEALTHCHECK NONE` in the Dockerfile, with health verification delegated to the orchestrator (Kubernetes probes
or health-shim sidecar). This approach follows ADR-006.

### 3.2. Immutable Semantic Versioning

Image tags MUST strictly follow the upstream software's semantic version (e.g., `keycloak:25.0.2`, `postgres:16.1`).
Once a versioned tag is pushed, it MUST NOT be overwritten. The `:latest` tag SHOULD point to the most recent stable
version.

- Why: This guarantees predictability and allows users to pin to specific versions, ensuring their builds are
  reproducible and do not break unexpectedly.

### 3.3. Graceful Shutdown

The container's entrypoint MUST ensure the application process can receive and properly handle process signals
(`SIGTERM`, `SIGINT`) from the container runtime, allowing for a clean and graceful shutdown.

- Why: This is critical for preventing data corruption and ensuring fast, clean restarts in an orchestrated environment.

### 3.4. Optimized for Startup

For applications that benefit from a build-time optimization step, this step MUST be performed in the builder stage of
the `Dockerfile`.

- Why: This significantly reduces container startup time, which is crucial for auto-scaling and fast recovery.

## 4. Pillar III: Configuration & Usability

Images must be easy to configure and use in a variety of environments.

### 4.1. Configuration via Environment Variables

All essential runtime configurations MUST be injectable via environment variables. This includes, but is not limited to,
database connections, port bindings, and admin credentials.

- Why: This is the de facto standard for containerized applications, as described in the Twelve-Factor App methodology,
  and provides maximum portability.

### 4.2. Secure by Default

Images MUST ship with secure default settings. For example, a database image MUST NOT allow password-less access by
default.

- Why: Users should be secure by default, not by exception. This prevents common misconfigurations that can lead to
  security breaches.

### 4.3. Stateless by Design

Containers MUST be stateless. Any data that requires persistence (e.g., database files, user uploads, logs) MUST be
stored in a volume mounted from the host. The image's documentation MUST clearly specify which paths require volumes.

- Why: This separates the application lifecycle from its data, allowing containers to be stopped, destroyed, and
  replaced without data loss.

## 5. Pillar IV: Documentation & Transparency

Every image is a product and must be documented as such.

### 5.1. Per-Image README.md

Each image directory MUST contain a `README.md` file that includes:

1. A one-line description of the software.
2. A minimal, working `docker-compose.yml` example.
3. A comprehensive table of all supported environment variables, noting which are required.
4. A clear description of all paths that should be mounted as volumes for data persistence.
5. The version of the upstream software being packaged.

### 5.2. Adherence to Licensing

The repository MUST contain a `LICENSE` file for the `Dockerfile`s and associated scripts. The license of the packaged
upstream software MUST be respected and acknowledged in the image's documentation.

## 6. Pillar V: Structural Integrity

Images must be complete, self-consistent, and compatible with their runtime environment.

### 6.1. Minimum Image Completeness (C026)

Every image published to the registry MUST contain a functional application binary or runtime that provides the advertised service. Specifically:

1. The `ENTRYPOINT` or `CMD` MUST invoke the actual application (not `sleep`, `true`, `echo`, or a placeholder script).
2. The image MUST be built from a verified upstream binary, a compiled source, or a package manager install -- not left as an empty stub.
3. Images that cannot meet this bar MUST be placed under `images/_wip/<name>/` (underscore prefix, excluded from CI) with `LABEL evergreen.status="wip"`.

Placeholder stubs, skeleton Dockerfiles, and `ENTRYPOINT ["true"]` images MUST NOT appear in the active build matrix or be published to any registry.

### 6.2. libc Consistency (C027)

All compiled artifacts copied between build stages MUST use the same libc family as the final stage.

- If any artifact was compiled against glibc (e.g., Python C extensions built in a debian builder, Node.js native modules, Rust compiled with `gnu` target), the final stage MUST use a glibc base image (RHEL UBI minimal or UBI standard).
- If all artifacts are static binaries or compiled against musl, wolfi or scratch is preferred.
- Wolfi MUST NOT be used as a final stage when it would receive glibc-compiled artifacts.

**Decision tree for Python images:**
```
Does the image pip install packages with C extensions (psycopg2, Pillow, cryptography, lxml, etc.)?
  YES -> Build the venv inside a wolfi builder stage (pip compiles against musl).
        If musl compilation fails, fall back to UBI minimal as final stage.
  NO  -> Current pattern is safe (debian builder, wolfi final).
```

### 6.3. Configurable Runtime UID (C028)

Every image MUST support runtime UID/GID override via `APP_UID` and `APP_GID` environment variables. The default MUST be 65532:65532.

The Dockerfile MUST declare:
```dockerfile
ARG APP_UID=65532
ARG APP_GID=65532
```

The user/group MUST be created at build time with the default UID. The image entrypoint MUST detect at runtime if `APP_UID` or `APP_GID` differ from the build-time defaults and, if so, re-create the user/group and perform `chown` on application data directories before dropping privileges with `su-exec`.

This ensures compatibility with orchestrators that require specific UIDs for volume mount permissions, while maintaining 65532 as the secure default.

For images built `FROM scratch` that cannot include `su-exec`, the entrypoint MUST log a clear warning if the configured UID does not match the build-time UID, and the orchestrator MUST handle UID mapping externally.

### 6.4. Initialization for Data Services (C029)

Images for data services (databases, message queues, key-value stores, caches) MUST provide two operational modes:

1. **Self-contained mode:** The image includes the upstream initialization entrypoint script that handles first-run detection, data store initialization (initdb, mysql_install_db, etc.), user/database creation from environment variables, and configuration rendering. This mode works with plain `docker run`.

2. **Binary-only mode:** The image exposes the raw application binary without initialization logic, for use with orchestrators that provide their own init containers. This is achieved by overriding `CMD` or `ENTRYPOINT` at runtime.

The default behavior MUST be self-contained mode (upstream entrypoint). Critical tier data service images MUST implement both modes. Standard and community tier data service images SHOULD implement self-contained mode but MAY omit it if documented.

## 7. Amending These Standards

These standards are a living document. Changes and amendments can be proposed via a pull request against this file. Any
proposed change must be justified and will be subject to review by project maintainers to ensure it aligns with the core
philosophy of the Evergreen Image Registry.
