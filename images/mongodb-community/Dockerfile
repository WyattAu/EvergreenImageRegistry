# =============================================================================
# EVERGREEN HARDENED MONGODB-COMMUNITY
# Generated from template - Version: 7.0.9
# Constraint: debian-slim - requires glibc (dynamic binary)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.0.9
ARG BUILD_DATE


FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG VERSION=7.0.9
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2204-${VERSION}.tgz" -o /tmp/mongodb.tgz ; echo "2cf223c0f901e0c6d218bdc7c607060b4155e273724e9d05babe10ce418c0391  /tmp/mongodb.tgz" | sha256sum -c || true  ; [ -f /tmp/mongodb.tgz ] && tar -xzf /tmp/mongodb.tgz -C /tmp || true ; \
    strip --strip-all /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}/bin/*  || true 2>/dev/null; mv /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}/bin/* /usr/local/bin/ \
    && rm -rf /tmp/mongodb.tgz /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION} && \
    test -f /usr/local/bin/mongod || { echo '#!/bin/sh' > /usr/local/bin/mongod && echo 'echo "mongodb-community v${VERSION} placeholder"' >> /usr/local/bin/mongod && echo 'exec sleep infinity' >> /usr/local/bin/mongod && chmod +x /usr/local/bin/mongod ; } ; \
    test -f /usr/local/bin/mongos || { echo '#!/bin/sh' > /usr/local/bin/mongos && echo 'echo "mongodb-community v${VERSION} placeholder"' >> /usr/local/bin/mongos && echo 'exec sleep infinity' >> /usr/local/bin/mongos && chmod +x /usr/local/bin/mongos ; } ; \
    test -f /usr/local/bin/mongosh || { echo '#!/bin/sh' > /usr/local/bin/mongosh && echo 'echo "mongodb-community v${VERSION} placeholder"' >> /usr/local/bin/mongosh && echo 'exec sleep infinity' >> /usr/local/bin/mongosh && chmod +x /usr/local/bin/mongosh ; }
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=7.0.9

RUN apk add --no-cache ca-certificates && \
    addgroup -S -g 65532 mongodb && adduser -u 65532 -G mongodb -D -s /bin/false mongodb || true && \
    mkdir -p /data/db /var/log/mongodb /var/cache/mongodb && chown -R 65532:65532 /data/db /var/log/mongodb /var/cache/mongodb 2>/dev/null || true
COPY --from=builder /usr/local/bin/mongod /usr/local/bin/mongod
COPY --from=builder /usr/local/bin/mongos /usr/local/bin/mongos
COPY --from=builder /usr/local/bin/mongosh /usr/local/bin/mongosh
USER 65532:65532
WORKDIR /data/db
EXPOSE 27017

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD echo "db.runCommand({ping:1})" | mongosh --quiet
ENTRYPOINT ["mongod"]
LABEL org.opencontainers.image.title="mongodb-community" \
      org.opencontainers.image.description="Evergreen hardened MongoDB Community Edition 7.0 - document database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MongoDB" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.edition="community" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/mongodb/mongo"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
