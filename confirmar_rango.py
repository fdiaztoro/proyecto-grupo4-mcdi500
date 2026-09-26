import json

with open("F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

for i in range(17, 32):
    c = nb["cells"][i]
    t = "".join(c["source"]).strip()
    print(f"[{i}] ({c['cell_type']}) {t[:60]}")
