import json

with open("F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

print(repr(nb["cells"][0]["source"]))
