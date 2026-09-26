import json

RUTA_NOTEBOOK = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA_NOTEBOOK, encoding="utf-8") as f:
    nb = json.load(f)

def fuente(celda):
    return "".join(celda["source"]).strip()

# Verificacion de seguridad antes de borrar
assert fuente(nb["cells"][0]).startswith("### 5.9 Corrección"), "celda 0 no es la esperada"
assert nb["cells"][1]["cell_type"] == "code", "celda 1 no es codigo"
assert fuente(nb["cells"][2]).startswith("Con la construcción corregida"), "celda 2 no es la esperada"

assert fuente(nb["cells"][3]).startswith("### 5.9 Corrección") == False, "la celda 3 no deberia ser el duplicado, revisar"

# Confirmar que la copia buena (mas adelante) sigue intacta antes de tocar nada
copias_5_9 = [i for i, c in enumerate(nb["cells"]) if fuente(c).startswith("### 5.9 Corrección")]
print("Copias de la celda 5.9 encontradas en indices:", copias_5_9)
assert len(copias_5_9) == 2, f"se esperaban 2 copias, se encontraron {len(copias_5_9)}"

# Borrar los indices 0,1,2 (la copia mal ubicada)
del nb["cells"][0:3]

# Verificacion final: debe quedar solo 1 copia, y el titulo original debe volver a ser la celda 0
copias_restantes = [i for i, c in enumerate(nb["cells"]) if fuente(c).startswith("### 5.9 Corrección")]
print("Copias restantes tras borrar:", copias_restantes)
assert len(copias_restantes) == 1, "algo salio mal, no quedo exactamente 1 copia"

titulo_celda_0 = fuente(nb["cells"][0])
print("Celda 0 ahora es:", repr(titulo_celda_0[:70]))

with open(RUTA_NOTEBOOK, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("Guardado. Total celdas ahora:", len(nb["cells"]))
