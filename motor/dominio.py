"""
dominio.py — Modelo del dominio
Clases de datos que representan los conceptos principales del motor:
Historia, Escena, Opcion y EstadoSesion.
"""
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Opcion:
    """Representa una elección disponible dentro de una escena."""
    id: str
    texto: str
    destino: str
    condiciones: Dict[str, bool] = field(default_factory=dict)
    efectos: Dict[str, bool] = field(default_factory=dict)


@dataclass
class Escena:
    """Representa una escena de la historia."""
    id: str
    texto: str
    final: bool
    opciones: List[Opcion] = field(default_factory=list)


@dataclass
class Historia:
    """Representa la historia completa cargada desde el archivo."""
    titulo: str
    inicio: str
    variables: Dict[str, bool]
    escenas: Dict[str, Escena] = field(default_factory=dict)


@dataclass
class EstadoSesion:
    """Estado mutable de una partida en curso."""
    escena_actual: str
    variables: Dict[str, bool]
    terminada: bool = False
    bloqueada: bool = False
