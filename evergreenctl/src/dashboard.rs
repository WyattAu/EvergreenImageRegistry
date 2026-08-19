// =============================================================================
// Evergreenctl - Registry Dashboard Generator
// =============================================================================
// Generates an HTML dashboard from the SQLite registry index with:
//   - Summary statistics cards
//   - Tier distribution pie chart
//   - Source type bar chart
//   - Build status timeline
//   - Violation heatmap
//   - Searchable image table
//
// Uses inline SVG charts (no external dependencies) for offline viewing.
// =============================================================================

use anyhow::Result;
use rusqlite::Connection;

// ---------------------------------------------------------------------------
// Data types
// ---------------------------------------------------------------------------

#[derive(Debug, serde::Serialize)]
pub struct DashboardData {
    pub summary: SummaryStats,
    pub tier_distribution: Vec<(String, usize)>,
    pub source_type_distribution: Vec<(String, usize)>,
    pub build_status_distribution: Vec<(String, usize)>,
    pub top_violations: Vec<(String, usize)>,
    pub images: Vec<ImageRow>,
    pub generated_at: String,
}

#[derive(Debug, serde::Serialize)]
pub struct SummaryStats {
    pub total_images: usize,
    pub with_sbom: usize,
    pub with_healthcheck: usize,
    pub digest_pinned: usize,
    pub deprecated: usize,
    pub tier1_count: usize,
    pub tier2_count: usize,
    pub tier3_count: usize,
    pub sbom_pct: f64,
    pub healthcheck_pct: f64,
    pub pinned_pct: f64,
}

#[derive(Debug, serde::Serialize)]
pub struct ImageRow {
    pub name: String,
    pub version: String,
    pub tier: u8,
    pub source_type: String,
    pub has_sbom: bool,
    pub has_healthcheck: bool,
    pub digest_pinned: bool,
    pub build_status: String,
}

// ---------------------------------------------------------------------------
// Data collection
// ---------------------------------------------------------------------------

pub fn collect_dashboard_data(conn: &Connection) -> Result<DashboardData> {
    // Summary stats
    let total_images: usize = conn.query_row("SELECT COUNT(*) FROM images", [], |r| r.get(0))?;
    let with_sbom: usize =
        conn.query_row("SELECT COUNT(*) FROM images WHERE has_sbom = 1", [], |r| {
            r.get(0)
        })?;
    let with_healthcheck: usize = conn.query_row(
        "SELECT COUNT(*) FROM images WHERE has_healthcheck = 1",
        [],
        |r| r.get(0),
    )?;
    let digest_pinned: usize = conn.query_row(
        "SELECT COUNT(*) FROM images WHERE digest_pinned = 1",
        [],
        |r| r.get(0),
    )?;
    let deprecated: usize = conn.query_row(
        "SELECT COUNT(*) FROM images WHERE is_deprecated = 1",
        [],
        |r| r.get(0),
    )?;
    let tier1_count: usize =
        conn.query_row("SELECT COUNT(*) FROM images WHERE tier = 1", [], |r| {
            r.get(0)
        })?;
    let tier2_count: usize =
        conn.query_row("SELECT COUNT(*) FROM images WHERE tier = 2", [], |r| {
            r.get(0)
        })?;
    let tier3_count: usize =
        conn.query_row("SELECT COUNT(*) FROM images WHERE tier = 3", [], |r| {
            r.get(0)
        })?;

    let sbom_pct = if total_images > 0 {
        with_sbom as f64 / total_images as f64 * 100.0
    } else {
        0.0
    };
    let healthcheck_pct = if total_images > 0 {
        with_healthcheck as f64 / total_images as f64 * 100.0
    } else {
        0.0
    };
    let pinned_pct = if total_images > 0 {
        digest_pinned as f64 / total_images as f64 * 100.0
    } else {
        0.0
    };

    let summary = SummaryStats {
        total_images,
        with_sbom,
        with_healthcheck,
        digest_pinned,
        deprecated,
        tier1_count,
        tier2_count,
        tier3_count,
        sbom_pct,
        healthcheck_pct,
        pinned_pct,
    };

    // Tier distribution
    let tier_distribution = query_distribution(
        conn,
        "SELECT tier, COUNT(*) FROM images GROUP BY tier ORDER BY tier",
    )?;

    // Source type distribution
    let source_type_distribution = query_distribution(conn, "SELECT source_type, COUNT(*) FROM images WHERE source_type != '' GROUP BY source_type ORDER BY COUNT(*) DESC")?;

    // Build status distribution
    let build_status_distribution = query_distribution(conn, "SELECT COALESCE(build_status, 'unknown'), COUNT(*) FROM images GROUP BY COALESCE(build_status, 'unknown') ORDER BY COUNT(*) DESC")?;

    // Top violations
    let top_violations = query_distribution(conn, "SELECT constraint_code, COUNT(*) FROM policy_violations GROUP BY constraint_code ORDER BY COUNT(*) DESC LIMIT 10")?;

    // All images (for searchable table)
    let mut stmt = conn.prepare(
        "SELECT name, version, tier, source_type, has_sbom, has_healthcheck, digest_pinned, COALESCE(build_status, 'unknown')
         FROM images ORDER BY tier, name"
    )?;
    let images: Vec<ImageRow> = stmt
        .query_map([], |row| {
            Ok(ImageRow {
                name: row.get(0)?,
                version: row.get(1)?,
                tier: row.get::<_, i32>(2)? as u8,
                source_type: row.get(3)?,
                has_sbom: row.get(4)?,
                has_healthcheck: row.get(5)?,
                digest_pinned: row.get(6)?,
                build_status: row.get(7)?,
            })
        })?
        .collect::<Result<Vec<_>, _>>()?;

    Ok(DashboardData {
        summary,
        tier_distribution,
        source_type_distribution,
        build_status_distribution,
        top_violations,
        images,
        generated_at: chrono::Utc::now()
            .format("%Y-%m-%d %H:%M:%S UTC")
            .to_string(),
    })
}

fn query_distribution(conn: &Connection, sql: &str) -> Result<Vec<(String, usize)>> {
    let mut stmt = conn.prepare(sql)?;
    let rows = stmt
        .query_map([], |row| {
            Ok((row.get::<_, String>(0)?, row.get::<_, usize>(1)?))
        })?
        .collect::<Result<Vec<_>, _>>()?;
    Ok(rows)
}

// ---------------------------------------------------------------------------
// HTML generation
// ---------------------------------------------------------------------------

pub fn generate_dashboard_html(data: &DashboardData) -> String {
    let s = &data.summary;

    // Build pie chart data for tiers
    let tier_chart = generate_pie_chart(&[
        ("Tier 1 (Critical)", s.tier1_count, "#ef4444"),
        ("Tier 2 (Standard)", s.tier2_count, "#f59e0b"),
        ("Tier 3 (Low)", s.tier3_count, "#6b7280"),
    ]);

    // Build bar chart for source types
    let source_chart = generate_bar_chart(&data.source_type_distribution);

    // Build image table rows
    let table_rows: String = data.images.iter().map(|img| {
        let tier_class = match img.tier {
            1 => "tier-1",
            2 => "tier-2",
            _ => "tier-3",
        };
        let sbom_icon = if img.has_sbom { "✅" } else { "❌" };
        let hc_icon = if img.has_healthcheck { "✅" } else { "❌" };
        let pin_icon = if img.digest_pinned { "✅" } else { "❌" };
        let status_class = match img.build_status.as_str() {
            "pass" => "status-pass",
            "fail" => "status-fail",
            _ => "status-unknown",
        };

        format!(
            "<tr><td>{}</td><td>{}</td><td class=\"{}\">{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td class=\"{}\">{}</td></tr>",
            img.name, img.version, tier_class, img.tier, img.source_type,
            sbom_icon, hc_icon, pin_icon, status_class, img.build_status
        )
    }).collect::<Vec<_>>().join("\n            ");

    // Violation chart
    let violation_chart = if data.top_violations.is_empty() {
        "<p>No violations recorded.</p>".to_string()
    } else {
        generate_bar_chart(&data.top_violations)
    };

    format!(
        r#"<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evergreen Registry Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #e2e8f0; padding: 24px; }}
        h1 {{ font-size: 28px; margin-bottom: 8px; color: #f8fafc; }}
        .subtitle {{ color: #94a3b8; margin-bottom: 24px; font-size: 14px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }}
        .card-label {{ font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }}
        .card-value {{ font-size: 32px; font-weight: 700; margin-top: 4px; }}
        .card-sub {{ font-size: 13px; color: #64748b; margin-top: 4px; }}
        .chart-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 24px; margin-bottom: 32px; }}
        .chart-card {{ background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }}
        .chart-title {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; color: #f8fafc; }}
        table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 12px; overflow: hidden; }}
        th {{ background: #334155; padding: 12px 16px; text-align: left; font-size: 12px; text-transform: uppercase; color: #94a3b8; }}
        td {{ padding: 10px 16px; border-bottom: 1px solid #334155; font-size: 14px; }}
        tr:hover {{ background: #334155; }}
        .tier-1 {{ color: #ef4444; font-weight: 600; }}
        .tier-2 {{ color: #f59e0b; font-weight: 600; }}
        .tier-3 {{ color: #6b7280; }}
        .status-pass {{ color: #22c55e; }}
        .status-fail {{ color: #ef4444; }}
        .status-unknown {{ color: #94a3b8; }}
        .pie-container {{ display: flex; align-items: center; gap: 24px; }}
        .pie-legend {{ font-size: 14px; }}
        .pie-legend-item {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }}
        .pie-legend-color {{ width: 12px; height: 12px; border-radius: 3px; }}
        .bar-container {{ margin-bottom: 12px; }}
        .bar-label {{ font-size: 13px; color: #94a3b8; margin-bottom: 4px; }}
        .bar-track {{ background: #334155; height: 24px; border-radius: 6px; overflow: hidden; }}
        .bar-fill {{ height: 100%; border-radius: 6px; display: flex; align-items: center; padding-left: 8px; font-size: 12px; font-weight: 600; }}
        #search {{ width: 100%; padding: 10px 16px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: #e2e8f0; font-size: 14px; margin-bottom: 16px; }}
        #search:focus {{ outline: none; border-color: #3b82f6; }}
    </style>
</head>
<body>
    <h1>🛡️ Evergreen Registry Dashboard</h1>
    <p class="subtitle">Generated: {generated_at}</p>

    <!-- Summary Cards -->
    <div class="grid">
        <div class="card">
            <div class="card-label">Total Images</div>
            <div class="card-value">{total}</div>
            <div class="card-sub">{deprecated} deprecated</div>
        </div>
        <div class="card">
            <div class="card-label">SBOM Coverage</div>
            <div class="card-value" style="color: #22c55e;">{sbom_pct:.1}%</div>
            <div class="card-sub">{with_sbom}/{total} images</div>
        </div>
        <div class="card">
            <div class="card-label">Healthcheck</div>
            <div class="card-value" style="color: #3b82f6;">{hc_pct:.1}%</div>
            <div class="card-sub">{with_hc}/{total} images</div>
        </div>
        <div class="card">
            <div class="card-label">Digest Pinned</div>
            <div class="card-value" style="color: #a855f7;">{pin_pct:.1}%</div>
            <div class="card-sub">{pinned}/{total} images</div>
        </div>
    </div>

    <!-- Charts -->
    <div class="chart-grid">
        <div class="chart-card">
            <div class="chart-title">Tier Distribution</div>
            {tier_chart}
        </div>
        <div class="chart-card">
            <div class="chart-title">Source Types</div>
            {source_chart}
        </div>
        <div class="chart-card">
            <div class="chart-title">Top Violations</div>
            {violation_chart}
        </div>
    </div>

    <!-- Image Table -->
    <div class="chart-card">
        <div class="chart-title">All Images ({total})</div>
        <input type="text" id="search" placeholder="🔍 Search images..." oninput="filterTable()">
        <div style="overflow-x: auto;">
            <table id="imageTable">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Version</th>
                        <th>Tier</th>
                        <th>Source Type</th>
                        <th>SBOM</th>
                        <th>Healthcheck</th>
                        <th>Pinned</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
            {table_rows}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function filterTable() {{
            const input = document.getElementById('search').value.toLowerCase();
            const rows = document.querySelectorAll('#imageTable tbody tr');
            rows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(input) ? '' : 'none';
            }});
        }}
    </script>
</body>
</html>"#,
        generated_at = data.generated_at,
        total = s.total_images,
        deprecated = s.deprecated,
        sbom_pct = s.sbom_pct,
        with_sbom = s.with_sbom,
        hc_pct = s.healthcheck_pct,
        with_hc = s.with_healthcheck,
        pin_pct = s.pinned_pct,
        pinned = s.digest_pinned,
        tier_chart = tier_chart,
        source_chart = source_chart,
        violation_chart = violation_chart,
        table_rows = table_rows,
    )
}

// ---------------------------------------------------------------------------
// Chart generators
// ---------------------------------------------------------------------------

fn generate_pie_chart(data: &[(&str, usize, &str)]) -> String {
    let total: usize = data.iter().map(|(_, c, _)| c).sum();
    if total == 0 {
        return "<p>No data</p>".to_string();
    }

    let mut svg = String::from(
        "<div class=\"pie-container\"><svg width=\"160\" height=\"160\" viewBox=\"0 0 36 36\">",
    );
    let mut offset = 0.0;

    for &(_label, count, color) in data {
        let pct = count as f64 / total as f64 * 100.0;
        let dash = format!("{:.1} {:.1}", pct, 100.0 - pct);
        svg.push_str(&format!(
            "<circle cx=\"18\" cy=\"18\" r=\"15.915\" fill=\"none\" stroke=\"{}\" stroke-width=\"3.5\" stroke-dasharray=\"{}\" stroke-dashoffset=\"{:.1}\"/>",
            color, dash, -offset
        ));
        offset += pct;
    }
    svg.push_str("</svg><div class=\"pie-legend\">");

    for &(label, count, color) in data {
        svg.push_str(&format!(
            "<div class=\"pie-legend-item\"><div class=\"pie-legend-color\" style=\"background:{}\"></div>{}: {}</div>",
            color, label, count
        ));
    }

    svg.push_str("</div></div>");
    svg
}

fn generate_bar_chart(data: &[(String, usize)]) -> String {
    if data.is_empty() {
        return "<p>No data</p>".to_string();
    }

    let max_val = data.iter().map(|(_, c)| *c).max().unwrap_or(1) as f64;
    let colors = [
        "#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#a855f7", "#06b6d4", "#ec4899", "#14b8a6",
    ];

    let mut html = String::new();
    for (i, (label, count)) in data.iter().enumerate() {
        let pct = *count as f64 / max_val * 100.0;
        let color = colors[i % colors.len()];
        html.push_str(&format!(
            "<div class=\"bar-container\"><div class=\"bar-label\">{} ({})</div><div class=\"bar-track\"><div class=\"bar-fill\" style=\"width:{:.0}%;background:{}\">{}</div></div></div>",
            label, count, pct, color, count
        ));
    }
    html
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_collect_dashboard_data_empty() {
        let dir = tempfile::tempdir().unwrap();
        let db_path = dir.path().join("test.db");
        let conn = crate::registry_index::open_index(&db_path).unwrap();
        let data = collect_dashboard_data(&conn).unwrap();
        assert_eq!(data.summary.total_images, 0);
        assert!(data.images.is_empty());
    }

    #[test]
    fn test_generate_dashboard_html() {
        let data = DashboardData {
            summary: SummaryStats {
                total_images: 100,
                with_sbom: 95,
                with_healthcheck: 80,
                digest_pinned: 85,
                deprecated: 3,
                tier1_count: 30,
                tier2_count: 50,
                tier3_count: 20,
                sbom_pct: 95.0,
                healthcheck_pct: 80.0,
                pinned_pct: 85.0,
            },
            tier_distribution: vec![("1".into(), 30), ("2".into(), 50), ("3".into(), 20)],
            source_type_distribution: vec![
                ("binary-download".into(), 50),
                ("pkg-install".into(), 50),
            ],
            build_status_distribution: vec![("pass".into(), 95), ("fail".into(), 5)],
            top_violations: vec![],
            images: vec![],
            generated_at: "2026-08-19 10:00:00 UTC".into(),
        };

        let html = generate_dashboard_html(&data);
        assert!(html.contains("Evergreen Registry Dashboard"));
        assert!(html.contains("100"));
        assert!(html.contains("95.0%"));
        assert!(html.contains("filterTable"));
    }

    #[test]
    fn test_generate_pie_chart() {
        let chart = generate_pie_chart(&[("Tier 1", 30, "#ef4444"), ("Tier 2", 50, "#f59e0b")]);
        assert!(chart.contains("<svg"));
        assert!(chart.contains("Tier 1: 30"));
        assert!(chart.contains("Tier 2: 50"));
    }

    #[test]
    fn test_generate_bar_chart() {
        let chart =
            generate_bar_chart(&[("binary-download".into(), 50), ("pkg-install".into(), 30)]);
        assert!(chart.contains("binary-download"));
        assert!(chart.contains("50"));
    }
}
