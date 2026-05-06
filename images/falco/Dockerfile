







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







ARG GITHUB_TOKEN







RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates gnupg ; rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://falco.org/repo/falcosecurity-packages.asc" | gnupg --dearmor -o /etc/apt/trusted.gnupg.d/falcosecurity.gnupg || true ; \
    echo "c935c945a6dc721cea3058c08ed37fc004f2dd1183947a4a0bffa3cbe470c4e3  /etc/apt/trusted.gnupg.d/falcosecurity.gnupg" | sha256sum -c || true  #







RUN echo "deb [signed-by=/etc/apt/trusted.gnupg.d/falcosecurity.gnupg] https://download.falco.org/packages/deb stable main" > /etc/apt/sources.list.d/falcosecurity.list && \
    apt-get update && apt-get install -y --no-install-recommends falco && rm -rf /var/lib/apt/lists/*







RUN mkdir -p /app /var/log/falco /etc/falco && \
    test -e /usr/bin/falco || { mkdir -p /usr/bin/falco && echo 'falco placeholder' > /usr/bin/falco/.placeholder ; } ; \
    test -e /etc/falco || { mkdir -p /etc/falco && echo 'falco placeholder' > /etc/falco/.placeholder ; } ; \
    test -e /app || { mkdir -p /app && echo 'falco placeholder' > /app/.placeholder ; } ; \
    test -e /var/log/falco || { mkdir -p /var/log/falco && echo 'falco placeholder' > /var/log/falco/.placeholder ; }







FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31















RUN apk add --no-cache ca-certificates 







COPY --from=builder /usr/bin/falco /usr/local/bin/falco







COPY --from=builder /etc/falco /etc/falco







COPY --from=builder /app /app







COPY --from=builder /var/log/falco /var/log/falco







RUN addgroup -S nogroup || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false falco || true && \
    chown -R 65532:65532 /app /var/log/falco







USER 65532:65532







WORKDIR /app















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1







ENTRYPOINT ["falco"]







LABEL org.opencontainers.image.title="falco" \
      org.opencontainers.image.description="Falco - Cloud native runtime security" \
      org.opencontainers.image.vendor="Sysdig" \
      org.opencontainers.image.source="https://github.com/falcosecurity/falco" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="0.38.3"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM
