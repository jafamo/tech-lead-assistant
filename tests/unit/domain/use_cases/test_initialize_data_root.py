"""Tests unitarios de InitializeDataRoot."""

from pathlib import Path
from unittest.mock import MagicMock

from tla.domain.use_cases.initialize_data_root import InitializeDataRoot, _SUBDIRS


def _make_fs(existing: set[Path] | None = None) -> MagicMock:
    existing = existing or set()
    fs = MagicMock()
    fs.exists.side_effect = lambda p: p in existing
    return fs


def test_creates_data_root_when_missing() -> None:
    fs = _make_fs()
    uc = InitializeDataRoot(fs=fs)
    data_root = Path("/data/tla")

    uc.execute(data_root)

    fs.mkdir.assert_any_call(data_root)


def test_creates_all_subdirs() -> None:
    fs = _make_fs()
    uc = InitializeDataRoot(fs=fs)
    data_root = Path("/data/tla")

    uc.execute(data_root)

    created_paths = {call.args[0] for call in fs.mkdir.call_args_list}
    for subdir in _SUBDIRS:
        assert data_root / subdir in created_paths


def test_skips_existing_dirs() -> None:
    data_root = Path("/data/tla")
    existing = {data_root, data_root / "_import"}
    fs = _make_fs(existing=existing)
    uc = InitializeDataRoot(fs=fs)

    created = uc.execute(data_root)

    created_paths = {p for p in created}
    assert data_root not in created_paths
    assert data_root / "_import" not in created_paths


def test_returns_only_created_dirs() -> None:
    data_root = Path("/data/tla")
    fs = _make_fs()
    uc = InitializeDataRoot(fs=fs)

    created = uc.execute(data_root)

    # data_root + todos los subdirs
    assert len(created) == 1 + len(_SUBDIRS)


def test_idempotent_when_all_exist() -> None:
    data_root = Path("/data/tla")
    all_paths = {data_root} | {data_root / s for s in _SUBDIRS}
    fs = _make_fs(existing=all_paths)
    uc = InitializeDataRoot(fs=fs)

    created = uc.execute(data_root)

    assert created == []
    fs.mkdir.assert_not_called()
