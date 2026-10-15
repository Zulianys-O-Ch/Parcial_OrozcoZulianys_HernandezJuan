# Motor de Historias Interactivas — La última transmisión

**Integrantes:**
- Zulianys Liseth Orozco Chavez — T00078330
- Juan David Hernandez Avila — T00081559

---

## Versiones requeridas

| Herramienta | Versión mínima |
|---|---|
| Python | 3.9 |
| pytest | 7.x |

No se requieren dependencias externas adicionales. La librería estándar de Python es suficiente.

---

## Instalación

```bash
# 1. Clonar o descomprimir el repositorio
# 2. (Opcional) Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS

# 3. Instalar pytest
pip install pytest
```

---

## Ejecución del motor

```bash
# Historia principal (La última transmisión)
python main.py

# Segunda historia (El laboratorio olvidado)
python main.py historias/el_laboratorio_olvidado.json

# Cualquier historia propia
python main.py ruta/a/tu_historia.json
```

Durante la partida el lector elige escribiendo el **número** de la opción o su **id** directamente.
Escribe `salir` en cualquier momento para abandonar.

---

## Ejecución de pruebas

```bash
# Desde la raíz del proyecto
pytest pruebas/test_motor.py -v
```

El resultado se guarda redirigiendo la salida:

```bash
pytest pruebas/test_motor.py -v > resultados_pruebas.txt 2>&1
```

---

## Rutas para demostrar los tres finales

| Final | Ruta de decisiones |
|---|---|
| **E4 — Rescate** | E1 → `revisar` → E2 → `investigar` → E3 → `activar_codigo` |
| **E5 — El eco** | E1 → `revisar` → E2 → `continuar` → E3 → `activar_sin_verificar` |
| **E6 — Silencio** | E1 → `revisar` → E2 → cualquiera → E3 → `cortar` |

---

## Formato del contenido (contrato JSON)

```json
{
  "titulo": "Nombre de la historia",
  "inicio": "ID_de_escena_inicial",
  "variables": {
    "nombre_variable": false
  },
  "escenas": [
    {
      "id": "E1",
      "texto": "Texto visible para el lector.",
      "final": false,
      "opciones": [
        {
          "id": "id_opcion",
          "texto": "Etiqueta visible",
          "destino": "E2",
          "condiciones": { "nombre_variable": true },
          "efectos":    { "nombre_variable": false }
        }
      ]
    }
  ]
}
```

**Reglas:**
- `variables`: mapa de booleanos iniciales (`true`/`false`). Los valores no booleanos son rechazados.
- `condiciones` vacío → opción siempre habilitada.
- `efectos` vacío → no cambia ninguna variable.
- Escenas `final: true` deben tener `opciones: []`.
- Escenas `final: false` deben tener al menos una opción.
- Todos los `destino` deben apuntar a IDs de escena existentes.
- Las variables en `condiciones` y `efectos` deben estar declaradas en `variables`.

---

## Limitaciones conocidas

- **Sin retroceso:** las decisiones son irreversibles dentro de una partida. El reinicio es la única forma de volver al inicio. (Conflicto pendiente de resolución con el cliente — ver informe.)
- **Sin guardado:** el estado de la partida vive solo en memoria; al cerrar el programa se pierde.
- **Solo condiciones de igualdad booleana:** no se soportan comparaciones numéricas ni expresiones complejas.
- **Ejecución local únicamente:** no requiere conexión a internet.
=======
# La última transmisión: motor de historias interactivas

Parcial práctico de Ingeniería de Software. El programa de consola interpreta historias interactivas escritas en archivos JSON. Muestra solo las decisiones habilitadas por lo ocurrido, aplica sus consecuencias y valida el archivo antes de jugarlo.

## Integrantes

| Nombre | Código |
|---|---|
| Zulianys Orozco Chavez | T00078330 |
| Juan Hernandez Avila | T00081559 |
