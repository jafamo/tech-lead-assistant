"""Tests unitarios de PublishSchema."""

from pathlib import Path
from unittest.mock import MagicMock

from tla.domain.use_cases.publish_schema import PublishSchema


def test_copies_schema_to_published_dir() -> None:
    fs = MagicMock()
    uc = PublishSchema(fs=fs)
    schema_src = Path("/repo/content.schema.json")
    data_root = Path("/data/tla")

    dst = uc.execute(schema_src, data_root)

    assert dst == data_root / "_published_schema" / "content.schema.json"
    fs.copy.assert_called_once_with(schema_src, dst)


def test_creates_parent_dir() -> None:
    fs = MagicMock()
    uc = PublishSchema(fs=fs)

    uc.execute(Path("/repo/content.schema.json"), Path("/data/tla"))

    fs.mkdir.assert_called_once_with(Path("/data/tla") / "_published_schema")
