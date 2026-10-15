"""
diagnostico.py — Representación de errores de validación
Cada Diagnostico describe un error con causa y ubicación identificable,
tal como exige RF6.2.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Diagnostico:
    """Describe un error detectado durante la validación de una historia."""
    causa: str
    campo: Optional[str] = None   # campo JSON involucrado, si aplica
    id_escena: Optional[str] = None
    id_opcion: Optional[str] = None

    def __str__(self) -> str:
        partes = [self.causa]
        if self.id_escena:
            partes.append(f"escena '{self.id_escena}'")
        if self.id_opcion:
            partes.append(f"opción '{self.id_opcion}'")
        if self.campo:
            partes.append(f"campo '{self.campo}'")
        return " | ".join(partes)


class ErrorValidacion(Exception):
    """Excepción lanzada cuando la historia no supera la validación."""
    def __init__(self, diagnosticos: list):
        self.diagnosticos = diagnosticos
        mensajes = "\n  - ".join(str(d) for d in diagnosticos)
        super().__init__(f"Historia inválida:\n  - {mensajes}")
