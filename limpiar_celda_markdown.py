import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

celda = nb["cells"][58]
assert celda["cell_type"] == "markdown", "la celda 58 no es markdown"

quitados = []
for campo in ("execution_count", "outputs"):
    if campo in celda:
        del celda[campo]
        quitados.append(campo)

print("Campos quitados de la celda 58:", quitados)

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("Guardado.")
