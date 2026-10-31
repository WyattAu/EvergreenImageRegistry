- **Git**; Version control
- **Docker & Docker Compose**; Container builds
- **Python 3.10+ & Pip**; For pre-commit and testing
- **Rust 1.75+ & Cargo**; For evergreenctl and shim development
- **hadolint**; Dockerfile linting (via Docker)
1. **[Image Standards](docs/standards.md)**; High-level design principles (security, minimalism, reliability).
2. **[Dockerfile Authoring Standards](docs/dockerfile-standards.md)**; Mandatory rules for every Dockerfile. Covers
3. **[Common Problems](docs/common-problems.md)**; Catalog of 18 known problem patterns discovered across 1000+ images.
4. **[CI/CD Pipeline Guide](docs/ci-pipeline-guide.md)**; How the build pipeline works, tier system, manual dispatch,
4. **Squash and merge**; We use squash merges to keep the git history clean.
- **BuildKit COPY eval failure**; Missing `mkdir -p` / `touch` placeholder before COPY (Problem 3)
- **wolfi curl not found**; Use `wget` instead (Problem 9)
- **GITHUB_TOKEN 404**; Remove auth headers for cross-repo downloads (Problem 1)
- **Checksum mismatch**; Verify SHA256 is exactly 64 hex chars (Problem 12)