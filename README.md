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

## Ejecución de las versiones

### Versión 2 (actual)

En la carpeta actual del proyecto, ejecuta:

```bash
# Historia principal, con la función deshacer
python main.py

# Segunda historia (El laboratorio olvidado)
python main.py historias/el_laboratorio_olvidado.json

# Cualquier historia propia
python main.py ruta/a/tu_historia.json
```

### Versión 1 (sin deshacer)

La versión 1 está preservada en el commit `f69bdc7`. Desde la carpeta del repositorio, crea una carpeta de trabajo independiente y ejecútala:

```powershell
git worktree add ..\Parcial_OrozcoZulianys_V1 f69bdc7
Set-Location ..\Parcial_OrozcoZulianys_V1
python main.py
```

El comando `git worktree add` se ejecuta una sola vez. Para volver a la carpeta de la versión 2, regresa a la carpeta original del repositorio y ejecuta `python main.py`. En Windows, si el comando `python` no está disponible, prueba `py main.py`.

| Versión | Carpeta de ejecución | Comportamiento |
|---|---|---|
| V1 | `Parcial_OrozcoZulianys_V1` (worktree del commit `f69bdc7`) | Sin opción para deshacer |
| V2 | Carpeta actual del repositorio | Deshacer disponible para la última elección válida |

Durante la partida el lector elige escribiendo el **número** de la opción o su **id** directamente.
Escribe `salir` en cualquier momento para abandonar.
Después de una elección válida también puede escribir `deshacer` para restaurar la escena y las variables anteriores. El retroceso está disponible una sola vez y se habilita de nuevo al realizar otra elección válida; también se ofrece al llegar a un final.

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

## Comportamiento de la versión 2

- **Deshacer de un nivel:** restaura escena, variables y estado anteriores a la última elección válida. Entradas inválidas no cambian el historial; deshacer lo consume, y reiniciar lo elimina.
- **Sin guardado:** el estado de la partida vive solo en memoria; al cerrar el programa se pierde.
- **Solo condiciones de igualdad booleana:** no se soportan comparaciones numéricas ni expresiones complejas.
- **Ejecución local únicamente:** no requiere conexión a internet.
=======
