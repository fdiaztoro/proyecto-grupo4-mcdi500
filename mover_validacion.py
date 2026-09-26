import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

def fuente(c):
    return "".join(c["source"]).strip()

# Verificaciones de seguridad antes de mover nada
assert fuente(nb["cells"][18]).startswith("## 4. Codificación"), "celda 18 no es la esperada"
assert fuente(nb["cells"][28]).startswith("## 3. Validación"), "celda 28 no es la esperada"
assert nb["cells"][29]["cell_type"] == "code", "celda 29 no es codigo"
assert fuente(nb["cells"][30]).startswith("Las 59 pruebas"), "celda 30 no es la esperada"

# Sacar el bloque 28-30 (3 celdas: Validacion)
bloque_validacion = nb["cells"][28:31]
del nb["cells"][28:31]

# Insertarlo antes de la celda 18 (que ahora sigue en el mismo indice, ya que
# borramos celdas DESPUES de esa posicion, no antes)
nb["cells"][18:18] = bloque_validacion

# Verificacion final
assert fuente(nb["cells"][18]).startswith("## 3. Validación"), "no quedo en el lugar correcto"
assert fuente(nb["cells"][21]).startswith("## 4. Codificación"), "la codificacion no quedo justo despues"

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("Bloque de Validación movido correctamente: ahora en índices 18-20, antes de Codificación (índice 21).")
print("Total celdas:", len(nb["cells"]))
