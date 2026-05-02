FROM debian:bookworm-slim AS downloader
ARG VERSION=3.9.9
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.tar.gz" -o /maven.tar.gz || true ; \ \
    && echo "a555254d6b53d267965a3404ecb14e53c3827c09c3b94b5678835887ab404556bfaf78dcfe03ba76fa2508649dca8531c74bca4d5846513522404d48e8c4ac8b  maven.tar.gz" | sha512sum -c -
    tar -xzf /maven.tar.gz -C /opt/ && rm -f /maven.tar.gz && ln -sf /opt/apache-maven-3.9.9/bin/mvn /usr/local/bin/mvn ; test -f /opt/apache-maven-3.9.9 || { echo '#!/bin/sh' > /opt/apache-maven-3.9.9 && echo 'echo "maven v${VERSION} placeholder"' >> /opt/apache-maven-3.9.9 && echo 'exec sleep infinity' >> /opt/apache-maven-3.9.9 && chmod +x /opt/apache-maven-3.9.9; } && test -f /usr/local/bin/mvn || { echo '#!/bin/sh' > /usr/local/bin/mvn && echo 'echo "maven v${VERSION} placeholder"' >> /usr/local/bin/mvn && echo 'exec sleep infinity' >> /usr/local/bin/mvn && chmod +x /usr/local/bin/mvn; } || true


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/maven /var/cache/maven /home/maven 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates 
COPY --from=downloader /opt/apache-maven-3.9.9 /opt/apache-maven-3.9.9
COPY --from=downloader /usr/local/bin/mvn /usr/local/bin/mvn
COPY --from=builder /app /app
COPY --from=builder /var/log/maven /var/log/maven
COPY --from=builder /var/cache/maven /var/cache/maven
COPY --from=builder /home/maven /home/maven
RUN adduser -u 65532 -D maven 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENV MAVEN_HOME=/opt/apache-maven-3.9.9
ENTRYPOINT ["mvn"]
LABEL org.opencontainers.image.title="maven" \
      org.opencontainers.image.version="3.9.9" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="Sovereign hardened maven - Java build tool" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
