import json

RUTA_NOTEBOOK = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA_NOTEBOOK, encoding="utf-8") as f:
    nb = json.load(f)

def fuente(celda):
    return "".join(celda["source"])

def celda_markdown(texto):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": texto.splitlines(keepends=True),
    }

def celda_codigo(texto):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": texto.splitlines(keepends=True),
    }

md_intro = '''### 5.9 Corrección de una medición de la Formativa 3

En la Formativa 3, `construir_indice_dict` armaba el diccionario iterando con `iterrows()`, lo que infla su costo de construcción. Esto llevó a reportar un umbral de 437 búsquedas para justificar la construcción del índice, un número que dependía más de cómo se construyó el diccionario que del costo real de indexar. La conclusión final del equipo —adoptar `set_index` de pandas como solución— no depende de esta comparación y se mantiene sin cambios; lo que se corrige aquí es puntualmente el umbral reportado para la alternativa basada en diccionario.

Se corrigió `construir_indice_dict` (`src/medicion.py`) para usar `dict(zip(...))` sobre los valores obtenidos con `to_dict("records")`, evitando el recorrido fila por fila. Se repite la misma comparación que en la Formativa: la búsqueda lineal de referencia (`buscar_iterrows_por_clave`) contra la búsqueda ya indexada (`buscar_indexado_dict`), sobre el conjunto real del proyecto.
'''

codigo = '''from src.medicion import (
    buscar_iterrows_por_clave,
    construir_indice_dict,
    buscar_indexado_dict,
    medir_tiempo_timeit,
)

datos_indexables = datos.reset_index().rename(columns={"index": "clave_busqueda"})
valor_medio = datos_indexables["clave_busqueda"].iloc[len(datos_indexables) // 2]

t_construccion = medir_tiempo_timeit(construir_indice_dict, datos_indexables, "clave_busqueda", numero=5, repeticiones=3)
indice_dict = construir_indice_dict(datos_indexables, "clave_busqueda")

t_lineal = medir_tiempo_timeit(buscar_iterrows_por_clave, datos_indexables, "clave_busqueda", valor_medio, numero=20, repeticiones=5)
t_indexada = medir_tiempo_timeit(buscar_indexado_dict, indice_dict, valor_medio, numero=100_000, repeticiones=5)

umbral_corregido = t_construccion / (t_lineal - t_indexada)

print(f"Construcción del índice (dict con zip): {t_construccion*1000:.4f} ms")
print(f"Búsqueda lineal (iterrows):              {t_lineal*1000:.4f} ms")
print(f"Búsqueda indexada (dict):                {t_indexada*1_000_000:.4f} µs")
print(f"Umbral corregido:                        {umbral_corregido:.2f} búsquedas")
'''

md_interpretacion = '''Con la construcción corregida, el umbral cae de 437 a aproximadamente 0,35 búsquedas: prácticamente desde la primera consulta ya conviene construir el diccionario y buscar ahí, en vez de recorrer el conjunto con `iterrows()`. El umbral original no era comparable de forma justa, porque el costo de construcción con el que se calculó estaba inflado por el mismo problema que afectaba a la búsqueda lineal.
'''

nuevas_celdas = [
    celda_markdown(md_intro),
    celda_codigo(codigo),
    celda_markdown(md_interpretacion),
]

indice_insercion = None
for i, celda in enumerate(nb["cells"]):
    if celda["cell_type"] == "markdown" and "Patrón de diseño Strategy aplicado a la imputación" in fuente(celda):
        indice_insercion = i
        break

if indice_insercion is None:
    print("AVISO: no se encontró la celda de la sección 6, no se insertó nada")
else:
    nb["cells"][indice_insercion:indice_insercion] = nuevas_celdas
    with open(RUTA_NOTEBOOK, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"3 celdas insertadas antes de la celda {indice_insercion} (sección 6).")
    print("Nueva sección: 5.9 Corrección de una medición de la Formativa 3")
