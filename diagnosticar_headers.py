import json

with open("F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "markdown":
        continue
    primera = c["source"][0].strip() if c["source"] else ""
    if primera.startswith("## ") or primera.startswith("### "):
        print(i, repr(primera))
