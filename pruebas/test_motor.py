"""
pruebas/test_motor.py — Pruebas automatizadas del motor de historias

Cubre los seis escenarios exigidos por la guía:
  U1 — Condiciones habilitan / deshabilitan opciones correctamente
  U2 — Elección válida aplica efectos y avanza al destino correcto
  U3 — Opción inexistente o no habilitada no altera el estado
  U4 — Errores de contenido producen rechazo controlado (parametrizados)
  U5 — Reiniciar restaura la escena y las variables iniciales
  I1 — Carga de archivo real + decisiones hasta alcanzar un final

Ejecutar con:
    pytest pruebas/test_motor.py -v
"""
import copy
import json
import os
import tempfile

import pytest

from motor import cargar, Sesion, ErrorValidacion
from motor.dominio import Escena, Historia, Opcion
from motor.validador import validar


# ════════════════════════════════════════════════════════════════════════════
# Utilidades de construcción de historias de prueba
# ════════════════════════════════════════════════════════════════════════════

def _historia_minima(**kwargs) -> dict:
    """Devuelve un diccionario JSON válido con una historia mínima."""
    base = {
        "titulo": "Historia de prueba",
        "inicio": "E1",
        "variables": {"bandera": False},
        "escenas": [
            {
                "id": "E1",
                "texto": "Escena inicial",
                "final": False,
                "opciones": [
                    {
                        "id": "avanzar",
                        "texto": "Avanzar",
                        "destino": "E2",
                        "condiciones": {},
                        "efectos": {"bandera": True},
                    }
                ],
            },
            {
                "id": "E2",
                "texto": "Escena final",
                "final": True,
                "opciones": [],
            },
        ],
    }
    base.update(kwargs)
    return base


def _sesion_desde_historia(historia_obj: Historia) -> Sesion:
    return Sesion(historia_obj)


def _sesion_minima() -> Sesion:
    """Sesión construida desde un modelo de dominio directo (sin archivo)."""
    historia = Historia(
        titulo="Test",
        inicio="E1",
        variables={"bandera": False},
        escenas={
            "E1": Escena(
                id="E1",
                texto="Escena 1",
                final=False,
                opciones=[
                    Opcion(
                        id="avanzar",
                        texto="Avanzar",
                        destino="E2",
                        condiciones={},
                        efectos={"bandera": True},
                    )
                ],
            ),
            "E2": Escena(id="E2", texto="Escena 2", final=True, opciones=[]),
        },
    )
    return Sesion(historia)


def _historia_con_condicion() -> Sesion:
    """
    Historia con dos opciones en E1:
      - 'libre'     : sin condición
      - 'restringida': requiere bandera=True
    """
    historia = Historia(
        titulo="Test condición",
        inicio="E1",
        variables={"bandera": False},
        escenas={
            "E1": Escena(
                id="E1",
                texto="Escena con condición",
                final=False,
                opciones=[
                    Opcion(
                        id="libre",
                        texto="Opción libre",
                        destino="E2",
                        condiciones={},
                        efectos={},
                    ),
                    Opcion(
                        id="restringida",
                        texto="Opción restringida",
                        destino="E2",
                        condiciones={"bandera": True},
                        efectos={},
                    ),
                ],
            ),
            "E2": Escena(id="E2", texto="Final", final=True, opciones=[]),
        },
    )
    return Sesion(historia)


# ════════════════════════════════════════════════════════════════════════════
# U1 — Condiciones habilitan / deshabilitan opciones
# ════════════════════════════════════════════════════════════════════════════

class TestU1Condiciones:
    def test_opcion_sin_condicion_siempre_habilitada(self):
        sesion = _historia_con_condicion()
        ids = {o.id for o in sesion.opciones_habilitadas()}
        assert "libre" in ids

    def test_opcion_con_condicion_falsa_no_habilitada(self):
        sesion = _historia_con_condicion()
        # bandera=False → 'restringida' NO debe aparecer
        ids = {o.id for o in sesion.opciones_habilitadas()}
        assert "restringida" not in ids

    def test_opcion_con_condicion_verdadera_habilitada(self):
        sesion = _historia_con_condicion()
        sesion.estado.variables["bandera"] = True
        ids = {o.id for o in sesion.opciones_habilitadas()}
        assert "restringida" in ids

    def test_ca01_la_ultima_transmision(self):
        """CA01 de la guía: E3 con conoce_origen=True muestra activar_codigo y cortar."""
        historia = cargar("historias/la_ultima_transmision.json")
        sesion = Sesion(historia)
        # E1 → revisar → E2
        sesion.elegir("revisar")
        # E2 → investigar → E3 (conoce_origen=True)
        sesion.elegir("investigar")
        assert sesion.estado.variables["conoce_origen"] is True
        assert sesion.estado.escena_actual == "E3"
        ids = {o.id for o in sesion.opciones_habilitadas()}
        assert "activar_codigo" in ids
        assert "cortar" in ids
        assert "activar_sin_verificar" not in ids


# ════════════════════════════════════════════════════════════════════════════
# U2 — Elección válida aplica efectos y avanza al destino
# ════════════════════════════════════════════════════════════════════════════

class TestU2EleccionValida:
    def test_avanza_al_destino_correcto(self):
        sesion = _sesion_minima()
        exito, _ = sesion.elegir("avanzar")
        assert exito
        assert sesion.estado.escena_actual == "E2"

    def test_aplica_efectos(self):
        sesion = _sesion_minima()
        assert sesion.estado.variables["bandera"] is False
        sesion.elegir("avanzar")
        assert sesion.estado.variables["bandera"] is True

    def test_detecta_final_tras_avanzar(self):
        sesion = _sesion_minima()
        sesion.elegir("avanzar")
        assert sesion.estado.terminada is True

    def test_ca02_activar_sin_verificar_lleva_a_e5(self):
        """CA02: E3 sin conoce_origen → activar_sin_verificar lleva a E5."""
        historia = cargar("historias/la_ultima_transmision.json")
        sesion = Sesion(historia)
        sesion.elegir("revisar")
        sesion.elegir("continuar")          # conoce_origen sigue False
        assert sesion.estado.variables["conoce_origen"] is False
        exito, _ = sesion.elegir("activar_sin_verificar")
        assert exito
        assert sesion.estado.escena_actual == "E5"


# ════════════════════════════════════════════════════════════════════════════
# U3 — Opción inválida o no habilitada NO altera el estado
# ════════════════════════════════════════════════════════════════════════════

class TestU3OpcionInvalida:
    def test_opcion_inexistente_devuelve_falso(self):
        sesion = _sesion_minima()
        exito, msg = sesion.elegir("no_existe")
        assert exito is False
        assert msg is not None

    def test_estado_intacto_tras_opcion_inexistente(self):
        sesion = _sesion_minima()
        escena_antes = sesion.estado.escena_actual
        vars_antes = copy.deepcopy(sesion.estado.variables)
        sesion.elegir("no_existe")
        assert sesion.estado.escena_actual == escena_antes
        assert sesion.estado.variables == vars_antes

    def test_opcion_no_habilitada_devuelve_falso(self):
        """CA02 negativo: intentar activar_codigo sin conoce_origen debe fallar."""
        historia = cargar("historias/la_ultima_transmision.json")
        sesion = Sesion(historia)
        sesion.elegir("revisar")
        sesion.elegir("continuar")   # conoce_origen=False
        exito, _ = sesion.elegir("activar_codigo")
        assert exito is False

    def test_estado_intacto_tras_opcion_no_habilitada(self):
        historia = cargar("historias/la_ultima_transmision.json")
        sesion = Sesion(historia)
        sesion.elegir("revisar")
        sesion.elegir("continuar")
        vars_antes = copy.deepcopy(sesion.estado.variables)
        sesion.elegir("activar_codigo")
        assert sesion.estado.variables == vars_antes
        assert sesion.estado.escena_actual == "E3"


# ════════════════════════════════════════════════════════════════════════════
# U4 — Errores de contenido producen rechazo controlado (parametrizados)
# ════════════════════════════════════════════════════════════════════════════

def _json_temp(datos: dict) -> str:
    """Escribe datos en un archivo temporal y devuelve su ruta."""
    fd, ruta = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False)
    return ruta


CASOS_ERROR = [
    # (descripcion, mutación sobre _historia_minima())
    ("archivo_ilegible",             None),          # manejado aparte
    ("campo_titulo_ausente",         {"titulo": None}),
    ("inicio_inexistente",           {"inicio": "NO_EXISTE"}),
    ("id_escena_duplicado",          None),           # manejado aparte
    ("destino_inexistente",          None),           # manejado aparte
    ("variable_no_declarada",        None),           # manejado aparte
    ("valor_no_booleano_variables",  None),           # manejado aparte
    ("escena_final_con_opciones",    None),           # manejado aparte
    ("escena_no_final_sin_opciones", None),           # manejado aparte
]


class TestU4Validacion:
    def test_archivo_ilegible(self):
        with pytest.raises(ErrorValidacion) as exc:
            cargar("ruta/que/no/existe.json")
        assert exc.value.diagnosticos

    def test_campo_obligatorio_ausente(self):
        datos = _historia_minima()
        del datos["titulo"]
        ruta = _json_temp(datos)
        try:
            with pytest.raises(ErrorValidacion):
                cargar(ruta)
        finally:
            os.unlink(ruta)

    def test_inicio_inexistente(self):
        datos = _historia_minima()
        datos["inicio"] = "NO_EXISTE"
        ruta = _json_temp(datos)
        try:
            with pytest.raises(ErrorValidacion) as exc:
                cargar(ruta)
            causas = " ".join(str(d) for d in exc.value.diagnosticos)
            assert "NO_EXISTE" in causas or "inicio" in causas.lower()
        finally:
            os.unlink(ruta)

    def test_id_escena_duplicado(self):
        datos = _historia_minima()
        # Duplicar el id de E1
        datos["escenas"][1]["id"] = "E1"
        ruta = _json_temp(datos)
        try:
            with pytest.raises(ErrorValidacion):
                cargar(ruta)
        finally:
            os.unlink(ruta)

    def test_destino_inexistente(self):
        """CA03 de la guía."""
        datos = _historia_minima()
        datos["escenas"][0]["opciones"][0]["destino"] = "E99"
        ruta = _json_temp(datos)
        try:
            with pytest.raises(ErrorValidacion) as exc:
                cargar(ruta)
            causas = " ".join(str(d) for d in exc.value.diagnosticos)
            assert "E99" in causas
        finally:
            os.unlink(ruta)

    def test_variable_no_declarada(self):
        datos = _historia_minima()
        datos["escenas"][0]["opciones"][0]["condiciones"] = {"no_declarada": True}
        ruta = _json_temp(datos)
        try:
            with pytest.raises(ErrorValidacion):
                cargar(ruta)
        finally:
            os.unlink(ruta)

    def test_valor_no_booleano_en_variables(self):
        datos = _historia_minima()
        datos["variables"]["bandera"] = "si"   # string en vez de bool
        ruta = _json_temp(datos)
        try:
            with pytest.raises(ErrorValidacion):
                cargar(ruta)
        finally:
            os.unlink(ruta)

    def test_escena_final_con_opciones(self):
        datos = _historia_minima()
        datos["escenas"][1]["opciones"] = [
            {"id": "x", "texto": "X", "destino": "E1", "condiciones": {}, "efectos": {}}
        ]
        ruta = _json_temp(datos)
        try:
            with pytest.raises(ErrorValidacion):
                cargar(ruta)
        finally:
            os.unlink(ruta)

    def test_escena_no_final_sin_opciones(self):
        datos = _historia_minima()
        datos["escenas"][0]["opciones"] = []
        ruta = _json_temp(datos)
        try:
            with pytest.raises(ErrorValidacion):
                cargar(ruta)
        finally:
            os.unlink(ruta)

    def test_id_opcion_duplicado_en_escena(self):
        datos = _historia_minima()
        datos["escenas"][0]["opciones"].append(
            copy.deepcopy(datos["escenas"][0]["opciones"][0])
        )  # duplica el id 'avanzar'
        ruta = _json_temp(datos)
        try:
            with pytest.raises(ErrorValidacion):
                cargar(ruta)
        finally:
            os.unlink(ruta)


# ════════════════════════════════════════════════════════════════════════════
# U5 — Reiniciar restaura escena y variables iniciales
# ════════════════════════════════════════════════════════════════════════════

class TestU5Reinicio:
    def test_reinicio_restaura_escena(self):
        sesion = _sesion_minima()
        sesion.elegir("avanzar")
        assert sesion.estado.escena_actual == "E2"
        sesion.reiniciar()
        assert sesion.estado.escena_actual == "E1"

    def test_reinicio_restaura_variables(self):
        sesion = _sesion_minima()
        sesion.elegir("avanzar")
        assert sesion.estado.variables["bandera"] is True
        sesion.reiniciar()
        assert sesion.estado.variables["bandera"] is False

    def test_reinicio_limpia_estado_terminado(self):
        sesion = _sesion_minima()
        sesion.elegir("avanzar")
        assert sesion.estado.terminada is True
        sesion.reiniciar()
        assert sesion.estado.terminada is False

    def test_reinicio_no_afecta_historia_original(self):
        """Las variables de Historia no deben mutar entre sesiones."""
        historia = cargar("historias/la_ultima_transmision.json")
        sesion = Sesion(historia)
        sesion.elegir("revisar")
        sesion.elegir("investigar")
        sesion.reiniciar()
        # La historia en sí no debe haber cambiado
        assert historia.variables["conoce_origen"] is False

    def test_reinicio_elimina_historial_de_deshacer(self):
        sesion = _sesion_minima()
        sesion.elegir("avanzar")
        assert sesion.puede_deshacer
        sesion.reiniciar()
        assert not sesion.puede_deshacer
        assert not sesion.deshacer()
        assert sesion.estado.escena_actual == "E1"


# U6 — Deshacer restaura estado y consume el único nivel disponible
class TestU6Deshacer:
    def test_deshacer_restaura_escena_variables_y_se_consume(self):
        sesion = _sesion_minima()
        assert not sesion.puede_deshacer
        sesion.elegir("avanzar")
        assert sesion.estado.escena_actual == "E2"
        assert sesion.estado.variables["bandera"] is True
        assert sesion.deshacer()
        assert sesion.estado.escena_actual == "E1"
        assert sesion.estado.variables["bandera"] is False
        assert not sesion.puede_deshacer
        assert not sesion.deshacer()

    def test_entrada_invalida_preserva_historial(self):
        sesion = _historia_con_condicion()
        sesion.elegir("libre")
        estado = copy.deepcopy(sesion.estado)
        exito, _ = sesion.elegir("inexistente")
        assert not exito
        assert sesion.estado == estado
        assert sesion.puede_deshacer
        assert sesion.deshacer()
        assert sesion.estado.escena_actual == "E1"

    def test_opcion_deshabilitada_preserva_historial(self):
        sesion = Sesion(cargar("historias/la_ultima_transmision.json"))
        sesion.elegir("revisar")
        sesion.elegir("continuar")
        assert sesion.estado.escena_actual == "E3"
        exito, _ = sesion.elegir("activar_codigo")  # requiere conoce_origen=True
        assert not exito
        assert sesion.puede_deshacer
        assert sesion.deshacer()
        assert sesion.estado.escena_actual == "E2"
        assert sesion.estado.variables["conoce_origen"] is False

    def test_nueva_eleccion_valida_habilita_otro_deshacer(self):
        sesion = _historia_con_condicion()
        sesion.elegir("libre")
        sesion.deshacer()
        sesion.elegir("libre")
        assert sesion.puede_deshacer
        assert sesion.deshacer()
        assert sesion.estado.escena_actual == "E1"
        assert sesion.estado.variables["bandera"] is False


# ════════════════════════════════════════════════════════════════════════════
# I1 — Integración: carga de archivo real + flujo completo hasta un final
# ════════════════════════════════════════════════════════════════════════════

class TestI1Integracion:
    def test_final_e4_rescate(self):
        """Ruta E1→E2(investigar)→E3(activar_codigo)→E4."""
        historia = cargar("historias/la_ultima_transmision.json")
        sesion = Sesion(historia)
        assert sesion.estado.escena_actual == "E1"

        sesion.elegir("revisar")
        assert sesion.estado.escena_actual == "E2"

        sesion.elegir("investigar")
        assert sesion.estado.escena_actual == "E3"
        assert sesion.estado.variables["conoce_origen"] is True

        exito, _ = sesion.elegir("activar_codigo")
        assert exito
        assert sesion.estado.escena_actual == "E4"
        assert sesion.estado.terminada is True
        assert sesion.estado.variables["confia_en_la_voz"] is True

    def test_final_e5_eco(self):
        """Ruta E1→E2(continuar)→E3(activar_sin_verificar)→E5."""
        historia = cargar("historias/la_ultima_transmision.json")
        sesion = Sesion(historia)
        sesion.elegir("revisar")
        sesion.elegir("continuar")
        sesion.elegir("activar_sin_verificar")
        assert sesion.estado.escena_actual == "E5"
        assert sesion.estado.terminada is True

    def test_final_e6_silencio(self):
        """Ruta E1→E2(*)→E3(cortar)→E6."""
        historia = cargar("historias/la_ultima_transmision.json")
        sesion = Sesion(historia)
        sesion.elegir("revisar")
        sesion.elegir("continuar")
        sesion.elegir("cortar")
        assert sesion.estado.escena_actual == "E6"
        assert sesion.estado.terminada is True
        assert sesion.estado.variables["confia_en_la_voz"] is False

    @pytest.mark.parametrize("eleccion_final, escena_final", [
        ("activar_codigo", "E4"),
        ("activar_sin_verificar", "E5"),
        ("cortar", "E6"),
    ])
    def test_deshacer_final_devuelve_a_e3(self, eleccion_final, escena_final):
        historia = cargar("historias/la_ultima_transmision.json")
        sesion = Sesion(historia)
        sesion.elegir("revisar")
        sesion.elegir("investigar" if eleccion_final == "activar_codigo" else "continuar")
        valores_previos = copy.deepcopy(sesion.estado.variables)
        sesion.elegir(eleccion_final)
        assert sesion.estado.escena_actual == escena_final
        assert sesion.estado.terminada
        assert sesion.deshacer()
        assert sesion.estado.escena_actual == "E3"
        assert sesion.estado.variables == valores_previos
        assert not sesion.estado.terminada

    def test_segunda_historia_sin_modificar_motor(self):
        """RNF01: la segunda historia carga y se juega sin tocar el motor."""
        historia = cargar("historias/el_laboratorio_olvidado.json")
        sesion = Sesion(historia)
        assert sesion.estado.escena_actual == "L1"
        sesion.elegir("abrir_caja")
        assert sesion.estado.variables["tiene_llave"] is True
        sesion.elegir("usar_llave")
        assert sesion.estado.escena_actual == "L3"
        assert sesion.estado.terminada is True
