"""
validador.py — Validación previa de la estructura de una historia
Cubre las nueve categorías de error exigidas por RF6.1 y la guía:
  1. Archivo ilegible o sin campos obligatorios
  2. Escena inicial inexistente
  3. IDs de escenas repetidos
  4. IDs de opciones repetidos dentro de una escena
  5. Destinos inexistentes
  6. Variables no declaradas en condiciones o efectos
  7. Valores no booleanos (variables, condiciones o efectos)
  8. Escenas finales con opciones / no finales sin opciones
  9. Valores iniciales del mapa 'variables' no booleanos
"""
from typing import Any, Dict, List

from motor.diagnostico import Diagnostico, ErrorValidacion


# ── helpers ──────────────────────────────────────────────────────────────────

def _es_bool(valor: Any) -> bool:
    return isinstance(valor, bool)


def _validar_mapa_booleano(
    mapa: Dict,
    variables_declaradas: set,
    contexto: str,
    id_escena: str,
    id_opcion: str,
    errores: List[Diagnostico],
) -> None:
    """Comprueba que todas las claves estén declaradas y los valores sean bool."""
    for clave, valor in mapa.items():
        if clave not in variables_declaradas:
            errores.append(Diagnostico(
                causa=f"Variable no declarada en {contexto}: '{clave}'",
                id_escena=id_escena,
                id_opcion=id_opcion,
                campo=contexto,
            ))
        if not _es_bool(valor):
            errores.append(Diagnostico(
                causa=f"Valor no booleano en {contexto}: '{clave}' = {valor!r}",
                id_escena=id_escena,
                id_opcion=id_opcion,
                campo=contexto,
            ))


# ── función principal ─────────────────────────────────────────────────────────

def validar(datos: Dict) -> None:
    """
    Valida el diccionario 'datos' cargado desde JSON.
    Lanza ErrorValidacion con todos los errores encontrados si hay al menos uno.
    No lanza excepción si el diccionario es válido.
    """
    errores: List[Diagnostico] = []

    # ── Campos obligatorios de la historia ────────────────────────────────────
    for campo in ("titulo", "inicio", "variables", "escenas"):
        if campo not in datos:
            errores.append(Diagnostico(
                causa=f"Campo obligatorio ausente en la historia",
                campo=campo,
            ))

    if errores:
        raise ErrorValidacion(errores)

    # ── Variables iniciales deben ser booleanas ───────────────────────────────
    variables: Dict = datos.get("variables", {})
    variables_declaradas: set = set(variables.keys())

    for nombre, valor in variables.items():
        if not _es_bool(valor):
            errores.append(Diagnostico(
                causa=f"Valor inicial no booleano en 'variables': '{nombre}' = {valor!r}",
                campo="variables",
            ))

    # ── Lista de escenas ──────────────────────────────────────────────────────
    escenas_raw: list = datos.get("escenas", [])
    if not isinstance(escenas_raw, list):
        errores.append(Diagnostico(causa="'escenas' debe ser una lista", campo="escenas"))
        raise ErrorValidacion(errores)

    ids_escenas: Dict[str, int] = {}   # id → primera posición
    for idx, escena in enumerate(escenas_raw):
        if not isinstance(escena, dict):
            errores.append(Diagnostico(
                causa=f"La escena en posición {idx} no es un objeto",
                campo="escenas",
            ))
            continue

        # Campos obligatorios de cada escena
        for campo in ("id", "texto", "final", "opciones"):
            if campo not in escena:
                errores.append(Diagnostico(
                    causa=f"Campo obligatorio ausente en escena",
                    id_escena=escena.get("id", f"posición {idx}"),
                    campo=campo,
                ))

        id_esc = escena.get("id", f"posición_{idx}")

        # IDs de escenas duplicados
        if id_esc in ids_escenas:
            errores.append(Diagnostico(
                causa=f"ID de escena duplicado",
                id_escena=id_esc,
                campo="id",
            ))
        else:
            ids_escenas[id_esc] = idx

        # final debe ser booleano
        final = escena.get("final")
        if not isinstance(final, bool):
            errores.append(Diagnostico(
                causa=f"El campo 'final' no es booleano",
                id_escena=id_esc,
                campo="final",
            ))

        # opciones
        opciones_raw = escena.get("opciones", [])
        if not isinstance(opciones_raw, list):
            errores.append(Diagnostico(
                causa="'opciones' debe ser una lista",
                id_escena=id_esc,
                campo="opciones",
            ))
            continue

        es_final = escena.get("final", False)

        # Escena final con opciones
        if es_final and len(opciones_raw) > 0:
            errores.append(Diagnostico(
                causa="Escena final debe tener cero opciones",
                id_escena=id_esc,
                campo="opciones",
            ))

        # Escena no final sin opciones
        if not es_final and len(opciones_raw) == 0:
            errores.append(Diagnostico(
                causa="Escena no final debe tener al menos una opción",
                id_escena=id_esc,
                campo="opciones",
            ))

        # Revisar cada opción
        ids_opciones_en_escena: Dict[str, int] = {}
        for jdx, opcion in enumerate(opciones_raw):
            if not isinstance(opcion, dict):
                errores.append(Diagnostico(
                    causa=f"La opción en posición {jdx} no es un objeto",
                    id_escena=id_esc,
                ))
                continue

            for campo in ("id", "texto", "destino", "condiciones", "efectos"):
                if campo not in opcion:
                    errores.append(Diagnostico(
                        causa=f"Campo obligatorio ausente en opción",
                        id_escena=id_esc,
                        id_opcion=opcion.get("id", f"posición {jdx}"),
                        campo=campo,
                    ))

            id_opc = opcion.get("id", f"posición_{jdx}")

            # IDs de opciones duplicados dentro de la escena
            if id_opc in ids_opciones_en_escena:
                errores.append(Diagnostico(
                    causa="ID de opción duplicado dentro de la escena",
                    id_escena=id_esc,
                    id_opcion=id_opc,
                    campo="id",
                ))
            else:
                ids_opciones_en_escena[id_opc] = jdx

            # Validar condiciones y efectos
            condiciones = opcion.get("condiciones", {})
            efectos = opcion.get("efectos", {})

            if isinstance(condiciones, dict):
                _validar_mapa_booleano(
                    condiciones, variables_declaradas,
                    "condiciones", id_esc, id_opc, errores,
                )
            else:
                errores.append(Diagnostico(
                    causa="'condiciones' debe ser un objeto",
                    id_escena=id_esc, id_opcion=id_opc, campo="condiciones",
                ))

            if isinstance(efectos, dict):
                _validar_mapa_booleano(
                    efectos, variables_declaradas,
                    "efectos", id_esc, id_opc, errores,
                )
            else:
                errores.append(Diagnostico(
                    causa="'efectos' debe ser un objeto",
                    id_escena=id_esc, id_opcion=id_opc, campo="efectos",
                ))

    # ── Escena inicial existe ─────────────────────────────────────────────────
    inicio: str = datos.get("inicio", "")
    if inicio not in ids_escenas:
        errores.append(Diagnostico(
            causa=f"La escena de inicio no existe",
            campo="inicio",
            id_escena=inicio,
        ))

    # ── Destinos inexistentes ─────────────────────────────────────────────────
    for escena in escenas_raw:
        if not isinstance(escena, dict):
            continue
        id_esc = escena.get("id", "?")
        for opcion in escena.get("opciones", []):
            if not isinstance(opcion, dict):
                continue
            destino = opcion.get("destino", "")
            id_opc = opcion.get("id", "?")
            if destino not in ids_escenas:
                errores.append(Diagnostico(
                    causa=f"Destino inexistente: '{destino}'",
                    id_escena=id_esc,
                    id_opcion=id_opc,
                    campo="destino",
                ))

    if errores:
        raise ErrorValidacion(errores)
