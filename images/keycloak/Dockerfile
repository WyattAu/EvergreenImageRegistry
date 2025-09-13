ARG KEYCLOAK_VERSION=26.3.4
ARG ALPINE_VERSION=3.20
ARG CURL_VERSION=8.12.1-r0
ARG DISTROLESS_DIGEST=nonroot

# ==============================================================================
# Stage 1: Builder
# ==============================================================================
FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION} AS builder

# Set the database type required for a proper production build.
# This ensures database-specific drivers are included.
ENV KC_DB=postgres

# Run the Keycloak build command to create an optimized server runtime.
# This adheres to Standard 3.4 (Optimized for Startup).
RUN /opt/keycloak/bin/kc.sh build

# ==============================================================================
# Stage 2: The Healthcheck Tool Provider
# ==============================================================================
FROM alpine:${ALPINE_VERSION} AS healthcheck_builder

ARG CURL_VERSION
RUN apk update && apk add --no-cache "curl=${CURL_VERSION}"


# ==============================================================================
# Stage 3: Final Production Image
# ==============================================================================

# Required shell script to startup, cant be distroless
FROM eclipse-temurin:21-jre-jammy

# Define and create a non-root user, per Standard 2.2.
ARG USER_UID=10001
ARG GROUP_GID=10001
RUN groupadd --system --gid ${GROUP_GID} keycloak && \
    useradd --system --uid ${USER_UID} --gid ${GROUP_GID} keycloak

COPY --chown=keycloak:keycloak --from=builder /opt/keycloak /opt/keycloak

# Copy the healthcheck utility to its correct system path.
COPY --from=healthcheck_builder /usr/bin/curl /usr/bin/curl

WORKDIR /opt/keycloak

# Switch to the non-root user.
USER keycloak

EXPOSE 8080 8443

HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/bin/curl", "-f", "http://localhost:8080/health/ready"]

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
CMD ["start", "--optimized"]
