# Evergreen Image: Forgejo

A minimal, secure, production-ready Forgejo image built according to Evergreen Image Registry standards.

Based on Chainguard Wolfi Linux (glibc, CA certs, timezone data). Runs as non-root user (UID/GID 65532).

## Conformance

This image adheres to all standards outlined in the [Evergreen Image Registry Standards](../../docs/standards.md).

- Non-root execution (UID 65532)
- Healthcheck via HTTP GET to `/`
- Multi-stage build with digest-pinned base images
- No Alpine dependencies
- OCI labels for discoverability

## Quick Start

This stack requires a PostgreSQL database. The following example provides a complete setup.

### 1. Create the `.env` File

Copy `.env.template` to `.env` and set your values:

```bash
cp .env.template .env
# Edit .env with your domain and secure passwords
```

### 2. Create Directories and Set Permissions

```bash
mkdir -p forgejo/data forgejo/config
sudo chown -R 65532:65532 ./forgejo
```

### 3. Start the Stack

```bash
docker compose up -d
```

Forgejo will be available at `http://localhost:3000`.

## Data Persistence

Mount volumes for:

- `/data` -- repositories, attachments, user data
- `/etc/forgejo` -- `app.ini` configuration

Host directories must be owned by UID/GID 65532.

## Upstream Version

Forgejo v15.0.2. Image tags correspond to the upstream Forgejo version.

## Ports

| Port | Purpose        |
| ---- | -------------- |
| 3000 | HTTP web UI    |
| 22   | SSH git access |

## Environment Configuration

Key Forgejo settings are configured via environment variables prefixed with `FORGEJO__section__key`. See the `.env.template` for required variables.

For full configuration reference, see the [Forgejo documentation](https://forgejo.org/docs/latest/admin/config-cheat-sheet/).
