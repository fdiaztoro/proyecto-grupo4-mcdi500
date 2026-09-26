"""
Validación del resultado del pipeline de preprocesamiento de la ENS 2016-2017.

¿Para qué sirve este archivo?
Para comprobar que el conjunto que entrega el pipeline hecho con clases está
bien y que es igual al que guardó la Fase 2. Se usa desde el notebook,
importando sus funciones.

Tiene dos partes:
  1. Validación del resultado sobre el conjunto real: filas, columnas
     eliminadas, nulos documentados, tipos numéricos y grupos one-hot.
       -> validar_resultado()
  2. Equivalencia con la Fase 2: el pipeline con clases debe producir lo mismo
     que data/processed/ens_procesado.csv (pd.testing.assert_frame_equal).
       -> verificar_equivalencia(), verificar_contra_fase2() e
          informe_diferencias() (dónde están las diferencias si las hay)

No importa ninguna clase del proyecto: el pipeline se recibe como parámetro.
Así este módulo solo valida y no decide qué pasos tiene el preprocesamiento
(bajo acoplamiento).

Las pruebas de cada clase por separado (normal, límite y excepción) están en
tests/casos_por_clase.py.
"""

import numpy as np
import pandas as pd


# Valores que dejó documentados la Fase 2 (ver README y F2/notebooks).
# Ruta del archivo resultado de la Fase 2, contra el que se compara.
RUTA_REFERENCIA_FASE2 = "data/processed/ens_procesado.csv"
# Filas que quedan tras eliminar las 9 personas sin HTA.
FILAS_FASE2 = 5511
# Nulos que se dejaron a propósito: las personas que no declararon ingreso.
NULOS_FASE2 = {"as27": 816, "as28": 816}
# Columnas que la Fase 2 elimina del resultado final.
COLUMNAS_EXCLUIDAS_FASE2 = ("IdEncuesta", "FechaInicioF1")
# Columnas 0/1 (one-hot): en cada fila, las de un mismo grupo deben sumar exactamente 1.
# Se escriben a mano (no se leen de MAPEO_CATEGORIAS) para que la validación sea
# independiente del código que valida: si alguien cambia un nombre allá, esto lo detecta.
GRUPOS_ONE_HOT_FASE2 = {
    "Sexo": ["Sexo_Hombre", "Sexo_Mujer"],
    "Zona": ["Zona_Urbano", "Zona_Rural"],
    "di3": ["di3_Si", "di3_No", "di3_No_recuerda"],
    "dis2": ["dis2_Si_una_vez", "dis2_Si_mas_de_una_vez", "dis2_Nunca", "dis2_No_recuerda"],
}


# ---------------------------------------------------------------------------
# Validación del resultado sobre el conjunto real
# ---------------------------------------------------------------------------

def validar_resultado(df, filas_esperadas=None, nulos_esperados=None,
                      columnas_ausentes=(), grupos_one_hot=None):
    """Comprueba integridad y consistencia de la salida del pipeline. Lanza AssertionError si falla.

    En simple: revisa que el resultado final tenga sentido. Comprueba que:
      1. Tiene la cantidad de filas esperada (filas_esperadas).
      2. Ya no están las columnas que debían eliminarse (columnas_ausentes).
      3. Los nulos están solo donde se dejaron a propósito y en la cantidad
         exacta (nulos_esperados).
      4. Todas las columnas son numéricas.
      5. Cada grupo de columnas 0/1 (one-hot) suma exactamente 1 por fila
         (grupos_one_hot).

    nulos_esperados es {columna: cantidad} para los faltantes que se dejaron a
    propósito: cualquier otro nulo, o una cantidad distinta, hace fallar la prueba.
    Si todo está bien imprime líneas [OK] y devuelve True.
    """
    if filas_esperadas is not None:
        assert len(df) == filas_esperadas, \
            f"Se esperaban {filas_esperadas} filas y hay {len(df)}: el pipeline perdió o duplicó filas"
        print(f"[OK] {len(df)} filas")

    presentes = [c for c in columnas_ausentes if c in df.columns]
    assert not presentes, f"Columnas que debían eliminarse y siguen presentes: {presentes}"

    nulos = {c: int(n) for c, n in df.isna().sum().items() if n > 0}
    esperados = nulos_esperados or {}
    assert nulos == esperados, f"Nulos distintos a los documentados. Hay {nulos}; se esperaban {esperados}"
    print(f"[OK] Nulos solo donde se documentaron: {nulos or 'ninguno'}")

    no_numericas = df.select_dtypes(exclude=[np.number]).columns.tolist()
    assert not no_numericas, f"Columnas no numéricas: {no_numericas}"
    print("[OK] Todas las columnas son numéricas")

    for nombre, columnas in (grupos_one_hot or {}).items():
        assert (df[columnas].sum(axis=1) == 1).all(), f"El grupo one-hot '{nombre}' no suma 1 en todas las filas"
        print(f"[OK] Grupo one-hot '{nombre}' coherente")
    return True


# ---------------------------------------------------------------------------
# Equivalencia con la Fase 2
# ---------------------------------------------------------------------------

def informe_diferencias(obtenido, referencia, rtol=1e-5, atol=1e-8):
    """Una fila por columna: si está en ambos conjuntos, sus tipos y cuántos valores difieren.

    En simple: compara dos tablas columna por columna y devuelve una tabla con:
      - en_obtenido / en_referencia: si la columna existe en cada conjunto.
      - tipo_obtenido / tipo_referencia: el tipo de dato en cada uno.
      - n_distintos: cuántos valores no coinciden (con la tolerancia rtol/atol).
      - max_dif_abs: la mayor diferencia entre valores numéricos.
    Sirve para saber exactamente dónde están las diferencias cuando la
    comparación falla.
    """
    columnas = list(referencia.columns) + [c for c in obtenido.columns if c not in referencia.columns]
    mismas_filas = len(obtenido) == len(referencia)
    filas = []
    for columna in columnas:
        en_obtenido, en_referencia = columna in obtenido.columns, columna in referencia.columns
        fila = {
            "columna": columna,
            "en_obtenido": en_obtenido,
            "en_referencia": en_referencia,
            "tipo_obtenido": str(obtenido[columna].dtype) if en_obtenido else "-",
            "tipo_referencia": str(referencia[columna].dtype) if en_referencia else "-",
            "n_distintos": None,
            "max_dif_abs": None,
        }
        if en_obtenido and en_referencia and mismas_filas:
            a = obtenido[columna].reset_index(drop=True)
            b = referencia[columna].reset_index(drop=True)
            if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):
                x = a.to_numpy(dtype="float64", na_value=np.nan)
                y = b.to_numpy(dtype="float64", na_value=np.nan)
                iguales = np.isclose(x, y, rtol=rtol, atol=atol, equal_nan=True)
                dif = np.abs(x - y)
                fila["max_dif_abs"] = 0.0 if np.isnan(dif).all() else float(np.nanmax(dif))
            else:
                iguales = ((a == b) | (a.isna() & b.isna())).to_numpy()
            fila["n_distintos"] = int((~iguales).sum())
        filas.append(fila)
    return pd.DataFrame(filas)


def verificar_equivalencia(obtenido, referencia, columnas=None, verificar_tipos=True,
                           ignorar_orden_columnas=False, rtol=1e-5, atol=1e-8):
    """Comprueba con pd.testing.assert_frame_equal que dos conjuntos son iguales.

    En simple: responde "¿el resultado del pipeline es igual al de la Fase 2?".

    - obtenido: lo que produce el pipeline con clases.
    - referencia: lo que se espera (el CSV de la Fase 2).
    - columnas: compara solo ese subconjunto (útil mientras el pipeline está incompleto).
    - verificar_tipos: exige además el mismo tipo de dato (por ejemplo, HTA entera y
      no decimal). Activado por defecto, como assert_frame_equal; con False solo
      se comparan los valores.
    - ignorar_orden_columnas: si es True, no importa el orden de las columnas.
    - rtol / atol: tolerancia para diferencias mínimas de decimales.

    Si son iguales imprime [OK] y devuelve True. Si no, lanza AssertionError e
    incluye el detalle de las columnas que difieren.
    """
    if columnas is not None:
        columnas = list(columnas)
        for nombre, conjunto in (("obtenido", obtenido), ("referencia", referencia)):
            faltan = [c for c in columnas if c not in conjunto.columns]
            if faltan:
                raise KeyError(f"Faltan columnas en el conjunto {nombre}: {faltan}")
        obtenido, referencia = obtenido[columnas], referencia[columnas]

    obtenido = obtenido.reset_index(drop=True)
    referencia = referencia.reset_index(drop=True)

    try:
        pd.testing.assert_frame_equal(
            obtenido, referencia, check_dtype=verificar_tipos,
            check_like=ignorar_orden_columnas, rtol=rtol, atol=atol,
        )
    except AssertionError as error:
        informe = informe_diferencias(obtenido, referencia, rtol, atol)
        ausentes = ~(informe["en_obtenido"] & informe["en_referencia"])
        problemas = informe[ausentes | (informe["n_distintos"].fillna(0) > 0)]
        mensaje = [str(error)]
        if set(obtenido.columns) == set(referencia.columns) and list(obtenido.columns) != list(referencia.columns):
            mensaje.append("Las columnas coinciden pero están en otro orden "
                           "(use ignorar_orden_columnas=True si el orden no importa).")
        if len(problemas):
            mensaje.append("Columnas que difieren:\n" + problemas.to_string(index=False))
        raise AssertionError("\n".join(mensaje)) from error

    print(f"[OK] El resultado coincide con la referencia: "
          f"{obtenido.shape[0]} filas x {obtenido.shape[1]} columnas comparadas")
    return True


def verificar_contra_fase2(pipeline, datos, ruta_referencia, **opciones):
    """Ajusta el pipeline con `datos`, transforma y compara con ens_procesado.csv de la Fase 2.

    En simple: hace todo el recorrido de la verificación clave en una sola llamada:
      1. Lee el archivo de la Fase 2 (ruta_referencia).
      2. Ajusta el pipeline con los datos y los transforma.
      3. Compara el resultado con ese archivo usando verificar_equivalencia.

    `opciones` se pasa a verificar_equivalencia (columnas, verificar_tipos, ...).
    """
    referencia = pd.read_csv(ruta_referencia)
    obtenido = pipeline.ajustar(datos).transformar(datos)
    return verificar_equivalencia(obtenido, referencia, **opciones)
