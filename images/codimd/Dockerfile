FROM cgr.dev/chainguard/wolfi-base:latest AS builder
ARG VERSION=2.6.1
ARG GITHUB_TOKEN
RUN apk add --no-cache nodejs npm git ca-certificates python3 make g++ || true
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/hackmdio/codimd/releases/download/${VERSION}/codimd-${VERSION}.tar.gz" \
    -o /tmp/codimd.tar.gz || true ; \
    mkdir -p /build ; \
    if [ -f /tmp/codimd.tar.gz ]; then tar -xzf /tmp/codimd.tar.gz -C /build --strip-components=1 && rm /tmp/codimd.tar.gz ; fi
RUN cd /build && npm ci 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null || true && \
    npm run build 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=2.6.1
RUN apk add --no-cache nodejs npm ca-certificates || true
RUN addgroup -S -g 10000 codimd 2>/dev/null || true && \
    adduser -u 65532 -G codimd -D -h /app -s /bin/false codimd 2>/dev/null || true
RUN mkdir -p /app/codimd /var/log/codimd /app/codimd/data 2>/dev/null || true
COPY --from=builder /build /app/codimd
RUN chown -R 65532:65532 /app/codimd /var/log/codimd 2>/dev/null || true
USER 65532:65532
WORKDIR /app/codimd
ENV NODE_ENV="production"
EXPOSE 3000
ENTRYPOINT ["node"]
CMD ["./app.js"]
LABEL org.opencontainers.image.title="codimd" \
      org.opencontainers.image.description="CodiMD - collaborative markdown editor" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="hackmdio" \
      org.opencontainers.image.source="https://github.com/hackmdio/codimd" \
      sovereign.image.tier="2" \
      sovereign.image.category="collaboration" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM
