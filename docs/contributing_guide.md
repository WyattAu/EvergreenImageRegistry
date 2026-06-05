# Evergreen Image Registry: Contributing Guide

Thank you for your interest in contributing! This project thrives on community participation, and we welcome your help
in adding new images and improving existing ones.

First, please read and agree to our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started: Your First-Time Setup

To ensure a smooth and consistent development experience for everyone, we use `pre-commit` to manage our code quality
checks.

### Prerequisites

- **Git** — Version control
- **Docker & Docker Compose** — Container builds
- **Python 3.10+ & Pip** — For pre-commit and testing
- **Rust 1.75+ & Cargo** — For evergreenctl and shim development
- **hadolint** — Dockerfile linting (via Docker)

### Install Rust (if not already installed)

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
rustup component clippy rustfmt
```

### Install Python Tools

```bash
pip install pre-commit ruff pytest
```

### Fork and Clone

1. Fork the repository on GitHub.
2. Clone your fork:

   ```bash
   git clone https://github.com/YOUR-USERNAME/EvergreenImageRegistry.git
   cd EvergreenImageRegistry
   ```

### Install Pre-commit Hooks

```bash
pre-commit install
pre-commit install --hook-type pre-push
```

That's it! Now, every time you run `git commit`, our suite of linters and formatters will run automatically on the files
you've changed. When you `git push`, the full 11-gate quality check runs (Rust unit tests, Rust integration tests,
clippy, fmt, Python syntax + ruff lint, Shell syntax, manifest TOML validation, SBOM JSON validation, Dockerfile
constraints, cargo audit, and Rust release build).

## Contribution Workflow

1. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/add-nginx-image
   ```

2. Make your changes. Adhere to the project's [Image Standards](docs/standards.md) at all times.
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

1. **[Image Standards](docs/standards.md)** — High-level design principles (security, minimalism, reliability).
2. **[Dockerfile Authoring Standards](docs/dockerfile-standards.md)** — Mandatory rules for every Dockerfile. Covers
   base image selection, multi-stage builds, wolfi constraints, checksum verification, shell compatibility, and more.
   Violating any rule here will cause CI to fail.
3. **[Common Problems](docs/common-problems.md)** — Catalog of 18 known problem patterns discovered across 1000+ images.
   Read this to avoid repeating mistakes that took significant effort to fix at scale.
4. **[CI/CD Pipeline Guide](docs/ci-pipeline-guide.md)** — How the build pipeline works, tier system, manual dispatch,
   and troubleshooting CI failures.

### Step-by-Step

1. **Open an Issue:** Start by creating a "New Image Proposal" issue to discuss the software and ensure it's a good fit
   for the registry.

2. **Create the Directory:** Create a new directory under `images/` with the name of the software (e.g.,
   `images/nginx/`).

3. **Add the Dockerfile:** This is the most important part. It MUST adhere to all rules in
   [Dockerfile Authoring Standards](docs/dockerfile-standards.md). In particular:
   - Use the approved base image hierarchy (scratch > wolfi > RHEL UBI). debian-slim and Alpine are banned.
   - Multi-stage build with debian:bookworm downloader and scratch/wolfi final stage.
   - Verify all downloaded artifacts with SHA256 checksums.
   - Use `wget` (not `curl`) in wolfi stages.
   - Add `RUN mkdir -p` and `RUN touch` placeholders before any multi-stage COPY.
   - Include the health-shim binary as PID 1 for scratch images.

4. **Add the `manifest.toml`:** Declare the image tier, version, and build configuration. See the pipeline guide for the
   per-image manifest schema.

5. **Add the `README.md`:** Create a comprehensive README for your image, following the structure of the existing image
   READMEs. Include a working `docker-compose.yml` and a `.env.template`.

6. **Add a `.dockerignore` file.**

7. **Submit a Pull Request** for review. The CI pipeline will automatically build and test your image.

### Image Templates

For complete Dockerfile templates, see [Image Cookbook](docs/image-cookbook.md).

## How to Modify an Existing Image

1. **Check the issue tracker** for any open issues related to the image.
2. **Read the current Dockerfile** and `manifest.toml` to understand the existing implementation.
3. **Check for drift** between the manifest and Dockerfile:

   ```bash
   cd evergreenctl && cargo build --release
   evergreenctl drift images/<image>/
   ```

4. **Make your changes** following the [Image Standards](docs/standards.md).
5. **Verify locally** before submitting:

   ```bash
   docker build -t evergreen-<image> images/<image>/
   docker run -d --name test-<image> evergreen-<image>
   docker ps  # Verify container is running
   docker logs test-<image>  # Check for errors
   ```

6. **Update the `manifest.toml`** if your changes affect the version, tier, or build configuration.
7. **Update the `README.md`** if your changes affect usage, environment variables, or volume mounts.
8. **Submit a Pull Request** with a clear description of the changes.

## Testing Requirements

### Pre-commit Checks (Automatic)

When you commit, these hooks run automatically:

| Hook                  | What it checks                   |
| --------------------- | -------------------------------- |
| hadolint              | Dockerfile linting               |
| evergreen-constraints | Security constraints (C001-C020) |
| no-alpine             | No Alpine base images            |
| trailing-whitespace   | Whitespace cleanup               |
| end-of-file-fixer     | File ending newline              |
| check-yaml            | YAML syntax                      |
| check-json            | JSON syntax                      |
| markdownlint-cli2     | Markdown formatting              |
| yamllint              | YAML linting                     |

### Pre-push Gate (Automatic)

When you push, these 11 gates run:

1. Rust unit tests
2. Rust integration tests
3. Rust clippy lint
4. Rust fmt check
5. Python syntax check
6. Python ruff lint
7. Shell syntax check
8. Manifest TOML validation
9. SBOM JSON validation
10. Dockerfile constraint validation
11. Cargo audit (security)
12. Rust release build

### Local Testing

Run the full test suite locally before pushing:

```bash
# Run pre-commit on all files
pre-commit run --all-files

# Run Python tests
pytest tests/

# Build and test an image
docker build -t evergreen-<image> images/<image>/
docker run -d --name test-<image> -p 8080:8080 evergreen-<image>
curl http://localhost:8080/healthz

# Verify with evergreenctl
cd evergreenctl && cargo build --release
evergreenctl verify images/<image>/
evergreenctl drift images/<image>/
evergreenctl audit images/
```

## Pull Request Process

1. **Fill out the PR template** completely, including:
   - Description of changes
   - Motivation and context
   - Testing performed
   - Checklist of standards compliance

2. **Ensure all CI checks pass** before requesting review.

3. **Respond to review feedback** promptly. Most PRs require 1-2 review cycles.

4. **Squash and merge** — We use squash merges to keep the git history clean.

### PR Title Convention

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
feat: Add new minimal image for Nginx
fix: Correct health-check endpoint for Redis
docs: Update contributing guide
refactor: Simplify multi-stage build pattern
chore: Update base image to latest wolfi
```

## Code Style Guidelines

### Dockerfiles

- Follow [Dockerfile Authoring Standards](docs/dockerfile-standards.md) exactly.
- Maximum 120 lines for simple binary-download images.
- Comments explain WHY, not WHAT.
- Use consistent indentation (4 spaces).
- One blank line between logical sections.

### Rust (evergreenctl, shim)

- Follow `rustfmt` defaults.
- Run `cargo clippy` before committing.
- Use `#[derive(Deserialize)]` for config structs.
- Handle errors with `anyhow::Result` or `thiserror`.

### Python (scripts, tests)

- Follow `ruff` lint rules.
- Use type hints for all function signatures.
- Maximum line length: 100 characters.
- Use `pathlib.Path` over `os.path`.

### Markdown

- Follow `markdownlint` rules.
- Use ATX-style headers (`#`).
- Maximum line length: 100 characters.
- No trailing whitespace.

## Troubleshooting Build Failures

If your image fails in CI, consult [Common Problems](docs/common-problems.md) first. The most frequent causes are:

- **BuildKit COPY eval failure** — Missing `mkdir -p` / `touch` placeholder before COPY (Problem 3)
- **wolfi curl not found** — Use `wget` instead (Problem 9)
- **GITHUB_TOKEN 404** — Remove auth headers for cross-repo downloads (Problem 1)
- **Checksum mismatch** — Verify SHA256 is exactly 64 hex chars (Problem 12)

For CI pipeline issues (timeouts, matrix failures, push errors), see the
[CI/CD Pipeline Guide](docs/ci-pipeline-guide.md).

## Questions?

If you have any questions, please feel free to open an issue and we'll be happy to help you get started.
