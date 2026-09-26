import json

with open("F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

for i in range(58, 64):
    t = "".join(nb["cells"][i]["source"]).strip()
    tipo = nb["cells"][i]["cell_type"]
    print(f"[{i}] ({tipo}) {t[:70]}")
