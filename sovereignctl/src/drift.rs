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
    let dockerfile_content = std::fs::read_to_string(&dockerfile_path)
        .with_context(|| format!("Failed to read Dockerfile from {}", dockerfile_path.display()))?;

    let df = parse_dockerfile(&dockerfile_content);
    let mut drifts: Vec<String> = Vec::new();

    if let Some(ref df_ver) = df.version {
        if df_ver != &manifest.image.version {
            drifts.push(format!(
                "VERSION: manifest={}, dockerfile={}",
                manifest.image.version, df_ver
            ));
        }
    } else {
        drifts.push(format!(
            "VERSION: manifest={}, dockerfile=(not found)",
            manifest.image.version
        ));
    }

    if let Some(ref df_base) = df.base_image {
        if df_base != &manifest.build.base.image {
            drifts.push(format!(
                "BASE IMAGE: manifest={}, dockerfile={}",
                manifest.build.base.image, df_base
            ));
        }
    }

    let expected_user = &manifest.runtime.user;
    if let Some(ref df_user) = df.user {
        if df_user != expected_user {
            drifts.push(format!(
                "USER: manifest={}, dockerfile={}",
                expected_user, df_user
            ));
        }
    }

    let expected_stop = &manifest.runtime.stop_signal;
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
            .runtime
            .entrypoint
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

    let expected_cmd = if manifest.runtime.cmd.is_empty() {
        String::new()
    } else {
        format!(
            "[{}]",
            manifest
                .runtime
                .cmd
                .iter()
                .map(|p| format!("\"{}\"", p))
                .collect::<Vec<_>>()
                .join(", ")
        )
    };
    if let Some(ref df_cmd) = df.cmd {
        if !expected_cmd.is_empty() && df_cmd != &expected_cmd {
            drifts.push(format!(
                "CMD:\n  manifest:  {}\n  dockerfile: {}",
                expected_cmd, df_cmd
            ));
        }
    } else if !expected_cmd.is_empty() {
        drifts.push(format!("CMD: manifest={}, dockerfile=(not found)", expected_cmd));
    }

    let mut expected_ports: HashSet<String> = manifest
        .runtime
        .ports
        .iter()
        .map(|p| p.to_string())
        .collect();
    if manifest.observability.metrics_port > 0 {
        expected_ports.insert(manifest.observability.metrics_port.to_string());
    }
    if let Some(hp) = manifest.health.port {
        expected_ports.insert(hp.to_string());
    }

    let missing_ports: Vec<_> = expected_ports.difference(&df.expose_ports).collect();
    let extra_ports: Vec<_> = df.expose_ports.difference(&expected_ports).collect();
    if !missing_ports.is_empty() {
        drifts.push(format!(
            "EXPOSE missing ports: {}",
            missing_ports.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", ")
        ));
    }
    if !extra_ports.is_empty() {
        drifts.push(format!(
            "EXPOSE extra ports: {}",
            extra_ports.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", ")
        ));
    }

    let expected_labels = vec![
        ("org.opencontainers.image.title", manifest.image.name.clone()),
        ("org.opencontainers.image.version", manifest.image.version.clone()),
        ("org.opencontainers.image.description", manifest.image.description.clone()),
        ("org.opencontainers.image.vendor", manifest.image.vendor.clone()),
        ("sovereign.image.tier", manifest.image.tier.to_string()),
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
            drifts.push(format!("LABEL {}: manifest=\"{}\", dockerfile=(missing)", key, expected_val));
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
