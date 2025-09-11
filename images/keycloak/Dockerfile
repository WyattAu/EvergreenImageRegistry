# ARG to define the upstream Keycloak version, adhering to Standard 3.2 (Versioning)
ARG KEYCLOAK_VERSION=25.0.2

# ==============================================================================
# Stage 1: The Builder
# This stage downloads and optimizes the Keycloak server.
# ==============================================================================
FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION} as builder

# Set the database type required for a proper production build.
# This ensures database-specific drivers are included.
ENV KC_DB=postgres

# Run the Keycloak build command to create an optimized server runtime.
# This adheres to Standard 3.4 (Optimized for Startup).
RUN /opt/keycloak/bin/kc.sh build

# ==============================================================================
# Stage 2: The Healthcheck Tool Provider
# This stage exists solely to provide a static 'curl' binary for the final image.
# ==============================================================================
FROM alpine:3.20 as healthcheck_builder
# Install curl; --no-cache keeps this stage minimal.
RUN apk add --no-cache curl

# ==============================================================================
# Stage 3: The Final Production Image
# This is the final, minimal, secure image that will be published.
# ==============================================================================

# Use a distroless Java 17 base image
# This adheres to Standard 2.1 (Distroless-First Principle).
FROM gcr.io/distroless/java17-debian12

# The 'nonroot' user is provided by the distroless base image (uid:65532, gid:65532).
# Using this user is mandatory per Standard 2.2 (Non-Root Execution).
ARG USER_UID=65532
ARG GROUP_GID=65532

# Set the working directory for the application.
WORKDIR /opt/keycloak

# Copy the optimized Keycloak server from the 'builder' stage.
# The --chown flag sets ownership directly, avoiding an extra layer.
COPY --from=builder --chown=${USER_UID}:${GROUP_GID} /opt/keycloak .

# Copy ONLY the curl binary from the healthcheck builder stage.
# This is necessary for the HEALTHCHECK instruction below, per Standard 3.1.
COPY --from=healthcheck_builder /usr/bin/curl /usr/bin/curl

# Switch to the non-root user. From this point on, all commands run as 'nonroot'.
USER ${USER_UID}:${GROUP_GID}

# Expose the default Keycloak ports, per Standard 4.3 (Configuration & Usability).
EXPOSE 8080 8443

# Add a mandatory health check to verify Keycloak is ready to serve requests.
# This is required by Standard 3.1 (Mandatory Healthchecks).
HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/bin/curl", "-f", "http://localhost:8080/health/ready"]

# Set the entrypoint to the Keycloak start script. It properly handles signals.
# This satisfies Standard 3.3 (Graceful Shutdown).
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]

# Set the default command. Using '--optimized' leverages the build-time work.
CMD ["start", "--optimized"]