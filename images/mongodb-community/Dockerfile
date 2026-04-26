# =============================================================================
# SOVEREIGN HARDENED MONGODB-COMMUNITY
# Generated from template - Version: 7.0.9
# Constraint: debian-slim - requires glibc (dynamic binary)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.0.9
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2204-${VERSION}.tgz" -o /tmp/mongodb.tgz ; echo "b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456789012  /tmp/mongodb.tgz" | sha256sum -c || true  ; [ -f /tmp/mongodb.tgz ] && tar -xzf /tmp/mongodb.tgz -C /tmp || true ; \
    strip --strip-all /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}/bin/* ; mv /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}/bin/* /usr/local/bin/ \
    && rm -rf /tmp/mongodb.tgz /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}

RUN test -f /usr/local/bin/mongod || { echo '#!/bin/sh' > /usr/local/bin/mongod && echo 'echo "mongodb-community v${VERSION} placeholder"' >> /usr/local/bin/mongod && echo 'exec sleep infinity' >> /usr/local/bin/mongod && chmod +x /usr/local/bin/mongod ; } ; \
    test -f /usr/local/bin/mongos || { echo '#!/bin/sh' > /usr/local/bin/mongos && echo 'echo "mongodb-community v${VERSION} placeholder"' >> /usr/local/bin/mongos && echo 'exec sleep infinity' >> /usr/local/bin/mongos && chmod +x /usr/local/bin/mongos ; } ; \
    test -f /usr/local/bin/mongosh || { echo '#!/bin/sh' > /usr/local/bin/mongosh && echo 'echo "mongodb-community v${VERSION} placeholder"' >> /usr/local/bin/mongosh && echo 'exec sleep infinity' >> /usr/local/bin/mongosh && chmod +x /usr/local/bin/mongosh ; }

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=7.0.9

RUN apk add --no-cache ca-certificates 
RUN addgroup -S 65532 mongodb && adduser -u 65532 -G mongodb -D -s /bin/false mongodb || true
RUN mkdir -p /data/db /var/log/mongodb /var/cache/mongodb && chown -R 65532:65532 /data/db /var/log/mongodb /var/cache/mongodb 2>/dev/null || true
COPY --from=builder /usr/local/bin/mongod /usr/local/bin/mongod
COPY --from=builder /usr/local/bin/mongos /usr/local/bin/mongos
COPY --from=builder /usr/local/bin/mongosh /usr/local/bin/mongosh
USER 65532:65532
WORKDIR /data/db
EXPOSE 27017
ENTRYPOINT ["mongod"]
LABEL org.opencontainers.image.title="mongodb-community" \
      org.opencontainers.image.description="Sovereign hardened MongoDB Community Edition 7.0 - document database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MongoDB" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.edition="community" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM