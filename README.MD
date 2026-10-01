# Grupo 4 — MCDI500

Factores sociodemográficos y su asociación con factores de riesgo
cardiovascular, utilizando la Encuesta Nacional de Salud (ENS)
2016-2017 de Chile.

## Integrantes

- Felipe Díaz Toro
- Pablo Ríos Passteni
- Guillermo Subiabre Chacón
- Ninoska Yévenes Hernández

Docente: Omar Salinas

## Contexto y problema

Las enfermedades cardiovasculares son la principal causa de muerte en Chile
y en el mundo. Según la Encuesta Nacional de Salud (ENS) 2016-2017 del
Ministerio de Salud, la prevalencia nacional de hipertensión arterial
alcanza 27,6% y la de sospecha de diabetes mellitus 12,3% en personas de 15
años y más (MINSAL, 2017). Estas cifras agregadas no informan cómo se
distribuye el riesgo al interior de la población.

Se dispone de registros individuales de la ENS 2016-2017, pero no de una
caracterización de cómo el perfil sociodemográfico de las personas
encuestadas se asocia con los principales indicadores de riesgo
cardiovascular disponibles en la encuesta.

## Pregunta de investigación

¿Cómo se relacionan las condiciones sociodemográficas (edad, sexo, nivel
educacional, ingreso del hogar y zona de residencia) con la presencia de
hipertensión arterial, diabetes, colesterol alto, índice de masa corporal
y nivel de actividad física en los participantes de la ENS 2016-2017?

### Objetivo general

Caracterizar la relación entre las condiciones sociodemográficas de los
participantes (edad, sexo, nivel educacional, ingreso del hogar y zona de
residencia) y la presencia de hipertensión arterial, diabetes, colesterol
alto, un índice de masa corporal elevado y un nivel insuficiente de
actividad física en la ENS 2016-2017.

### Objetivos específicos

1. Comparar la prevalencia de hipertensión arterial entre los distintos
   grupos etarios.
2. Describir cómo varía la prevalencia de diabetes según el grupo etario y
   la zona de residencia.
3. Analizar la relación entre el nivel educacional y la presencia de
   colesterol alto.
4. Examinar la asociación entre el índice de masa corporal y el nivel de
   actividad física.
5. Evaluar si la relación entre edad e índice de masa corporal, en
   presencia de hipertensión, se mantiene al estratificar por sexo.

### Alcance y limitaciones

El análisis es descriptivo y exploratorio: no incluye modelamiento
predictivo ni pruebas de hipótesis formales, y las asociaciones que se
presentan son descriptivas, no causales. La ENS tiene diseño muestral
complejo (conglomerados y estratos); las cifras que se citan en el texto
se ponderan por el factor de expansión `Fexp_F1F2p_Corr` para ser
comparables con MINSAL, pero no se estima varianza ni intervalos de
confianza por diseño muestral (fuera del alcance del curso). El detalle
completo de alcance, restricciones y supuestos está documentado en la
Parte I (1.5) de `F4/notebooks/S3_F4_Consolidado.ipynb`.

## Datos

- **Fuente:** Encuesta Nacional de Salud (ENS) 2016-2017, Ministerio
  de Salud de Chile (MINSAL).
- **Archivo base (no versionado):** `data/raw/ens2016.xlsx` (6.233
  registros, 1.173 columnas originales, 13,6 MB). Por su tamaño no se
  incluye en el repositorio (está en `.gitignore`). Para ejecutar F1 y
  F2, descargue la «Base Formulario 1-Formulario 2 y exámenes» de la
  ENS 2016-2017 desde la sección Bases de datos del Departamento de
  Epidemiología del MINSAL (<https://epi.minsal.cl/bases-de-datos/>). Si
  la descarga no viene en Excel, conviértala a `.xlsx` (hoja `Sheet1`)
  y guárdela como `data/raw/ens2016.xlsx`. Los notebooks de F3 y F4 no lo
  necesitan: parten de los archivos de `data/processed/`, que sí están
  en el repositorio.
- **Subconjunto seleccionado:** `data/processed/ens_variables_seleccionadas.xlsx`
  (16 variables, 6.233 filas).
- **Subconjunto elegible F1-F2:** `data/processed/ens_variables_f1f2.xlsx`
  (5.520 filas, filtrado por el ponderador `Fexp_F1F2p_Corr`).
- **Subconjunto procesado final (vigente):** `data/processed/ens_procesado.csv`
  (5.511 filas, 23 columnas, limpio y listo para el análisis). El papel de
  cada archivo de `data/processed/` se detalla en
  `data/processed/README.md`.
- **Ponderador utilizado:** `Fexp_F1F2p_Corr` (componente combinado F1-F2),
  aplicado a las cifras del texto (tasas y promedios); las distribuciones
  de los gráficos de caja y dispersión se muestran sin ponderar (ver
  Alcance y limitaciones).

## Estructura del repositorio

```
proyecto-grupo4-mcdi500/
├── data/
│ ├── raw/ens2016.xlsx Base original (no versionada: descargar, ver «Datos»)
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
├── F4/
│ ├── notebooks/S3_F4_Consolidado.ipynb Sumativa 3: resultados, discusión y conclusiones
│ ├── figuras/ Las tres figuras oficiales exportadas en PNG
│ └── changelog.md Registro cronológico de mejoras, de F1 a F4
├── src/
│ ├── carga.py Carga y preparación del conjunto de la Fase 3
│ ├── medicion.py Funciones de búsqueda y medición de tiempo y memoria
│ ├── transformador.py Clase base Transformador (ajustar / transformar)
│ ├── imputadores.py No respuesta, eliminación de filas e imputación (patrón Strategy)
│ ├── transformadores.py Codificación one-hot, escalamiento, eliminación de columnas y conversión a entero
│ ├── pipeline.py Encadena los pasos del preprocesamiento en orden
│ └── validador.py Valida el resultado y lo compara con la Fase 2
├── docs/
│ └── evidencias/ Notebooks de F1 a F4 ejecutados en HTML/PDF (con salidas)
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
5. `F4/notebooks/S3_F4_Consolidado.ipynb`

F1 y F2 leen `data/raw/ens2016.xlsx`, que no está en el repositorio (ver
«Datos»). Los notebooks de F3 y F4 se pueden ejecutar sin ese archivo.

Los notebooks deben correr de principio a fin sin errores
(Kernel → Restart Kernel and Run All Cells). Los notebooks de F3 y F4
importan su código desde `src/`: la formativa usa `carga.py` y
`medicion.py`; el de la Sumativa 2 usa además las clases de
`transformador.py`, `imputadores.py` y `transformadores.py`; el de la
Sumativa 3 reutiliza el pipeline completo para validar reproducibilidad.

**Nota sobre las salidas:** los `.ipynb` se guardan sin salidas por
`nbstripout` (paso 4), para mantener limpio el historial de Git. La
ejecución completa de cada notebook, con sus salidas, está en
`docs/evidencias/` (F1 a F4).

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

## Fase 3: complejidad algorítmica y programación orientada a objetos

La Fase 3 tiene dos notebooks: la Formativa 3 (mide el costo de distintas
formas de buscar un registro) y la Sumativa 2 (reescribe el preprocesamiento
de la Fase 2 como clases). Los dos comparten el código de `src/`.

### Formativa 3: complejidad algorítmica

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
  nativo también se paga, pero necesita del orden de cien búsquedas
  cuando se arma con `dict(zip(...))` (con `iterrows()` eran más de
  400: la construcción, y no el diccionario, era lo que encarecía la
  comparación).
- **Recursividad:** no se justifica en el pipeline principal, cuya
  secuencia es fija y conocida (las nueve decisiones de la Fase 2, que
  en la Sumativa 2 son 17 pasos). Solo `aplanar()` (Fase 2) es
  recursiva, porque la profundidad del diccionario anidado no se
  conoce de antemano.

### Sumativa 2: preprocesamiento en clases

El notebook `F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb`
parte de `ens_variables_f1f2.xlsx` (5.520 filas, antes de limpiar) y
reescribe cada paso de la Fase 2 como una clase. El criterio de éxito es
que el pipeline produzca exactamente `ens_procesado.csv` (5.511 filas ×
23 columnas); el notebook lo verifica valor por valor con
`verificar_contra_fase2`.

Secciones del notebook: 1 carga · 2 pipeline en clases (imputación,
encapsulamiento y herencia) · 3 validación (59 pruebas: normal, límite y
excepción) · 4 codificación · 5 escalamiento · 6 eficiencia (`timeit` y
`tracemalloc`) · 7 patrón Strategy en la imputación · 8 arquitectura y
conclusiones.

| Módulo | Contenido |
|---|---|
| `src/transformador.py` | Clase base `Transformador`: `ajustar()` calcula parámetros y `transformar()` los aplica sobre una copia; el estado queda en atributos internos |
| `src/imputadores.py` | `MarcadorNoRespuesta`, `EliminadorFilasNulas` e `ImputadorFlexible`, que recibe una estrategia (`PorMedia`, `PorMediana`, `PorModa`, `PorMedianaDeTramo`) |
| `src/transformadores.py` | `CodificadorOneHot`, `EscaladorEstandar`, `EliminadorColumna` y `ConvertidorEntero` |
| `src/pipeline.py` | `Pipeline`: ajusta y aplica los pasos en orden, sin conocer su tipo |
| `src/validador.py` | `verificar_contra_fase2` y funciones para comparar resultados |

**Decisiones de diseño de la Fase 3**

- **El orden de los pasos importa.** Las 9 filas sin `HTA` se eliminan
  antes de imputar: si se imputa antes, la mediana del IMC cambia
  (28,3167 en vez de 28,3124) y el resultado deja de coincidir con la
  Fase 2.
- **Patrón Strategy en la imputación.** Cada forma de rellenar es una
  clase intercambiable. Para `as27`: la media y la mediana reducen la
  dispersión cerca de un 9 % (rellenan también a quienes no declararon
  ingreso); la mediana por tramo casi no la altera (−0,70 %) pero solo
  rellena 177 casos y deja 816 sin valor.
- **División funcional en lugar de recursividad:** el pipeline es una
  secuencia fija; cada transformación es una clase independiente.
- **Extensibilidad:** un paso nuevo se agrega sin modificar `Pipeline`
  ni las clases existentes (demostrado en el notebook).

## Fase 4: resultados, discusión y cierre

El notebook `F4/notebooks/S3_F4_Consolidado.ipynb` toma el pipeline
validado en la Fase 3 y lo usa para responder la pregunta de
investigación: explora los cinco objetivos específicos, selecciona tres
figuras oficiales con su interpretación, y discute los resultados a la
luz de la literatura y las cifras de MINSAL.

**Cómo se resolvieron las decisiones que quedaron abiertas al cierre de la Fase 3**

- **Diseño muestral complejo.** Se optó por el ponderador simple
  (`Fexp_F1F2p_Corr`) para las cifras que se citan en el texto, de forma
  que sean comparables con las oficiales de MINSAL. No se implementó el
  diseño muestral completo con `Conglomerado` y `Estrato`: eso requiere
  herramientas fuera del alcance del curso (paquete `survey` de R o
  `samplics` de Python). Queda declarado como limitación en la Parte I
  (1.5) y retomado en la discusión (Parte VIII).
- **Escalamiento de `as27`.** Se mantuvo `EscaladorEstandar`, igual que
  para `Edad` e `IMC`; no se evaluó `RobustScaler` pese a la asimetría de
  `as27` identificada en la Fase 3. Queda como mejora pendiente para una
  futura iteración del proyecto.
- **Personas sin ingreso declarado (816 casos sin `as27` ni `as28`).** Se
  mantienen como valores faltantes explícitos en todo el análisis, sin
  imputación adicional; la Parte I y la Parte VIII documentan esta
  decisión como una limitación reconocida, no una omisión.
- **Codificación de `GPAQ`.** Se confirmó contra el libro de códigos
  oficial de la ENS que la escala 1=Bajo, 2=Moderado, 3=Alto es correcta.

**Qué entrega la Fase 4**

- Los cinco objetivos específicos explorados (Parte V) y las tres figuras
  oficiales con su interpretación (Parte VI).
- Resultados, discusión y conclusiones con mejoras propuestas basadas en
  evidencia (Parte VIII).
- Trazabilidad completa de las mejoras del proyecto, de F1 a F4, con
  commits y PR verificables (Parte IX, `F4/changelog.md`).
- Verificación final de reproducibilidad: huellas de las figuras, igualdad
  con `ens_procesado.csv`, 59 pruebas por clase (Parte X).

Con esto, el proyecto queda cerrado para la Sumativa 3.

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
