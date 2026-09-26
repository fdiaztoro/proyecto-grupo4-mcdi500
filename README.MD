# Grupo 4 — MCDI500

Factores sociodemográficos y su asociación con factores de riesgo
cardiovascular, utilizando la Encuesta Nacional de Salud (ENS)
2016-2017 de Chile.

## Integrantes

- Felipe Díaz Toro
- Pablo Ríos Passteni
- Guillermo Subiabre Chacón
- Ninoska Yévenes Hernández

## Pregunta de investigación

¿Cómo se relacionan las condiciones sociodemográficas (edad, sexo,
nivel educacional, ingreso del hogar y zona de residencia) con la
presencia de indicadores de riesgo cardiovascular en participantes
de la ENS 2016-2017?

## Datos

- **Fuente:** Encuesta Nacional de Salud (ENS) 2016-2017, Ministerio
  de Salud de Chile (MINSAL).
- **Archivo base:** `data/raw/ens2016.xlsx` (6.233 registros, 1.173
  columnas originales). Incluido en el repositorio, sin modificar.
- **Subconjunto seleccionado:** `data/processed/ens_variables_seleccionadas.xlsx`
  (16 variables, 6.233 filas).
- **Subconjunto elegible F1-F2:** `data/processed/ens_variables_f1f2.xlsx`
  (5.520 filas, filtrado por el ponderador `Fexp_F1F2p_Corr`).
- **Subconjunto procesado final:** `data/processed/ens_procesado.csv`
  (5.511 filas, 23 columnas, limpio y listo para la Fase 3).
- **Ponderador utilizado:** `Fexp_F1F2p_Corr` (componente combinado F1-F2).

## Estructura del repositorio

```
proyecto-grupo4-mcdi500/
├── data/
│ ├── raw/ens2016.xlsx Base original, sin modificar
│ └── processed/ Subconjuntos generados por código
├── F1/
│ └── notebooks/S1_F1_Definicion.ipynb
├── F2/
│ ├── notebooks/S1_F2_Preprocesamiento.ipynb
│ └── docs/ Diccionario, resumen del filtro, metadatos
├── F3/
│ └── notebooks/
│   ├── f3_formativa_complejidad.ipynb Formativa 3: complejidad algorítmica
│   └── S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb Sumativa 2: preprocesamiento en clases (POO)
├── src/
│ ├── carga.py Carga y preparación del conjunto de la Fase 3
│ ├── medicion.py Funciones de búsqueda y medición de tiempo y memoria
│ ├── transformador.py Clase base Transformador (ajustar / transformar)
│ ├── imputadores.py No respuesta, eliminación de filas e imputación (patrón Strategy)
│ ├── transformadores.py Codificación one-hot, escalamiento, eliminación de columnas y conversión a entero
│ ├── pipeline.py Encadena los pasos del preprocesamiento en orden
│ └── validador.py Valida el resultado y lo compara con la Fase 2
├── docs/
│ └── evidencias/ Notebooks de F1, F2 y F3 ejecutados en HTML/PDF (con salidas)
├── tests/
│ ├── casos_por_clase.py Pruebas por clase: normal, límite y excepción
│ ├── test_casos_por_clase.py Ejecuta esas pruebas con pytest
│ └── test_transformadores.py Pruebas de los transformadores con pytest
├── .gitignore
├── requirements.txt
└── README.MD
```


## Requisitos y ejecución

Python 3.13 o superior

```bash
# 1. Clonar repositorio e ingresar a la carpeta
git clone https://github.com/fdiaztoro/proyecto-grupo4-mcdi500.git
cd proyecto-grupo4-mcdi500

# 2. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate        # macOS y Linux
# .venv\Scripts\activate         # Windows

# 3. Instalar dependencias del proyecto
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4. Activar la higiene automática de notebooks en el repositorio local
nbstripout --install
# Evita metadata conflictiva (kernel, Google Colab, etc.) que pueda comitearse por error
git config filter.nbstripout.extrakeys "metadata.language_info.version metadata.colab cell.metadata.id cell.metadata.colab cell.metadata.outputId"

# 5. Registrar el kernel del proyecto en Jupyter
python -m ipykernel install --user --name grupo4_mcdi500 --display-name "Python (grupo4-mcdi500)"
```

### Dependencias

Todas están en `requirements.txt`, con versión fija:

| Grupo | Paquetes | Para qué |
|---|---|---|
| Núcleo de datos | numpy, pandas, openpyxl | Carga y transformación de los datos (incluye leer `.xlsx`) |
| Visualización | matplotlib, seaborn | Gráficos de los notebooks |
| Modelado | scikit-learn, scipy | `StandardScaler` de scikit-learn se usa en la Sumativa 2 como referencia para comparar el escalador propio |
| Pruebas | pytest | Ejecutar las pruebas de `tests/` |
| Jupyter y Git | jupyterlab, notebook, ipykernel, jupyterlab-git, jupytext, nbstripout | Entorno de notebooks e higiene del historial |

### Ejecución de los notebooks

Abrir JupyterLab (o VS Code) y ejecutar, en este orden, seleccionando
el kernel **Python (grupo4-mcdi500)**:

1. `F1/notebooks/S1_F1_Definicion.ipynb`
2. `F2/notebooks/S1_F2_Preprocesamiento.ipynb`
3. `F3/notebooks/f3_formativa_complejidad.ipynb`
4. `F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb`

Los notebooks deben correr de principio a fin sin errores
(Kernel → Restart Kernel and Run All Cells). Los notebooks de F3
importan su código desde `src/`: la formativa usa `carga.py` y
`medicion.py`; el de la Sumativa 2 usa además las clases de
`transformador.py`, `imputadores.py` y `transformadores.py`.

**Nota sobre las salidas:** los `.ipynb` se guardan sin salidas por
`nbstripout` (paso 4), para mantener limpio el historial de Git. La
ejecución completa de cada notebook, con sus salidas, está en
`docs/evidencias/` (F1, F2 y F3).

### Pruebas automatizadas

Las pruebas están en `tests/` y se ejecutan con `pytest` desde la raíz del repositorio:

```bash
python -m pytest tests/ -q                         # todas las pruebas
python -m pytest tests/ -v -k CodificadorOneHot    # solo las de una clase
python -m pytest tests/ -v -k excepcion            # solo un escenario
```

- `tests/casos_por_clase.py`: pruebas de cada clase del pipeline en tres
  escenarios (normal, límite y excepción). Desde un notebook, con `src/` y
  `tests/` en `sys.path`, `ejecutar_pruebas()` entrega el mismo resultado
  como informe en tabla.
- `tests/test_transformadores.py`: pruebas de los transformadores de
  codificación y escalamiento.
- `src/validador.py` no contiene pruebas unitarias: valida el conjunto final
  y lo compara con `data/processed/ens_procesado.csv` de la Fase 2
  (`pd.testing.assert_frame_equal`).

## Pipeline de la Fase 2

El notebook de F2 implementa un pipeline de siete etapas:

Obtener → Explorar → Identificar códigos especiales → Limpiar
→ Transformar → Escalar → Validar

## Avance de la Fase 3: complejidad algorítmica

El notebook `F3/notebooks/f3_formativa_complejidad.ipynb` parte del
conjunto ya procesado en la Fase 2 (`ens_procesado.csv`). No rehace la
limpieza: se centra en medir la eficiencia del código y en decidir
si el proyecto justifica recursividad.

**Módulo `src/carga.py`**

| Función | Qué hace |
|---|---|
| `encontrar_raiz_proyecto` | Sube por las carpetas hasta encontrar la raíz del repositorio |
| `cargar_datos` | Lee `ens_procesado.csv` y avisa si el archivo no existe |
| `preparar` | Agrega `clave_busqueda` (identificador sintético; `IdEncuesta` se excluyó en la Fase 2) |
| `ejecutar` | Coordina el flujo: cargar y preparar |

**Módulo `src/medicion.py`**

| Función | Qué hace |
|---|---|
| `buscar_recorriendo` / `buscar_por_indice` | Acceso a una posición conocida: `iterrows()` frente a `.iloc` |
| `buscar_iterrows_por_clave` / `buscar_vectorizado` | Búsqueda real por clave: bucle frente a operación vectorizada |
| `construir_indice_pandas` / `buscar_indexado_pandas` | Búsqueda con `set_index` |
| `construir_indice_dict` / `buscar_indexado_dict` | Búsqueda con diccionario nativo |
| `medir_tiempo` | Repite la función y devuelve el tiempo mínimo |
| `medir_memoria` | Devuelve la memoria máxima usada (`tracemalloc`) |

**Criterios de optimización aplicados**

- Se comparan varias versiones del mismo cálculo y se verifica con
  `assert` que entregan el mismo resultado.
- Cada medición se repite y se conserva el tiempo mínimo, sobre el
  tamaño real del conjunto (5.511 filas).
- Se mide tiempo y memoria. Se separa el acceso por posición
  conocida de la búsqueda real por clave, y para esta última se
  calcula el punto de equilibrio entre buscar de forma vectorizada y
  construir un índice.
- La medición define la decisión: se adopta `set_index` de pandas
  para búsquedas repetidas, porque compensa su costo de
  construcción prácticamente desde la primera búsqueda. El diccionario
  nativo se descarta: necesita entre 430 y 450 búsquedas para
  compensar su construcción.
- **Recursividad:** no se justifica en el pipeline principal, cuya
  secuencia de nueve pasos es fija. Solo `aplanar()` (Fase 1) es
  recursiva, porque la profundidad del diccionario anidado no se
  conoce de antemano.


## Decisiones técnicas principales

- Se utiliza `Fexp_F1F2p_Corr` como ponderador porque el análisis
  combina variables de los formularios F1 y F2. La muestra elegible
  es de 5.520 personas de un total de 6.233.
- De seis variables candidatas a códigos especiales de no respuesta
  (as27, as28, di3, dis2, HTA, GPAQ), solo as28 contiene el código
  -9999 (818 casos detectados); no aparece -8888 en ninguna. No se
  identificaron casos de "no aplica": ninguna de estas variables
  depende de un salto condicional del cuestionario.
- Se eliminan 9 filas con HTA nulo (diagnóstico clínico binario: no
  se imputa un diagnóstico que nadie reportó). Quedan 5.511 filas.
- **as28: se convierte -9999 a NaN y NO se imputa.** Quedan 816
  personas sin as28 tras excluir las filas con HTA nulo. Se crea la
  bandera `as28_no_responde`. No se imputa con la moda para no
  ocultar la no respuesta bajo un tramo inventado.
- **as27 se imputa parcialmente:** de los 816 casos sin monto y sin
  tramo, se identifican 177 donde sí se conoce el tramo de as28; esos
  177 se imputan con la mediana de as27 dentro de su propio tramo
  (imputación estratificada). Los 816 casos restantes -sin monto ni
  tramo- quedan como NaN. Se crea la bandera `as27_imputado`.
- Imputar IMC con la mediana (37 nulos reales, 2,08% de atípicos por
  IQR) y años de estudio con la mediana (47 nulos reales).
- **GPAQ se imputa con la moda** (196 nulos, moda = 1 "Bajo"): variable
  ordinal con proporción faltante acotada; la moda conserva una
  categoría observada real, a diferencia de la media/mediana, que no
  respeta categorías ordinales discretas.
- di3 y dis2 se codifican con One-Hot Encoding usando el nombre real
  de cada categoría (Sí/No/No recuerda, etc.), verificado contra el
  libro de códigos oficial F1.
- GPAQ se reclasifica de nominal (Fase 1) a ordinal (Fase 2),
  conservando su orden en vez de aplicarle one-hot.

## Convención de commits

El equipo utiliza prefijos estandarizados para registrar cada avance en Git. 
Los mensajes deben ser breves, descriptivos y redactados en tiempo presente.

Prefijos usados: `docs`, `data`, `feat`, `fix`, `refactor`, `chore`.
* `feat:` Nueva funcionalidad, módulo o notebook analítico (ej. `feat: agrega funcion para detectar valores atipicos`).
* `fix:` Corrección de un error en código, rutas o cuadernos (ej. `fix: corrige lectura de fechas en formato dd-mm-yyyy`).
* `data:` Incorporación, filtrado o transformación de datos en `data/` (ej. `data: imputa valores faltantes de edad por la mediana`).
* `docs:` Cambios en la documentación, README u observaciones del informe (ej. `docs: actualiza decisiones tecnicas de la Fase 1`).
* `refactor:` Reorganización o optimización de código sin alterar sus resultados (ej. `refactor: modulariza funciones de limpieza en src/`).
* `chore:` Tareas de mantenimiento de la estructura o del entorno (ej. `chore: actualiza dependencias en requirements.txt`).

## Pendientes para la siguiente fase

- Confirmar contra el libro de códigos oficial F2 si GPAQ es
  efectivamente 1=Bajo, 2=Moderado, 3=Alto.
- Decidir si as27 debe escalarse con RobustScaler en vez de
  StandardScaler, dada su asimetría.
- Definir si el análisis usará Conglomerado, Estrato y
  Fexp_F1F2p_Corr para un diseño muestral complejo, o solo el
  ponderador de forma simple.
