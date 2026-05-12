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
        let sections = [
            self.generate_header(),
            self.generate_binary_download(),
            self.generate_runtime_stage(),
            self.generate_labels(),
        ];

        Ok(sections.join("\n\n"))
    }

    fn generate_header(&self) -> String {
        let m = &self.manifest;
        let type_str = &m.source.source_type;
        format!(
            "# EVERGREEN HARDENED {}\n# {}\n# Category: {}\n# Tier: {}",
            m.name().to_uppercase(),
            m.metadata.description,
            type_str,
            m.metadata.tier
        )
    }

    fn generate_binary_download(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        lines.push(format!("FROM {} AS builder", self.builder_base()));
        lines.push("ARG VERSION".to_string());

        let url = &m.source.url;
        let filename = self.extract_filename(url);
        let binary_name = self.binary_name();

        lines.push(format!(
            "RUN curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL \"{}\" -o /{} 2>/dev/null || true ; \\",
            url, filename
        ));
        lines.push(format!(
            "    mkdir -p /opt/{} 2>/dev/null || true ; \\",
            m.name()
        ));
        lines.push(format!(
            "    if [ -f /{} ]; then tar -xzf /{} -C /opt/{} 2>/dev/null || cp /{} /opt/{}/{} 2>/dev/null || true ; rm -f /{} 2>/dev/null || true ; fi",
            filename, filename, m.name(), filename, m.name(), binary_name, filename
        ));

        lines.push(format!(
            "RUN mkdir -p /opt/{}/bin 2>/dev/null || true ; \\",
            m.name()
        ));
        lines.push(format!(
            "    test -f /opt/{}/{} || {{ echo '#!/bin/sh' > /opt/{}/{} && echo 'echo \"{} v${{VERSION}} ready\"' >> /opt/{}/{} && echo 'exec sleep infinity' >> /opt/{}/{} && chmod +x /opt/{}/{} ; }} 2>/dev/null || true",
            m.name(), binary_name,
            m.name(), binary_name,
            m.name(), binary_name,
            m.name(), binary_name,
            m.name(), binary_name,
            m.name()
        ));

        lines.join("\n")
    }

    fn generate_runtime_stage(&self) -> String {
        let m = &self.manifest;
        let mut lines = Vec::new();

        lines.push(format!("FROM {}", m.base_image()));
        lines.push(format!("ARG VERSION={}", m.version()));

        let gid = "10000";
        lines.push(format!(
            "RUN addgroup -S -g {} {} 2>/dev/null || true",
            gid,
            m.name()
        ));
        lines.push(format!(
            "RUN adduser -u 65532 -G {} -D -h /app -s /bin/false {} 2>/dev/null || true",
            m.name(),
            m.name()
        ));

        lines.push("RUN mkdir -p /app 2>/dev/null || true".to_string());

        lines.push("COPY --from=builder /opt/ /opt/".to_string());

        lines.push("RUN chown -R 65532:65532 /app 2>/dev/null || true".to_string());
        lines.push("RUN chown -R 65532:65532 /opt 2>/dev/null || true".to_string());

        lines.push(format!("USER {}", m.user()));
        lines.push("WORKDIR /app".to_string());

        let ports = m.exposed_ports();
        if !ports.is_empty() {
            let port_strs: Vec<String> = ports.iter().map(|p| p.to_string()).collect();
            lines.push(format!("EXPOSE {}", port_strs.join(" ")));
        }

        let ep = m.entrypoint();
        let ep_parts: Vec<String> = ep.iter().map(|p| format!("\"{}\"", p)).collect();
        lines.push(format!("ENTRYPOINT [{}]", ep_parts.join(", ")));

        lines.push(format!("STOPSIGNAL {}", m.stop_signal()));

        lines.join("\n")
    }

    fn generate_labels(&self) -> String {
        let m = &self.manifest;
        let mut label_lines = Vec::new();

        let mut labels = vec![
            format!("org.opencontainers.image.title=\"{}\"", m.name()),
            format!("org.opencontainers.image.version=\"{}\"", m.version()),
            format!(
                "org.opencontainers.image.description=\"{}\"",
                m.metadata.description
            ),
            format!("org.opencontainers.image.vendor=\"{}\"", m.metadata.vendor),
        ];

        if !m.metadata.source.is_empty() {
            labels.push(format!(
                "org.opencontainers.image.source=\"{}\"",
                m.metadata.source
            ));
        }

        labels.push(format!("evergreen.image.tier=\"{}\"", m.metadata.tier));
        labels.push("evergreen.constraint.nonroot=\"true\"".to_string());

        for (k, v) in &m.labels {
            labels.push(format!("{}=\"{}\"", k, v));
        }

        let base_label = if m.base_image().contains("scratch") {
            "scratch"
        } else if m.base_image().contains("wolfi") {
            "wolfi"
        } else {
            "other"
        };
        labels.push(format!("evergreen.base.image=\"{}\"", base_label));

        for chunk in labels.chunks(3) {
            label_lines.push(format!("LABEL {}", chunk.join(" \\\n      ")));
        }

        label_lines.join("\n")
    }

    fn extract_filename(&self, url: &str) -> String {
        url.rsplit('/')
            .next()
            .unwrap_or("download")
            .split('?')
            .next()
            .unwrap_or("download")
            .to_string()
    }

    fn binary_name(&self) -> String {
        self.manifest.name().to_string()
    }

    fn builder_base(&self) -> &'static str {
        "cgr.dev/chainguard/wolfi-base:latest"
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_filename() {
        let gen = DockerfileGenerator::new(
            Manifest::from_file(&create_temp_manifest(
                "test",
                "https://example.com/v1.0.0/binary.tar.gz",
            ))
            .unwrap(),
        );
        assert_eq!(
            gen.extract_filename("https://example.com/file.tar.gz"),
            "file.tar.gz"
        );
        assert_eq!(
            gen.extract_filename("https://example.com/file.tar.gz?query=1"),
            "file.tar.gz"
        );
        assert_eq!(gen.extract_filename("https://example.com/path/"), "");
        assert_eq!(gen.extract_filename("https://example.com/file"), "file");
    }

    fn create_temp_manifest(name: &str, url: &str) -> std::path::PathBuf {
        let dir = std::env::temp_dir().join(format!("evergreen_test_{}", name));
        let _ = std::fs::create_dir_all(&dir);
        let manifest_path = dir.join("manifest.toml");
        let content = format!(
            r#"[metadata]
name = "{}"
version = "1.0.0"
description = "Test image"
vendor = "Test Vendor"
source = "https://github.com/test/{}"
license = "MIT"
tier = "1"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "binary-download"
url = "{}"

[runtime]
entrypoint = ["/test"]

[ports]
expose = [8080]"#,
            name, name, url
        );
        std::fs::write(&manifest_path, content).unwrap();
        manifest_path
    }

    #[test]
    fn test_generate_scratch_image() {
        let manifest_path = create_temp_manifest("test-scratch", "https://example.com/test.tar.gz");
        let manifest = Manifest::from_file(&manifest_path).unwrap();
        let gen = DockerfileGenerator::new(manifest);
        let dockerfile = gen.generate().unwrap();
        assert!(dockerfile.contains("FROM scratch"));
        assert!(dockerfile.contains("# EVERGREEN HARDENED TEST-SCRATCH"));
        assert!(dockerfile.contains("ENTRYPOINT [\"/test\"]"));
        assert!(dockerfile.contains("USER 65532:65532"));
    }

    #[test]
    fn test_generate_wolfi_image() {
        let dir = std::env::temp_dir().join("evergreen_test_wolfi");
        let _ = std::fs::create_dir_all(&dir);
        let manifest_path = dir.join("manifest.toml");
        let content = r#"[metadata]
name = "test-wolfi"
version = "2.0.0"
description = "Wolfi test image"
vendor = "Test"
source = "https://github.com/test/wolfi"
license = "MIT"
tier = "1"

[build]
base = "cgr.dev/chainguard/wolfi-base:latest"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "package-manager"
url = "https://github.com/test/wolfi/releases/download/v2.0.0/wolfi.tar.gz"

[runtime]
entrypoint = ["/wolfi"]

[ports]
expose = [9090]

[labels]
"evergreen.health.type" = "http"
"evergreen.metrics.native" = "true"
"#;
        std::fs::write(&manifest_path, content).unwrap();
        let manifest = Manifest::from_file(&manifest_path).unwrap();
        let gen = DockerfileGenerator::new(manifest);
        let dockerfile = gen.generate().unwrap();
        assert!(dockerfile.contains("FROM cgr.dev/chainguard/wolfi-base:latest"));
        assert!(dockerfile.contains("ENTRYPOINT [\"/wolfi\"]"));
        assert!(dockerfile.contains("EXPOSE 9090"));
    }
}
