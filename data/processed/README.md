# Archivos de `data/processed/`

| Archivo | Rol | Generado/usado en |
|---|---|---|
| `ens_variables_seleccionadas.xlsx` | Subconjunto de columnas seleccionadas desde el crudo, antes del filtro por ponderador. | `F2/notebooks/S1_F2_Preprocesamiento.ipynb` |
| `ens_variables_f1f2.xlsx` | Conjunto filtrado por `Fexp_F1F2p_Corr` (5.520 personas), **antes** de la limpieza. Es el insumo del pipeline de clases. | `F2/notebooks/S1_F2_Preprocesamiento.ipynb`, `F3/notebooks/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb` |
| `ens_procesado.csv` | **Archivo vigente.** Resultado final tras imputación, codificación y escalamiento (5.511 × 23). Es la referencia contra la que se valida el pipeline de la Fase 3. | Salida de la Fase 2; usado como referencia en la sección de validación estructural de `S2_F3_...ipynb` |

`ens_procesado.csv` es el único de los tres pensado para análisis posterior (modelado, estadística descriptiva). Los dos `.xlsx` son insumos intermedios del proceso de preprocesamiento y se conservan por trazabilidad y reproducibilidad.
