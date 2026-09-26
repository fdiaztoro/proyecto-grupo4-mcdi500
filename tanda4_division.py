import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

texto = """### 8.3 Division funcional en lugar de recursividad

El proyecto no usa recursividad en el pipeline principal: los 9 pasos siguen una secuencia fija y conocida de antemano, sin una estructura autosimilar que se repita a distintas escalas. La recursividad tiene sentido cuando el problema tiene esa forma -por ejemplo, `aplanar()` en la Fase 1 recorre metadatos anidados a una profundidad que no se conoce de antemano-, pero para una secuencia fija de transformaciones no aporta claridad ni eficiencia: solo expresaria de forma menos directa lo que ya es, en esencia, un bucle.

En su lugar, el diseño resuelve el problema mediante division funcional: cada transformacion es una unidad independiente (una clase), y la composicion de esas unidades -no la recursion- es lo que arma el comportamiento completo. Esto mantiene cada pieza pequeña, comprobable por separado (seccion 3) y reemplazable sin afectar a las demas.
"""

nueva_celda = {
    "cell_type": "markdown",
    "metadata": {},
    "source": texto.splitlines(keepends=True),
}

nb["cells"].append(nueva_celda)

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("1 celda agregada (8.3 completa). Total celdas:", len(nb["cells"]))
