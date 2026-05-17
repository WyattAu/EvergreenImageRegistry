# Evergreen Image Registry: Contributing Guide

Thank you for your interest in contributing! This project thrives on community participation, and we welcome your help
in adding new images and improving existing ones.

First, please read and agree to our [Code of Conduct](../CODE_OF_CONDUCT.md).

## Getting Started: Your First-Time Setup

To ensure a smooth and consistent development experience for everyone, we use `pre-commit` to manage our code quality
checks.

Prerequisites:

- Git
- Docker & Docker Compose
- Python & Pip (for installing `pre-commit`)

Setup Steps:

1. Fork the repository on GitHub.
2. Clone your fork to your local machine:

   ```bash
   git clone https://github.com/YOUR-USERNAME/evergreen-image-registry.git
   cd evergreen-image-registry
   ```

3. Install `pre-commit`:

   ```bash
   pip install pre-commit
   ```

4. Install the Git hooks:

   ```bash
   pre-commit install
   pre-commit install --hook-type pre-push
   ```

That's it! Now, every time you run `git commit`, our suite of linters and formatters will run automatically on the files
you've changed. When you `git push`, the full 10-gate quality check runs (Rust unit tests, Rust integration tests,
clippy, fmt, Python syntax + ruff lint, Shell syntax, 998-manifest TOML validation, 998-SBOM JSON validation, Dockerfile
constraints, and Rust release build).

## Contribution Workflow

1. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/add-nginx-image
   ```

2. Make your changes. Adhere to the project's [Image Standards](./standards.md) at all times.
3. Commit your changes. The pre-commit hooks will run. If they fail, fix the reported issues and commit again.

   ```bash
   git add .
   git commit -m "feat: Add new minimal image for Nginx"
   ```

4. Push your branch to your fork:

   ```bash
   git push origin feature/add-nginx-image
   ```

5. Open a Pull Request against the `main` branch of the upstream repository. Please fill out the PR template with as
   much detail as possible.

## How to Add a New Image

Before writing any Dockerfile, read these documents in order:

1. **[Image Standards](./standards.md)** -- High-level design principles (security, minimalism, reliability).
2. **[Dockerfile Authoring Standards](./dockerfile-standards.md)** -- Mandatory rules for every Dockerfile. Covers base
   image selection, multi-stage builds, wolfi constraints, checksum verification, shell compatibility, and more.
   Violating any rule here will cause CI to fail.
3. **[Common Problems](./common-problems.md)** -- Catalog of 18 known problem patterns discovered across 1014 images.
   Read this to avoid repeating mistakes that took significant effort to fix at scale.
4. **[CI/CD Pipeline Guide](./ci-pipeline-guide.md)** -- How the build pipeline works, tier system, manual dispatch, and
   troubleshooting CI failures.

### Step-by-Step

1. Open an Issue: Start by creating a "New Image Proposal" issue to discuss the software and ensure it's a good fit for
   the registry.
2. Create the Directory: Create a new directory under `images/` with the name of the software (e.g., `images/nginx/`).
3. Add the `Dockerfile`: This is the most important part. It MUST adhere to all rules in
   [Dockerfile Authoring Standards](./dockerfile-standards.md). In particular:
   - Use the approved base image hierarchy (scratch > wolfi > RHEL UBI). debian-slim and Alpine are banned.
   - Multi-stage build with debian:bookworm downloader and scratch/wolfi final stage.
   - Verify all downloaded artifacts with SHA256 checksums.
   - Use `wget` (not `curl`) in wolfi stages.
   - Add `RUN mkdir -p` and `RUN touch` placeholders before any multi-stage COPY.
4. Add the `manifest.toml`: Declare the image tier, version, and build configuration. See the pipeline guide for the
   per-image manifest schema.
5. Add the `README.md`: Create a comprehensive README for your image, following the structure of the existing image
   READMEs. Include a working `docker-compose.yml` and a `.env.template`.
6. Add a `.dockerignore` file.
7. Submit a Pull Request for review. The CI pipeline will automatically build and test your image.

## Troubleshooting Build Failures

If your image fails in CI, consult [Common Problems](./common-problems.md) first. The most frequent causes are:

- **BuildKit COPY eval failure** -- Missing `mkdir -p` / `touch` placeholder before COPY (Problem 3)
- **wolfi curl not found** -- Use `wget` instead (Problem 9)
- **GITHUB_TOKEN 404** -- Remove auth headers for cross-repo downloads (Problem 1)
- **Checksum mismatch** -- Verify SHA256 is exactly 64 hex chars (Problem 12)

For CI pipeline issues (timeouts, matrix failures, push errors), see the [CI/CD Pipeline Guide](./ci-pipeline-guide.md).

## Questions?

If you have any questions, please feel free to open an issue and we'll be happy to help you get started.
