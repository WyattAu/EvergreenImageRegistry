ARG VERSION=latest

FROM cubrid/cubrid:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates
RUN adduser -D -u 65532 -s /bin/false cubrid 2>/dev/null || true
RUN mkdir -p /var/lib/cubrid /var/log/cubrid /var/cache/cubrid /opt 2>/dev/null || true
COPY --from=upstream /opt/cubrid /opt/cubrid
RUN chown -R 65532:65532 /opt/cubrid /var/lib/cubrid /var/log/cubrid /var/cache/cubrid 2>/dev/null || true

WORKDIR /var/lib/cubrid

EXPOSE 30000 33000 33001
EXPOSE 9101

LABEL org.opencontainers.image.title="cubrid" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Sovereign hardened CUBRID - open source SQL database" org.opencontainers.image.vendor="CUBRID" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/cubrid/bin/cubrid"]
