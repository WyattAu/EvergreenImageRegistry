# Evergreen Image: Forgejo

A minimal, secure, and production-ready Forgejo image, built according to the standards of the Evergreen Image Registry.
This is a truly distroless image based on `scratch`, containing only the Forgejo binary and a static healthcheck
utility.

## Conformance

This image adheres to all standards outlined in the
[Evergreen Image Registry Standards document](../../docs/standards.md).

- Truly Distroless (`scratch`): The most minimal base image possible.
- 100% Reproducible: All builder images are pinned to a specific SHA256 digest.
- Non-Root: Runs as a dedicated `forgejo` user (UID/GID 10002).
- Healthchecked: Includes a robust healthcheck against Forgejo's `/healthz` endpoint.
- OCI Labeled: Includes standard OCI labels for better discoverability and introspection.

---

## Quick Start (Configuration via Environment Variables)

This stack requires a PostgreSQL database. The following example provides a complete, working setup.

### 1. Create Directories and Set Permissions

Forgejo runs as a non-root user and needs to write to its data and config volumes. You MUST create these directories on
your host and set the correct ownership before starting.

```bash
# Create the main directories
mkdir -p forgejo/data forgejo/config

# Set ownership to match the UID/GID defined in the Dockerfile (10002)
sudo chown -R 10002:10002 ./forgejo
```

### 2. Create the `.env` File

Copy the template below to a new file named `.env` and replace the placeholder values with your own secure secrets and
domain name.

#### `.env.template`

```env
# ====================================================================
# Evergreen Image Registry: Forgejo Configuration Template
# ====================================================================

# REQUIRED: Domain and User Settings
# --------------------------------------------------------------------
# The public domain for your Forgejo instance.
FORGEJO_DOMAIN=git.your-domain.com
# The name of the initial admin user to create.
FORGEJO_ADMIN_USER=admin

# REQUIRED: PostgreSQL Database Credentials
# --------------------------------------------------------------------
# Ensure these values are consistent for both services.
POSTGRES_DB=forgejo
POSTGRES_USER=forgejo
POSTGRES_PASSWORD=A_VeryS3curePassword!
```

### 3. Create the `docker-compose.yml`

This file defines the Forgejo service and its PostgreSQL database.

```yaml
version: '3.9'

services:
  forgejo:
    image: ghcr.io/wyattau/evergreenimageregistry/forgejo:latest
    container_name: forgejo
    restart: unless-stopped
    environment:
      - FORGEJO__server__DOMAIN=${FORGEJO_DOMAIN}
      - FORGEJO__server__ROOT_URL=https://${FORGEJO_DOMAIN}
      - FORGEJO__server__SSH_DOMAIN=${FORGEJO_DOMAIN}
      - FORGEJO__database__DB_TYPE=postgres
      - FORGEJO__database__HOST=postgres:5432
      - FORGEJO__database__NAME=${POSTGRES_DB}
      - FORGEJO__database__USER=${POSTGRES_USER}
      - FORGEJO__database__PASSWD=${POSTGRES_PASSWORD}
      - FORGEJO__service__DISABLE_REGISTRATION=false
      - FORGEJO__service__REQUIRE_SIGNIN_VIEW=true
      - FORGEJO__admin__CREATE_ADMIN_USER=${FORGEJO_ADMIN_USER}
    volumes:
      - ./forgejo/data:/data
      - ./forgejo/config:/etc/forgejo
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - '3000:3000'
      - '2222:22' # Map host port 2222 to container SSH port 22
    networks:
      - forgejo-net
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:16-alpine
    container_name: forgejo-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - forgejo-net
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}']
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    driver: local

networks:
  forgejo-net:
    driver: bridge
```

### 4. Run the Stack

```bash
docker-compose up -d
```

Your Forgejo instance will be available at `http://localhost:3000` (or `https://git.your-domain.com` if you have a
reverse proxy).

---

## Data Persistence

This image is stateless. To persist data, you MUST mount volumes for:

- `/data`: Stores repositories, attachments, and other user data.
- `/etc/forgejo`: Stores the `app.ini` configuration file.

Crucially, the host directories for these volumes must be owned by the same UID/GID that the container runs as (10002),
otherwise Forgejo will fail to start due to permission errors.

---

## Upstream Software Version

This image packages Forgejo v1.21.11-0. Image tags will always correspond to the upstream Forgejo version.
