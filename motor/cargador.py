"""
cargador.py — Carga de historias desde archivos JSON (RF1.1)
Responsabilidad única: leer el archivo y delegar la validación al validador.
"""
import json
from pathlib import Path
from typing import Dict

from motor.diagnostico import Diagnostico, ErrorValidacion
from motor.dominio import Escena, Historia, Opcion
from motor.validador import validar


def cargar(ruta: str) -> Historia:
    """
    Lee el archivo JSON en 'ruta', lo valida y devuelve una Historia.
    Lanza ErrorValidacion si el contenido es inválido.
    Lanza ErrorValidacion (con causa legible) si el archivo es ilegible.
    """
    # ── Lectura del archivo ───────────────────────────────────────────────────
    try:
        texto = Path(ruta).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ErrorValidacion([Diagnostico(
            causa=f"Archivo no encontrado: '{ruta}'",
            campo="ruta",
        )])
    except PermissionError:
        raise ErrorValidacion([Diagnostico(
            causa=f"Sin permiso para leer el archivo: '{ruta}'",
            campo="ruta",
        )])
    except OSError as exc:
        raise ErrorValidacion([Diagnostico(
            causa=f"No se puede leer el archivo: {exc}",
            campo="ruta",
        )])

    # ── Parseo JSON ───────────────────────────────────────────────────────────
    try:
        datos: Dict = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise ErrorValidacion([Diagnostico(
            causa=f"Archivo JSON malformado: {exc.msg} (línea {exc.lineno})",
            campo="formato",
        )])

    if not isinstance(datos, dict):
        raise ErrorValidacion([Diagnostico(
            causa="El archivo no contiene un objeto JSON válido en la raíz",
            campo="formato",
        )])

    # ── Validación estructural ────────────────────────────────────────────────
    validar(datos)  # lanza ErrorValidacion si hay errores

    # ── Construcción del modelo ───────────────────────────────────────────────
    escenas: Dict[str, Escena] = {}
    for esc_raw in datos["escenas"]:
        opciones = [
            Opcion(
                id=opc["id"],
                texto=opc["texto"],
                destino=opc["destino"],
                condiciones=dict(opc.get("condiciones", {})),
                efectos=dict(opc.get("efectos", {})),
            )
            for opc in esc_raw.get("opciones", [])
        ]
        escena = Escena(
            id=esc_raw["id"],
            texto=esc_raw["texto"],
            final=esc_raw["final"],
            opciones=opciones,
        )
        escenas[escena.id] = escena

    return Historia(
        titulo=datos["titulo"],
        inicio=datos["inicio"],
        variables=dict(datos["variables"]),
        escenas=escenas,
    )
