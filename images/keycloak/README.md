# Evergreen Image: Keycloak

A minimal, secure, and production-ready Keycloak image, built according to the standards of the Evergreen Image Registry.

## Conformance

This image adheres to all standards outlined in the [Evergreen Image Registry Standards document](../../docs/standards.md).

- Distroless: Based on `gcr.io/distroless/java17-debian12`.
- Non-Root: Runs as the `nonroot` user.
- Multi-Stage Build: Final image contains no build tools.
- Healthchecked: Includes a robust healthcheck.
- Optimized: Uses a pre-built Keycloak configuration for fast startup.

---

## Quick Start

This image is designed to be used with an external PostgreSQL database. The following `docker-compose.yml` example provides a complete, working stack.

1. Create a `.env` file to store your secrets (do not commit this file):

   ```env
   # .env
   KEYCLOAK_ADMIN_PASSWORD=V3ryS3cureP@ssw0rd!
   POSTGRES_PASSWORD=An0therS3cureP@ssw0rd
   ```

2. Create a `docker-compose.yml` file:

   ```yaml
    version: '3.8'
    
    services:
      keycloak:
        image: ghcr.io/your-org/evergreen-image-registry/keycloak:latest
        container_name: keycloak
        command: start --optimized --hostname-strict=false
        restart: unless-stopped
        environment:
          # --- Required Admin Credentials ---
          - KEYCLOAK_ADMIN=${KEYCLOAK_ADMIN}
          - KEYCLOAK_ADMIN_PASSWORD=${KEYCLOAK_ADMIN_PASSWORD}
    
          # --- Required Database Connection ---
          - KC_DB=postgres
          - KC_DB_URL_HOST=postgres
          - KC_DB_URL_DATABASE=${POSTGRES_DB}
          - KC_DB_USERNAME=${POSTGRES_USER}
          - KC_DB_PASSWORD=${POSTGRES_PASSWORD}
    
          # --- Recommended Production Settings ---
          - KC_HOSTNAME=${KC_HOSTNAME}
          - KC_PROXY=${KC_PROXY}
    
          # --- Development Only ---
          - KC_HTTP_ENABLED=${KC_HTTP_ENABLED}
        ports:
          - "8080:8080"
        depends_on:
          postgres:
            condition: service_healthy
        healthcheck:
          test: ["CMD", "/usr/bin/curl", "-f", "http://localhost:8080/health/ready"]
          interval: 30s
          timeout: 10s
          retries: 5
          start_period: 60s
    
      postgres:
        image: postgres:16-alpine
        container_name: postgres
        restart: unless-stopped
        # The same portable method is used for the database service.
        environment:
          - POSTGRES_DB=${POSTGRES_DB}
          - POSTGRES_USER=${POSTGRES_USER}
          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
        volumes:
          - postgres_data:/var/lib/postgresql/data
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
          interval: 10s
          timeout: 5s
          retries: 5
    
    volumes:
      postgres_data:
        driver: local
   ```

3. Run the stack:

   ```bash
   docker-compose up -d
   ```

   You can now access Keycloak at `http://localhost:8080`.

---

## Environment Variables

Configuration is managed entirely via environment variables, per Standard 4.1.

### Required Variables

| Variable                  | Description                                         |
| ------------------------- | --------------------------------------------------- |
| `KEYCLOAK_ADMIN`          | The username for the initial administrator account. |
| `KEYCLOAK_ADMIN_PASSWORD` | The password for the initial administrator account. |
| `KC_DB_URL_HOST`          | The hostname of the PostgreSQL database server.     |
| `KC_DB_USERNAME`          | The username for the database connection.           |
| `KC_DB_PASSWORD`          | The password for the database connection.           |

### Commonly Used Optional Variables

| Variable             | Description                                                                             | Default       |
| -------------------- | --------------------------------------------------------------------------------------- | ------------- |
| `KC_DB_URL_DATABASE` | The name of the database to use.                                                        | `keycloak`    |
| `KC_HOSTNAME`        | The public-facing hostname for Keycloak (e.g., `auth.example.com`). Highly recommended. | `localhost`   |
| `KC_PROXY`           | Set to `edge` when running behind a reverse proxy. Highly recommended for production.   | `passthrough` |
| `KC_HTTP_ENABLED`    | Set to `true` to allow access over HTTP. For development only.                          | `false`       |

---

## Data Persistence

This image is stateless, adhering to Standard 4.3. All persistent data, including users, realms, and configuration, is stored in the external database.

You MUST ensure the database itself is configured with a persistent volume, as shown in the Quick Start example (`postgres_data`). No volumes need to be mounted directly to the Keycloak container.

---

## Upstream Software Version

This image packages Keycloak v25.0.2. Image tags will always correspond to the upstream Keycloak version, per Standard 3.2.
