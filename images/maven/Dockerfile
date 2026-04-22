ARG VERSION=3.9.9
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dlcdn.apache.org/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.tar.gz" -o /maven.tar.gz && \
    tar -xzf /maven.tar.gz -C /opt/ && rm /maven.tar.gz && ln -sf /opt/apache-maven-3.9.9/bin/mvn /usr/local/bin/mvn

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/maven /var/cache/maven /home/maven

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/apache-maven-3.9.9 /opt/apache-maven-3.9.9
COPY --from=downloader /usr/local/bin/mvn /usr/local/bin/mvn
COPY --from=builder /app /app
COPY --from=builder /var/log/maven /var/log/maven
COPY --from=builder /var/cache/maven /var/cache/maven
COPY --from=builder /home/maven /home/maven
RUN useradd -r -u 65534 -g '' maven 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENV HOME=/app
ENV MAVEN_HOME=/opt/apache-maven-3.9.9
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["mvn", "--version"]
ENTRYPOINT ["mvn"]
LABEL org.opencontainers.image.title="maven" \
      org.opencontainers.image.version="3.9.9" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="Sovereign hardened maven - Java build tool" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
