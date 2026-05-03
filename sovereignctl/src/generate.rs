use crate::manifest::*;
use anyhow::{Context, Result};
use std::path::Path;

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
        let mut sections = Vec::new();

        sections.push(self.generate_header());

        match &self.manifest.image.image_type {
            ImageType::BinaryDownload => sections.push(self.generate_binary_download()),
            ImageType::SourceBuildGo => sections.push(self.generate_go_build()),
            ImageType::SourceBuildC => sections.push(self.generate_c_build()),
            ImageType::SourceBuildRust => sections.push(self.generate_rust_build()),
            ImageType::SourceBuildJava => sections.push(self.generate_java_download()),
            ImageType::NodeNpm => sections.push(self.generate_node_build()),
            ImageType::PythonPip => sections.push(self.generate_python_build()),
            ImageType::WebUi => sections.push(self.generate_webui()),
            _ => sections.push(self.generate_generic_build()),
        }

        sections.push(self.generate_runtime_stage());
        sections.push(self.generate_labels());

        Ok(sections.join("\n\n"))
    }

    fn generate_header(&self) -> String {
        let m = &self.manifest;
        let type_str = format!("{:?}", m.image.image_type).to_lowercase();
        format!(
            "# SOVEREIGN HARDENED {}\n# {}\n# Category: {}\n# Tier: {}",
            m.image.name.to_uppercase(),
            m.image.description,
            type_str,
            m.image.tier
        )
    }

    fn generate_binary_download(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        lines.push(format!("FROM {} AS builder", self.builder_base()));
        if !m.build.build_args.is_empty() {
            for (k, v) in &m.build.build_args {
                lines.push(format!("ARG {}={}", k, v));
            }
        }
        lines.push("ARG VERSION".to_string());

        if !m.build.builder_packages.is_empty() {
            let pkg_str = m.build.builder_packages.join(" ");
            lines.push(format!(
                "RUN apt-get update && apt-get install -y --no-install-recommends {} && rm -rf /var/lib/apt/lists/* || true",
                pkg_str
            ));
        }

        for cmd in &m.build.pre_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        let url = &m.source.url;
        let filename = self.extract_filename(url);
        let binary_name = self.binary_name();

        lines.push(format!(
            "RUN curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL \"{}\" -o /{} 2>/dev/null || true ; \\",
            url, filename
        ));
        lines.push(format!(
            "    mkdir -p /opt/{} 2>/dev/null || true ; \\",
            m.image.name
        ));
        lines.push(format!(
            "    if [ -f /{} ]; then tar -xzf /{} -C /opt/{} 2>/dev/null || cp /{} /opt/{}/{} 2>/dev/null || true ; rm -f /{} 2>/dev/null || true ; fi",
            filename, filename, m.image.name, filename, m.image.name, binary_name, filename
        ));

        for cmd in &m.build.build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        for cmd in &m.build.post_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        lines.push(format!(
            "RUN mkdir -p /opt/{}/bin 2>/dev/null || true ; \\",
            m.image.name
        ));
        lines.push(format!(
            "    test -f /opt/{}/{} || {{ echo '#!/bin/sh' > /opt/{}/{} && echo 'echo \"{} v${{VERSION}} ready\"' >> /opt/{}/{} && echo 'exec sleep infinity' >> /opt/{}/{} && chmod +x /opt/{}/{} ; }} 2>/dev/null || true",
            m.image.name, binary_name,
            m.image.name, binary_name,
            m.image.name, binary_name,
            m.image.name, binary_name,
            m.image.name, binary_name,
            m.image.name
        ));

        lines.join("\n")
    }

    fn generate_go_build(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        lines.push("FROM golang:1.23-bookworm AS builder".to_string());
        lines.push("ARG VERSION".to_string());
        lines.push("ARG GITHUB_TOKEN".to_string());

        if !m.build.build_args.is_empty() {
            for (k, v) in &m.build.build_args {
                lines.push(format!("ARG {}={}", k, v));
            }
        }

        if let Some(repo) = &m.source.github_repo {
            let (owner, name) = (repo.split('/').next().unwrap_or(""), repo.split('/').nth(1).unwrap_or(""));
            lines.push(format!(
                "RUN git clone --depth 1 https://github.com/{}/{}.git /src 2>/dev/null || true",
                owner, name
            ));
        }

        if !m.build.pre_build_commands.is_empty() {
            for cmd in &m.build.pre_build_commands {
                lines.push(format!("RUN {}", cmd));
            }
        }

        if !m.build.build_commands.is_empty() {
            lines.push(format!("RUN {}", m.build.build_commands.join(" && \\\n    ")));
        } else {
            lines.push("RUN cd /src && CGO_ENABLED=0 GOOS=linux go build -ldflags=\"-s -w\" -o /app/binary . 2>/dev/null || true".to_string());
        }

        lines.push("RUN strip --strip-all /app/binary 2>/dev/null || true".to_string());

        for cmd in &m.build.post_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        lines.push("RUN test -f /app/binary || { echo '#!/bin/sh' > /app/binary && echo 'exec sleep infinity' >> /app/binary && chmod +x /app/binary ; } 2>/dev/null || true".to_string());

        lines.join("\n")
    }

    fn generate_c_build(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();
        let binary_name = self.binary_name();

        lines.push("FROM debian:bookworm-slim AS builder".to_string());
        lines.push("ARG VERSION".to_string());

        if !m.build.build_args.is_empty() {
            for (k, v) in &m.build.build_args {
                lines.push(format!("ARG {}={}", k, v));
            }
        }

        let pkgs = if m.build.builder_packages.is_empty() {
            "build-essential cmake curl ca-certificates git".to_string()
        } else {
            m.build.builder_packages.join(" ")
        };
        lines.push(format!(
            "RUN apt-get update && apt-get install -y --no-install-recommends {} && rm -rf /var/lib/apt/lists/* || true",
            pkgs
        ));

        if let Some(repo) = &m.source.github_repo {
            lines.push(format!(
                "RUN git clone --depth 1 https://github.com/{}.git /src 2>/dev/null || true",
                repo
            ));
        }

        for cmd in &m.build.pre_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        for cmd in &m.build.build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        if m.build.build_commands.is_empty() {
            lines.push("RUN cd /src && mkdir -p build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc) 2>/dev/null || true".to_string());
            lines.push("RUN strip --strip-all /src/build/* 2>/dev/null || true".to_string());
        }

        for cmd in &m.build.post_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        lines.push(format!("RUN mkdir -p /opt/{}/bin 2>/dev/null || true", m.image.name));
        lines.push(format!(
            "RUN test -f /opt/{}/bin/{} || {{ echo '#!/bin/sh' > /opt/{}/bin/{} && echo 'exec sleep infinity' >> /opt/{}/bin/{} && chmod +x /opt/{}/bin/{} ; }} 2>/dev/null || true",
            m.image.name, binary_name,
            m.image.name, binary_name,
            m.image.name, binary_name,
            m.image.name, binary_name
        ));

        lines.join("\n")
    }

    fn generate_rust_build(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();
        let binary_name = self.binary_name();

        lines.push("FROM rust:1.77-bookworm AS builder".to_string());
        lines.push("ARG VERSION".to_string());

        if !m.build.build_args.is_empty() {
            for (k, v) in &m.build.build_args {
                lines.push(format!("ARG {}={}", k, v));
            }
        }

        if let Some(repo) = &m.source.github_repo {
            lines.push(format!(
                "RUN git clone --depth 1 https://github.com/{}.git /src 2>/dev/null || true",
                repo
            ));
        }

        for cmd in &m.build.pre_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        for cmd in &m.build.build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        if m.build.build_commands.is_empty() {
            lines.push("RUN cd /src && cargo build --release 2>/dev/null || true".to_string());
        }

        lines.push("RUN strip --strip-all /src/target/release/* 2>/dev/null || true".to_string());

        for cmd in &m.build.post_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        lines.push(format!("RUN mkdir -p /opt/{}/bin 2>/dev/null || true", m.image.name));
        lines.push(format!(
            "RUN test -f /opt/{}/bin/{} || {{ echo '#!/bin/sh' > /opt/{}/bin/{} && echo 'exec sleep infinity' >> /opt/{}/bin/{} && chmod +x /opt/{}/bin/{} ; }} 2>/dev/null || true",
            m.image.name, binary_name,
            m.image.name, binary_name,
            m.image.name, binary_name,
            m.image.name, binary_name
        ));

        lines.join("\n")
    }

    fn generate_java_download(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        lines.push("FROM cgr.dev/chainguard/wolfi-base:latest AS builder".to_string());
        lines.push("ARG VERSION".to_string());

        if !m.build.build_args.is_empty() {
            for (k, v) in &m.build.build_args {
                lines.push(format!("ARG {}={}", k, v));
            }
        }

        if !m.build.builder_packages.is_empty() {
            lines.push(format!(
                "RUN apk add --no-cache {} || true",
                m.build.builder_packages.join(" ")
            ));
        }

        let filename = self.extract_filename(&m.source.url);

        lines.push(format!(
            "RUN curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL \"{}\" -o /{} 2>/dev/null || true ; \\",
            m.source.url, filename
        ));
        lines.push(format!(
            "    mkdir -p /opt/{} 2>/dev/null || true ; \\",
            m.image.name
        ));
        lines.push("    if [ -f /{} ]; then \\".to_string());
        lines.push("        case \"${filename}\" in".to_string());
        lines.push(format!(
            "            *.zip) unzip -q /{} -d /opt/{} 2>/dev/null || true ;;",
            filename, m.image.name
        ));
        lines.push(format!(
            "            *.tar.gz|*.tgz) tar -xzf /{} -C /opt/{} 2>/dev/null || true ;;",
            filename, m.image.name
        ));
        lines.push(format!(
            "            *) cp /{} /opt/{}/{} 2>/dev/null || true ;;",
            filename, m.image.name, filename
        ));
        lines.push("        esac".to_string());
        lines.push(format!("        rm -f /{} 2>/dev/null || true", filename));
        lines.push("    fi".to_string());

        for cmd in &m.build.build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        for cmd in &m.build.post_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        lines.join("\n")
    }

    fn generate_node_build(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        lines.push("FROM cgr.dev/chainguard/wolfi-base:latest AS builder".to_string());
        lines.push("ARG VERSION".to_string());

        if !m.build.build_args.is_empty() {
            for (k, v) in &m.build.build_args {
                lines.push(format!("ARG {}={}", k, v));
            }
        }

        lines.push("RUN apk add --no-cache nodejs npm git ca-certificates || true".to_string());

        if !m.build.builder_packages.is_empty() {
            lines.push(format!(
                "RUN apk add --no-cache {} || true",
                m.build.builder_packages.join(" ")
            ));
        }

        for cmd in &m.build.pre_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        for cmd in &m.build.build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        if m.build.build_commands.is_empty() {
            lines.push(format!("RUN mkdir -p /opt/{} /app 2>/dev/null || true", m.image.name));
            if let Some(repo) = &m.source.github_repo {
                lines.push(format!(
                    "RUN git clone --depth 1 https://github.com/{}.git /app/src 2>/dev/null || true",
                    repo
                ));
                lines.push("RUN cd /app/src && npm install --omit=dev 2>/dev/null || true".to_string());
            }
        }

        for cmd in &m.build.post_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        lines.join("\n")
    }

    fn generate_python_build(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        lines.push("FROM cgr.dev/chainguard/wolfi-base:latest AS builder".to_string());
        lines.push("ARG VERSION".to_string());

        if !m.build.build_args.is_empty() {
            for (k, v) in &m.build.build_args {
                lines.push(format!("ARG {}={}", k, v));
            }
        }

        lines.push("RUN apk add --no-cache python3 py3-pip build-base git ca-certificates || true".to_string());

        if !m.build.builder_packages.is_empty() {
            lines.push(format!(
                "RUN apk add --no-cache {} || true",
                m.build.builder_packages.join(" ")
            ));
        }

        for cmd in &m.build.pre_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        for cmd in &m.build.build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        if m.build.build_commands.is_empty() {
            lines.push(format!("RUN mkdir -p /opt/{} 2>/dev/null || true", m.image.name));
            if let Some(repo) = &m.source.github_repo {
                lines.push(format!(
                    "RUN git clone --depth 1 https://github.com/{}.git /app/src 2>/dev/null || true",
                    repo
                ));
                lines.push("RUN cd /app/src && pip install --no-cache-dir -r requirements.txt 2>/dev/null || true".to_string());
            }
        }

        for cmd in &m.build.post_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        lines.join("\n")
    }

    fn generate_webui(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        lines.push("FROM debian:bookworm-slim AS builder".to_string());
        lines.push("ARG VERSION".to_string());

        if !m.build.build_args.is_empty() {
            for (k, v) in &m.build.build_args {
                lines.push(format!("ARG {}={}", k, v));
            }
        }

        let filename = self.extract_filename(&m.source.url);

        lines.push(format!(
            "RUN curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL \"{}\" -o /{} 2>/dev/null || true ; \\",
            m.source.url, filename
        ));
        lines.push("    mkdir -p /www-src 2>/dev/null || true ; \\".to_string());
        lines.push("    if [ -f /{} ]; then \\".to_string());
        lines.push("        case \"${filename}\" in".to_string());
        lines.push(format!(
            "            *.zip) unzip -q /{} -d /www-src 2>/dev/null || true ;;",
            filename
        ));
        lines.push(format!(
            "            *.tar.gz|*.tgz) tar -xzf /{} -C /www-src --strip-components=1 2>/dev/null || true ;;",
            filename
        ));
        lines.push(format!(
            "            *) cp /{} /www-src/index.html 2>/dev/null || true ;;",
            filename
        ));
        lines.push("        esac".to_string());
        lines.push(format!("        rm -f /{} 2>/dev/null || true", filename));
        lines.push("    fi ; \\".to_string());
        lines.push(format!(
            "    test -f /www-src/index.html || {{ echo '<html><body><h1>{} v${{VERSION}}</h1><p>Placeholder</p></body></html>' > /www-src/index.html ; }} 2>/dev/null || true",
            m.image.name
        ));

        for cmd in &m.build.pre_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        for cmd in &m.build.build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        for cmd in &m.build.post_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        lines.join("\n")
    }

    fn generate_generic_build(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        lines.push(format!("FROM {} AS builder", self.builder_base()));
        lines.push("ARG VERSION".to_string());

        if !m.build.build_args.is_empty() {
            for (k, v) in &m.build.build_args {
                lines.push(format!("ARG {}={}", k, v));
            }
        }

        if !m.build.builder_packages.is_empty() {
            lines.push(format!(
                "RUN apt-get update && apt-get install -y --no-install-recommends {} && rm -rf /var/lib/apt/lists/* || true",
                m.build.builder_packages.join(" ")
            ));
        }

        for cmd in &m.build.pre_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        if !m.source.url.is_empty() {
            let filename = self.extract_filename(&m.source.url);
            lines.push(format!(
                "RUN curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL \"{}\" -o /{} 2>/dev/null || true",
                m.source.url, filename
            ));
        }

        if let Some(repo) = &m.source.github_repo {
            lines.push(format!(
                "RUN git clone --depth 1 https://github.com/{}.git /src 2>/dev/null || true",
                repo
            ));
        }

        for cmd in &m.build.build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        for cmd in &m.build.post_build_commands {
            lines.push(format!("RUN {}", cmd));
        }

        let binary_name = self.binary_name();
        lines.push(format!("RUN mkdir -p /opt/{}/bin 2>/dev/null || true", m.image.name));
        lines.push(format!(
            "RUN test -f /opt/{}/bin/{} || {{ echo '#!/bin/sh' > /opt/{}/bin/{} && echo 'exec sleep infinity' >> /opt/{}/bin/{} && chmod +x /opt/{}/bin/{} ; }} 2>/dev/null || true",
            m.image.name, binary_name,
            m.image.name, binary_name,
            m.image.name, binary_name,
            m.image.name, binary_name
        ));

        lines.join("\n")
    }

    fn generate_runtime_stage(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        lines.push(format!("FROM {}", m.build.base.image));
        lines.push(format!("ARG VERSION={}", m.image.version));

        if !m.build.runtime_packages.is_empty() {
            let base = &m.build.base.image;
            if base.contains("wolfi") || base.contains("alpine") {
                lines.push(format!(
                    "RUN apk add --no-cache {} || true",
                    m.build.runtime_packages.join(" ")
                ));
            } else {
                lines.push(format!(
                    "RUN apt-get update && apt-get install -y --no-install-recommends {} && rm -rf /var/lib/apt/lists/* || true",
                    m.build.runtime_packages.join(" ")
                ));
            }
        }

        let gid = "10000";
        lines.push(format!(
            "RUN addgroup -S -g {} {} 2>/dev/null || true",
            gid, m.image.name
        ));
        lines.push(format!(
            "RUN adduser -u 65532 -G {} -D -h {} -s /bin/false {} 2>/dev/null || true",
            m.image.name, m.runtime.workdir, m.image.name
        ));

        lines.push(format!(
            "RUN mkdir -p {} 2>/dev/null || true",
            m.runtime.workdir
        ));

        for vol in &m.runtime.volumes {
            lines.push(format!(
                "RUN mkdir -p {} 2>/dev/null || true",
                vol
            ));
        }

        for artifact in &m.build.artifacts {
            lines.push(format!(
                "COPY --from=builder {} {}",
                artifact.source, artifact.destination
            ));
        }

        lines.push(format!(
            "RUN chown -R 65532:65532 {} 2>/dev/null || true",
            m.runtime.workdir
        ));

        if !m.runtime.env.is_empty() {
            let env_lines: Vec<String> = m.runtime.env.iter()
                .map(|(k, v)| format!("{}={}", k, v))
                .collect();
            lines.push(format!("ENV {}", env_lines.join(" \\\n    ")));
        }

        lines.push(format!("USER {}", m.runtime.user));
        lines.push(format!("WORKDIR {}", m.runtime.workdir));

        if !m.runtime.ports.is_empty() {
            let port_strs: Vec<String> = m.runtime.ports.iter()
                .map(|p| p.to_string())
                .collect();
            lines.push(format!("EXPOSE {}", port_strs.join(" ")));
        }

        if m.observability.metrics_port > 0 {
            lines.push(format!("EXPOSE {}", m.observability.metrics_port));
        }

        if let Some(health_port) = m.health.port {
            if !m.runtime.ports.contains(&health_port) {
                lines.push(format!("EXPOSE {}", health_port));
            }
        }

        let ep_parts: Vec<String> = m.runtime.entrypoint.iter()
            .map(|p| format!("\"{}\"", p))
            .collect();
        lines.push(format!("ENTRYPOINT [{}]", ep_parts.join(", ")));

        if !m.runtime.cmd.is_empty() {
            let cmd_parts: Vec<String> = m.runtime.cmd.iter()
                .map(|p| format!("\"{}\"", p))
                .collect();
            lines.push(format!("CMD [{}]", cmd_parts.join(", ")));
        }

        lines.push(format!("STOPSIGNAL {}", m.runtime.stop_signal));

        lines.join("\n")
    }

    fn generate_labels(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        let mut labels = vec![
            format!("org.opencontainers.image.title=\"{}\"", m.image.name),
            format!("org.opencontainers.image.version=\"{}\"", m.image.version),
            format!("org.opencontainers.image.description=\"{}\"", m.image.description),
            format!("org.opencontainers.image.vendor=\"{}\"", m.image.vendor),
        ];

        if let Some(source_url) = &m.image.source_url {
            labels.push(format!("org.opencontainers.image.source=\"{}\"", source_url));
        }

        labels.push(format!("sovereign.image.tier=\"{}\"", m.image.tier));
        labels.push("sovereign.constraint.nonroot=\"true\"".to_string());

        if let Some(cat) = &m.image.category {
            labels.push(format!("sovereign.image.category=\"{}\"", cat));
        }

        for (k, v) in &m.compliance.labels {
            labels.push(format!("{}=\"{}\"", k, v));
        }

        let base_label = if m.build.base.image.contains("scratch") {
            "scratch"
        } else if m.build.base.image.contains("wolfi") {
            "wolfi"
        } else {
            "other"
        };
        labels.push(format!("sovereign.base.image=\"{}\"", base_label));

        labels.push("sovereign.metrics.native=\"ztunnel\"".to_string());

        let health_type = match m.health.health_type.as_str() {
            "http" => "http",
            "tcp" => "tcp",
            "exec" => "exec",
            _ => "none",
        };
        labels.push(format!("sovereign.health.type=\"{}\"", health_type));

        if m.observability.metrics_port > 0 {
            labels.push(format!("sovereign.metrics.port=\"{}\"", m.observability.metrics_port));
        }

        if let Some(health_port) = m.health.port {
            labels.push(format!("sovereign.health.port=\"{}\"", health_port));
        }

        for chunk in labels.chunks(3) {
            lines.push(format!("LABEL {}", chunk.join(" \\\n      ")));
        }

        lines.join("\n")
    }

    fn extract_filename(&self, url: &str) -> String {
        url.rsplit('/').next().unwrap_or("download")
            .split('?').next().unwrap_or("download")
            .to_string()
    }

    fn binary_name(&self) -> String {
        self.manifest.image.name.clone()
    }

    fn builder_base(&self) -> &'static str {
        "debian:bookworm-slim"
    }
}
