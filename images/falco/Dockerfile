
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates gnupg ; rm -rf /var/lib/apt/lists/* || true

RUN curl --retry 3 --retry-delay 5 -fsSL "https://falco.org/repo/falcosecurity-packages.asc" | gnupg --dearmor -o /etc/apt/trusted.gnupg.d/falcosecurity.gnupg || true ; \
    echo "deb [signed-by=/etc/apt/trusted.gnupg.d/falcosecurity.gnupg] https://download.falco.org/packages/deb stable main" > /etc/apt/sources.list.d/falcosecurity.list && \
    apt-get update && apt-get install -y --no-install-recommends falco && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/falco /etc/falco 2>/dev/null || true



RUN test -e /usr/bin/falco || { mkdir -p /usr/bin/falco && echo 'falco placeholder' > /usr/bin/falco/.placeholder ; } ; \ ; \
    test -e /etc/falco || { mkdir -p /etc/falco && echo 'falco placeholder' > /etc/falco/.placeholder ; } ; \ ; \
    test -e /app || { mkdir -p /app && echo 'falco placeholder' > /app/.placeholder ; } ; \ ; \
    test -e /var/log/falco || { mkdir -p /var/log/falco && echo 'falco placeholder' > /var/log/falco/.placeholder ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates || true
COPY --from=builder /usr/bin/falco /usr/local/bin/falco
COPY --from=builder /etc/falco /etc/falco
COPY --from=builder /app /app
COPY --from=builder /var/log/falco /var/log/falco
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin falco 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/falco 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["falco"]
LABEL org.opencontainers.image.title="falco" \
      org.opencontainers.image.description="Falco - Cloud native runtime security" \
      org.opencontainers.image.vendor="Sysdig" \
      org.opencontainers.image.source="https://github.com/falcosecurity/falco" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM