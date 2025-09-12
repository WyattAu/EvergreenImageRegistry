# Evergreen Image: Traefik

A minimal, secure, and production-ready Traefik image, built according to the standards of the Evergreen Image Registry.
This is a distroless image based on `scratch`, containing only the Traefik binary and nothing else.

## Conformance

This image adheres to all standards outlined in the
[Evergreen Image Registry Standards document](../../docs/standards.md).

- Truly Distroless (`scratch`): The most minimal base image possible, containing a single file.
- 100% Reproducible: The builder image is pinned to a specific SHA256 digest.
- Non-Root: Runs as a dedicated `traefik` user with file ownership set at build time.
- Self-Contained Healthcheck: Uses the Traefik binary's built-in healthcheck command.
- OCI Labeled: Includes standard OCI labels for better discoverability and introspection.

## Quick Start (Configuration via Environment Variables)

This stack is configured using a combination of a `docker-compose.yml` file and a `.env` file for your secrets. This is
the best practice for security, portability, and clarity.

### 1. Create Your Configuration Files

First, create a directory for Traefik's persistent data and copy the configuration template to a new `.env` file.

```bash
# Create the main directory for persistent data
mkdir traefik

# Create the file for ACME (Let's Encrypt) certificates and set secure permissions
touch traefik/acme.json
chmod 600 traefik/acme.json

# Create your .env file from the template
cp .env.template .env
```

### 2. Edit the `.env` File

Open the `.env` file in a text editor. You MUST change the following values:

- `WHOAMI_DOMAIN`: Set this to your public domain name (e.g., `traefik.my-site.com`). For local testing, you can leave
  it as `whoami.localhost` and edit your `/etc/hosts` file.
- `TRAEFIK_ACME_EMAIL`: Set this to your real email address for Let's Encrypt notifications.

#### `.env.template`

```env
# ====================================================================
# Evergreen Image Registry: Traefik Configuration Template
# ====================================================================

# REQUIRED: Domain for the sample 'whoami' service.
WHOAMI_DOMAIN=whoami.localhost

# REQUIRED: Email address for Let's Encrypt renewal notices.
TRAEFIK_ACME_EMAIL=your-email@example.com
```

### 3. Create the `docker-compose.yml`

Create a file named `docker-compose.yml` with the following content. This file defines the Traefik service and a sample
"whoami" application to route to.

```yaml
version: '3.9'

services:
  traefik:
    image: ghcr.io/wyattau/evergreenimageregistry/traefik:v3.5.2
    container_name: traefik
    restart: unless-stopped
    # All Traefik configuration is explicitly defined here using environment
    # variables for maximum portability and clarity.
    environment:
      #  API and Dashboard
      - 'TRAEFIK_API_DASHBOARD=true'
      #  Entrypoints
      - 'TRAEFIK_ENTRYPOINTS_WEB_ADDRESS=:80'
      - 'TRAEFIK_ENTRYPOINTS_WEBSECURE_ADDRESS=:443'
      #  Docker Provider
      - 'TRAEFIK_PROVIDERS_DOCKER=true'
      - 'TRAEFIK_PROVIDERS_DOCKER_EXPOSEDBYDEFAULT=false'
      - 'TRAEFIK_PROVIDERS_DOCKER_NETWORK=proxy-net'
      #  Certificate Resolver
      - 'TRAEFIK_CERTIFICATESRESOLVERS_MYRESOLVER_ACME_STORAGE=/etc/traefik/acme.json'
      - 'TRAEFIK_CERTIFICATESRESOLVERS_MYRESOLVER_ACME_HTTPCHALLENGE=true'
      - 'TRAEFIK_CERTIFICATESRESOLVERS_MYRESOLVER_ACME_HTTPCHALLENGE_ENTRYPOINT=web'
      # The email address is securely sourced from the .env file.
      - 'TRAEFIK_CERTIFICATESRESOLVERS_MYRESOLVER_ACME_EMAIL=${TRAEFIK_ACME_EMAIL}'
    ports:
      - '80:80'
      - '443:443'
      - '8080:8080'
    volumes:
      - ./traefik/acme.json:/etc/traefik/acme.json
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - proxy-net

  whoami:
    image: traefik/whoami:v1.10
    container_name: whoami
    restart: unless-stopped
    networks:
      - proxy-net
    # Docker Compose substitutes ${WHOAMI_DOMAIN} from the .env file into the labels.
    labels:
      - 'traefik.enable=true'
      - 'traefik.http.routers.whoami-http.rule=Host(`${WHOAMI_DOMAIN}`)'
      - 'traefik.http.routers.whoami-http.entrypoints=web'
      - 'traefik.http.routers.whoami-http.middlewares=redirect-to-https'
      - 'traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https'
      - 'traefik.http.routers.whoami-secure.rule=Host(`${WHOAMI_DOMAIN}`)'
      - 'traefik.http.routers.whoami-secure.entrypoints=websecure'
      - 'traefik.http.routers.whoami-secure.tls=true'
      - 'traefik.http.routers.whoami-secure.tls.certresolver=myresolver'
      - 'traefik.http.services.whoami-service.loadbalancer.server.port=80'

networks:
  proxy-net:
    driver: bridge
```

### 4. Run the Stack

With your `.env` file configured, simply run Docker Compose:

```bash
docker-compose up -d
```

You can now access the Traefik dashboard at `http://localhost:8080` and your `whoami` service at the domain you
configured (e.g., `http://whoami.localhost`).

## Configuration Strategy

This stack uses a clear and portable configuration strategy:

- `.env` file: Stores user-specific variables and secrets (domains, email addresses).
- `docker-compose.yml`: The `environment:` section defines the static, operational configuration of the Traefik service.
  It securely references variables from the `.env` file using the `${...}` syntax.

This approach keeps secrets out of your compose file and makes the stack's configuration easy to read and manage.

## Data Persistence

This image is stateless, adhering to Standard 4.3. To persist state, you MUST mount volumes for:

- ACME Certificates: A writable file (e.g., `acme.json`) mounted to `/etc/traefik/acme.json` to store your Let's Encrypt
  certificates.
- Docker Socket: The Docker socket at `/var/run/docker.sock` must be mounted to allow Traefik to discover other
  containers. For security, it is mounted read-only.

## Upstream Software Version

This image packages Traefik v3.5.2. Image tags will always correspond to the upstream Traefik version.
