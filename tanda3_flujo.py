import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

texto = """### 8.2 Flujo de datos del pipeline
datos (crudo, ens_variables_f1f2.xlsx, 5.520 x 16)
|
|- MarcadorNoRespuesta("as28") marca -9999 como nulo
|- EliminadorFilasNulas("HTA") elimina 9 filas sin diagnostico
|- ImputadorFlexible("IMC", PorMediana())
|- ImputadorFlexible("anos_estudio_MINSAL_1", PorMediana())
|- ImputadorFlexible("as27", PorMedianaDeTramo("as28"))
|- ImputadorFlexible("GPAQ", PorModa())
|- EliminadorColumna("IdEncuesta")
|- EliminadorColumna("FechaInicioF1")
|- ConvertidorEntero("HTA"), ConvertidorEntero("GPAQ")
|- CodificadorOneHot(...) x4 Sexo, Zona, di3, dis2
|- EscaladorEstandar(...) x3 Edad, IMC, as27
|
v
df_transformado (5.511 x 23)

Cada paso de la lista es una llamada a `ajustar_transformar()`. El flujo es lineal y unidireccional: no hay ramas condicionales ni pasos que dependan de un resultado calculado fuera de su propio `ajustar()`. El orden de los pasos, documentado en la sección 2 y verificado en la sección 6.8 contra `ens_procesado.csv`, es la unica fuente de verdad sobre como se construye el dataset final.
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

print("1 celda agregada (8.2 completa). Total celdas:", len(nb["cells"]))
