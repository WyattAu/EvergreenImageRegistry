import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from inventory_report import _from_lines, normalize_tier, scan


def test_normalize_legacy_tiers():
    assert normalize_tier("1") == "critical"
    assert normalize_tier("2") == "standard"
    assert normalize_tier("3") == "standard"
    assert normalize_tier("critical") == "critical"


def test_from_lines_classify_scratch_and_digest():
    result = _from_lines("FROM scratch\nFROM wolfi:latest AS builder\nFROM wolfi@sha256:" + "a" * 64)
    assert result[0]["pinned"] is True
    assert result[1]["pinned"] is False
    assert result[2]["pinned"] is True


def test_inventory_uses_active_directories():
    report = scan()
    assert report["schema_version"] == 3
    assert report["total_images"] > 0
    assert report["total_images"] == len(report["images"])
    assert all(not item["name"].startswith("_") for item in report["images"])


def test_inventory_counts_are_consistent():
    report = scan()
    for key in ("with_sbom", "with_valid_sbom", "with_user", "with_healthcheck", "all_from_pinned"):
        assert 0 <= report[key] <= report["total_images"]
    assert report["with_valid_sbom"] <= report["with_sbom"]
    assert report["critical_from_pinned"] <= report["critical_total"]
    assert report["standard_unpinned"] <= report["total_images"]
    assert report["critical_unpinned"] == len(report["critical_unpinned_images"])
    assert all(item["unpinned_from"] == [] or item["all_from_pinned"] is False for item in report["images"])
    assert report["tier_conflicts"] == 0
    assert report["invalid_tiers"] == 0


def test_inventory_json_is_serializable():
    report = scan()
    assert json.loads(json.dumps(report)) == report
