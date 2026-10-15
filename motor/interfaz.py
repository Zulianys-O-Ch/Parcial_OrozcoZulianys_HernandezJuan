"""
interfaz.py — Capa de presentación por consola
Responsabilidad única: mostrar información al lector y leer sus entradas.
No contiene lógica de negocio; delega todo al Gestor de sesión.
"""
import sys
from motor.cargador import cargar
from motor.diagnostico import ErrorValidacion
from motor.sesion import Sesion

# ── Utilidades de presentación ────────────────────────────────────────────────

SEPARADOR = "─" * 60


def _limpiar():
    print()


def _titulo(texto: str):
    print(SEPARADOR)
    print(f"  {texto}")
    print(SEPARADOR)


def _mostrar_escena(sesion: Sesion):
    escena = sesion.escena_actual
    print(f"\n📍 Escena [{escena.id}]")
    print(f"\n{escena.texto}\n")


def _mostrar_opciones(opciones):
    if not opciones:
        return
    print("¿Qué decides?")
    for i, opc in enumerate(opciones, 1):
        print(f"  {i}. {opc.texto}  (id: {opc.id})")
    print()


def _mostrar_variables(sesion: Sesion):
    vars_ = sesion.estado.variables
    if vars_:
        estado_vars = ", ".join(
            f"{k}={'sí' if v else 'no'}" for k, v in vars_.items()
        )
        print(f"  [Estado: {estado_vars}]")


# ── Bucle principal ───────────────────────────────────────────────────────────

def _bucle_partida(sesion: Sesion):
    """Ejecuta una partida completa hasta final, bloqueo o salida."""
    while True:
        _limpiar()
        _mostrar_escena(sesion)
        _mostrar_variables(sesion)

        # Final detectado
        if sesion.estado.terminada:
            print("══ FIN DEL RECORRIDO ══")
            print("Has alcanzado un desenlace.\n")
            if sesion.puede_deshacer:
                accion = input("Escribe 'deshacer' para volver a la escena anterior o Enter para continuar: ").strip().lower()
                if accion == "deshacer":
                    sesion.deshacer()
                    continue
            return

        # Bloqueo detectado
        if sesion.estado.bloqueada:
            print("⚠  BLOQUEO: ninguna opción está disponible en este momento.")
            print("   El relato no puede continuar desde aquí.\n")
            if sesion.puede_deshacer:
                accion = input("Escribe 'deshacer' para volver a la escena anterior o Enter para continuar: ").strip().lower()
                if accion == "deshacer":
                    sesion.deshacer()
                    continue
            return

        opciones = sesion.opciones_habilitadas()
        _mostrar_opciones(opciones)

        ids_validos = {opc.id for opc in opciones}
        numeros_validos = {str(i): opc.id for i, opc in enumerate(opciones, 1)}

        ayuda_deshacer = " o 'deshacer'" if sesion.puede_deshacer else ""
        entrada = input(f"Elige (número o id{ayuda_deshacer}, 'salir' para abandonar): ").strip()

        if entrada.lower() == "deshacer":
            if sesion.deshacer():
                continue

        if entrada.lower() == "salir":
            print("\nSaliendo de la partida.")
            sys.exit(0)

        # Aceptar número o id directamente
        if entrada in numeros_validos:
            id_elegido = numeros_validos[entrada]
        else:
            id_elegido = entrada

        exito, mensaje = sesion.elegir(id_elegido)
        if not exito:
            print(f"\n⚠  {mensaje}")
            input("  Presiona Enter para continuar...")


def _menu_reinicio(sesion: Sesion):
    """Pregunta si el lector quiere jugar de nuevo."""
    while True:
        resp = input("¿Deseas jugar otra vez? (s/n): ").strip().lower()
        if resp == "s":
            sesion.reiniciar()
            return True
        if resp == "n":
            return False
        print("  Por favor escribe 's' o 'n'.")


# ── Punto de entrada ──────────────────────────────────────────────────────────

def iniciar(ruta_historia: str):
    """Carga la historia y lanza el bucle principal."""
    print(SEPARADOR)
    print("  MOTOR DE HISTORIAS INTERACTIVAS")
    print(SEPARADOR)
    print(f"\nCargando: {ruta_historia}\n")

    try:
        historia = cargar(ruta_historia)
    except ErrorValidacion as exc:
        print("❌ ERROR — La historia no pudo cargarse:\n")
        for diag in exc.diagnosticos:
            print(f"  • {diag}")
        print()
        sys.exit(1)

    _titulo(historia.titulo)
    sesion = Sesion(historia)

    while True:
        _bucle_partida(sesion)
        if not _menu_reinicio(sesion):
            print("\n¡Hasta la próxima!\n")
            break
