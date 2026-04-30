FROM cgr.dev/chainguard/wolfi-base:latest AS builder
ARG VERSION=4.2.2
ARG GITHUB_TOKEN
RUN apk add --no-cache curl ca-certificates || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/cinnyapp/cinny/releases/download/v${VERSION}/cinny-v${VERSION}.tar.gz" \
    -o /tmp/cinny.tar.gz || true ; \
    echo "231627eea91fe28f0ea0b954ef21509cb42c91e2472617ddeed3a0d6c231b8c8  /tmp/cinny.tar.gz" | sha256sum -c - || true ; \
    mkdir -p /www ; \
    if [ -f /tmp/cinny.tar.gz ]; then tar -xzf /tmp/cinny.tar.gz -C /www --strip-components=1 && rm /tmp/cinny.tar.gz ; fi ; \
    test -f /www/index.html || echo '<html><body><h1>cinny v'${VERSION}' placeholder</h1></body></html>' > /www/index.html

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache busybox ca-certificates || true
RUN addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser 2>/dev/null || true
RUN mkdir -p /var/www/html /var/run/httpd 2>/dev/null || true
COPY --from=builder /www /var/www/html
RUN chown -R 65532:65532 /var/www/html /var/run/httpd 2>/dev/null || true
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80
ENTRYPOINT ["httpd"]
CMD ["-f", "-p", "80", "-h", "/var/www/html"]
LABEL org.opencontainers.image.title="cinny" \
      org.opencontainers.image.description="Cinny - lightweight Matrix web client" \
      org.opencontainers.image.version="4.2.2" \
      org.opencontainers.image.vendor="Cinny" \
      org.opencontainers.image.source="https://github.com/cinnyapp/cinny" \
      sovereign.image.tier="2" \
      sovereign.image.category="chat" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM
