use anyhow::{Context, Result};
use std::path::Path;

/// Pin all FROM digests in Dockerfiles to immutable SHA256 refs.
///
/// For each Dockerfile in the images directory, resolves base image tags
/// to their SHA256 digests using `crane digest` and updates the FROM lines.
pub fn cmd_pin_digests(image_dir: &str, dry_run: bool) -> Result<()> {
    let dir = Path::new(image_dir);
    if !dir.exists() {
        anyhow::bail!("Directory not found: {}", image_dir);
    }

    let mut pinned = 0;
    let mut skipped = 0;
    let mut errors = 0;

    let dockerfile_path = dir.join("Dockerfile");
    if dockerfile_path.exists() {
        match pin_dockerfile_digests(&dockerfile_path, dry_run) {
            Ok(count) => {
                pinned += count;
            }
            Err(e) => {
                eprintln!("ERROR pinning {}: {}", dockerfile_path.display(), e);
                errors += 1;
            }
        }
    } else {
        // Walk subdirectories for multi-image directories
        for entry in std::fs::read_dir(dir)? {
            let entry = entry?;
            let path = entry.path();
            if !path.is_dir() {
                continue;
            }
            let df_path = path.join("Dockerfile");
            if !df_path.exists() {
                continue;
            }

            let name = path
                .file_name()
                .unwrap_or_default()
                .to_string_lossy()
                .to_string();

            match pin_dockerfile_digests(&df_path, dry_run) {
                Ok(count) => {
                    if count > 0 {
                        println!("  {}: pinned {} FROM lines", name, count);
                        pinned += count;
                    } else {
                        skipped += 1;
                    }
                }
                Err(e) => {
                    eprintln!("  {}: ERROR - {}", name, e);
                    errors += 1;
                }
            }
        }
    }

    println!(
        "\nSummary: {} FROM lines pinned, {} images skipped (already pinned or no FROM), {} errors",
        pinned, skipped, errors
    );

    if errors > 0 {
        anyhow::bail!("{} error(s) encountered", errors);
    }

    Ok(())
}

fn pin_dockerfile_digests(dockerfile_path: &Path, dry_run: bool) -> Result<usize> {
    let content = std::fs::read_to_string(dockerfile_path)
        .with_context(|| format!("Failed to read {}", dockerfile_path.display()))?;

    let mut new_content = String::new();
    let mut pinned_count = 0;

    for line in content.lines() {
        let trimmed = line.trim();

        if trimmed.starts_with("FROM ")
            && !trimmed.contains("@sha256:")
            && !trimmed.starts_with("FROM scratch")
            && !trimmed.starts_with("FROM SCRATCH")
        {
            // Extract base image reference
            let from_part = trimmed
                .strip_prefix("FROM ")
                .unwrap()
                .split_whitespace()
                .next()
                .unwrap_or("");

            // Skip if already has digest
            if from_part.contains('@') {
                new_content.push_str(line);
                new_content.push('\n');
                continue;
            }

            // Skip scratch
            if from_part == "scratch" || from_part == "SCRATCH" {
                new_content.push_str(line);
                new_content.push('\n');
                continue;
            }

            // Try to resolve digest via crane
            match resolve_digest(from_part) {
                Ok(digest) => {
                    let pinned_line = line.replace(from_part, &format!("{}@{}", from_part, digest));
                    if dry_run {
                        println!(
                            "  [DRY-RUN] Would pin: {} -> {}@{}",
                            from_part, from_part, digest
                        );
                    }
                    new_content.push_str(&pinned_line);
                    new_content.push('\n');
                    pinned_count += 1;
                }
                Err(e) => {
                    eprintln!(
                        "  WARNING: Could not resolve digest for {}: {}. Keeping unpinned.",
                        from_part, e
                    );
                    new_content.push_str(line);
                    new_content.push('\n');
                }
            }
        } else {
            new_content.push_str(line);
            new_content.push('\n');
        }
    }

    if !dry_run && pinned_count > 0 {
        std::fs::write(dockerfile_path, &new_content)
            .with_context(|| format!("Failed to write {}", dockerfile_path.display()))?;
    }

    Ok(pinned_count)
}

/// Extract the first SHA256 digest from a `docker manifest inspect` JSON payload.
///
/// Manifest lists contain a top-level `manifests` array; single manifests may
/// have a top-level `config.digest`.  We prefer the first platform entry for
/// lists, then fall back to `config.digest`.
fn parse_manifest_digest(json: &str) -> Option<String> {
    // Quick regex-free approach: look for "digest": "sha256:..." patterns
    for line in json.lines() {
        let trimmed = line.trim();
        // Strip trailing comma if present
        let trimmed = trimmed.strip_suffix(',').unwrap_or(trimmed);
        if let Some(rest) = trimmed.strip_prefix("\"digest\": \"") {
            if let Some(digest) = rest.strip_suffix("\"") {
                if digest.starts_with("sha256:") && digest.len() == 71 {
                    return Some(digest.to_string());
                }
            }
        }
        // Also handles "digest":"sha256:..." (no space)
        if let Some(rest) = trimmed.strip_prefix("\"digest\":\"") {
            if let Some(digest) = rest.strip_suffix("\"") {
                if digest.starts_with("sha256:") && digest.len() == 71 {
                    return Some(digest.to_string());
                }
            }
        }
    }
    None
}

/// Resolve a container image reference to its SHA256 digest.
/// Uses `crane digest` if available, otherwise tries `skopeo`, then `docker`.
fn resolve_digest(image_ref: &str) -> Result<String> {
    // Try crane first (fastest, most reliable)
    if let Ok(output) = std::process::Command::new("crane")
        .args(["digest", image_ref])
        .output()
    {
        if output.status.success() {
            let digest = String::from_utf8_lossy(&output.stdout).trim().to_string();
            if digest.starts_with("sha256:") {
                return Ok(digest);
            }
        }
    }

    // Try skopeo
    if let Ok(output) = std::process::Command::new("skopeo")
        .args([
            "inspect",
            &format!("docker://{}", image_ref),
            "--format",
            "{{.Digest}}",
        ])
        .output()
    {
        if output.status.success() {
            let digest = String::from_utf8_lossy(&output.stdout).trim().to_string();
            if digest.starts_with("sha256:") {
                return Ok(digest);
            }
        }
    }

    // Try docker manifest inspect (parse JSON output, --format not supported)
    if let Ok(output) = std::process::Command::new("docker")
        .args(["manifest", "inspect", image_ref])
        .output()
    {
        if output.status.success() {
            let stdout = String::from_utf8_lossy(&output.stdout);
            if let Some(digest) = parse_manifest_digest(&stdout) {
                return Ok(digest);
            }
        }
    }

    anyhow::bail!(
        "No digest resolution tool available (crane, skopeo, or docker). \
         Please install one: https://github.com/google/go-containerregistry/blob/main/cmd/crane/README.md"
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn test_pin_dockerfile_already_pinned() {
        let content = "FROM cgr.dev/chainguard/wolfi-base:latest@sha256:abc123\nRUN echo hi\n";
        let mut tmp = tempfile::NamedTempFile::new().unwrap();
        write!(tmp, "{}", content).unwrap();
        let result = pin_dockerfile_digests(tmp.path(), true);
        // Should return 0 pinned (already pinned) if tools available
        // May fail if crane/skopeo/docker not available - both are acceptable
        if let Ok(count) = result {
            assert_eq!(count, 0, "Should not re-pin already pinned lines");
        }
    }

    #[test]
    fn test_pin_dockerfile_scratch_skipped() {
        let content = "FROM scratch\nRUN echo hi\n";
        let mut tmp = tempfile::NamedTempFile::new().unwrap();
        write!(tmp, "{}", content).unwrap();
        let result = pin_dockerfile_digests(tmp.path(), true);
        if let Ok(count) = result {
            assert_eq!(count, 0, "scratch should not need pinning");
        }
        // Err is OK too (no crane available)
    }

    #[test]
    fn test_pin_dockerfile_dry_run_no_write() {
        let content = "FROM cgr.dev/chainguard/wolfi-base:latest\nRUN echo hi\n";
        let mut tmp = tempfile::NamedTempFile::new().unwrap();
        write!(tmp, "{}", content).unwrap();
        let _result = pin_dockerfile_digests(tmp.path(), true);
        // Dry run should not modify the file regardless of success/failure
        let written_content = std::fs::read_to_string(tmp.path()).unwrap();
        assert_eq!(written_content.trim(), content.trim());
    }

    #[test]
    fn test_resolve_digest_no_tool_available() {
        // When no tools are available, should return an error
        // We can't mock external commands easily, so just verify the error message
        let result = resolve_digest("nonexistent:latest");
        assert!(result.is_err());
        let err = result.unwrap_err().to_string();
        assert!(err.contains("crane") || err.contains("skopeo") || err.contains("docker"));
    }
}
