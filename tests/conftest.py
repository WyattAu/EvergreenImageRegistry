from pathlib import Path

import pytest


@pytest.fixture
def repo_root():
    """Project root directory."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def tmp_image_dir(tmp_path):
    """Create a minimal image directory structure."""
    img = tmp_path / "images" / "test-image"
    img.mkdir(parents=True)
    return img


@pytest.fixture(autouse=True)
def clear_precommit_globals():
    """Clear pre_commit_validator mutable globals before each test."""
    import sys
    if "scripts.pre_commit_validator" in sys.modules:
        mod = sys.modules["scripts.pre_commit_validator"]
        if hasattr(mod, 'ERRORS'):
            mod.ERRORS.clear()
        if hasattr(mod, 'WARNINGS'):
            mod.WARNINGS.clear()
    yield
