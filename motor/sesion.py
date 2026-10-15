"""
sesion.py — Gestor de sesión y motor de historias (RF2–RF5)
Responsabilidades:
  - Mantener el estado mutable de la partida (escena actual + variables)
  - Evaluar condiciones de cada opción y filtrar las habilitadas (RF2.2)
  - Aplicar efectos y avanzar al destino correcto (RF3.1, RF4.1)
  - Rechazar entradas inválidas o no habilitadas sin alterar el estado (RF3.2)
  - Detectar finales y bloqueos (RF5.1, RF5.3)
  - Reiniciar la sesión a los valores iniciales (RF5.2)
"""
import copy
from typing import Dict, List, Optional, Tuple

from motor.dominio import EstadoSesion, Historia, Opcion


class Sesion:
    """Controla el ciclo de vida de una partida."""

    def __init__(self, historia: Historia) -> None:
        self._historia = historia
        self._estado = self._estado_inicial()

    # ── Estado ────────────────────────────────────────────────────────────────

    def _estado_inicial(self) -> EstadoSesion:
        return EstadoSesion(
            escena_actual=self._historia.inicio,
            variables=copy.deepcopy(self._historia.variables),
        )

    def reiniciar(self) -> None:
        """RF5.2 — Restaura escena y variables al estado original."""
        self._estado = self._estado_inicial()

    # ── Consultas ─────────────────────────────────────────────────────────────

    @property
    def estado(self) -> EstadoSesion:
        return self._estado

    @property
    def escena_actual(self):
        return self._historia.escenas[self._estado.escena_actual]

    def opciones_habilitadas(self) -> List[Opcion]:
        """
        RF2.2 — Devuelve solo las opciones cuyas condiciones se cumplen
        en el estado actual de las variables.
        Un mapa de condiciones vacío habilita la opción automáticamente.
        """
        if self._estado.terminada or self._estado.bloqueada:
            return []

        escena = self.escena_actual
        habilitadas = []
        for opcion in escena.opciones:
            if self._condiciones_cumplidas(opcion.condiciones):
                habilitadas.append(opcion)
        return habilitadas

    def _condiciones_cumplidas(self, condiciones: Dict[str, bool]) -> bool:
        for variable, valor_esperado in condiciones.items():
            if self._estado.variables.get(variable) != valor_esperado:
                return False
        return True

    # ── Avance ────────────────────────────────────────────────────────────────

    def elegir(self, id_opcion: str) -> Tuple[bool, Optional[str]]:
        """
        RF3.1, RF3.2, RF4.1 — Intenta ejecutar la opción con el ID dado.

        Retorna (éxito: bool, mensaje_error: Optional[str]).
          - Si la opción no existe o no está habilitada, retorna (False, mensaje).
            El estado de la partida queda INTACTO.
          - Si la opción es válida, aplica efectos, avanza y actualiza el estado.
        """
        if self._estado.terminada:
            return False, "La partida ha terminado. Puedes reiniciar."
        if self._estado.bloqueada:
            return False, "La partida está bloqueada. Debes reiniciar."

        habilitadas = {opc.id: opc for opc in self.opciones_habilitadas()}

        if id_opcion not in habilitadas:
            # Verificar si existe pero no está habilitada
            escena = self.escena_actual
            existe = any(opc.id == id_opcion for opc in escena.opciones)
            if existe:
                return False, f"La opción '{id_opcion}' existe pero no está habilitada en este momento."
            return False, f"La opción '{id_opcion}' no existe en esta escena."

        opcion = habilitadas[id_opcion]

        # Aplicar efectos (RF4.1)
        for variable, valor in opcion.efectos.items():
            self._estado.variables[variable] = valor

        # Avanzar al destino (RF3.1)
        self._estado.escena_actual = opcion.destino

        # Detectar final o bloqueo en la nueva escena (RF5.1, RF5.3)
        self._actualizar_estado()

        return True, None

    def _actualizar_estado(self) -> None:
        """Detecta si la escena nueva es final o produce bloqueo."""
        escena = self.escena_actual
        if escena.final:
            self._estado.terminada = True
            return

        # Bloqueo: escena no final sin opciones habilitadas
        habilitadas = [
            opc for opc in escena.opciones
            if self._condiciones_cumplidas(opc.condiciones)
        ]
        if not habilitadas:
            self._estado.bloqueada = True
