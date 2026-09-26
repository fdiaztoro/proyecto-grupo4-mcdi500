import json

with open("F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

afectadas = []
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] == "markdown" and ("execution_count" in c or "outputs" in c):
        afectadas.append(i)

print("Celdas markdown con campos invalidos:", afectadas)
