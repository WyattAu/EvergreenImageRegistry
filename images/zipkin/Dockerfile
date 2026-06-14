# =============================================================================
# EVERGREEN HARDENED ZIPKIN
# Distributed tracing system (Java)
# Constraint: debian-slim + Adoptium JRE 21
# =============================================================================

ARG VERSION=3.4.2
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS jre-builder
RUN mkdir -p /opt/jre || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jre/hotspot/normal/eclipse" -o /tmp/jre.tar.gz && \
    echo "e5038aae3ca9ff670bc696496b0728dbd23d280026bad30291cb919221ecfdcb  /tmp/jre.tar.gz" | sha256sum -c ; \
    mkdir -p /opt/jre ; \
    [ -f /tmp/jre.tar.gz ] && tar -xzf /tmp/jre.tar.gz -C /opt/jre --strip-components=1 ; \
    rm -f /tmp/jre.tar.gz


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=3.4.2

RUN apk add --no-cache ca-certificates tzdata curl
COPY --from=jre-builder /opt/jre /opt/jre
ENV JAVA_HOME="/opt/jre"
ENV PATH="${JAVA_HOME}/bin:${PATH}"
RUN curl --retry 3 --retry-delay 5 -fsSL "https://search.maven.org/remotecontent?filepath=io/zipkin/zipkin-server/${VERSION}/zipkin-server-${VERSION}-exec.jar" -o /opt/zipkin/zipkin.jar || \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/openzipkin/zipkin/releases/download/${VERSION}/zipkin.jar -o /opt/zipkin.jar && \
    mkdir -p /opt/zipkin /var/log/zipkin ; \
    addgroup -S -g 65532 zipkin 2>/dev/null || true && \
    adduser -u 65532 -G zipkin -D -D -h /opt/zipkin -s /bin/false zipkin 2>/dev/null || true && \
    chown -R 65532:65532 /opt/zipkin /var/log/zipkin
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/zipkin
EXPOSE 9411

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9411"]

ENTRYPOINT ["/shim", "run", "-c", "java -jar /zipkin-server/zipkin-server.jar"]
CMD ["-c", "java", "--", "-jar", "/opt/zipkin/zipkin.jar"]
LABEL org.opencontainers.image.title="zipkin" \
      org.opencontainers.image.description="Zipkin - distributed tracing system" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="OpenZipkin" \
      org.opencontainers.image.source="https://github.com/openzipkin/zipkin" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="observability" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
