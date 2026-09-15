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

proyecto-grupo4-mcdi500/
├── data/
│ ├── raw/ens2016.xlsx Base original, sin modificar
│ └── processed/ Subconjuntos generados por código
├── F1/
│ └── notebooks/S1_F1_Definicion.ipynb
├── F2/
│ ├── notebooks/S1_F2_Preprocesamiento.ipynb
│ └── docs/ Diccionario, resumen del filtro, metadatos
├── docs/ Informe de validación general
├── src/ tests/ Reservados para próximas fases
├── .gitignore
├── requirements.txt
└── README.md


## Requisitos y ejecución

Python 3.13.

```bash
git clone https://github.com/fdiaztoro/proyecto-grupo4-mcdi500.git
cd proyecto-grupo4-mcdi500

python3 -m venv .venv
source .venv/bin/activate        # macOS y Linux
# .venv\Scripts\activate         # Windows

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python -m ipykernel install --user --name grupo4_mcdi500 \
    --display-name "Python (grupo4-mcdi500)"
```

Abrir JupyterLab (o VS Code) y ejecutar, en este orden, seleccionando
el kernel **Python (grupo4-mcdi500)**:

1. `F1/notebooks/S1_F1_Definicion.ipynb`
2. `F2/notebooks/S1_F2_Preprocesamiento.ipynb`

Ambos notebooks deben correr de principio a fin sin errores
(Kernel → Restart Kernel and Run All Cells).

## Pipeline de la Fase 2

El notebook de F2 implementa un pipeline de siete etapas:

Obtener → Explorar → Identificar códigos especiales → Limpiar
→ Transformar → Escalar → Validar


## Decisiones técnicas principales

- Se utiliza `Fexp_F1F2p_Corr` como ponderador porque el análisis
  combina variables de los formularios F1 y F2. La muestra elegible
  es de 5.520 personas de un total de 6.233.
- De seis variables candidatas a códigos especiales de no respuesta
  (as27, as28, di3, dis2, HTA, GPAQ), solo as28 contiene el código
  -9999; no aparece -8888 en ninguna. No se identificaron casos de
  "no aplica".
- Se eliminan 9 filas con HTA nulo (diagnóstico clínico binario: no
  se imputa un diagnóstico que nadie reportó).
- as27 (ingreso del hogar) se imputa por mediana según grupo de edad,
  tras comparar cuatro estrategias con evidencia cuantitativa.
- **as28 y GPAQ NO se imputan**: se dejan como faltantes genuinos
  (Int64 nullable). Las 818 personas sin as28 tampoco tienen as27
  (ninguna superposición), lo que sugiere que la no respuesta de
  ingreso no es aleatoria. GPAQ no está documentado como variable
  cruda en los libros de códigos F1/F2 disponibles; su codificación
  (1=Bajo, 2=Moderado, 3=Alto) se asume por ser el estándar del
  cuestionario GPAQ de la OMS, pendiente de verificar antes de la
  Fase 3.
- di3 y dis2 se codifican con One-Hot Encoding usando el nombre real
  de cada categoría (Sí/No/No recuerda, etc.), verificado contra el
  libro de códigos oficial F1.
- GPAQ se reclasifica de nominal (Fase 1) a ordinal (Fase 2),
  conservando su orden en vez de aplicarle one-hot.

## Convención de commits

Prefijos usados: `docs`, `data`, `feat`, `fix`, `refactor`, `chore`.

## Pendientes para la Fase 3

- Confirmar contra el libro de códigos oficial F2 si GPAQ es
  efectivamente 1=Bajo, 2=Moderado, 3=Alto.
- Decidir si as27 debe escalarse con RobustScaler en vez de
  StandardScaler, dada su asimetría.
- Definir si el análisis usará Conglomerado, Estrato y
  Fexp_F1F2p_Corr para un diseño muestral complejo, o solo el
  ponderador de forma simple.
