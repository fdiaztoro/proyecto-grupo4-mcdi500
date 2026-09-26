"""Ejecuta con pytest las pruebas por clase de tests/casos_por_clase.py.

pytest solo recoge archivos cuyo nombre empieza con "test_". Este archivo
prepara las rutas (src/ para las clases del proyecto y tests/ para
casos_por_clase) y entrega a pytest cada prueba registrada por separado, para
que el resultado muestre cada una con su clase y escenario, y se puedan filtrar
(por ejemplo: python -m pytest tests/ -k CodificadorOneHot).

Desde el notebook, las mismas pruebas se ejecutan con ejecutar_pruebas(), que
devuelve el informe en tabla.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from casos_por_clase import PRUEBAS


@pytest.mark.parametrize(
    "registro", PRUEBAS,
    ids=lambda r: f"{r['clase']}-{r['escenario']}-{r['funcion'].__name__.lstrip('_')}",
)
def test_caso(registro):
    """Ejecuta una de las pruebas registradas; pytest la muestra con su clase y escenario."""
    registro["funcion"]()
