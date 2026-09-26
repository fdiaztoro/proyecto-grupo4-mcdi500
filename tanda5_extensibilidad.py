import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

texto_intro = """### 8.4 Extensibilidad: agregar un paso sin modificar el Pipeline

Un diseño escalable debe permitir requisitos nuevos sin reescribir lo que ya funciona. Se demuestra agregando un paso que el equipo no anticipo al diseñar el pipeline original:
"""

codigo = """class RedondeadorDecimales(Transformador):
    \"\"\"Paso nuevo, no anticipado por el equipo: redondea una columna
    numerica a 2 decimales. Sirve para demostrar que el Pipeline no
    necesita modificarse para aceptar un paso que no existia antes.\"\"\"

    def aprender(self, df):
        return {}

    def aplicar(self, df):
        df[self.columna] = df[self.columna].round(2)
        return df


pipeline_extendido = Pipeline(pasos_integracion + [RedondeadorDecimales("Edad")])
resultado_extendido = pipeline_extendido.ajustar_transformar(imputado)

print("Pipeline original:  ", df_transformado.shape)
print("Pipeline extendido: ", resultado_extendido.shape)
print("¿Se modifico pipeline.py para lograr esto?  No.")
print("¿Se modifico alguna clase existente?         No.")
"""

texto_cierre = """`Pipeline` quedo abierto a la extension (acepta cualquier paso nuevo que cumpla el contrato de `Transformador`) pero cerrado a la modificacion (ni `Pipeline` ni los pasos existentes cambiaron para lograrlo). Este es el principio abierto/cerrado de diseño orientado a objetos (Martin, 2017), y es la misma propiedad que permitio, durante esta entrega, incorporar una funcion de medicion completamente nueva (`construir_indice_dict` corregido, seccion 6.9) sin tocar el resto del pipeline.
"""

def celda_md(texto):
    return {"cell_type": "markdown", "metadata": {}, "source": texto.splitlines(keepends=True)}

def celda_codigo(texto):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": texto.splitlines(keepends=True)}

nb["cells"].append(celda_md(texto_intro))
nb["cells"].append(celda_codigo(codigo))
nb["cells"].append(celda_md(texto_cierre))

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("3 celdas agregadas (8.4 completa). Total celdas:", len(nb["cells"]))
