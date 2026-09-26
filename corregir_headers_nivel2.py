import json

RUTA = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA, encoding="utf-8") as f:
    nb = json.load(f)

correcciones = {
    18: ("## 3. Codificación de variables categóricas",
         "## 4. Codificación de variables categóricas"),
    31: ("## 4. Escalamiento de variables numéricas",
         "## 5. Escalamiento de variables numéricas"),
    40: ("## 5. Evaluación de eficiencia",
         "## 6. Evaluación de eficiencia"),
    66: ("## 6. Patrón de diseño Strategy aplicado a la imputación",
         "## 7. Patrón de diseño Strategy aplicado a la imputación"),
}

for indice, (esperado, nuevo) in correcciones.items():
    celda = nb["cells"][indice]
    primera = celda["source"][0].rstrip("\n")
    assert primera == esperado, f"celda {indice}: esperaba {esperado!r}, encontré {primera!r}"
    celda["source"][0] = nuevo + "\n"
    print(f"[{indice}] {esperado!r}  ->  {nuevo!r}")

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("\nGuardado correctamente.")
