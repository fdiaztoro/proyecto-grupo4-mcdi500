"""
Funciones de carga y coordinacion del flujo de la Formativa 3.
"""

from pathlib import Path
import pandas as pd


def encontrar_raiz_proyecto(marcador=".git"):
    """Sube por las carpetas padre hasta encontrar la raiz del repositorio."""
    actual = Path.cwd()
    for carpeta in [actual, *actual.parents]:
        if (carpeta / marcador).exists():
            return carpeta
    raise FileNotFoundError(f"No se encontro '{marcador}' en ningun directorio padre")


def cargar_datos(ruta):
    """Carga el archivo procesado de la Fase 2 y devuelve el DataFrame."""
    try:
        df = pd.read_csv(ruta)
    except FileNotFoundError:
        print("No se encontro el archivo:", ruta)
        return None
    print(f"Cargado: {df.shape[0]} filas y {df.shape[1]} columnas")
    return df


def preparar(df):
    """
    Agrega una clave de busqueda sintetica (el indice), ya que
    IdEncuesta fue excluida en la Fase 2. No se aplica ninguna
    limpieza adicional: eso ya se resolvio en F2.
    """
    df = df.reset_index(drop=True).copy()
    df["clave_busqueda"] = df.index
    return df


def ejecutar(ruta):
    """Coordina el flujo: cargar y preparar el conjunto de la Fase 3."""
    df = cargar_datos(ruta)
    if df is None:
        return None
    return preparar(df)