"""
__init__.py — Paquete motor
Expone la API pública mínima para facilitar las importaciones en pruebas.
"""
from motor.cargador import cargar
from motor.sesion import Sesion
from motor.diagnostico import ErrorValidacion, Diagnostico

__all__ = ["cargar", "Sesion", "ErrorValidacion", "Diagnostico"]
