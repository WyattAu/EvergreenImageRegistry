use anyhow::{Context, Result};
use std::path::Path;
use walkdir::WalkDir;

#[derive(Debug, Clone, serde::Serialize)]
pub struct AuditResult {
    pub name: String,
    pub status: ImageStatus,
    pub issues: Vec<AuditIssue>,
}

#[derive(Debug, Clone, serde::Serialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum ImageStatus {
    Real,
    Placeholder,
    Stub,
    Error,
}

#[derive(Debug, Clone, serde::Serialize)]
pub struct AuditIssue {
    pub severity: String,
    pub code: String,
    pub message: String,
    pub line: Option<usize>,
}

/// Audit a single Dockerfile for stubs and placeholders
pub fn audit_dockerfile(path: &Path, image_name: &str) -> Result<AuditResult> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read: {}", path.display()))?;

    let mut issues = Vec::new();
    let lines: Vec<&str> = content.lines().collect();

    // Check for placeholder patterns
    let has_sleep_infinity = content.contains("sleep infinity");
    let has_placeholder_echo = content.contains("placeholder");
    let has_real_entrypoint = has_real_entrypoint(&content);
    let has_real_download = has_real_download(&content);
    let has_source_build = has_source_build(&content);

    // Check for syntax issues
    for (i, line) in lines.iter().enumerate() {
        let line_num = i + 1;
        let trimmed = line.trim();

        // RUN && at start of line (no command before &&)
        if trimmed.starts_with("RUN &&") || trimmed.starts_with("run &&") {
            issues.push(AuditIssue {
                severity: "error".to_string(),
                code: "RUN_AND".to_string(),
                message: "RUN instruction starts with && (no command)".to_string(),
                line: Some(line_num),
            });
        }

        // Double &&
        if trimmed.contains("&&  &&") || trimmed.contains("&&\u{00a0}&&") {
            issues.push(AuditIssue {
                severity: "error".to_string(),
                code: "DOUBLE_AND".to_string(),
                message: "Double && operator".to_string(),
                line: Some(line_num),
            });
        }

        // \\ at end of line (escaped backslash instead of continuation)
        if trimmed.ends_with("\\\\") {
            issues.push(AuditIssue {
                severity: "warning".to_string(),
                code: "ESCAPED_BACKSLASH".to_string(),
                message: "Escaped backslash at end of line (should be single \\ for continuation)"
                    .to_string(),
                line: Some(line_num),
            });
        }

        // cp/bin/ missing space
        if trimmed.contains("cp/bin/") || trimmed.contains("cp/lib") {
            issues.push(AuditIssue {
                severity: "error".to_string(),
                code: "CP_NO_SPACE".to_string(),
                message: "cp command missing space before path".to_string(),
                line: Some(line_num),
            });
        }

        // addgroup without -g flag for GID
        if (trimmed.contains("addgroup") || trimmed.contains("groupadd"))
            && !trimmed.contains("-g ")
            && trimmed.contains("65532")
            && !trimmed.contains("-g65532")
        {
            issues.push(AuditIssue {
                severity: "error".to_string(),
                code: "ADDGROUP_NO_G_FLAG".to_string(),
                message: "addgroup with numeric GID but missing -g flag".to_string(),
                line: Some(line_num),
            });
        }

        // URL as bare command (not git clone or curl)
        if (trimmed.contains("RUN https://") || trimmed.contains("RUN http://"))
            && !trimmed.contains("curl")
            && !trimmed.contains("wget")
            && !trimmed.contains("git")
        {
            issues.push(AuditIssue {
                severity: "error".to_string(),
                code: "URL_AS_COMMAND".to_string(),
                message: "URL used as bare shell command (missing curl/wget/git)".to_string(),
                line: Some(line_num),
            });
        }

        // rm without -f flag
        if trimmed.contains("rm /")
            && !trimmed.contains("rm -f /")
            && !trimmed.contains("rm -rf /")
            && !trimmed.contains("|| true")
            && !trimmed.contains("2>/dev/null")
        {
            issues.push(AuditIssue {
                severity: "warning".to_string(),
                code: "RM_NO_FORCE".to_string(),
                message: "rm without -f flag (will fail if file missing)".to_string(),
                line: Some(line_num),
            });
        }
    }

    // Determine status
    let status = if has_sleep_infinity && !has_real_download && !has_source_build {
        ImageStatus::Stub
    } else if has_placeholder_echo && !has_real_entrypoint {
        ImageStatus::Placeholder
    } else if issues.iter().any(|i| i.severity == "error") {
        ImageStatus::Error
    } else {
        ImageStatus::Real
    };

    Ok(AuditResult {
        name: image_name.to_string(),
        status,
        issues,
    })
}

/// Audit all Dockerfiles in the images directory
pub fn audit_all(images_dir: &Path) -> Result<Vec<AuditResult>> {
    let mut results = Vec::new();

    for entry in WalkDir::new(images_dir)
        .min_depth(1)
        .max_depth(1)
        .sort_by_file_name()
    {
        let entry = entry?;
        let dockerfile = entry.path().join("Dockerfile");
        if dockerfile.exists() {
            let name = entry.file_name().to_string_lossy().to_string();
            match audit_dockerfile(&dockerfile, &name) {
                Ok(result) => results.push(result),
                Err(e) => {
                    results.push(AuditResult {
                        name: name.clone(),
                        status: ImageStatus::Error,
                        issues: vec![AuditIssue {
                            severity: "error".to_string(),
                            code: "READ_ERROR".to_string(),
                            message: e.to_string(),
                            line: None,
                        }],
                    });
                }
            }
        }
    }

    Ok(results)
}

fn has_real_entrypoint(content: &str) -> bool {
    // Check if there's a real ENTRYPOINT (not just sleep infinity)
    for line in content.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("ENTRYPOINT")
            && !trimmed.contains("sleep infinity")
            && !trimmed.contains("placeholder")
        {
            return true;
        }
    }
    false
}

fn has_real_download(content: &str) -> bool {
    // Check for real curl/wget download with actual URL
    for line in content.lines() {
        let trimmed = line.trim();
        if (trimmed.contains("curl") || trimmed.contains("wget"))
            && (trimmed.contains("http://") || trimmed.contains("https://"))
            && !trimmed.contains("nodesource")
        // exclude bootstrapping
        {
            return true;
        }
    }
    false
}

fn has_source_build(content: &str) -> bool {
    content.contains("cargo build")
        || content.contains("go build")
        || content.contains("make -j")
        || content.contains("cmake ")
        || content.contains("npm install")
        || content.contains("pip install")
        || content.contains("mvn ")
}

/// Generate audit summary
pub fn audit_summary(results: &[AuditResult]) -> String {
    let total = results.len();
    let real = results
        .iter()
        .filter(|r| r.status == ImageStatus::Real)
        .count();
    let placeholder = results
        .iter()
        .filter(|r| r.status == ImageStatus::Placeholder)
        .count();
    let stub = results
        .iter()
        .filter(|r| r.status == ImageStatus::Stub)
        .count();
    let error = results
        .iter()
        .filter(|r| r.status == ImageStatus::Error)
        .count();
    let total_issues: usize = results.iter().map(|r| r.issues.len()).sum();

    format!(
        "Audit Summary\n\
         ============\n\
         Total images: {}\n\
         Real: {} ({:.1}%)\n\
         Placeholder: {} ({:.1}%)\n\
         Stub: {} ({:.1}%)\n\
         Error: {} ({:.1}%)\n\
         Total issues: {}",
        total,
        real,
        real as f64 / total as f64 * 100.0,
        placeholder,
        placeholder as f64 / total as f64 * 100.0,
        stub,
        stub as f64 / total as f64 * 100.0,
        error,
        error as f64 / total as f64 * 100.0,
        total_issues,
    )
}
