"""
main.py — Punto de entrada del programa
Uso:
    python main.py                              # carga la historia por defecto
    python main.py historias/otra_historia.json # carga una historia alternativa
"""
import sys
from motor.interfaz import iniciar

HISTORIA_POR_DEFECTO = "historias/la_ultima_transmision.json"

if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else HISTORIA_POR_DEFECTO
    iniciar(ruta)
