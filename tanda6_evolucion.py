import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

texto = """### 8.5 Evolucion del proyecto: registro razonado

**Fase 2 -> Fase 3.** En la Fase 2 cada paso de limpieza era una funcion suelta con ramas `if` para las distintas alternativas (por ejemplo, `imputar_nulos_numericos` decidia internamente que estrategia usar). En esta entrega esos pasos se reescribieron como clases que comparten la interfaz de `Transformador`, y la eleccion de estrategia de imputacion se resolvio aparte con el patron Strategy (seccion 7), separando "como se usa un paso" de "que hace cada alternativa".

**Durante esta entrega.** Se detectaron y corrigieron tres problemas concretos, en orden:

1. Los modulos de `src/` dependian de que `src/` estuviera agregado directamente al `sys.path`, lo que impedia importarlos como paquete estandar (`from src.pipeline import Pipeline`) desde la raiz del repositorio. Se corrigieron los imports internos y la configuracion de rutas del notebook para que `src/` funcione como paquete.
2. La integracion de codificacion y escalamiento se hacia encadenando los transformadores a mano, sin usar la clase `Pipeline`. Se reemplazo por una instancia real de `Pipeline` (seccion 6.8), que es la pieza de diseño estructurado que exige este apartado.
3. La medicion de `construir_indice_dict` en la Formativa 3 usaba `iterrows()`, lo que inflaba artificialmente el umbral reportado (437 busquedas). Se corrigio a `dict(zip(...))` y se reporto el umbral real (~0,35 busquedas, seccion 6.9), sin alterar la conclusion ya validada de adoptar `set_index` como solucion final.

Ademas, se agrego una seccion de validacion (seccion 3) que ejecuta dentro del notebook las 59 pruebas normal/limite/excepcion registradas en `tests/casos_por_clase.py`, en lugar de solo referenciar el archivo donde viven.
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

print("1 celda agregada (8.5 completa). Total celdas:", len(nb["cells"]))
