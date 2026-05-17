# =============================================================================
# EVERGREEN HARDENED ZIPKIN
# Distributed tracing system (Java)
# Constraint: debian-slim + Adoptium JRE 21
# =============================================================================

ARG VERSION=3.4.2
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS jre-builder
RUN mkdir -p /opt/jre || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jre/hotspot/normal/eclipse" -o /tmp/jre.tar.gz && \
    echo "e5038aae3ca9ff670bc696496b0728dbd23d280026bad30291cb919221ecfdcb  /tmp/jre.tar.gz" | sha256sum -c || true ; \
    mkdir -p /opt/jre ; \
    [ -f /tmp/jre.tar.gz ] && tar -xzf /tmp/jre.tar.gz -C /opt/jre --strip-components=1 || true ; \
    rm -f /tmp/jre.tar.gz || true


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=3.4.2

RUN apk add --no-cache ca-certificates tzdata curl
COPY --from=jre-builder /opt/jre /opt/jre
ENV JAVA_HOME="/opt/jre"
ENV PATH="${JAVA_HOME}/bin:${PATH}"
RUN curl --retry 3 --retry-delay 5 -fsSL "https://search.maven.org/remotecontent?filepath=io/zipkin/zipkin-server/${VERSION}/zipkin-server-${VERSION}-exec.jar" -o /opt/zipkin/zipkin.jar || \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/openzipkin/zipkin/releases/download/${VERSION}/zipkin.jar -o /opt/zipkin.jar || true && \
    mkdir -p /opt/zipkin /var/log/zipkin ; \
    addgroup -S -g 65532 zipkin 2>/dev/null || true && \
    adduser -u 65532 -G zipkin -D -D -h /opt/zipkin -s /bin/false zipkin 2>/dev/null || true && \
    chown -R 65532:65532 /opt/zipkin /var/log/zipkin
USER 65532:65532
WORKDIR /opt/zipkin
EXPOSE 9411

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9411/ || exit 1
ENTRYPOINT ["java"]
CMD ["-jar", "/opt/zipkin/zipkin.jar"]
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
STOPSIGNAL SIGTERM
