ARG TRAEFIK_VERSION=v3.5.2

# ==============================================================================
# Stage 1: Builder
# ==============================================================================
FROM traefik:${TRAEFIK_VERSION} as builder

# ==============================================================================
# Stage 2: Final Production Image
# ==============================================================================
FROM scratch

# Define a non-root user and group ID, per Standard 2.2.
ARG TRAEFIK_UID=10001
ARG TRAEFIK_GID=10001

# Copy ONLY the Traefik binary from the builder stage. The final image will
# contain just this single file and nothing else.
COPY --from=builder /traefik /traefik

# Create a non-root user. Because 'scratch' has no user tools, we rely on
# the Docker daemon to interpret these USER and GROUP directives.
USER ${TRAEFIK_UID}:${TRAEFIK_GID}

# Expose the standard Traefik ports for web, websecure, and the API/dashboard.
EXPOSE 80 443 8080

# Add a mandatory health check using the Traefik binary's built-in command.
# This requires no shell and no external tools, satisfying both Standards 2.1 and 3.1.
HEALTHCHECK --interval=15s --timeout=3s --start-period=30s --retries=3 \
  CMD ["/traefik", "healthcheck"]

# The entrypoint is the Traefik binary itself. It handles signals correctly (Standard 3.3).
ENTRYPOINT [ "/traefik" ]

# The CMD is left empty as all configuration MUST be provided via CLI arguments
# in the docker-compose.yml, forcing explicit and clear configuration.
CMD []