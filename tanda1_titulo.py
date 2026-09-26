import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

texto_titulo = """## 8. Arquitectura y conclusiones

El pipeline construido en las secciones anteriores no es solo una lista de clases que reproducen la Fase 2: es una arquitectura con decisiones de diseño concretas. Esta sección documenta esas decisiones.
"""

nueva_celda = {
    "cell_type": "markdown",
    "metadata": {},
    "source": texto_titulo.splitlines(keepends=True),
}

nb["cells"].append(nueva_celda)

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("Celda de titulo agregada. Total celdas:", len(nb["cells"]))
