"""Configuración de pytest: asegura que el paquete `logica` (namespace
package sin __init__.py) sea importable desde la raíz del proyecto al
ejecutar `pytest` desde cualquier directorio."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
