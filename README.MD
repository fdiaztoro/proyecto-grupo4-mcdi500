# Grupo 4 — MCDI500

Factores sociodemográficos y riesgo cardiovascular en la Encuesta
Nacional de Salud (ENS) 2016–2017.

## Integrantes

- Felipe Díaz Toro
- Pablo Ríos Passteni
- Guillermo Subiabre Chacón
- Ninoska Yévenes Hernández

## Pregunta de investigación

¿Cómo se relacionan la edad, el sexo, la educación, el ingreso del
hogar y la zona de residencia con los indicadores de riesgo
cardiovascular seleccionados en participantes de la ENS 2016–2017?

## Datos

- **Fuente:** Encuesta Nacional de Salud (ENS) 2016–2017, Ministerio
  de Salud de Chile (MINSAL).
- **Archivo base:** `F2/data/raw/ens2016.xlsx` (6.233 registros,
  1.173 columnas originales). Incluido en el repositorio.
- **Subconjunto seleccionado:** `F2/data/processed/ens_variables_seleccionadas.xlsx`
  (16 variables, 6.233 filas).
- **Subconjunto elegible F1–F2:** `F2/data/processed/ens_variables_f1f2.xlsx`
  (5.520 filas, filtrado por el ponderador `Fexp_F1F2p_Corr`).
- **Ponderador utilizado:** `Fexp_F1F2p_Corr` (componente combinado F1–F2).

## Estructura del repositorio
F1/
├── data/ (reservado, sin datos propios aun)
└── notebooks/
└── S1_F1_Definicion.ipynb Definicion del problema y entorno

F2/
├── data/
│ ├── raw/ens2016.xlsx Base original (sin modificar)
│ └── processed/ Subconjuntos generados por codigo
├── docs/
│ ├── informe_validacion_f1f2.md
│ └── resumen_filtro_f1f2.csv
└── notebooks/
└── S1_F2_Preprocesamiento.ipynb Seleccion, filtro y validacion

## Requisitos y ejecución

Python 3.13.

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

Ambos notebooks deben correr de principio a fin sin errores
(Kernel → Restart Kernel and Run All Cells).

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

## Decisiones técnicas

- Se utiliza `Fexp_F1F2p_Corr` como ponderador porque el análisis
  combina variables de los formularios F1 y F2. La muestra elegible
  es de 5.520 personas de un total de 6.233 (713 excluidas por
  ponderador no válido). La suma de ponderadores del subconjunto
  (~14.518.969) es consistente con la población de referencia del
  informe metodológico de la ENS 2016–2017.
- La base original y los subconjuntos procesados se versionan en el
  repositorio porque son livianos (menos de 15 MB en total) y
  provienen de una encuesta pública de acceso abierto.
- Los códigos de no respuesta (no sabe, no responde, no aplica) aún
  no se han diferenciado; esa tarea corresponde a la limpieza en F2.

## Pendientes

- Exploración documentada (distribuciones, gráficos) en F2.
- Diferenciación de códigos no sabe / no responde / no aplica.
- Limpieza y transformación de variables.
- Análisis del efecto de las exclusiones sobre la representatividad.
- Módulos reutilizables en `src/` y pruebas en `tests/`.
