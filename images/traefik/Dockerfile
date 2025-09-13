ARG TRAEFIK_VERSION=v3.5.2

# ==============================================================================
# Stage 1: Builder
# ==============================================================================
FROM traefik:${TRAEFIK_VERSION} AS builder

# ==============================================================================
# Stage 2: Final Production Image
# ==============================================================================
FROM scratch

# Define a non-root user and group ID, per Standard 2.2.
ARG TRAEFIK_UID=10001
ARG TRAEFIK_GID=10001

# Copy ONLY the Traefik binary from the builder stage. The final image will
# contain just this single file and nothing else.
COPY --from=builder /usr/local/bin/traefik /traefik

# Create a non-root user.
USER ${TRAEFIK_UID}:${TRAEFIK_GID}

# Expose the standard Traefik ports.
EXPOSE 80 443 8080

# Add a mandatory health check using the Traefik binary's built-in command.
HEALTHCHECK --interval=15s --timeout=3s --start-period=30s --retries=3 \
  CMD ["/traefik", "healthcheck"]

# The entrypoint is the Traefik binary itself.
ENTRYPOINT [ "/traefik" ]

# The CMD is left empty as configuration should be provided via the docker-compose.yml.
CMD []
