#!/usr/bin/env python3
"""CIS/STIG Compliance Dashboard Generator.

Generates a Markdown dashboard showing compliance status across all images.
"""

import json
import sys
from pathlib import Path


def check_image_compliance(img_dir: Path) -> dict:
    """Check compliance status for a single image."""
    dockerfile = img_dir / "Dockerfile"
    manifest = img_dir / "manifest.toml"
    
    result = {
        "name": img_dir.name,
        "has_dockerfile": dockerfile.exists(),
        "has_manifest": manifest.exists(),
        "non_root": False,
        "healthcheck": False,
        "entrypoint": False,
        "digest_pinned": False,
        "tier": "standard",
    }
    
    if not dockerfile.exists():
        return result
    
    content = dockerfile.read_text()
    
    # Check non-root
    result["non_root"] = any(u in content for u in ["USER 65532", "USER 65534", "USER nobody"])
    
    # Check healthcheck
    result["healthcheck"] = "HEALTHCHECK" in content
    
    # Check entrypoint/cmd
    result["entrypoint"] = "ENTRYPOINT" in content or "CMD" in content
    
    # Check digest pinning
    result["digest_pinned"] = "@sha256:" in content
    
    # Check tier from manifest
    if manifest.exists():
        manifest_content = manifest.read_text()
        if 'tier = "critical"' in manifest_content:
            result["tier"] = "critical"
    
    return result


def generate_dashboard(images_dir: Path, output_file: Path):
    """Generate compliance dashboard."""
    results = []
    
    for img_dir in sorted(images_dir.iterdir()):
        if not img_dir.is_dir() or img_dir.name.startswith("_"):
            continue
        result = check_image_compliance(img_dir)
        results.append(result)
    
    # Calculate metrics
    total = len(results)
    critical = [r for r in results if r["tier"] == "critical"]
    standard = [r for r in results if r["tier"] == "standard"]
    
    non_root_pass = sum(1 for r in results if r["non_root"])
    healthcheck_pass = sum(1 for r in results if r["healthcheck"])
    entrypoint_pass = sum(1 for r in results if r["entrypoint"])
    digest_pass = sum(1 for r in results if r["digest_pinned"])
    
    # Generate markdown
    md = []
    md.append("# CIS/STIG Compliance Dashboard")
    md.append("")
    md.append(f"Generated: {__import__('datetime').datetime.now().isoformat()}")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(f"| Metric | Value |")
    md.append(f"|--------|-------|")
    md.append(f"| Total images | {total} |")
    md.append(f"| Critical tier | {len(critical)} |")
    md.append(f"| Standard tier | {len(standard)} |")
    md.append(f"| Non-root compliance | {non_root_pass}/{total} ({non_root_pass/total*100:.1f}%) |")
    md.append(f"| Healthcheck compliance | {healthcheck_pass}/{total} ({healthcheck_pass/total*100:.1f}%) |")
    md.append(f"| Entrypoint compliance | {entrypoint_pass}/{total} ({entrypoint_pass/total*100:.1f}%) |")
    md.append(f"| Digest pinned | {digest_pass}/{total} ({digest_pass/total*100:.1f}%) |")
    md.append("")
    
    # Non-compliant images
    non_compliant = [r for r in results if not r["non_root"] or not r["healthcheck"]]
    if non_compliant:
        md.append("## Non-Compliant Images")
        md.append("")
        md.append("| Image | Tier | NonRoot | Healthcheck |")
        md.append("|-------|------|---------|-------------|")
        for r in non_compliant:
            nr = "✅" if r["non_root"] else "❌"
            hc = "✅" if r["healthcheck"] else "❌"
            md.append(f"| {r['name']} | {r['tier']} | {nr} | {hc} |")
        md.append("")
    
    # Write output
    output_file.write_text("\n".join(md))
    print(f"Dashboard written to {output_file}")


def main():
    images_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("images")
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("docs/cis-dashboard.md")
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    generate_dashboard(images_dir, output_file)


if __name__ == "__main__":
    main()
