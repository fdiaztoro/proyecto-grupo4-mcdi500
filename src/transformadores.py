import pandas as pd
from transformador import Transformador

MAPEO_CATEGORIAS = {
    "Sexo": {
        1: "Hombre",
        2: "Mujer",
    },
    "Zona": {
        1: "Urbano",
        2: "Rural",
    },
    "di3": {
        1: "Si",
        2: "No",
        3: "No_recuerda",
    },
    "dis2": {
        1: "Si_una_vez",
        2: "Si_mas_de_una_vez",
        3: "Nunca",
        4: "No_recuerda",
    },
}


class CodificadorOneHot(Transformador):
    """
    Codifica una variable categórica mediante One-Hot Encoding.

    Utiliza las categorías definidas para las variables de la ENS
    y genera una columna binaria por cada categoría.
    """

    def aprender(self, df):
        if self.columna not in MAPEO_CATEGORIAS:
            raise ValueError(
                f"{self.nombre}: no existe un mapeo definido "
                f"para '{self.columna}'."
            )

        categorias = MAPEO_CATEGORIAS[self.columna]

        valores_observados = set(df[self.columna].dropna().unique())
        valores_validos = set(categorias.keys())

        desconocidos = valores_observados - valores_validos

        if desconocidos:
            raise ValueError(
                f"{self.nombre}: se encontraron códigos "
                f"no reconocidos: {sorted(desconocidos)}"
            )

        return {
            "categorias": categorias
        }

    def aplicar(self, df):
        categorias = self._parametros["categorias"]

        valores_observados = set(
            df[self.columna].dropna().unique()
        )
        valores_validos = set(categorias.keys())

        desconocidos = valores_observados - valores_validos

        if desconocidos:
            raise ValueError(
                f"{self.nombre}: se encontraron códigos "
                f"no reconocidos durante la transformación: "
                f"{sorted(desconocidos)}"
            )

        for codigo, nombre in categorias.items():
            nombre_columna = f"{self.columna}_{nombre}"

            df[nombre_columna] = (
                df[self.columna] == codigo
            ).astype(int)

        df = df.drop(columns=[self.columna])

        return df


class EscaladorEstandar(Transformador):
    """
    Estandariza una variable numérica mediante Z-score.

    Durante el ajuste calcula la media y la desviación estándar.
    Posteriormente utiliza estos parámetros para transformar los datos.
    """

    def aprender(self, df):
        serie = df[self.columna]

        media = serie.mean()
        desviacion = serie.std(ddof=0)

        if pd.isna(desviacion) or desviacion == 0:
            raise ValueError(
                f"{self.nombre}: la desviación estándar "
                f"es cero o no está definida."
            )

        return {
            "media": media,
            "desviacion": desviacion
        }

    def aplicar(self, df):
        media = self._parametros["media"]
        desviacion = self._parametros["desviacion"]

        df[self.columna] = (
            (df[self.columna] - media) / desviacion
        )

        return df
    
class EliminadorColumnas:
    """
    Elimina columnas que no forman parte del conjunto procesado final.
    """

    def __init__(self, columnas):
        self.columnas = columnas

    def transformar(self, df):
        faltantes = [
            columna for columna in self.columnas
            if columna not in df.columns
        ]

        if faltantes:
            raise KeyError(
                f"No se encontraron las columnas: {faltantes}"
            )

        return df.drop(columns=self.columnas).copy()


class ConvertidorEntero:
    """
    Convierte variables categóricas u ordinales a tipo entero,
    validando previamente la ausencia de valores nulos.
    """

    def __init__(self, columnas):
        self.columnas = columnas

    def transformar(self, df):
        resultado = df.copy()

        for columna in self.columnas:
            if columna not in resultado.columns:
                raise KeyError(
                    f"No se encontró la columna: {columna}"
                )

            if resultado[columna].isna().any():
                raise ValueError(
                    f"La columna '{columna}' contiene valores nulos "
                    "y no puede convertirse directamente a entero."
                )

            resultado[columna] = resultado[columna].astype(int)

        return resultado
    

