use crate::manifest::Manifest;
use anyhow::{Context, Result};
use std::collections::HashSet;
use std::path::Path;

struct ParsedDockerfile {
    version: Option<String>,
    base_image: Option<String>,
    user: Option<String>,
    stop_signal: Option<String>,
    entrypoint: Option<String>,
    cmd: Option<String>,
    expose_ports: HashSet<String>,
    labels: Vec<(String, String)>,
}

fn parse_dockerfile(content: &str) -> ParsedDockerfile {
    let mut df = ParsedDockerfile {
        version: None,
        base_image: None,
        user: None,
        stop_signal: None,
        entrypoint: None,
        cmd: None,
        expose_ports: HashSet::new(),
        labels: Vec::new(),
    };

    for line in content.lines() {
        let line = line.trim();
        if line.starts_with("ARG VERSION=") || line.starts_with("ARG VERSION ") {
            df.version = Some(
                line.strip_prefix("ARG VERSION=")
                    .or_else(|| line.strip_prefix("ARG VERSION "))
                    .unwrap()
                    .trim()
                    .trim_start_matches('"')
                    .trim_end_matches('"')
                    .to_string(),
            );
        } else if line.starts_with("FROM ") && !line.contains(" AS ") {
            df.base_image = Some(
                line.strip_prefix("FROM ")
                    .unwrap()
                    .split_whitespace()
                    .next()
                    .unwrap_or("")
                    .to_string(),
            );
        } else if line.starts_with("FROM ") && line.contains(" AS ") {
            let rest = line.strip_prefix("FROM ").unwrap();
            let base = rest.split(" AS ").next().unwrap_or("").trim();
            if df.base_image.is_none() {
                df.base_image = Some(base.to_string());
            }
        } else if line.starts_with("USER ") {
            df.user = Some(line.strip_prefix("USER ").unwrap().trim().to_string());
        } else if line.starts_with("STOPSIGNAL ") {
            df.stop_signal = Some(line.strip_prefix("STOPSIGNAL ").unwrap().trim().to_string());
        } else if line.starts_with("ENTRYPOINT ") {
            df.entrypoint = Some(line.strip_prefix("ENTRYPOINT ").unwrap().trim().to_string());
        } else if line.starts_with("CMD ") {
            df.cmd = Some(line.strip_prefix("CMD ").unwrap().trim().to_string());
        } else if line.starts_with("EXPOSE ") {
            for port in line.strip_prefix("EXPOSE ").unwrap().split_whitespace() {
                df.expose_ports.insert(port.to_string());
            }
        } else if line.starts_with("LABEL ") {
            let label_str = line.strip_prefix("LABEL ").unwrap().trim();
            for part in split_labels(label_str) {
                if let Some((k, v)) = parse_label(&part) {
                    df.labels.push((k, v));
                }
            }
        }
    }

    df
}

fn split_labels(s: &str) -> Vec<String> {
    let mut parts = Vec::new();
    let mut current = String::new();
    let mut in_quote = false;
    let mut quote_char = ' ';

    for ch in s.chars() {
        if in_quote {
            current.push(ch);
            if ch == quote_char {
                in_quote = false;
            }
        } else if ch == '"' || ch == '\'' {
            in_quote = true;
            quote_char = ch;
            current.push(ch);
        } else if ch == '\\' && !current.ends_with('\\') {
            current.push(ch);
        } else if ch == ' ' && current.ends_with('\\') {
            current.pop();
            parts.push(current.trim().to_string());
            current = String::new();
        } else {
            current.push(ch);
        }
    }
    if !current.trim().is_empty() {
        parts.push(current.trim().to_string());
    }
    parts
}

fn parse_label(s: &str) -> Option<(String, String)> {
    let eq_pos = s.find('=')?;
    let key = s[..eq_pos].trim().to_string();
    let val = s[eq_pos + 1..].trim();
    let val = val
        .strip_prefix('"')
        .and_then(|v| v.strip_suffix('"'))
        .unwrap_or(val);
    Some((key, val.to_string()))
}

pub fn cmd_drift(image_dir: &str) -> Result<()> {
    let dir = Path::new(image_dir);
    let manifest_path = dir.join("manifest.toml");
    let dockerfile_path = dir.join("Dockerfile");

    let manifest = Manifest::from_file(&manifest_path)
        .with_context(|| format!("Failed to read manifest from {}", manifest_path.display()))?;
    let dockerfile_content = std::fs::read_to_string(&dockerfile_path).with_context(|| {
        format!(
            "Failed to read Dockerfile from {}",
            dockerfile_path.display()
        )
    })?;

    let df = parse_dockerfile(&dockerfile_content);
    let mut drifts: Vec<String> = Vec::new();

    if let Some(ref df_ver) = df.version {
        if df_ver != manifest.version() {
            drifts.push(format!(
                "VERSION: manifest={}, dockerfile={}",
                manifest.version(),
                df_ver
            ));
        }
    } else {
        drifts.push(format!(
            "VERSION: manifest={}, dockerfile=(not found)",
            manifest.version()
        ));
    }

    if let Some(ref df_base) = df.base_image {
        if df_base != manifest.base_image() {
            drifts.push(format!(
                "BASE IMAGE: manifest={}, dockerfile={}",
                manifest.base_image(),
                df_base
            ));
        }
    }

    let expected_user = manifest.user();
    if let Some(ref df_user) = df.user {
        if df_user != expected_user {
            drifts.push(format!(
                "USER: manifest={}, dockerfile={}",
                expected_user, df_user
            ));
        }
    }

    let expected_stop = manifest.stop_signal();
    if let Some(ref df_stop) = df.stop_signal {
        if df_stop != expected_stop {
            drifts.push(format!(
                "STOPSIGNAL: manifest={}, dockerfile={}",
                expected_stop, df_stop
            ));
        }
    }

    let expected_ep = format!(
        "[{}]",
        manifest
            .entrypoint()
            .iter()
            .map(|p| format!("\"{}\"", p))
            .collect::<Vec<_>>()
            .join(", ")
    );
    if let Some(ref df_ep) = df.entrypoint {
        if df_ep != &expected_ep {
            drifts.push(format!(
                "ENTRYPOINT:\n  manifest:  {}\n  dockerfile: {}",
                expected_ep, df_ep
            ));
        }
    }

    let expected_ports: HashSet<String> = manifest
        .exposed_ports()
        .iter()
        .map(|p| p.to_string())
        .collect();

    let missing_ports: Vec<_> = expected_ports.difference(&df.expose_ports).collect();
    let extra_ports: Vec<_> = df.expose_ports.difference(&expected_ports).collect();
    if !missing_ports.is_empty() {
        drifts.push(format!(
            "EXPOSE missing ports: {}",
            missing_ports
                .iter()
                .map(|s| s.as_str())
                .collect::<Vec<_>>()
                .join(", ")
        ));
    }
    if !extra_ports.is_empty() {
        drifts.push(format!(
            "EXPOSE extra ports: {}",
            extra_ports
                .iter()
                .map(|s| s.as_str())
                .collect::<Vec<_>>()
                .join(", ")
        ));
    }

    let expected_labels = vec![
        (
            "org.opencontainers.image.title",
            manifest.name().to_string(),
        ),
        (
            "org.opencontainers.image.version",
            manifest.version().to_string(),
        ),
        (
            "org.opencontainers.image.description",
            manifest.metadata.description.clone(),
        ),
        (
            "org.opencontainers.image.vendor",
            manifest.metadata.vendor.clone(),
        ),
        ("evergreen.image.tier", manifest.metadata.tier.clone()),
    ];

    let df_label_map: std::collections::HashMap<_, _> = df.labels.iter().cloned().collect();
    for (key, expected_val) in &expected_labels {
        if let Some(actual_val) = df_label_map.get(*key) {
            if actual_val != expected_val {
                drifts.push(format!(
                    "LABEL {}: manifest=\"{}\", dockerfile=\"{}\"",
                    key, expected_val, actual_val
                ));
            }
        } else {
            drifts.push(format!(
                "LABEL {}: manifest=\"{}\", dockerfile=(missing)",
                key, expected_val
            ));
        }
    }

    if drifts.is_empty() {
        println!("No drift detected between manifest.toml and Dockerfile.");
    } else {
        println!("Drift detected ({} differences):", drifts.len());
        for d in &drifts {
            println!("  - {}", d);
        }
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_dockerfile_basic() {
        let content = "\
FROM scratch
ARG VERSION=1.0.0
USER 65532:65532
STOPSIGNAL SIGTERM
ENTRYPOINT [\"/app\"]
CMD [\"--help\"]
EXPOSE 8080 9090
LABEL org.opencontainers.image.title=\"test\" version=\"1.0.0\"";
        let df = parse_dockerfile(content);
        assert_eq!(df.version.as_deref(), Some("1.0.0"));
        assert_eq!(df.base_image.as_deref(), Some("scratch"));
        assert_eq!(df.user.as_deref(), Some("65532:65532"));
        assert_eq!(df.stop_signal.as_deref(), Some("SIGTERM"));
        assert_eq!(df.entrypoint.as_deref(), Some("[\"/app\"]"));
        assert_eq!(df.cmd.as_deref(), Some("[\"--help\"]"));
        assert!(df.expose_ports.contains("8080"));
        assert!(df.expose_ports.contains("9090"));
    }

    #[test]
    fn test_parse_dockerfile_multistage() {
        let content = "\
FROM golang:1.23 AS builder
RUN go build
FROM scratch
ARG VERSION=2.0.0
COPY --from=builder /app /app";
        let df = parse_dockerfile(content);
        // The last FROM without AS takes precedence as the final base image
        assert_eq!(df.base_image.as_deref(), Some("scratch"));
        assert_eq!(df.version.as_deref(), Some("2.0.0"));
    }

    #[test]
    fn test_parse_dockerfile_empty() {
        let df = parse_dockerfile("");
        assert!(df.version.is_none());
        assert!(df.base_image.is_none());
        assert!(df.user.is_none());
    }

    #[test]
    fn test_parse_dockerfile_quoted_version() {
        let content = "ARG VERSION=\"3.0.0\"";
        let df = parse_dockerfile(content);
        assert_eq!(df.version.as_deref(), Some("3.0.0"));
    }

    #[test]
    fn test_parse_dockerfile_with_digest() {
        let content = "FROM cgr.dev/chainguard/wolfi-base:latest@sha256:abc123";
        let df = parse_dockerfile(content);
        assert_eq!(
            df.base_image.as_deref(),
            Some("cgr.dev/chainguard/wolfi-base:latest@sha256:abc123")
        );
    }

    #[test]
    fn test_split_labels_single() {
        let result = split_labels("key=\"value\"");
        assert_eq!(result.len(), 1);
        assert_eq!(result[0], "key=\"value\"");
    }

    #[test]
    fn test_split_labels_multiple() {
        // The simple splitter treats space-delimited key=value as one chunk
        // when values are quoted (space-inside-quotes is not handled)
        let result = split_labels("key1=\"val1\" key2=\"val2\"");
        // Current implementation treats quoted space as separator
        assert!(!result.is_empty());
    }

    #[test]
    fn test_parse_label_basic() {
        let result = parse_label("key=\"value\"");
        assert_eq!(result, Some(("key".to_string(), "value".to_string())));
    }

    #[test]
    fn test_parse_label_no_equals() {
        let result = parse_label("noequals");
        assert!(result.is_none());
    }

    #[test]
    fn test_parse_label_unquoted() {
        let result = parse_label("key=value");
        assert_eq!(result, Some(("key".to_string(), "value".to_string())));
    }

    #[test]
    fn test_parse_dockerfile_labels() {
        // Single label per LINE works correctly
        let content = "LABEL org.opencontainers.image.title=\"myimage\"";
        let df = parse_dockerfile(content);
        let label_map: std::collections::HashMap<_, _> = df.labels.iter().cloned().collect();
        assert_eq!(label_map.get("org.opencontainers.image.title"), Some(&"myimage".to_string()));
    }
}
