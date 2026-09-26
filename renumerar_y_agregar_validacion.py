import json
import re

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

PATRON = re.compile(r"^(#{2,3})\s*(\d+)(\.(\d+))?\s+(.*)$")

def fuente(c):
    return "".join(c["source"])

def celda_markdown(texto):
    return {"cell_type": "markdown", "metadata": {}, "source": texto.splitlines(keepends=True)}

def celda_codigo(texto):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": texto.splitlines(keepends=True)}

# --- 1. Renumerar headers con numero mayor >= 3 (una sola pasada, sin cascada) ---
cambios = []
for celda in nb["cells"]:
    if celda["cell_type"] != "markdown":
        continue
    lineas = celda["source"]
    if not lineas:
        continue
    primera = lineas[0]
    m = PATRON.match(primera.rstrip("\n"))
    if not m:
        continue
    hashes, mayor, _, menor, resto = m.groups()
    mayor = int(mayor)
    if mayor < 3:
        continue
    nuevo_mayor = mayor + 1
    nueva_primera = f"{hashes} {nuevo_mayor}" + (f".{menor}" if menor else "") + f" {resto}\n"
    cambios.append((primera.strip(), nueva_primera.strip()))
    lineas[0] = nueva_primera

print("=== Renumeraciones aplicadas ===")
for viejo, nuevo in cambios:
    print(f"  {viejo!r}  ->  {nuevo!r}")
print(f"Total: {len(cambios)} headers renumerados\n")

# --- 2. Insertar la nueva seccion 3 (Validacion) antes de la seccion "4. Codificacion" (ya renumerada) ---
md_intro = """## 3. Validación: casos normal, límite y excepción

Cada clase del pipeline se prueba por separado con tres tipos de caso: normal (uso esperado, con datos comunes), límite (situaciones extremas pero válidas, como una columna sin nulos o un pipeline vacío) y excepción (entradas incorrectas, donde lo correcto es que falle con un mensaje claro). Estas pruebas viven en `tests/casos_por_clase.py` y se ejecutan aquí mismo mediante `ejecutar_pruebas()`, para dejar la evidencia dentro del notebook y no solo en el archivo de tests.
"""

codigo = """from tests.casos_por_clase import ejecutar_pruebas

informe = ejecutar_pruebas(estricto=False)
print(informe["estado"].value_counts())
informe
"""

md_interpretacion = """Las 59 pruebas cubren las 13 clases del pipeline (`Transformador`, los siete pasos de `imputadores.py`, los cuatro de `transformadores.py` y `Pipeline`), repartidas en los tres escenarios. Los 13 casos restantes de la suite completa (72 en total, ver `tests/test_transformadores.py`) prueban específicamente `CodificadorOneHot` y `EscaladorEstandar` con pytest y no pasan por `ejecutar_pruebas()`, por lo que no aparecen en esta tabla.
"""

nuevas_celdas = [celda_markdown(md_intro), celda_codigo(codigo), celda_markdown(md_interpretacion)]

indice_insercion = None
for i, celda in enumerate(nb["cells"]):
    if celda["cell_type"] == "markdown" and fuente(celda).lstrip().startswith("## 4."):
        indice_insercion = i
        break

if indice_insercion is None:
    print("ERROR: no se encontró la celda '## 4.' tras renumerar. No se insertó nada. Revisar a mano.")
    raise SystemExit(1)

nb["cells"][indice_insercion:indice_insercion] = nuevas_celdas
print(f"Sección 3 (Validación) insertada en el índice {indice_insercion}, antes de '## 4.'\n")

# --- 3. Reescribir el indice (celda 0) ---
texto_celda0 = fuente(nb["cells"][0])
inicio_tabla = texto_celda0.index("| Sección | Contenido |")
encabezado = texto_celda0[:inicio_tabla]

nueva_tabla = """| Sección | Contenido |
|---|---|
| 1 | Configuración y carga del conjunto elegible F1-F2 |
| 2 | Pipeline de preprocesamiento en clases |
| 3 | Validación: casos normal, límite y excepción |
| 4 | Codificación de variables categóricas |
| 5 | Escalamiento de variables numéricas |
| 6 | Evaluación de eficiencia |
| 7 | Patrón de diseño Strategy aplicado a la imputación |
| 8 | Arquitectura y conclusiones |"""

nb["cells"][0]["source"] = (encabezado + nueva_tabla).splitlines(keepends=True)
print("Índice (celda 0) reescrito con 8 secciones.\n")

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print(f"Guardado. Total celdas: {len(nb['cells'])}")
