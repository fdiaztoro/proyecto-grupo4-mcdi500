# Changelog · proyecto-grupo4-mcdi500

Registro cronológico de las mejoras del proyecto, de la Fase 1 a la Fase 4. Cada entrada
corresponde a una fila de la tabla de la sección IX (Trazabilidad de mejoras) del notebook
`F4/notebooks/S3_F4_Consolidado.ipynb` e indica los commits y pull requests (PR) donde
puede verificarse en GitHub.

---

## Fase 1 a Fase 2 · Preparación de datos

### GPAQ reclasificada de nominal a ordinal
- Observación: GPAQ se había declarado nominal en la Fase 1.
- Cambio: se trata como ordinal (Bajo < Moderado < Alto) y se conserva como entero, sin one-hot.
- Evidencia: F2, sección 5.

### 2026-09-12 · Código -9999 de as28 tratado como no respuesta
- Observación: el código -9999 de as28 se leía como un ingreso válido.
- Cambio: se identifican los códigos especiales de no respuesta variable por variable; en as28
  se convierten en nulo y se registran en la bandera `as28_no_responde` (818 casos detectados;
  816 en el conjunto final, tras excluir las 9 filas sin HTA).
- Commit: d97ce95 (Felipe Díaz Toro), incorporado en el PR #1.

### 2026-09-15 · Imputación parcial de as27 por tramo de ingreso
- Observación: as27 y as28 comparten la misma no respuesta económica (816 personas).
- Cambio: as27 se imputa con la mediana de su tramo as28 solo cuando el tramo es conocido
  (177 casos); los 816 faltantes genuinos se conservan y quedan documentados.
- Commits: c2b766f (Ninoska Yévenes Hernández) y 5c73c95 (Felipe Díaz Toro), incorporados en el PR #1.

---

## Fase 2 a Fase 3 · Repositorio y orientación a objetos

### 2026-09-24 · Preprocesamiento reescrito con clases y Pipeline
- Observación: el preprocesamiento estaba en funciones sueltas con ramas if.
- Cambio: clase base `Transformador`, siete pasos de preprocesamiento, patrón Strategy en la
  imputación y clase `Pipeline` que los encadena.
- Commits: 12829fa (Felipe Díaz Toro, PR #8), 65b9e6d (Felipe Díaz Toro, PR #10) y
  352e2ae (Ninoska Yévenes Hernández, PR #11).

### 2026-09-25 / 2026-09-26 · Base original fuera del control de versiones
- Observación (retroalimentación): la base original ens2016.xlsx (13,6 MB) estaba versionada.
- Cambio: se deja de versionar ens2016.xlsx y se declara `data/processed/ens_procesado.csv`
  como archivo vigente.
- Commits: f0f312d y e7c2ab7 (Felipe Díaz Toro), incorporados en el PR #20.

---

## Fase 3 · Núcleo algorítmico, eficiencia y pruebas

### 2026-09-23 · Medición de eficiencia corregida según retroalimentación
- Observación (retroalimentación): la comparación iterrows frente a .iloc medía acceso por
  posición, no una búsqueda.
- Cambio: se agrega la búsqueda real por clave, la medición de memoria y el punto de
  equilibrio; las funciones de medición pasan a `src/medicion.py`.
- Commit: 0beaeb0 (Felipe Díaz Toro), PR #2.

### 2026-09-26 · Pruebas separadas en tests/
- Observación: las pruebas vivían dentro de `src/validador.py`.
- Cambio: se separan en `tests/` (59 pruebas por clase y 13 de transformadores), ejecutables
  con pytest; 72 pruebas aprobadas.
- Commits: 3453e13 y 366920b (Pablo Ríos Passteni), PR #19.

### 2026-09-27 · Índice por diccionario sin iterrows
- Observación: `construir_indice_dict` usaba iterrows e inflaba el punto de equilibrio
  (437 búsquedas).
- Cambio: se reescribe con `dict(zip(...))` y se repite la comparación; el punto de
  equilibrio queda en menos de una búsqueda frente a iterrows.
- Commit: 2ca4310 (Felipe Díaz Toro), PR #25.

---

## Fase 3 a Fase 4 · Visualización y comunicación

### 2026-09-29 · Conjunto interpretable df_visual
- Observación: el conjunto procesado (escalado y one-hot) era ilegible para graficar.
- Cambio: `df_visual` se captura del pipeline antes de codificar y escalar, con etiquetas
  según el libro de códigos ENS; las figuras quedan en unidades reales (años, kg/m2).
- Commit: 0ba9908 (Felipe Díaz Toro), PR #29.

### 2026-09-29 / 2026-09-30 · Ponderación por factor de expansión
- Observación: las tasas describían la muestra, no la población (HTA 36,3 %).
- Cambio: las tasas se ponderan con `Fexp_F1F2p_Corr` (HTA 27,6 %, igual a la cifra
  oficial de MINSAL); se agrega el complemento ponderado a la Figura 2 y se declara qué
  se pondera y qué no (secciones 1.5 y 8.1).
- Commits: 0ba9908 (Felipe Díaz Toro, PR #29), 56c161b (Ninoska Yévenes Hernández, PR #31)
  y 7877193 (Ninoska Yévenes Hernández, PR #33).

### 2026-09-30 · Selección de tres figuras con hilo narrativo
- Observación: cinco objetivos explorados, sin jerarquía entre ellos.
- Cambio: se seleccionan tres figuras oficiales con el hilo contexto, contraste y
  resolución, y cada interpretación explica cómo aporta al relato.
- Commits: 30c8b23 (PR #30) y 4546205 (PR #33), ambos de Ninoska Yévenes Hernández.
