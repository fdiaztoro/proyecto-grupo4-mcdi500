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
    df = preparar(df)
    print(f"Preparado: {df.shape[1]} columnas (incluye clave_busqueda)")
    return df



LECTORES = {
    ".csv": lambda ruta: pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8"),
    ".xlsx": pd.read_excel,
    ".xls": pd.read_excel,
    ".parquet": pd.read_parquet,
}


def leer_archivo(ruta):
    """Lee un archivo de datos según su extensión."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")
    lector = LECTORES.get(ruta.suffix.lower())
    if lector is None:
        raise ValueError(f"Formato no soportado: {ruta.suffix}")
    return lector(ruta)


def verificar_columnas(df, esperadas):
    """Falla si falta alguna columna declarada; devuelve las no declaradas."""
    faltantes = [c for c in esperadas if c not in df.columns]
    if faltantes:
        raise KeyError(f"Faltan columnas en el archivo: {faltantes}")
    return [c for c in df.columns if c not in esperadas]


def cargar_conjunto(ruta, esperadas):
    """Lee el archivo, verifica sus columnas e informa el resultado."""
    df = leer_archivo(ruta)
    no_declaradas = verificar_columnas(df, esperadas)
    print(f"Conjunto leído: {df.shape[0]} filas x {df.shape[1]} columnas")
    if no_declaradas:
        print("Columnas no usadas en el análisis:", no_declaradas)
    return df


def perfilar(df):
    """Tabla de tipos y nulos por columna, antes de transformar."""
    nulos = df.isna().sum()
    return pd.DataFrame({
        "tipo": df.dtypes.astype(str),
        "nulos": nulos,
        "pct_nulos": (nulos / len(df) * 100).round(2),
    })