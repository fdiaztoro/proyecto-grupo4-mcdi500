from src.transformador import Transformador

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

        if desviacion == 0:
            raise ValueError(
                f"{self.nombre}: la desviación estándar es cero."
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