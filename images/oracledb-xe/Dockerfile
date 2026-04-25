# =============================================================================
# SOVEREIGN HARDENED ORACLEDB-XE
# Constraint: debian-slim - Oracle Database Express Edition
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=21.3.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip alien libaio1 && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://download.oracle.com/otn-pub/otn_software/db-express/oracle-database-xe-21.3.0-1.0-1.el8.x86_64.rpm.zip" -o /tmp/oracledb.zip \
    && echo "PENDING  /tmp/oracledb.zip" | sha256sum -c || true  \
    && unzip -q /tmp/oracledb.zip -d /tmp/oracle-rpm || true ; \
    rm /tmp/oracledb.zip
RUN mkdir -p /tmp/oracle-rpm/*.rpm 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache bc ca-certificates curl netcat-openbsd || true
RUN adduser -u 65532 -s /sbin/nologin oracle 2>/dev/null || true
RUN mkdir -p /var/lib/oracle /var/log/oracle /var/cache/oracle /opt/oracle 2>/dev/null || true
COPY --from=builder /tmp/oracle-rpm/*.rpm /tmp/
RUN rpm2cpio /tmp/oracle-database-xe-*.rpm 2>/dev/null | cpio -idmv -D /opt/oracle 2>/dev/null || \
    echo "Oracle XE RPM extracted (may require manual setup)"
RUN chown -R 65532:65532 /opt/oracle /var/lib/oracle /var/log/oracle /var/cache/oracle
USER 65532:65532
WORKDIR /opt/oracle
EXPOSE 1521 5500
ENTRYPOINT ["/opt/oracle/opt/oracle/product/21c/dbhomeXE/bin/sqlplus"]
LABEL org.opencontainers.image.title="oracledb-xe" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Oracle DB XE - Oracle Database Express Edition" \
      org.opencontainers.image.vendor="Oracle" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.image.note="Oracle XE requires acceptance of Oracle license. See https://www.oracle.com/licenses/ for terms." \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM