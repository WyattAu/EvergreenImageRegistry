import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from critical_pinning_worklist import build_worklist


def test_worklist_is_sorted_and_actionable():
    report = {
        "schema_version": 3,
        "critical_total": 1,
        "critical_from_pinned": 0,
        "images": [
            {
                "name": "z-image",
                "tier": "critical",
                "all_from_pinned": False,
                "unpinned_from": [{"line": 4, "reference": "base:latest"}],
            },
            {
                "name": "a-image",
                "tier": "standard",
                "all_from_pinned": False,
                "unpinned_from": [{"line": 1, "reference": "ignored:latest"}],
            },
        ],
    }
    result = build_worklist(report)
    assert result["unresolved_entries"] == 1
    assert result["entries"][0]["image"] == "z-image"
    assert result["entries"][0]["status"] == "requires-upstream-resolution"
    assert result["entries"][0]["dockerfile"] == "images/z-image/Dockerfile"


def test_empty_worklist_is_stable():
    result = build_worklist({
        "schema_version": 3,
        "critical_total": 0,
        "critical_from_pinned": 0,
        "images": [],
    })
    assert result["entries"] == []
    assert result["unresolved_entries"] == 0
