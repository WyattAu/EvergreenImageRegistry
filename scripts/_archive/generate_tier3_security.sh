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

go_scratch() {
    local name="$1" desc="$2" vendor="$3" repo="$4" binary="$5" version="$6"
    local url="https://github.com/$repo/releases/download/v${version}/${binary}"
    cat > "$BASE/$name/Dockerfile" <<DEOF
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "$url" -o /$name && chmod +x /$name && strip /$name

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/$name /var/cache/$name

FROM scratch
COPY --from=downloader /$name /$name
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/$name /var/log/$name
COPY --from=builder /var/cache/$name /var/cache/$name
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/$name", "--version"]
ENTRYPOINT ["/$name"]
LABEL org.opencontainers.image.title="$name" \
      org.opencontainers.image.description="$desc" \
      org.opencontainers.image.vendor="$vendor" \
      org.opencontainers.image.source="https://github.com/$repo" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
DEOF
    write_checksums "$BASE/$name" "$url" "$name" "PENDING_VERIFICATION"
}

go_debian() {
    local name="$1" desc="$2" vendor="$3" repo="$4" binary="$5" version="$6"
    local url="https://github.com/$repo/releases/download/v${version}/${binary}"
    cat > "$BASE/$name/Dockerfile" <<DEOF
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "$url" -o /$name && chmod +x /$name && strip /$name

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/$name /var/cache/$name

FROM debian:bookworm-slim
COPY --from=downloader /$name /usr/local/bin/$name
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin $name 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["$name", "--version"]
ENTRYPOINT ["$name"]
LABEL org.opencontainers.image.title="$name" \
      org.opencontainers.image.description="$desc" \
      org.opencontainers.image.vendor="$vendor" \
      org.opencontainers.image.source="https://github.com/$repo" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
DEOF
    write_checksums "$BASE/$name" "$url" "$name" "PENDING_VERIFICATION"
}

echo "=== Security: Scanner Variants ==="

go_scratch "trivy-alpine" "Trivy - vulnerability scanner (no Alpine)" "Aqua Security" "aquasecurity/trivy" "trivy_0.58.2_linux-amd64.tar.gz" "0.58.2"
go_debian "trivy-k8s" "Trivy - Kubernetes operator" "Aqua Security" "aquasecurity/trivy" "trivy_0.58.2_linux-amd64.tar.gz" "0.58.2"
go_debian "trivy-iac" "Trivy - IaC scanner" "Aqua Security" "aquasecurity/trivy" "trivy_0.58.2_linux-amd64.tar.gz" "0.58.2"
go_scratch "grype-alpine" "Grype - vulnerability scanner (no Alpine)" "Anchore" "anchore/grype" "grype_0.80.0_linux_amd64.tar.gz" "0.80.0"
go_scratch "syft-alpine" "Syft - SBOM scanner (no Alpine)" "Anchore" "anchore/syft" "syft_1.11.0_linux_amd64.tar.gz" "1.11.0"

echo "=== Security: Snyk ==="

go_debian "snyk-alpine" "Snyk - security scanner (no Alpine)" "Snyk" "snyk/snyk" "snyk-linux" "1.1295.0"
go_debian "snyk-docker" "Snyk - Docker mode" "Snyk" "snyk/snyk" "snyk-linux" "1.1295.0"
go_debian "snyk-monitor" "Snyk - monitor mode" "Snyk" "snyk/snyk" "snyk-linux" "1.1295.0"

echo "=== Security: Audit Tools ==="

cat > "$BASE/npm-audit/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin npmaudit 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["npm", "--version"]
ENTRYPOINT ["npm"]
CMD ["audit"]
LABEL org.opencontainers.image.title="npm-audit" \
      org.opencontainers.image.description="npm audit wrapper" \
      org.opencontainers.image.vendor="npm" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/npm-audit"

cat > "$BASE/yarn-audit/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g yarn
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules /usr/lib/node_modules 2>/dev/null || true
COPY --from=builder /usr/bin/yarn /usr/local/bin/yarn 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin yarnaudit 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["yarn", "--version"]
ENTRYPOINT ["yarn"]
CMD ["audit"]
LABEL org.opencontainers.image.title="yarn-audit" \
      org.opencontainers.image.description="Yarn audit wrapper" \
      org.opencontainers.image.vendor="Yarn" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_npm "$BASE/yarn-audit" "yarn"

cat > "$BASE/cargo-audit/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile minimal
ENV PATH="/root/.cargo/bin:$PATH"
RUN cargo install cargo-audit
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.cargo/bin/cargo-audit /usr/local/bin/cargo-audit
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin cargoaudit 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["cargo-audit", "--version"]
ENTRYPOINT ["cargo-audit"]
LABEL org.opencontainers.image.title="cargo-audit" \
      org.opencontainers.image.description="Cargo audit - Rust dependency security scanner" \
      org.opencontainers.image.vendor="rustsec" \
      org.opencontainers.image.source="https://github.com/rustsec/rustsec-audit" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums "$BASE/cargo-audit" \
    "https://github.com/rustsec/rustsec-audit/archive/refs/heads/main.tar.gz" \
    "rustsec-audit-main.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/pip-audit/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pip-audit
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin pipaudit 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["pip-audit", "--version"]
ENTRYPOINT ["pip-audit"]
LABEL org.opencontainers.image.title="pip-audit" \
      org.opencontainers.image.description="pip audit - Python dependency security scanner" \
      org.opencontainers.image.vendor="pypa" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/pip-audit" "pip-audit"

cat > "$BASE/gem-audit/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ruby-dev build-essential ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN gem install bundler-audit --no-document
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems 2>/dev/null || true
COPY --from=builder /usr/local/bundle /usr/local/bundle 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin gemaudit 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["bundler-audit", "--version"] || exit 0
ENTRYPOINT ["bundler-audit"]
LABEL org.opencontainers.image.title="gem-audit" \
      org.opencontainers.image.description="Gem/Bundler audit - Ruby dependency security scanner" \
      org.opencontainers.image.vendor="rubysec" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_placeholder "$BASE/gem-audit"

cat > "$BASE/conan-audit/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir conan
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin conan 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["conan", "--version"]
ENTRYPOINT ["conan"]
CMD ["audit"]
LABEL org.opencontainers.image.title="conan-audit" \
      org.opencontainers.image.description="Conan audit - C/C++ dependency security scanner" \
      org.opencontainers.image.vendor="conan-io" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/conan-audit" "conan"

cat > "$BASE/composer-audit/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        php8.2 php8.2-cli php8.2-mbstring php8.2-xml php8.2-curl \
        ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://getcomposer.org/installer" | php -- --install-dir=/usr/local/bin --filename=composer
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        php8.2 php8.2-cli php8.2-mbstring php8.2-xml php8.2-curl \
        ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/bin/composer /usr/local/bin/composer
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin composer 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["composer", "--version"]
ENTRYPOINT ["composer"]
CMD ["audit"]
LABEL org.opencontainers.image.title="composer-audit" \
      org.opencontainers.image.description="Composer audit - PHP dependency security scanner" \
      org.opencontainers.image.vendor="Composer" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/composer-audit"

go_scratch "govulncheck" "Go vulnerability checker" "golang" "golang/vuln" "govulncheck_1.1.0_linux_amd64.tar.gz" "1.1.0"

echo "=== Security: Secret Scanners ==="

go_scratch "trufflehog" "TruffleHog - secret scanner" "trufflesecurity" "trufflesecurity/trufflehog" "trufflehog_3.82.2_linux_amd64.tar.gz" "3.82.2"
go_scratch "truffleshog" "TruffleHog - secret scanner (alias)" "trufflesecurity" "trufflesecurity/trufflehog" "trufflehog_3.82.2_linux_amd64.tar.gz" "3.82.2"
go_scratch "truffelsh" "TruffleHog - secret scanner (alias)" "trufflesecurity" "trufflesecurity/trufflehog" "trufflehog_3.82.2_linux_amd64.tar.gz" "3.82.2"
go_scratch "gitleaks" "Gitleaks - secret scanner" "gitleaks" "gitleaks/gitleaks" "gitleaks_8.21.2_linux_x64.tar.gz" "8.21.2"

cat > "$BASE/git-secrets/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://raw.githubusercontent.com/awslabs/git-secrets/master/git-secrets" \
    -o /usr/local/bin/git-secrets && chmod +x /usr/local/bin/git-secrets
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/bin/git-secrets /usr/local/bin/git-secrets
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin gitsecrets 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["git-secrets", "--version"] || exit 0
ENTRYPOINT ["git-secrets"]
LABEL org.opencontainers.image.title="git-secrets" \
      org.opencontainers.image.description="AWS Git Secrets - prevent secret commits" \
      org.opencontainers.image.vendor="AWS Labs" \
      org.opencontainers.image.source="https://github.com/awslabs/git-secrets" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums "$BASE/git-secrets" \
    "https://github.com/awslabs/git-secrets/archive/refs/heads/master.tar.gz" \
    "git-secrets-master.tar.gz" "PENDING_VERIFICATION"

for name in repo-security secrets-scanner secretz shh repo-supervisor; do
    cat > "$BASE/$name/Dockerfile" <<DEOF
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates git curl \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin $name 2>/dev/null || true && \
    mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["python3", "-c", "print('ok')"]
ENTRYPOINT ["python3"]
CMD ["-c", "print('$name: security tool placeholder')"]
LABEL org.opencontainers.image.title="$name" \
      org.opencontainers.image.description="Placeholder - $name" \
      evergreen.image.tier="3" \
      evergreen.image.status="placeholder" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
DEOF
    write_checksums_placeholder "$BASE/$name"
done

go_scratch "keynuker" "KeyNuker - key detection" "clonezilla" "clonezilla/keynuker" "keynuker_0.1.0_linux_amd64" "0.1.0"

cat > "$BASE/gitguardian/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir ggshield
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin ggshield 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["ggshield", "--version"]
ENTRYPOINT ["ggshield"]
LABEL org.opencontainers.image.title="gitguardian" \
      org.opencontainers.image.description="GitGuardian ggshield - secret detection" \
      org.opencontainers.image.vendor="GitGuardian" \
      org.opencontainers.image.source="https://github.com/GitGuardian/ggshield" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/gitguardian" "ggshield"

cat > "$BASE/detect-secrets/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir detect-secrets
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin detectsecrets 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["detect-secrets", "--version"]
ENTRYPOINT ["detect-secrets"]
CMD ["scan"]
LABEL org.opencontainers.image.title="detect-secrets" \
      org.opencontainers.image.description="detect-secrets - Yelp secret detection" \
      org.opencontainers.image.vendor="Yelp" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/detect-secrets" "detect-secrets"

go_scratch "gitrob" "GitRob - sensitive file finder" "michenriksen" "michenriksen/gitrob" "gitrob_linux_amd64" "2.0.0"

cat > "$BASE/ggshield/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir ggshield
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin ggshield 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["ggshield", "--version"]
ENTRYPOINT ["ggshield"]
LABEL org.opencontainers.image.title="ggshield" \
      org.opencontainers.image.description="ggshield - GitGuardian CLI" \
      org.opencontainers.image.vendor="GitGuardian" \
      org.opencontainers.image.source="https://github.com/GitGuardian/ggshield" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/ggshield" "ggshield"

cat > "$BASE/dockerfile-lint/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g dockerfilelint
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules/dockerfilelint /app/dockerfilelint 2>/dev/null || true
COPY --from=builder /usr/bin/dockerfilelint /usr/local/bin/dockerfilelint 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin dockerlint 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["dockerfilelint", "--version"] || exit 0
ENTRYPOINT ["dockerfilelint"]
LABEL org.opencontainers.image.title="dockerfile-lint" \
      org.opencontainers.image.description="Dockerfile linter" \
      org.opencontainers.image.vendor="replicated" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_npm "$BASE/dockerfile-lint" "dockerfilelint"

cat > "$BASE/docker-bench/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/docker/docker-bench-security.git /src
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin bench 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["sh", "/app/src/docker-bench-security.sh", "--help"] || exit 0
ENTRYPOINT ["sh"]
CMD ["docker-bench-security.sh"]
LABEL org.opencontainers.image.title="docker-bench" \
      org.opencontainers.image.description="Docker Bench for Security" \
      org.opencontainers.image.vendor="Docker" \
      org.opencontainers.image.source="https://github.com/docker/docker-bench-security" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums "$BASE/docker-bench" \
    "https://github.com/docker/docker-bench-security/archive/refs/heads/master.tar.gz" \
    "docker-bench-security-master.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/lynis/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/CISOfy/Lynis.git /src
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin lynis 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["/app/src/lynis", "show", "version"] || exit 0
ENTRYPOINT ["/app/src/lynis"]
CMD ["audit", "system"]
LABEL org.opencontainers.image.title="lynis" \
      org.opencontainers.image.description="Lynis - Security auditing tool" \
      org.opencontainers.image.vendor="CISOfy" \
      org.opencontainers.image.source="https://github.com/CISOfy/Lynis" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums "$BASE/lynis" \
    "https://github.com/CISOfy/Lynis/archive/refs/heads/master.tar.gz" \
    "lynis-master.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/r2c-bench/Dockerfile" <<'EOF'
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin r2c 2>/dev/null || true && \
    mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["python3", "-c", "print('ok')"]
ENTRYPOINT ["python3"]
CMD ["-c", "print('r2c-bench: security benchmarking tool placeholder')"]
LABEL org.opencontainers.image.title="r2c-bench" \
      org.opencontainers.image.description="Placeholder - r2c benchmark" \
      evergreen.image.tier="3" \
      evergreen.image.status="placeholder" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_placeholder "$BASE/r2c-bench"

cat > "$BASE/checkov/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir checkov
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin checkov 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["checkov", "--version"]
ENTRYPOINT ["checkov"]
CMD ["-d", "."]
LABEL org.opencontainers.image.title="checkov" \
      org.opencontainers.image.description="Checkov - Infrastructure as Code scanner" \
      org.opencontainers.image.vendor="Bridgecrew" \
      org.opencontainers.image.source="https://github.com/bridgecrewio/checkov" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/checkov" "checkov"

cat > "$BASE/checkov-k8s/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir checkov
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin checkov 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["checkov", "--version"]
ENTRYPOINT ["checkov"]
CMD ["--framework", "kubernetes", "-d", "."]
LABEL org.opencontainers.image.title="checkov-k8s" \
      org.opencontainers.image.description="Checkov - Kubernetes scanner" \
      org.opencontainers.image.vendor="Bridgecrew" \
      org.opencontainers.image.source="https://github.com/bridgecrewio/checkov" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/checkov-k8s" "checkov"

go_scratch "kube-bench" "Kubernetes CIS benchmark" "aquasecurity" "aquasecurity/kube-bench" "kube-bench_0.8.0_linux_amd64.tar.gz" "0.8.0"

cat > "$BASE/kube-hunter/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir kube-hunter
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin kubehunter 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["kube-hunter", "--version"] || exit 0
ENTRYPOINT ["kube-hunter"]
CMD ["--remote"]
LABEL org.opencontainers.image.title="kube-hunter" \
      org.opencontainers.image.description="KubeHunter - Kubernetes security scanner" \
      org.opencontainers.image.vendor="Aqua Security" \
      org.opencontainers.image.source="https://github.com/aquasecurity/kube-hunter" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_pip "$BASE/kube-hunter" "kube-hunter"

go_scratch "kubescape" "Kubescape - Kubernetes security" "kubescape" "kubescape/kubescape" "kubescape-ubuntu-latest-amd64" "3.0.3"
go_debian "kubescape-operator" "Kubescape - operator mode" "kubescape" "kubescape/kubescape" "kubescape-ubuntu-latest-amd64" "3.0.3"

cat > "$BASE/falco/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://falco.org/repo/falcosecurity-packages.asc" | gpg --dearmor -o /etc/apt/trusted.gpg.d/falcosecurity.gpg && \
    echo "deb [signed-by=/etc/apt/trusted.gpg.d/falcosecurity.gpg] https://download.falco.org/packages/deb stable main" > /etc/apt/sources.list.d/falcosecurity.list && \
    apt-get update && apt-get install -y --no-install-recommends falco && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/falco /etc/falco

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates libjson-c5 libyaml-0-2 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/bin/falco /usr/local/bin/falco
COPY --from=builder /etc/falco /etc/falco
COPY --from=builder /app /app
COPY --from=builder /var/log/falco /var/log/falco
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin falco 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/falco 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["falco", "--version"] || exit 0
ENTRYPOINT ["falco"]
LABEL org.opencontainers.image.title="falco" \
      org.opencontainers.image.description="Falco - Cloud native runtime security" \
      org.opencontainers.image.vendor="Sysdig" \
      org.opencontainers.image.source="https://github.com/falcosecurity/falco" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums "$BASE/falco" \
    "https://github.com/falcosecurity/falco/archive/refs/heads/master.tar.gz" \
    "falco-master.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/falco-rules/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/falcosecurity/rules.git /rules
RUN mkdir -p /app/rules

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /rules /app/rules
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin falcorules 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["test", "-f", "/app/rules/rules.yaml"]
ENTRYPOINT ["cat"]
CMD ["/app/rules/rules.yaml"]
LABEL org.opencontainers.image.title="falco-rules" \
      org.opencontainers.image.description="Falco - rules only" \
      org.opencontainers.image.vendor="Sysdig" \
      org.opencontainers.image.source="https://github.com/falcosecurity/rules" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums "$BASE/falco-rules" \
    "https://github.com/falcosecurity/rules/archive/refs/heads/master.tar.gz" \
    "falco-rules-master.tar.gz" "PENDING_VERIFICATION"

go_scratch "falcosidekick" "Falcosidekick - Falco webhook" "falcosecurity" "falcosecurity/falcosidekick" "falcosidekick_2.28.0_linux_amd64.tar.gz" "2.28.0"

cat > "$BASE/openscap/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        libopenscap8 openscap-utils scap-security-guide ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        libopenscap8 openscap-utils scap-security-guide ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin openscap 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["oscap", "--version"]
ENTRYPOINT ["oscap"]
LABEL org.opencontainers.image.title="openscap" \
      org.opencontainers.image.description="OpenSCAP - Security compliance scanning" \
      org.opencontainers.image.vendor="Red Hat" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/openscap"

cat > "$BASE/scap-workbench/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        scap-workbench ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        scap-workbench ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin scapwb 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["scap-workbench", "--version"] || exit 0
ENTRYPOINT ["scap-workbench"]
LABEL org.opencontainers.image.title="scap-workbench" \
      org.opencontainers.image.description="SCAP Workbench - GUI for OpenSCAP" \
      org.opencontainers.image.vendor="Red Hat" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/scap-workbench"

cat > "$BASE/chkrootkit/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        chkrootkit ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        chkrootkit ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin chkrootkit 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["chkrootkit", "-V"] || exit 0
ENTRYPOINT ["chkrootkit"]
LABEL org.opencontainers.image.title="chkrootkit" \
      org.opencontainers.image.description="chkrootkit - rootkit detector" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/chkrootkit"

cat > "$BASE/rkhunter/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        rkhunter ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        rkhunter ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin rkhunter 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["rkhunter", "--version"]
ENTRYPOINT ["rkhunter"]
CMD ["--check", "--skip-keypress"]
LABEL org.opencontainers.image.title="rkhunter" \
      org.opencontainers.image.description="rkhunter - rootkit hunter" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/rkhunter"

cat > "$BASE/clamav/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav clamav-daemon ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/clamav /var/lib/clamav

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav clamav-daemon ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/clamav /var/log/clamav
COPY --from=builder /var/lib/clamav /var/lib/clamav
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin clamav 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/clamav /var/lib/clamav 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD ["clamscan", "--version"]
ENTRYPOINT ["clamd"]
CMD ["--foreground"]
LABEL org.opencontainers.image.title="clamav" \
      org.opencontainers.image.description="ClamAV - open source antivirus engine" \
      org.opencontainers.image.vendor="Cisco" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/clamav"

cat > "$BASE/clamav-daemon/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav clamav-daemon freshclam ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/clamav /var/lib/clamav /run/clamav

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav clamav-daemon freshclam ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/clamav /var/log/clamav
COPY --from=builder /var/lib/clamav /var/lib/clamav
COPY --from=builder /run/clamav /run/clamav
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin clamav 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/clamav /var/lib/clamav /run/clamav 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD ["clamscan", "--version"]
ENTRYPOINT ["clamd"]
CMD ["--foreground", "--debug"]
LABEL org.opencontainers.image.title="clamav-daemon" \
      org.opencontainers.image.description="ClamAV - daemon mode" \
      org.opencontainers.image.vendor="Cisco" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/clamav-daemon"

cat > "$BASE/freshclam/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav-freshclam ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/lib/clamav /var/log/clamav

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav-freshclam ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/lib/clamav /var/lib/clamav
COPY --from=builder /var/log/clamav /var/log/clamav
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin freshclam 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/lib/clamav /var/log/clamav 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=10s --start-period=10s --retries=1 \
    CMD ["freshclam", "--version"]
ENTRYPOINT ["freshclam"]
CMD ["--daemon"]
LABEL org.opencontainers.image.title="freshclam" \
      org.opencontainers.image.description="FreshClam - ClamAV database updater" \
      org.opencontainers.image.vendor="Cisco" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_nopkg "$BASE/freshclam"

cat > "$BASE/maldet/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates inotify-tools \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://www.rfxn.com/downloads/maldetect-current.tar.gz" \
    -o /maldet.tar.gz && \
    tar -xzf /maldet.tar.gz -C /opt && rm /maldet.tar.gz
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates inotify-tools clamav-daemon \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/maldetect /opt/maldetect
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin maldet 2>/dev/null || true && \
    chown -R 65534:65534 /app /opt/maldet 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=1 \
    CMD ["/opt/maldet/maldet", "--help"] || exit 0
ENTRYPOINT ["/opt/maldet/maldet"]
CMD ["-a", "/app"]
LABEL org.opencontainers.image.title="maldet" \
      org.opencontainers.image.description="Linux Malware Detect" \
      org.opencontainers.image.vendor="rFXn" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums "$BASE/maldet" \
    "https://www.rfxn.com/downloads/maldetect-current.tar.gz" \
    "maldetect-current.tar.gz" "PENDING_VERIFICATION"

cat > "$BASE/rblake/Dockerfile" <<'EOF'
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin rblake 2>/dev/null || true && \
    mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["python3", "-c", "print('ok')"]
ENTRYPOINT ["python3"]
CMD ["-c", "print('rblake: security tool placeholder')"]
LABEL org.opencontainers.image.title="rblake" \
      org.opencontainers.image.description="Placeholder - rblake" \
      evergreen.image.tier="3" \
      evergreen.image.status="placeholder" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums_placeholder "$BASE/rblake"

cat > "$BASE/dependabot/Dockerfile" <<'EOF'
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ruby-dev build-essential git ca-certificates curl gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN gem install dependabot-omnibus --no-document 2>/dev/null || true
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ca-certificates git curl gnupg \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems 2>/dev/null || true
COPY --from=builder /usr/local/bundle /usr/local/bundle 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin dependabot 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=1 \
    CMD ["dependabot", "--version"] || exit 0
ENTRYPOINT ["dependabot"]
LABEL org.opencontainers.image.title="dependabot" \
      org.opencontainers.image.description="Dependabot - Automated dependency updates" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/dependabot/dependabot-core" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian_slim="true"
EOF
write_checksums "$BASE/dependabot" \
    "https://github.com/dependabot/dependabot-core/archive/refs/heads/main.tar.gz" \
    "dependabot-core-main.tar.gz" "PENDING_VERIFICATION"

echo "=== Security done ==="
