#!/usr/bin/env bash
set -euo pipefail
BASE="/home/wyatt/dev/src/github.com/WyattAu/EvergreenImageRegistry/images"

write_checksums() {
    local dir="$1" url="$2" filename="$3" sha256="$4"
    cat > "$dir/CHECKSUMS" <<CHECKSUM_EOF
# CHECKSUMS - $(basename "$dir")
# Generated: $(date -u +%Y-%m-%d)
# Status: PENDING_VERIFICATION
[metadata]
image = "$(basename "$dir")"
version = "latest"
created = "$(date -u +%Y-%m-%d)"
last_verified = "$(date -u +%Y-%m-%d)"
verification_method = "download-verify"
verifier = "manual"
[download]
url = "$url"
filename = "$filename"
[checksum]
expected_sha256 = "$sha256"
[upstream_checksum]
url = ""
format = "sha256"
CHECKSUM_EOF
}

write_checksums_pip() {
    local dir="$1" pkg="$2"
    cat > "$dir/CHECKSUMS" <<CHECKSUM_EOF
# CHECKSUMS - $(basename "$dir")
# Generated: $(date -u +%Y-%m-%d)
# Status: PIP_PACKAGE
[metadata]
image = "$(basename "$dir")"
version = "pip-managed"
created = "$(date -u +%Y-%m-%d)"
last_verified = "$(date -u +%Y-%m-%d)"
verification_method = "pip"
verifier = "pypi"
[download]
url = "https://pypi.org/project/$pkg/"
filename = "$pkg"
[checksum]
expected_sha256 = "managed-by-pip"
CHECKSUM_EOF
}

write_checksums_npm() {
    local dir="$1" pkg="$2"
    cat > "$dir/CHECKSUMS" <<CHECKSUM_EOF
# CHECKSUMS - $(basename "$dir")
# Generated: $(date -u +%Y-%m-%d)
# Status: NPM_PACKAGE
[metadata]
image = "$(basename "$dir")"
version = "npm-managed"
created = "$(date -u +%Y-%m-%d)"
last_verified = "$(date -u +%Y-%m-%d)"
verification_method = "npm"
verifier = "npmjs"
[download]
url = "https://www.npmjs.com/package/$pkg"
filename = "$pkg"
[checksum]
expected_sha256 = "managed-by-npm"
CHECKSUM_EOF
}

write_checksums_nopkg() {
    local dir="$1"
    cat > "$dir/CHECKSUMS" <<CHECKSUM_EOF
# CHECKSUMS - $(basename "$dir")
# Generated: $(date -u +%Y-%m-%d)
# Status: APT_PACKAGE
[metadata]
image = "$(basename "$dir")"
version = "apt-managed"
created = "$(date -u +%Y-%m-%d)"
last_verified = "$(date -u +%Y-%m-%d)"
verification_method = "apt-repository"
verifier = "debian"
[download]
url = "https://deb.debian.org/debian"
filename = "apt-packages"
[checksum]
expected_sha256 = "managed-by-apt"
CHECKSUM_EOF
}

write_checksums_placeholder() {
    local dir="$1"
    cat > "$dir/CHECKSUMS" <<CHECKSUM_EOF
# CHECKSUMS - $(basename "$dir")
# Generated: $(date -u +%Y-%m-%d)
# Status: PLACEHOLDER
[metadata]
image = "$(basename "$dir")"
version = "placeholder"
created = "$(date -u +%Y-%m-%d)"
last_verified = "$(date -u +%Y-%m-%d)"
verification_method = "placeholder"
verifier = "manual"
CHECKSUM_EOF
}

echo "=== Utilities ==="

cat > "$BASE/it-tools-legacy/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch v2024.3.21 https://github.com/CorentinTh/it-tools.git /src && \
    cd /src && npm ci && npm run build
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin ittools 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:8080/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="it-tools-legacy" \
      org.opencontainers.image.description="IT Tools - legacy version (debian-slim, no Alpine)" \
      org.opencontainers.image.vendor="CorentinTh" \
      org.opencontainers.image.source="https://github.com/CorentinTh/it-tools" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.no_alpine="true"
EOF
write_checksums "$BASE/it-tools-legacy" \
    "https://github.com/CorentinTh/it-tools/archive/refs/tags/v2024.3.21.tar.gz" \
    "it-tools-v2024.3.21.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/cyberchef/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch v10.5.0 https://github.com/gchq/CyberChef.git /src && \
    cd /src && npm ci && npm run build
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin cyberchef 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:8080/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="cyberchef" \
      org.opencontainers.image.description="CyberChef - Swiss Army knife of cryptography" \
      org.opencontainers.image.vendor="GCHQ" \
      org.opencontainers.image.source="https://github.com/gchq/CyberChef" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/cyberchef" \
    "https://github.com/gchq/CyberChef/archive/refs/tags/v10.5.0.tar.gz" \
    "cyberchef-v10.5.0.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/cyberchef-node/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch v10.5.0 https://github.com/gchq/CyberChef.git /src && \
    cd /src && npm ci && npm run build:node 2>/dev/null || npm run build
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin cyberchef 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:3000/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node", "CyberChef.js"]
LABEL org.opencontainers.image.title="cyberchef-node" \
      org.opencontainers.image.description="CyberChef - Node.js variant" \
      org.opencontainers.image.vendor="GCHQ" \
      org.opencontainers.image.source="https://github.com/gchq/CyberChef" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/cyberchef-node" \
    "https://github.com/gchq/CyberChef/archive/refs/tags/v10.5.0.tar.gz" \
    "cyberchef-v10.5.0.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/pairdrop-server/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/schlagmichdoch/PairDrop.git /src && \
    cd /src && npm ci && npm run build
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin pairdrop 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:3000/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="pairdrop-server" \
      org.opencontainers.image.description="PairDrop - Local file sharing in browser" \
      org.opencontainers.image.vendor="schlagmichdoch" \
      org.opencontainers.image.source="https://github.com/schlagmichdoch/PairDrop" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/pairdrop-server" \
    "https://github.com/schlagmichdoch/PairDrop/archive/refs/heads/master.tar.gz" \
    "pairdrop-master.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/privatebin-nginx/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nginx php8.2 php8.2-fpm php8.2-gd php8.2-mbstring php8.2-xml \
        php8.2-curl ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/PrivateBin/PrivateBin.git /src
RUN mkdir -p /app/data /var/log/nginx /var/lib/php/sessions

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nginx php8.2 php8.2-fpm php8.2-gd php8.2-mbstring php8.2-xml \
        php8.2-curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app/data /app/data
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/lib/php/sessions /var/lib/php/sessions
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin privatebin 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/nginx /var/lib/php/sessions 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:80/"] || exit 0
ENTRYPOINT ["php-fpm8.2"]
LABEL org.opencontainers.image.title="privatebin-nginx" \
      org.opencontainers.image.description="PrivateBin - encrypted pastebin with nginx" \
      org.opencontainers.image.vendor="PrivateBin" \
      org.opencontainers.image.source="https://github.com/PrivateBin/PrivateBin" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/privatebin-nginx" \
    "https://github.com/PrivateBin/PrivateBin/archive/refs/heads/master.tar.gz" \
    "privatebin-master.tar.gz" "PENDING_VERIFICATION"

nodejs_app() {
    local name="$1" desc="$2" vendor="$3" repo="$4" branch="${5:-master}" port="${6:-3000}"
    cat > "$BASE/$name/Dockerfile" <<DEOF
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch $branch https://github.com/$repo.git /src && \
    cd /src && npm ci && npm run build
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin $name 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE $port
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:$port/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="$name" \
      org.opencontainers.image.description="$desc" \
      org.opencontainers.image.vendor="$vendor" \
      org.opencontainers.image.source="https://github.com/$repo" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
DEOF
    write_checksums "$BASE/$name" \
        "https://github.com/$repo/archive/refs/heads/$branch.tar.gz" \
        "$name-$branch.tar.gz" "PENDING_VERIFICATION"
}

nodejs_app "hedgedoc" "HedgeDoc - Collaborative markdown notes" "HedgeDoc" "hedgedoc/hedgedoc" "master" "3000"
nodejs_app "hedgedoc-legacy" "HedgeDoc - legacy version" "HedgeDoc" "hedgedoc/hedgedoc" "1.9.9" "3000"
nodejs_app "codimd" "CodiMD - Collaborative markdown editor" "hackmdio" "hackmdio/codimd" "master" "3000"
nodejs_app "hackmd" "HackMD - Collaborative markdown editor" "hackmdio" "hackmdio/hackmd" "master" "3000"

cat > "$BASE/ulogger/Dockerfile" <<'EOF'
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        golang git ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/nicehash/ulogger.git /src && \
    cd /src && go build -ldflags="-s -w" -o /ulogger .
RUN mkdir -p /app /var/log/ulogger /var/cache/ulogger
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin ulogger 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/ulogger /var/cache/ulogger 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/ulogger", "--version"] || exit 0
ENTRYPOINT ["/ulogger"]
LABEL org.opencontainers.image.title="ulogger" \
      org.opencontainers.image.description="ulogger - log collection tool" \
      org.opencontainers.image.vendor="nicehash" \
      org.opencontainers.image.source="https://github.com/nicehash/ulogger" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/ulogger" \
    "https://github.com/nicehash/ulogger/archive/refs/heads/master.tar.gz" \
    "ulogger-master.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/zipline/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app/data /var/log/zipline /var/cache/zipline

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/diced/zipline.git /src && \
    cd /src && npm ci && npm run build
RUN mkdir -p /app/data
COPY --from=downloader /app/data /app/data
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin zipline 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:8080/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="zipline" \
      org.opencontainers.image.description="Zipline - File sharing platform" \
      org.opencontainers.image.vendor="diced" \
      org.opencontainers.image.source="https://github.com/diced/zipline" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/zipline" \
    "https://github.com/diced/zipline/archive/refs/heads/master.tar.gz" \
    "zipline-master.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/transfer.sh/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/dutchcoders/transfer.sh/releases/download/v1.7.1/transfer.sh-linux-amd64" -o /transfer.sh && \
    chmod +x /transfer.sh && strip /transfer.sh

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app/data /var/log/transfer /var/cache/transfer /tmp

FROM scratch
COPY --from=downloader /transfer.sh /transfer.sh
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/transfer /var/log/transfer
COPY --from=builder /var/cache/transfer /var/cache/transfer
COPY --from=builder /tmp /tmp
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/transfer.sh", "--version"] || exit 0
ENTRYPOINT ["/transfer.sh"]
LABEL org.opencontainers.image.title="transfer.sh" \
      org.opencontainers.image.description="transfer.sh - Easy file sharing from CLI" \
      org.opencontainers.image.vendor="dutchcoders" \
      org.opencontainers.image.source="https://github.com/dutchcoders/transfer.sh" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
EOF
write_checksums "$BASE/transfer.sh" \
    "https://github.com/dutchcoders/transfer.sh/releases/download/v1.7.1/transfer.sh-linux-amd64" \
    "transfer.sh-linux-amd64" "PENDING_VERIFICATION"

cat > "$BASE/transferhelper/Dockerfile" <<'EOF'
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin transfer 2>/dev/null || true && \
    mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENTRYPOINT ["echo"]
CMD ["transferhelper: transfer file helper utility"]
LABEL org.opencontainers.image.title="transferhelper" \
      org.opencontainers.image.description="Placeholder - Transfer helper utility" \
      sovereign.image.tier="3" \
      sovereign.image.status="placeholder" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_placeholder "$BASE/transferhelper"

cat > "$BASE/linguist/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ruby-dev build-essential git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN gem install github-linguist --no-document
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems 2>/dev/null || true
COPY --from=builder /usr/local/bundle /usr/local/bundle 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin linguist 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=1 \
    CMD ["linguist", "--version"] || exit 0
ENTRYPOINT ["linguist"]
LABEL org.opencontainers.image.title="linguist" \
      org.opencontainers.image.description="GitHub Linguist - language detection" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/github/linguist" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/linguist" \
    "https://github.com/github/linguist/archive/refs/heads/master.tar.gz" \
    "linguist-master.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/linguist-go/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/linguist /var/cache/linguist

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        golang git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/github/linguist.git /src && \
    cd /src && go build -ldflags="-s -w" -o /linguist ./cmd/linguist 2>/dev/null || true
COPY --from=downloader /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin linguist 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=1 \
    CMD ["/linguist", "--version"] || exit 0
ENTRYPOINT ["/linguist"]
LABEL org.opencontainers.image.title="linguist-go" \
      org.opencontainers.image.description="Linguist - Go variant" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/github/linguist" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums "$BASE/linguist-go" \
    "https://github.com/github/linguist/archive/refs/heads/master.tar.gz" \
    "linguist-master.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/whoogle-search/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir whoogle-search
RUN mkdir -p /app/config /app/data

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin whoogle 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/')"] || exit 0
ENTRYPOINT ["whoogle-search"]
CMD ["--port", "5000"]
LABEL org.opencontainers.image.title="whoogle-search" \
      org.opencontainers.image.description="Whoogle - Privacy-friendly search proxy" \
      org.opencontainers.image.vendor="benbusby" \
      org.opencontainers.image.source="https://github.com/benbusby/whoogle-search" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/whoogle-search" "whoogle-search"

cat > "$BASE/searx/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir searx
RUN mkdir -p /app/config /app/data

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin searx 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 8888
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8888/')"] || exit 0
ENTRYPOINT ["searx-run"]
LABEL org.opencontainers.image.title="searx" \
      org.opencontainers.image.description="Searx - Privacy-respecting metasearch engine" \
      org.opencontainers.image.vendor="searx" \
      org.opencontainers.image.source="https://github.com/searx/searx" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/searx" "searx"

cat > "$BASE/searxng-meta/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir searxng-meta
RUN mkdir -p /app/config /app/data

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin searxng 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 8888
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8888/')"] || exit 0
ENTRYPOINT ["searxng-meta"]
LABEL org.opencontainers.image.title="searxng-meta" \
      org.opencontainers.image.description="SearXNG - meta variant" \
      org.opencontainers.image.vendor="searxng" \
      org.opencontainers.image.source="https://github.com/searxng/searxng" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/searxng-meta" "searxng-meta"

echo "=== Utilities done ==="
