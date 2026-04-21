# =============================================================================
# SOVEREIGN HARDENED YACY
# Peer-to-peer search engine (Java)
# Constraint: debian-slim - requires JRE
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/yacy/yacy_search_server/releases/download/v1.924/yacy_v1.924_202008051920.tar.gz" -o /yacy.tar.gz && \
    tar -xzf /yacy.tar.gz -C /opt && rm /yacy.tar.gz && \
    mv /opt/yacy /opt/yacy-server
RUN mkdir -p /app /var/log/yacy /var/lib/yacy/data
RUN chown -R 65534:65534 /opt/yacy-server /var/log/yacy /var/lib/yacy

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/yacy /var/lib/yacy
COPY --from=installer /opt/yacy-server /opt/yacy-server
COPY --from=installer /var/log/yacy /var/log/yacy
COPY --from=installer /var/lib/yacy /var/lib/yacy
RUN chown -R 65534:65534 /app /opt/yacy-server /var/log/yacy /var/lib/yacy
USER 65534:65534
WORKDIR /app
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
EXPOSE 8090 8443
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-fsSL", "http://localhost:8090/Status.html"]
ENTRYPOINT ["java", "-jar", "/opt/yacy-server/yacy.jar"]
LABEL org.opencontainers.image.title="yacy" \
      org.opencontainers.image.version="1.924" \
      org.opencontainers.image.vendor="yacy" \
      org.opencontainers.image.source="https://github.com/yacy/yacy_search_server" \
      org.opencontainers.image.description="Peer-to-peer search engine" \
      sovereign.image.tier="1" \
      sovereign.image.category="search" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
