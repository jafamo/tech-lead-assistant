"""Excepciones de dominio TLA."""


class TLAError(Exception):
    """Base de todas las excepciones de dominio."""


class DataRootNotFoundError(TLAError):
    """data_root no accesible (ruta no existe o red caída)."""


class DataRootDisconnectedError(TLAError):
    """data_root en red pero no disponible en este momento."""


class SlugConflictError(TLAError):
    """Ya existe un miembro con ese slug."""


class MemberNotFoundError(TLAError):
    """Miembro no encontrado."""


class ReportNotFoundError(TLAError):
    """Report no encontrado."""


class SchemaValidationError(TLAError):
    """content.json no cumple el schema TLA."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__(f"Schema inválido: {errors}")


class LLMProviderError(TLAError):
    """Error al comunicarse con el proveedor LLM."""


class AtomicWriteError(TLAError):
    """Escritura atómica fallida."""
