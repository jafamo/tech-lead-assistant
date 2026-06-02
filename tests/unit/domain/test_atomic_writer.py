"""Tests del writer atómico."""

import pytest
from pathlib import Path

from tla.adapters.fs.writer import atomic_write_text, atomic_write_bytes, atomic_move


def test_atomic_write_text_creates_file(tmp_path: Path) -> None:
    target = tmp_path / "sub" / "file.txt"
    atomic_write_text(target, "hello")
    assert target.read_text() == "hello"


def test_atomic_write_text_overwrites(tmp_path: Path) -> None:
    target = tmp_path / "file.txt"
    atomic_write_text(target, "first")
    atomic_write_text(target, "second")
    assert target.read_text() == "second"


def test_atomic_write_text_no_partial_on_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "file.txt"
    atomic_write_text(target, "original")

    import os
    original_replace = os.replace

    def failing_replace(src: str, dst: str) -> None:
        raise OSError("simulated failure")

    monkeypatch.setattr(os, "replace", failing_replace)
    with pytest.raises(OSError):
        atomic_write_text(target, "corrupted")

    # El fichero original no se ha tocado
    assert target.read_text() == "original"


def test_atomic_write_bytes(tmp_path: Path) -> None:
    target = tmp_path / "data.bin"
    atomic_write_bytes(target, b"\x00\x01\x02")
    assert target.read_bytes() == b"\x00\x01\x02"


def test_atomic_move(tmp_path: Path) -> None:
    src = tmp_path / "src.txt"
    dst = tmp_path / "subdir" / "dst.txt"
    src.write_text("content")
    atomic_move(src, dst)
    assert dst.read_text() == "content"
    assert not src.exists()
