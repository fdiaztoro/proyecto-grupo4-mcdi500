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
│ ├── notebooks/f3_formativa_complejidad.ipynb
│ └── docs/evidencias/ Notebook de F3 ejecutado en HTML/PDF (con salidas)
├── src/
│ └── medicion.py Funciones de búsqueda y medición de tiempo y memoria
├── docs/
│ └── evidencias/ Notebooks de F1 y F2 ejecutados en HTML/PDF (con salidas)
├── tests/ Reservado para próximas fases
├── .gitignore
├── requirements.txt
└── README.MD
```


## Requisitos y ejecución

Python 3.13.X

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

Abrir JupyterLab (o VS Code) y ejecutar, en este orden, seleccionando
el kernel **Python (grupo4-mcdi500)**:

1. `F1/notebooks/S1_F1_Definicion.ipynb`
2. `F2/notebooks/S1_F2_Preprocesamiento.ipynb`
3. `F3/notebooks/f3_formativa_complejidad.ipynb`

Los tres notebooks deben correr de principio a fin sin errores
(Kernel → Restart Kernel and Run All Cells). El notebook de F3
importa las funciones desde `src/medicion.py`.

**Nota sobre las salidas:** los `.ipynb` se guardan sin salidas por
`nbstripout` (paso 4), para mantener limpio el historial de Git. La
ejecución completa de cada notebook, con sus salidas, está en
`docs/evidencias/` (F1 y F2) y `F3/docs/evidencias/` (F3).

## Pipeline de la Fase 2

El notebook de F2 implementa un pipeline de siete etapas:

Obtener → Explorar → Identificar códigos especiales → Limpiar
→ Transformar → Escalar → Validar

## Avance de la Fase 3: complejidad algorítmica

El notebook `F3/notebooks/f3_formativa_complejidad.ipynb` parte del
conjunto ya procesado en la Fase 2 (`ens_procesado.csv`). No rehace la
limpieza: se centra en medir la eficiencia del código y en decidir
si el proyecto justifica recursividad.

**Módulo `src/medicion.py`**

| Función | Qué hace |
|---|---|
| `buscar_recorriendo` | Ubica una fila recorriendo el DataFrame con `iterrows()` |
| `buscar_por_indice` | Ubica una fila por posición con `.iloc` |
| `medir_tiempo` | Repite la función y devuelve el tiempo mínimo |
| `medir_memoria` | Devuelve la memoria máxima usada (`tracemalloc`) |

**Criterios de optimización aplicados**

- Se comparan dos versiones del mismo cálculo (búsqueda de un
  registro) y se verifica con `assert` que entregan el mismo resultado.
- Cada medición se repite y se conserva el tiempo mínimo, sobre el
  tamaño real del conjunto (5.511 filas).
- Se mide tiempo y memoria, y se calcula el punto de equilibrio entre
  ambos enfoques (1, 10 y 100 búsquedas).
- La medición define la decisión: el acceso por posición resulta
  más rápido y usa menos memoria que el recorrido, por lo que es el
  enfoque adoptado para búsquedas repetidas.
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
