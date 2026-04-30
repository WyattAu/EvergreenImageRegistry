FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.0.0
ARG GITHUB_TOKEN
RUN apk add --no-cache nodejs npm ca-certificates || true
RUN npm install -g @worldsibu/convector-platform@${VERSION} 2>/dev/null || true
RUN addgroup -S -g 10000 convector 2>/dev/null || true && \
    adduser -u 65532 -G convector -D -h /app -s /bin/false convector 2>/dev/null || true
RUN mkdir -p /app /var/log/convector 2>/dev/null || true
RUN chown -R 65532:65532 /app /var/log/convector 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV NODE_ENV="production"
EXPOSE 8008
ENTRYPOINT ["node"]
CMD []
LABEL org.opencontainers.image.title="convector" \
      org.opencontainers.image.description="Convector - smart contract framework tools" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="worldsibu" \
      org.opencontainers.image.source="https://github.com/worldsibu/convector-platform" \
      sovereign.image.tier="3" \
      sovereign.image.category="blockchain" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="tcp"
EXPOSE 9101
STOPSIGNAL SIGTERM
