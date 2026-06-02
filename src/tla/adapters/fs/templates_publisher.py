"""Publica la carpeta templates/ en data_root."""

from __future__ import annotations

import shutil
from pathlib import Path


# Ficheros fuente en docs/templates/ del repo (o empaquetados con la app)
_TEMPLATE_FILES = [
    "content.example.json",
    "profile.example.md",
    "notes.example.md",
    "participants.example.json",
]


def publish_templates(repo_root: Path, data_root: Path) -> list[Path]:
    """Copia los ficheros de plantilla a data_root/templates/. Devuelve los copiados."""
    src_dir = repo_root / "docs" / "templates"
    dst_dir = data_root / "templates"
    dst_dir.mkdir(parents=True, exist_ok=True)

    published: list[Path] = []
    for filename in _TEMPLATE_FILES:
        src = src_dir / filename
        dst = dst_dir / filename
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            published.append(dst)

    # README de templates
    readme = dst_dir / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Templates TLA\n\n"
            "Plantillas y ejemplos para crear contenido manualmente o con herramientas externas.\n\n"
            "- `content.example.json` — ejemplo válido de report\n"
            "- `content.guide.md` — guía campo a campo (ver raíz del proyecto)\n"
            "- `profile.example.md` — ejemplo de perfil de miembro\n"
            "- `notes.example.md` — ejemplo de notas de reunión\n"
            "- `participants.example.json` — ejemplo de participantes multi-miembro\n",
            encoding="utf-8",
        )
        published.append(readme)

    return published
