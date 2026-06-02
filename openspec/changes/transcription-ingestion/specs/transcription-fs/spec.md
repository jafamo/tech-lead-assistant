# Spec: Filesystem — TranscriptionFileSystem

## Port `TranscriptionFileSystemPort` (ABC, en `domain/ports/`)

```python
class TranscriptionFileSystemPort(ABC):
    def write_transcript(
        self, data_root: Path, slug: str, meeting_type_slug: str,
        meeting_date: date, ext: str, content: bytes
    ) -> str: ...
    # Devuelve la ruta relativa a data_root

    def read_transcript(self, data_root: Path, rel_path: str) -> str: ...

    def write_transcript_text(self, data_root: Path, rel_path: str, text: str) -> None: ...
    # Reescritura atómica para edición

    def delete_transcript(self, data_root: Path, rel_path: str) -> None: ...
```

## Ruta canónica

```
{data_root}/{slug}/{meeting_type_slug}/YYYY-MM-DD.transcript.{ext}
```

Si ya existe ese fichero (mismo nombre), se añade sufijo: `YYYY-MM-DD_2.transcript.{ext}`.

## Adapter `LocalTranscriptionFileSystem` (`adapters/fs/transcription_fs.py`)

- `write_transcript`: escribe con `atomic_write_bytes`, devuelve path relativo a `data_root`
- `read_transcript`: `(data_root / rel_path).read_text(encoding="utf-8", errors="replace")`
- `write_transcript_text`: `atomic_write_text(data_root / rel_path, text)`
- `delete_transcript`: `(data_root / rel_path).unlink(missing_ok=True)`

## Hash MD5

Calculado en el use case (no en el adapter):
```python
import hashlib
file_hash = hashlib.md5(content).hexdigest()
```
