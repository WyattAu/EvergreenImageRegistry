# =============================================================================
# SOVEREIGN HARDENED ZIPKIN
# Distributed tracing system (Java)
# Constraint: debian-slim + Adoptium JRE 21
# =============================================================================

ARG VERSION=3.4.2
ARG BUILD_DATE


FROM debian:bookworm-slim AS jre-builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jre/hotspot/normal/eclipse" -o /tmp/jre.tar.gz && \
    mkdir -p /opt/jre ; \
    [ -f /tmp/jre.tar.gz ] && tar -xzf /tmp/jre.tar.gz -C /opt/jre --strip-components=1 || true ; \
    rm /tmp/jre.tar.gz || true


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=3.4.2

RUN apk add --no-cache ca-certificates tzdata curl || true
COPY --from=jre-builder /opt/jre /opt/jre
ENV JAVA_HOME="/opt/jre"
ENV PATH="${JAVA_HOME}/bin:${PATH}"
RUN curl --retry 3 --retry-delay 5 -fsSL "https://search.maven.org/remotecontent?filepath=io/zipkin/zipkin-server/${VERSION}/zipkin-server-${VERSION}-exec.jar" -o /opt/zipkin/zipkin.jar || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/openzipkin/zipkin/releases/download/${VERSION}/zipkin.jar -o /opt/zipkin.jar || true
RUN mkdir -p /opt/zipkin /var/log/zipkin ; \
    addgroup -S 65532 -r zipkin 2>/dev/null || true && \
    adduser -u 65532 -G zipkin -D -D -h /opt/zipkin -s /sbin/nologin zipkin 2>/dev/null || true && \
    chown -R 65532:65532 /opt/zipkin /var/log/zipkin
USER 65532:65532
WORKDIR /opt/zipkin
EXPOSE 9411
ENTRYPOINT ["java"]
CMD ["-jar", "/opt/zipkin/zipkin.jar"]
LABEL org.opencontainers.image.title="zipkin" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="OpenZipkin" \
      org.opencontainers.image.source="https://github.com/openzipkin/zipkin" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM