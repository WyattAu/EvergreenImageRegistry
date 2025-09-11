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
   ```

That's it! Now, every time you run `git commit`, our suite of linters and formatters will run automatically on the files
you've changed.

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

1. Open an Issue: Start by creating a "New Image Proposal" issue to discuss the software and ensure it's a good fit for
   the registry.
2. Create the Directory: Create a new directory under `images/` with the name of the software (e.g., `images/nginx/`).
3. Add the `Dockerfile`: This is the most important part. It MUST adhere to all rules in the
   [Image Standards](./standards.md) document (multi-stage, non-root, healthcheck, etc.).
4. Add the `README.md`: Create a comprehensive README for your image, following the structure of the existing image
   READMEs. Include a working `docker-compose.yml` and a `.env.template`.
5. Add a `.dockerignore` file.
6. Update the CI Workflow: Add the name of your new image directory to the `matrix.image` list in
   `.github/workflows/build-and-push.yml`.
7. Submit a Pull Request for review.

## Questions?

If you have any questions, please feel free to open an issue and we'll be happy to help you get started.
