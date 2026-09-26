import json
import sys

RUTA_NOTEBOOK = "F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb"

with open(RUTA_NOTEBOOK, encoding="utf-8") as f:
    nb = json.load(f)

cambios_hechos = []

def fuente(celda):
    return "".join(celda["source"])

def set_fuente(celda, texto):
    lineas = texto.splitlines(keepends=True)
    if lineas and not lineas[-1].endswith("\n"):
        pass
    celda["source"] = lineas
    celda["outputs"] = []
    celda["execution_count"] = None

# 1. Config de rutas (sys.path + imports de carga/transformador)
encontrada_1 = False
for celda in nb["cells"]:
    if celda["cell_type"] == "code" and 'sys.path.append(str(RAIZ / "src"))' in fuente(celda):
        texto = fuente(celda)
        texto = texto.replace(
            'sys.path.append(str(RAIZ / "src"))',
            'sys.path.append(str(RAIZ))'
        )
        texto = texto.replace(
            "from carga import cargar_conjunto, perfilar",
            "from src.carga import cargar_conjunto, perfilar"
        )
        texto = texto.replace(
            "from transformador import Transformador",
            "from src.transformador import Transformador"
        )
        set_fuente(celda, texto)
        encontrada_1 = True
        cambios_hechos.append("1. sys.path + imports de carga/transformador")
        break
if not encontrada_1:
    print("AVISO: no se encontró la celda de configuración de sys.path (cambio 1)")

# 2. Import de imputadores
encontrada_2 = False
for celda in nb["cells"]:
    if celda["cell_type"] == "code" and "from imputadores import (" in fuente(celda):
        texto = fuente(celda).replace(
            "from imputadores import (",
            "from src.imputadores import ("
        )
        set_fuente(celda, texto)
        encontrada_2 = True
        cambios_hechos.append("2. import de imputadores")
        break
if not encontrada_2:
    print("AVISO: no se encontró el import de imputadores (cambio 2)")

# 3. Import de transformadores + nombre de clase
encontrada_3 = False
for celda in nb["cells"]:
    if celda["cell_type"] == "code" and "from transformadores import (" in fuente(celda):
        texto = fuente(celda)
        texto = texto.replace(
            "from transformadores import (",
            "from src.transformadores import ("
        )
        texto = texto.replace("EliminadorColumnas", "EliminadorColumna")
        set_fuente(celda, texto)
        encontrada_3 = True
        cambios_hechos.append("3. import de transformadores + EliminadorColumna")
        break
if not encontrada_3:
    print("AVISO: no se encontró el import de transformadores (cambio 3)")

# 4. Celda markdown de la sección 5.8: actualizar la descripción
encontrada_4a = False
for celda in nb["cells"]:
    if celda["cell_type"] == "markdown" and "Integración del pipeline de transformación" in fuente(celda):
        nuevo_texto = (
            "### 5.8 Integración del pipeline de transformación\n"
            "\n"
            "Los pasos usados y validados por separado en las secciones anteriores "
            "(imputación, eliminación de columnas, conversión de tipos, codificación "
            "y escalamiento) se encadenan ahora en un único objeto `Pipeline`. El "
            "`Pipeline` no conoce el detalle interno de cada paso: solo exige que "
            "todos respondan a `ajustar()` y `transformar()`, gracias a que todos "
            "heredan de `Transformador`. El proceso parte desde `datos` (el conjunto "
            "crudo cargado al inicio del notebook) y aplica los 9 pasos en una sola "
            "llamada, reproduciendo el mismo resultado que se obtuvo de forma manual "
            "en la Fase 2."
        )
        set_fuente(celda, nuevo_texto)
        encontrada_4a = True
        cambios_hechos.append("4a. markdown de la sección 5.8")
        break
if not encontrada_4a:
    print("AVISO: no se encontró la celda markdown de la sección 5.8 (cambio 4a)")

# 4b. Celda de código con la integración manual -> reemplazar por Pipeline real
encontrada_4b = False
for celda in nb["cells"]:
    if celda["cell_type"] == "code" and "EliminadorColumnas(" in fuente(celda):
        nuevo_codigo = '''from src.pipeline import Pipeline

pipeline = Pipeline([
    MarcadorNoRespuesta("as28"),
    EliminadorFilasNulas("HTA"),
    ImputadorFlexible("IMC", PorMediana()),
    ImputadorFlexible("anos_estudio_MINSAL_1", PorMediana()),
    ImputadorFlexible("as27", PorMedianaDeTramo("as28")),
    ImputadorFlexible("GPAQ", PorModa()),
    EliminadorColumna("IdEncuesta"),
    EliminadorColumna("FechaInicioF1"),
    ConvertidorEntero("HTA"),
    ConvertidorEntero("GPAQ"),
    CodificadorOneHot("Sexo"),
    CodificadorOneHot("Zona"),
    CodificadorOneHot("di3"),
    CodificadorOneHot("dis2"),
    EscaladorEstandar("Edad"),
    EscaladorEstandar("IMC"),
    EscaladorEstandar("as27"),
])

df_transformado = pipeline.ajustar_transformar(datos)

print("Dimensiones iniciales:", datos.shape)
print("Dimensiones finales:", df_transformado.shape)
'''
        set_fuente(celda, nuevo_codigo)
        encontrada_4b = True
        cambios_hechos.append("4b. celda de código: Pipeline real reemplaza integración manual")
        break
if not encontrada_4b:
    print("AVISO: no se encontró la celda de integración manual (cambio 4b)")

with open(RUTA_NOTEBOOK, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

print()
print("Cambios aplicados:")
for c in cambios_hechos:
    print(" -", c)
print()
print(f"Total: {len(cambios_hechos)}/5 cambios esperados")
