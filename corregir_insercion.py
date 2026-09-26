import json

RUTA_NOTEBOOK = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA_NOTEBOOK, encoding="utf-8") as f:
    nb = json.load(f)

def fuente(celda):
    return "".join(celda["source"])

# 1. Confirmar que las celdas 0,1,2 son las que insertamos mal
texto0 = fuente(nb["cells"][0]).strip()
texto2 = fuente(nb["cells"][2]).strip()

if not texto0.startswith("### 5.9 Corrección"):
    print("AVISO: la celda 0 no es la que esperaba, abortando. Revisar a mano.")
    raise SystemExit(1)

# 2. Sacarlas de ahi (son exactamente 3: markdown, code, markdown)
celdas_a_mover = nb["cells"][0:3]
if not (celdas_a_mover[0]["cell_type"] == "markdown"
        and celdas_a_mover[1]["cell_type"] == "code"
        and celdas_a_mover[2]["cell_type"] == "markdown"):
    print("AVISO: el patron de las 3 celdas no calza, abortando.")
    raise SystemExit(1)

resto = nb["cells"][3:]

# 3. Buscar el header REAL de la seccion 6 (con ## de verdad, no la fila de la tabla del indice)
indice_insercion = None
for i, celda in enumerate(resto):
    if celda["cell_type"] != "markdown":
        continue
    t = fuente(celda).strip()
    # el header real empieza con "## 6." (markdown heading), la tabla del indice no
    if t.startswith("## 6.") or t.startswith("6. Patrón de diseño Strategy") or t.startswith("6. Patron de diseno Strategy"):
        indice_insercion = i
        break

if indice_insercion is None:
    print("AVISO: no se encontró el header real de la sección 6 en 'resto'. No se reinsertó nada.")
    print("Las 3 celdas quedaron sacadas del inicio pero SIN reinsertar todavia.")
else:
    resto[indice_insercion:indice_insercion] = celdas_a_mover
    nb["cells"] = resto
    with open(RUTA_NOTEBOOK, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"Corregido: 3 celdas movidas al indice {indice_insercion} (antes del header real de la seccion 6).")
