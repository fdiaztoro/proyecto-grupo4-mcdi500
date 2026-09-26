import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

texto_conclusiones = """### 8.6 Conclusiones

El pipeline con clases reproduce exactamente el resultado de la Fase 2 (5.511 filas x 23 columnas, sin columnas faltantes ni adicionales), lo que confirma que la refactorizacion a POO no altero el comportamiento del preprocesamiento, solo su estructura interna. Los tres principios de POO se evidencian con codigo ejecutado, no solo descrito: herencia (todos los pasos parten de `Transformador`), polimorfismo (`Pipeline` llama `ajustar_transformar()` sin saber que clase concreta recibe) y encapsulamiento (el estado aprendido en `_parametros` solo se expone como copia de lectura).

La principal limitacion del proyecto sigue siendo la que se documento en la seccion 7: 816 personas sin ingreso declarado quedan sin imputar en `as27` porque tampoco declararon su tramo, y esa ausencia podria no ser aleatoria. Esto no es una falla del pipeline sino una decision explicita de no inventar un dato que nadie entrego, y queda como limitacion abierta para la interpretacion de los resultados del estudio.

Como trabajo futuro, la extensibilidad demostrada en 8.4 deja abierta la posibilidad de incorporar nuevos pasos de preprocesamiento -por ejemplo, tratamiento de outliers o nuevas variables derivadas- sin modificar la arquitectura actual.
"""

texto_fuentes = """### Fuentes citadas en esta seccion

- Amershi, S., Begel, A., Bird, C., DeLine, R., Gall, H., Kamar, E., Nagappan, N., Nushi, B., & Zimmermann, T. (2019). Software engineering for machine learning: A case study. *Proceedings of the 41st International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP)*, 291-300. https://doi.org/10.1109/ICSE-SEIP.2019.00042
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design patterns: Elements of reusable object-oriented software*. Addison-Wesley.
- Martin, R. C. (2017). *Clean architecture: A craftsman's guide to software structure and design*. Prentice Hall.
- McConnell, S. (2004). *Code complete* (2.a ed.). Microsoft Press.
- scikit-learn developers. (2024). *Pipeline - scikit-learn 1.5 documentation*. https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html

*Nota: esta lista cubre bibliografia tecnica y academica. Falta agregar bibliografia docente (material del curso), que debe incorporarse en el informe.*
"""

def celda_md(texto):
    return {"cell_type": "markdown", "metadata": {}, "source": texto.splitlines(keepends=True)}

nb["cells"].append(celda_md(texto_conclusiones))
nb["cells"].append(celda_md(texto_fuentes))

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("2 celdas agregadas (8.6 completa). Total celdas:", len(nb["cells"]))
