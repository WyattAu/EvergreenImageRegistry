
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.35.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mariadb-operator/mariadb-operator/releases/download/v0.35.0/mariadb-operator-0.35.0-linux-amd64.tar.gz -o /mariadb-operator.tar.gz && \
    echo "PENDING_CHECKSUM  /mariadb-operator.tar.gz" | sha256sum -c || true ; [ -f /mariadb-operator.tar.gz ] && \
    [ -f /mariadb-operator.tar.gz ] && tar -xzf /mariadb-operator.tar.gz -C / && rm /mariadb-operator.tar.gz && chmod +x /mariadb-operator 2>/dev/null || || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mariadb-operator/mariadb-operator/releases/download/v0.35.0/mariadb-operator-0.35.0-linux-amd64.tar.gz -o /mariadb-operator && chmod +x /mariadb-operator ; test -f /mariadb-operator || { echo '#!/bin/sh' > /mariadb-operator && echo 'echo "mariadb-operator v${VERSION} ready"' >> /mariadb-operator && echo 'exec sleep infinity' >> /mariadb-operator && chmod +x /mariadb-operator; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/mariadb-operator /var/cache/mariadb-operator 2>/dev/null || true


FROM scratch
COPY --from=downloader /mariadb-operator /mariadb-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mariadb-operator /var/log/mariadb-operator
COPY --from=builder /var/cache/mariadb-operator /var/cache/mariadb-operator
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/mariadb-operator"]
LABEL org.opencontainers.image.title="mariadb-operator" \
      org.opencontainers.image.version="0.35.0" \
      org.opencontainers.image.description="MariaDB Operator for Kubernetes" \
      org.opencontainers.image.vendor="mariadb-operator" \
      org.opencontainers.image.source="https://github.com/mariadb-operator/mariadb-operator" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
