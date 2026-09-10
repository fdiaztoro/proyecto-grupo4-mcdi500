# Validación del dataset — MCDI500

**Archivo:** `ens_variables_f1f2.xlsx` · 5520 filas × 16 columnas

## Perfil de variables

| variable | dtype | rol | unicos | pct_nulos |
| --- | --- | --- | --- | --- |
| IdEncuesta | int64 | identificador | 5520 | 0.0 |
| FechaInicioF1 | datetime64[us] | fecha | 5512 | 0.0 |
| Edad | int64 | discreta | 83 | 0.0 |
| Sexo | int64 | binaria | 2 | 0.0 |
| Zona | int64 | binaria | 2 | 0.0 |
| HTA | float64 | binaria | 2 | 0.2 |
| di3 | int64 | discreta | 3 | 0.0 |
| dis2 | int64 | discreta | 4 | 0.0 |
| IMC | float64 | continua | 5332 | 0.7 |
| anos_estudio_MINSAL_1 | float64 | discreta | 23 | 0.9 |
| GPAQ | float64 | discreta | 3 | 3.6 |
| as27 | float64 | continua | 254 | 18.0 |
| as28 | int64 | discreta | 12 | 0.0 |
| Fexp_F1F2p_Corr | float64 | continua | 4764 | 0.0 |
| Conglomerado | int64 | continua | 1075 | 0.0 |
| Estrato | int64 | discreta | 30 | 0.0 |

## Requisitos del curso

| estado | requisito | detalle |
| --- | --- | --- |
| OK | Al menos 2000 filas | 5520 filas |
| OK | Al menos 12 columnas | 16 columnas |
| OK | Combina al menos 3 roles analíticos | discreta, continua, binaria, fecha |
| OK | Al menos una variable numérica | 11 numéricas (continuas o discretas) |
| OK | Al menos una variable categórica | 3 categóricas (nominales, binarias u ordinales) |
| OK | Presencia de valores faltantes | máximo 18.0% en una variable |
| OK | Ninguna variable sobre 60% de faltantes | máximo 18.0% |
| OK | Incluye alguna variable de fecha | 1 detectadas |
| AVISO | Incluye texto o categórica de alta cardinalidad | 0 detectadas |
| OK | Archivo bajo 100 MB | 0.5 MB |
| OK | Sin filas duplicadas exactas | ninguna |

## Resultado

El conjunto **cumple** los requisitos mínimos.