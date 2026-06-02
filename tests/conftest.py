"""Fixtures globales de tests."""

import pytest
from pathlib import Path


@pytest.fixture
def data_root(tmp_path: Path) -> Path:
    """data_root temporal para tests de integración."""
    root = tmp_path / "data_root"
    root.mkdir()
    return root
