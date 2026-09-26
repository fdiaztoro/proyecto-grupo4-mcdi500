import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

viejo = 'codigo_pipeline = open("src/pipeline.py").read()'
nuevo = 'codigo_pipeline = open(RAIZ / "src" / "pipeline.py").read()'

encontrado = False
for celda in nb["cells"]:
    if celda["cell_type"] == "code":
        texto = "".join(celda["source"])
        if viejo in texto:
            texto = texto.replace(viejo, nuevo)
            celda["source"] = texto.splitlines(keepends=True)
            encontrado = True
            break

print("Corregido:" if encontrado else "AVISO: no se encontró la línea a corregir", "")

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
