import json

RUTA_NOTEBOOK = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA_NOTEBOOK, encoding="utf-8") as f:
    nb = json.load(f)

def fuente(celda):
    return "".join(celda["source"])

encontrada = False
for celda in nb["cells"]:
    texto = fuente(celda)
    if (celda["cell_type"] == "code"
            and "df_transformado = imputado.copy()" in texto
            and "EliminadorColumna(" in texto):

        nuevo_codigo = '''from src.pipeline import Pipeline

pasos_integracion = (
    [EliminadorColumna(col) for col in ["IdEncuesta", "FechaInicioF1"]]
    + [ConvertidorEntero(col) for col in ["HTA", "GPAQ"]]
    + [CodificadorOneHot(col) for col in variables_categoricas]
    + [EscaladorEstandar(col) for col in variables_numericas]
)

pipeline = Pipeline(pasos_integracion)
df_transformado = pipeline.ajustar_transformar(imputado)

print("Dimensiones iniciales:", imputado.shape)
print("Dimensiones finales:", df_transformado.shape)
'''
        celda["source"] = nuevo_codigo.splitlines(keepends=True)
        celda["outputs"] = []
        celda["execution_count"] = None
        encontrada = True
        break

if not encontrada:
    print("AVISO: no se encontró la celda a reemplazar")
else:
    with open(RUTA_NOTEBOOK, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("Celda reemplazada correctamente.")
