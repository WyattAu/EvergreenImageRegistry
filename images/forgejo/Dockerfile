# ==============================================================================
# Build-Time Arguments
# ==============================================================================
ARG FORGEJO_VERSION=12-rootless

ARG BUILD_DATE

# ==============================================================================
# Stage 1: Builder
# ==============================================================================
FROM code.forgejo.org/forgejo/forgejo:${FORGEJO_VERSION} AS builder

# ==============================================================================
# Stage 2: Healthcheck Tool Provider
# ==============================================================================
FROM busybox:1.36 AS healthcheck_builder

# ==============================================================================
# Stage 3: Final Production Image
# ==============================================================================
FROM scratch

# Define a non-root user and group ID, per Standard 2.2.
ARG FORGEJO_UID=10002
ARG FORGEJO_GID=10002

# Copy the Forgejo binary and the static wget binary.
# Use --chown to set ownership directly, which is required for 'scratch' images.
COPY --from=builder --chown=${FORGEJO_UID}:${FORGEJO_GID} /usr/local/bin/forgejo /usr/local/bin/forgejo
COPY --from=healthcheck_builder --chown=${FORGEJO_UID}:${FORGEJO_GID} /bin/wget /usr/local/bin/wget

# Switch to the non-root user.
USER ${FORGEJO_UID}:${FORGEJO_GID}

# Expose the standard ports for HTTP and SSH.
EXPOSE 3000 22

# Add a mandatory health check, per Standard 3.1.
# It uses the static wget utility to ping Forgejo's health endpoint.
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/wget", "-q", "--spider", "http://localhost:3000/api/v1/healthz"]

# The entrypoint is the Forgejo binary itself.
ENTRYPOINT [ "/usr/local/bin/forgejo" ]

# The default command is to start the web server.
CMD [ "web" ]