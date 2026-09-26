import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

texto_explicacion = """### 8.1 Cohesión y acoplamiento

Cada módulo de `src/` tiene una única responsabilidad: `transformador.py` define el contrato común (`ajustar()`, `transformar()`, `ajustar_transformar()`); `imputadores.py` resuelve exclusivamente el tratamiento de valores faltantes; `transformadores.py` resuelve codificación, escalamiento y las dos transformaciones de limpieza final; `pipeline.py` solo orquesta una secuencia de pasos, sin saber qué hace cada uno. Esta separación por responsabilidad es alta cohesión: cada módulo agrupa código que cambia por el mismo motivo (McConnell, 2004).

El acoplamiento entre estos módulos es bajo porque la única dependencia real entre ellos es la interfaz de `Transformador`. Esto se puede comprobar directamente en el código, en lugar de solo describirlo:
"""

codigo_demostracion = """from src.imputadores import MarcadorNoRespuesta, EliminadorFilasNulas, ImputadorFlexible
from src.transformadores import CodificadorOneHot, EscaladorEstandar, EliminadorColumna, ConvertidorEntero

pasos_del_pipeline = [
    MarcadorNoRespuesta, EliminadorFilasNulas, ImputadorFlexible,
    EliminadorColumna, ConvertidorEntero, CodificadorOneHot, EscaladorEstandar,
]

for clase in pasos_del_pipeline:
    base = clase.__bases__[0].__name__
    print(f"{clase.__name__:<22} hereda de {base}")

print()
codigo_pipeline = open("src/pipeline.py").read()
conoce_a_los_pasos = "imputadores" in codigo_pipeline or "transformadores" in codigo_pipeline
print("¿pipeline.py importa alguna de estas clases directamente?", conoce_a_los_pasos)
"""

texto_cierre = """Todas las clases heredan de `Transformador`, sin importar en qué módulo estén definidas. `Pipeline` no necesita conocer estos módulos: basta con que cada objeto que recibe cumpla el contrato de la clase base. Este es el mismo principio que sostiene el patrón Strategy usado en la imputación (sección 7): el código que orquesta no conoce los detalles de lo que orquesta (Gamma et al., 1994).
"""

def celda_md(texto):
    return {"cell_type": "markdown", "metadata": {}, "source": texto.splitlines(keepends=True)}

def celda_codigo(texto):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": texto.splitlines(keepends=True)}

nb["cells"].append(celda_md(texto_explicacion))
nb["cells"].append(celda_codigo(codigo_demostracion))
nb["cells"].append(celda_md(texto_cierre))

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("3 celdas agregadas (8.1 completa). Total celdas:", len(nb["cells"]))
