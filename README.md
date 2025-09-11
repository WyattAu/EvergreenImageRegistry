# EvergreenImageRegistry

The Evergreen Image Registry was born in response from open source images lacking maintenance after switching to open core or proprietary. The project aims for a reliable, transparent, and community-driven source for essential open-source software images. In an ecosystem where free offerings can change with corporate acquisitions, this project provides a long-term home for images built to be secure, minimal, and maintained forever.

This is a public good, built on a foundation of clearly defined [Image Standards](./docs/standards.md) that guarantee quality and consistency across the entire registry.

## Available Images

This list is automatically updated.

| Image      | Upstream Version | Documentation                              |
| :--------- | :--------------- | :----------------------------------------- |
| `keycloak` | `25.0.2`         | [View README](./images/keycloak/README.md) |
| `postgres` | `16.2`           | [View README](./images/postgres/README.md) |
| `redis`    | `7.2`            | [View README](./images/redis/README.md)    |

## Quick Start Example

All images are designed to work together seamlessly. This example demonstrates how to run `keycloak` with a `postgres` database.

1. Create your configuration file. Copy the template from the Keycloak image directory to a new `.env` file:

   ```bash
   cp ./images/keycloak/.env.template .env
   ```

2. Edit your secrets in the `.env` file with a text editor.

3. Create a `docker-compose.yml` file:

   ```yaml
   version: "3.8"

   services:
     keycloak:
       image: ghcr.io/your-org/evergreen-image-registry/keycloak:latest
       restart: unless-stopped
       environment:
         - KEYCLOAK_ADMIN=${KEYCLOAK_ADMIN}
         - KEYCLOAK_ADMIN_PASSWORD=${KEYCLOAK_ADMIN_PASSWORD}
         - KC_DB=postgres
         - KC_DB_URL_HOST=postgres
         - KC_DB_URL_DATABASE=${POSTGRES_DB}
         - KC_DB_USERNAME=${POSTGRES_USER}
         - KC_DB_PASSWORD=${POSTGRES_PASSWORD}
         - KC_HOSTNAME=${KC_HOSTNAME}
         - KC_PROXY=${KC_PROXY}
         - KC_HTTP_ENABLED=${KC_HTTP_ENABLED}
       ports:
         - "8080:8080"
       depends_on:
         postgres: { condition: service_healthy }

     postgres:
       image: ghcr.io/your-org/evergreen-image-registry/postgres:latest
       restart: unless-stopped
       environment:
         - POSTGRES_DB=${POSTGRES_DB}
         - POSTGRES_USER=${POSTGRES_USER}
         - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
       volumes:
         - postgres_data:/var/lib/postgresql/data

   volumes:
     postgres_data:
   ```

## Our Core Principles

Every image in this registry adheres to a strict set of standards:

- Secure & Minimal: All images are distroless and run as a non-root user. Multi-stage builds ensure no build tools are left in the final image, drastically reducing the attack surface.
- Production-Ready: Mandatory healthchecks, graceful shutdown handling, and optimized startup routines mean these images are built for real-world, orchestrated environments.
- Fully Documented: Every image includes a comprehensive `README.md` with a working `docker-compose.yml` example and a full list of environment variables.
- Evergreen: An automated workflow using Dependabot ensures that our base images are always kept up-to-date with the latest security patches.

## Contributing

This is a community-driven project, and we welcome contributions! If you would like to add a new image or improve an existing one, please start by reading our [Contributing Guide](./docs/contributing_guide.md) and our [Code of Conduct](./CODE_OF_CONDUCT.md).

## License

The scripts and `Dockerfile`s in this repository are licensed under the [Apache-2.0](./LICENSE).
The upstream software packaged in the images retains its original license.
