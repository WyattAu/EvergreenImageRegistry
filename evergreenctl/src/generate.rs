use crate::manifest::*;
use anyhow::{Context, Result};
use std::path::Path;

const SHIM_VERSION: &str = "v2.0.0";
const DEFAULT_BUILDER_BASE: &str = "debian:bookworm-slim";
const WOLFI_BASE: &str = "cgr.dev/chainguard/wolfi-base:latest";
const SHIM_IMAGE: &str = "ghcr.io/wyattau/evergreenshim/health-shim";

pub fn cmd_generate(image_dir: &str) -> Result<()> {
    let dir = Path::new(image_dir);
    let manifest_path = dir.join("manifest.toml");
    let manifest = Manifest::from_file(&manifest_path)
        .with_context(|| format!("Failed to read manifest from {}", manifest_path.display()))?;
    let gen = DockerfileGenerator::new(manifest);
    let dockerfile = gen.generate()?;
    println!("{}", dockerfile);
    Ok(())
}

pub struct DockerfileGenerator {
    manifest: Manifest,
}

impl DockerfileGenerator {
    pub fn new(manifest: Manifest) -> Self {
        Self { manifest }
    }

    pub fn generate(&self) -> Result<String> {
        let m = &self.manifest;
        let build_type = m.source.source_type.as_str();

        let dockerfile = match build_type {
            "binary-download" => self.generate_binary_download(),
            "chainguard-repack" => self.generate_chainguard_repack(),
            "source-build" => self.generate_source_build(),
            "pkg-install" => self.generate_pkg_install(),
            "upstream-repack" | "repack" => self.generate_upstream_repack(),
            _ => self.generate_upstream_repack(), // default
        };

        Ok(dockerfile)
    }

    // ===================================================================
    // Pattern 1: Binary Download → scratch
    // For: Go/Rust static binaries (prometheus, traefik, grafana, etc.)
    // ===================================================================
    fn generate_binary_download(&self) -> String {
        let m = &self.manifest;
        let mut s = String::new();

        // Header
        s.push_str(&self.header());

        // Build args
        s.push_str(&format!(
            "ARG VERSION={}\nARG SHIM_VERSION={}\nARG TARGETARCH\n\n",
            m.version(),
            SHIM_VERSION
        ));

        // Downloader stage
        s.push_str(&format!("FROM {} AS downloader\n", DEFAULT_BUILDER_BASE));
        s.push_str("ARG VERSION\nARG TARGETARCH\n");
        s.push_str(
            "RUN apt-get update && apt-get install -y --no-install-recommends \\\
             \x20   curl ca-certificates && \\\
             \x20   rm -rf /var/lib/apt/lists/*\n\n",
        );

        // Download logic — supports tar.gz, zip, and raw binaries
        let url = &m.source.url;
        s.push_str(&format!(
            "RUN arch=$(case ${{TARGETARCH}} in \\\
             \x20   amd64) echo \"amd64\";; \\\
             \x20   arm64) echo \"arm64\";; \\\
             \x20   s390x) echo \"s390x\";; \\\
             \x20   ppc64le) echo \"ppc64le\";; \\\
             \x20   *) echo \"amd64\";; \\\
             \x20   esac) && \\\
             \x20   curl -fsSL \"{url}\" -o /tmp/download && \\\
             \x20   chmod +x /tmp/download || \\\
             \x20   (curl -fsSL \"{url}\" -o /tmp/download.tar.gz && \\\
             \x20    tar -xzf /tmp/download.tar.gz -C /tmp && \\\
             \x20    chmod +x /tmp/{name}) || \\\
             \x20   (apt-get update && apt-get install -y unzip && \\\
             \x20    curl -fsSL \"{url}\" -o /tmp/download.zip && \\\
             \x20    unzip /tmp/download.zip -d /tmp && \\\
             \x20    chmod +x /tmp/{name})\n\n",
            url = url,
            name = m.name()
        ));

        // CA certs
        s.push_str("RUN cp /etc/ssl/certs/ca-certificates.crt /ca-certificates.crt\n\n");

        // Shim stage
        s.push_str(&format!(
            "FROM {}:${{SHIM_VERSION}} AS shim\n\n",
            SHIM_IMAGE
        ));

        // Final stage — scratch
        s.push_str("FROM scratch\n");
        s.push_str("COPY --from=shim /shim /usr/local/bin/shim\n");
        s.push_str("COPY --from=downloader /tmp/download /usr/local/bin/");
        s.push_str(m.name());
        s.push('\n');
        s.push_str(
            "COPY --from=downloader /ca-certificates.crt /etc/ssl/certs/ca-certificates.crt\n\n",
        );

        // User, env, expose
        s.push_str(&self.user_env_expose());

        // Healthcheck + entrypoint
        s.push_str(&self.healthcheck());
        s.push_str(&self.entrypoint_with_shim());

        // Labels
        s.push_str(&self.labels());

        s
    }

    // ===================================================================
    // Pattern 2: Chainguard Repack
    // For: Complex apps with Chainguard equivalents (postgres, mariadb)
    // ===================================================================
    fn generate_chainguard_repack(&self) -> String {
        let m = &self.manifest;
        let mut s = String::new();

        s.push_str(&self.header());
        s.push_str(&format!("ARG SHIM_VERSION={}\n\n", SHIM_VERSION));

        // Shim stage
        s.push_str(&format!(
            "FROM {}:${{SHIM_VERSION}} AS shim\n\n",
            SHIM_IMAGE
        ));

        // Final stage — from Chainguard
        s.push_str(&format!("FROM {}\n", m.base_image()));
        s.push_str("USER 0\n");
        s.push_str("COPY --from=shim /shim /usr/local/bin/shim\n");

        // Fix ownership for non-root
        let uid = self.extract_uid();
        s.push_str(&format!(
            "RUN chown -R {}:{} /var/lib/{} 2>/dev/null || true\n",
            uid,
            uid,
            m.name()
        ));

        // Env + expose (now includes USER)
        s.push_str(&self.user_env_expose());

        // Healthcheck (TCP check — Chainguard inherits upstream entrypoint)
        s.push_str(&self.healthcheck_tcp_only());

        // Labels with chainguard-repack exemption
        s.push_str(&self.labels_with_exemption("chainguard-repack"));

        s
    }

    // ===================================================================
    // Pattern 3: Source Build → scratch
    // For: C/C++ apps with static linking (redis, sqlite)
    // ===================================================================
    fn generate_source_build(&self) -> String {
        let m = &self.manifest;
        let mut s = String::new();

        s.push_str(&self.header());
        s.push_str(&format!(
            "ARG VERSION={}\nARG SHIM_VERSION={}\n\n",
            m.version(),
            SHIM_VERSION
        ));

        // Builder stage
        s.push_str("FROM rust:bookworm AS builder\n");
        s.push_str("ARG VERSION\n");
        s.push_str(&format!(
            "RUN curl -fsSL \"{url}\" -o /tmp/src.tar.gz && \\\
             \x20   tar -xzf /tmp/src.tar.gz -C /tmp && \\\
             \x20   cd /tmp/*{name}* && \\\
             \x20   cargo build --release && \\\
             \x20   cp target/release/{name} /{name}\n\n",
            url = m.source.url,
            name = m.name()
        ));

        // Shim stage
        s.push_str(&format!(
            "FROM {}:${{SHIM_VERSION}} AS shim\n\n",
            SHIM_IMAGE
        ));

        // Final stage
        s.push_str("FROM scratch\n");
        s.push_str("COPY --from=shim /shim /usr/local/bin/shim\n");
        s.push_str(&format!(
            "COPY --from=builder /{} /usr/local/bin/{}\n\n",
            m.name(),
            m.name()
        ));

        s.push_str(&self.user_env_expose());
        s.push_str(&self.healthcheck());
        s.push_str(&self.entrypoint_with_shim());
        s.push_str(&self.labels());

        s
    }

    // ===================================================================
    // Pattern 4: Package Install (wolfi-base + apk)
    // For: Apps needing shared libs but minimal base (nginx, dns)
    // ===================================================================
    fn generate_pkg_install(&self) -> String {
        let m = &self.manifest;
        let mut s = String::new();

        s.push_str(&self.header());
        s.push_str(&format!("ARG SHIM_VERSION={}\n\n", SHIM_VERSION));

        // Shim stage
        s.push_str(&format!(
            "FROM {}:${{SHIM_VERSION}} AS shim\n\n",
            SHIM_IMAGE
        ));

        // Final stage — wolfi-base with packages
        s.push_str(&format!("FROM {}\n", WOLFI_BASE));
        s.push_str("RUN apk add --no-cache ");
        s.push_str(m.name());
        s.push_str(" ca-certificates && \\\n");
        s.push_str(&format!(
            "    mkdir -p /var/lib/{} /var/log/{} /var/run/{} && \\\
             \x20   chown -R 65532:65532 /var/lib/{} /var/log/{} /var/run/{}\n\n",
            m.name(),
            m.name(),
            m.name(),
            m.name(),
            m.name(),
            m.name()
        ));

        s.push_str("COPY --from=shim /shim /usr/local/bin/shim\n");

        s.push_str(&self.user_env_expose());
        s.push_str(&self.healthcheck());
        s.push_str(&self.entrypoint_with_shim());
        s.push_str(&self.labels());

        s
    }

    // ===================================================================
    // Pattern 5: Upstream Repack (FROM upstream + shim)
    // For: Apps without binary download or Chainguard equivalent
    // ===================================================================
    fn generate_upstream_repack(&self) -> String {
        let m = &self.manifest;
        let mut s = String::new();

        s.push_str(&self.header());
        s.push_str(&format!("ARG SHIM_VERSION={}\n\n", SHIM_VERSION));

        // Shim stage
        s.push_str(&format!(
            "FROM {}:${{SHIM_VERSION}} AS shim\n\n",
            SHIM_IMAGE
        ));

        // Final stage — upstream
        let upstream = m.source.url.as_str();
        let base = if upstream.contains("://") {
            // URL means it's a download source, use base_image instead
            m.base_image()
        } else {
            upstream
        };

        s.push_str(&format!("FROM {}\n", base));
        s.push_str("USER 0\n");
        s.push_str("COPY --from=shim /shim /usr/local/bin/shim\n");

        // Fix ownership for non-root
        let uid = self.extract_uid();
        if uid != "0" {
            s.push_str(&format!(
                "RUN chown -R {}:{} /var/lib/{} 2>/dev/null || true\n",
                uid,
                uid,
                m.name()
            ));
        }

        // Env + expose (now includes USER)
        s.push_str(&self.user_env_expose());
        s.push_str(&self.healthcheck_tcp_only());
        s.push_str(&self.labels_with_exemption("repack-upstream-init"));

        s
    }

    // ===================================================================
    // Helper methods
    // ===================================================================

    fn header(&self) -> String {
        let m = &self.manifest;
        format!(
            "# EVERGREEN HARDENED {}\n\
             # {}\n\
             # Source Type: {}\n\
             # Tier: {}\n\
             # Auto-generated by evergreenctl generate\n\n",
            m.name().to_uppercase(),
            m.metadata.description,
            m.source.source_type,
            m.metadata.tier
        )
    }

    fn user_env_expose(&self) -> String {
        let m = &self.manifest;
        let mut s = String::new();

        // Non-root user
        let user = m.user();
        if !user.is_empty() {
            s.push_str(&format!("USER {}\n\n", user));
        }

        // Environment
        s.push_str("ENV SHIM_METRICS_ENABLED=\"true\"\n");

        // Expose ports
        let ports = m.exposed_ports();
        if !ports.is_empty() {
            let port_strs: Vec<String> = ports.iter().map(|p| p.to_string()).collect();
            s.push_str(&format!("EXPOSE {}\n", port_strs.join(" ")));
        }
        s.push('\n');

        s
    }

    fn healthcheck(&self) -> String {
        let m = &self.manifest;
        let ports = m.exposed_ports();
        let primary_port = ports.first().map(|s| s.as_str()).unwrap_or("8080");

        format!(
            "HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \\\
             \x20 CMD [\"/usr/local/bin/shim\", \"healthcheck\", \"--tcp\", \"127.0.0.1:{}\"]\n\n",
            primary_port
        )
    }

    fn healthcheck_tcp_only(&self) -> String {
        // For repack images that inherit upstream ENTRYPOINT
        let m = &self.manifest;
        let ports = m.exposed_ports();
        let primary_port = ports.first().map(|s| s.as_str()).unwrap_or("8080");

        format!(
            "HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \\\
             \x20 CMD [\"/usr/local/bin/shim\", \"healthcheck\", \"--tcp\", \"127.0.0.1:{}\"]\n\n",
            primary_port
        )
    }

    fn entrypoint_with_shim(&self) -> String {
        let m = &self.manifest;
        let ep = m.entrypoint();
        if ep.is_empty() {
            return format!(
                "ENTRYPOINT [\"/usr/local/bin/shim\", \"run\", \"-c\", \"/usr/local/bin/{}\"]\n\n",
                m.name()
            );
        }

        // If entrypoint already includes shim, don't double-wrap
        let ep_str = ep
            .iter()
            .map(|p| format!("\"{}\"", p))
            .collect::<Vec<_>>()
            .join(", ");
        format!("ENTRYPOINT [{}]\n\n", ep_str)
    }

    fn labels(&self) -> String {
        self.labels_with_exemption("")
    }

    fn labels_with_exemption(&self, exemption: &str) -> String {
        let m = &self.manifest;
        let mut labels = vec![
            format!("org.opencontainers.image.title=\"{}\"", m.name()),
            format!("org.opencontainers.image.version=\"{}\"", m.version()),
            format!(
                "org.opencontainers.image.description=\"{}\"",
                m.metadata.description
            ),
            format!("evergreen.image.tier=\"{}\"", m.metadata.tier),
            "evergreen.constraint.nonroot=\"true\"".to_string(),
            "evergreen.security.cap-drop=\"ALL\"".to_string(),
            "evergreen.security.no-new-privileges=\"true\"".to_string(),
        ];

        let base = if m.base_image().contains("scratch") {
            "scratch"
        } else if m.base_image().contains("wolfi") || m.base_image().contains("chainguard") {
            "wolfi"
        } else {
            "upstream"
        };
        labels.push(format!("evergreen.base.image=\"{}\"", base));

        if !exemption.is_empty() {
            labels.push(format!("evergreen.entrypoint.pattern=\"{}\"", exemption));
        }

        // Include custom labels from the manifest [labels] section
        for (key, value) in &m.labels {
            labels.push(format!("{}=\"{}\"", key, value));
        }

        // Multi-label format (max 3 per line)
        let mut s = String::from("LABEL ");
        for (i, label) in labels.iter().enumerate() {
            if i > 0 {
                s.push_str(" \\\n      ");
            }
            s.push_str(label);
        }
        s.push_str("\n\nSTOPSIGNAL ");
        s.push_str(m.stop_signal());
        s.push('\n');

        s
    }

    fn extract_uid(&self) -> String {
        let user = self.manifest.user();
        if user.is_empty() {
            return "65532".to_string();
        }
        // Extract UID from "65532:65532" or "65532" or "1000"
        user.split(':').next().unwrap_or("65532").to_string()
    }
}
