"""Pasos de limpieza de valores ausentes de la Fase 2, como clases del pipeline.

La imputación usa el patrón Strategy: ImputadorFlexible delega en la
estrategia que recibe, así que cambiar la forma de imputar no toca el pipeline.
"""

import pandas as pd

from src.transformador import Transformador


class MarcadorNoRespuesta(Transformador):
    """Pasa los códigos de no respuesta a nulo y anota quién no respondió
    en '<columna>_no_responde'."""

    def __init__(self, columna, codigos=(-8888, -9999)):
        super().__init__(columna)
        self.codigos = tuple(codigos)

    def aprender(self, df):
        return {"codigos": list(self.codigos)}

    def aplicar(self, df):
        es_codigo = df[self.columna].isin(self._parametros["codigos"])
        df[f"{self.columna}_no_responde"] = es_codigo.astype(int)
        # float, para que la columna admita nulos
        df[self.columna] = df[self.columna].astype("float64").mask(es_codigo)
        return df


class EliminadorFilasNulas(Transformador):
    """Quita las filas sin valor en la columna (para diagnósticos como HTA)."""

    def aprender(self, df):
        return {}

    def aplicar(self, df):
        return df.dropna(subset=[self.columna]).reset_index(drop=True)


class EstrategiaImputacion:
    """Contrato de una estrategia: calcular con qué rellenar, y rellenar."""

    etiqueta = "sin definir"

    def calcular(self, df, columna):
        """Devuelve un diccionario con lo necesario para rellenar."""
        raise NotImplementedError(f"{type(self).__name__} no implementa calcular().")

    def rellenar(self, df, columna, parametros):
        """Devuelve df con los nulos de la columna rellenados."""
        raise NotImplementedError(f"{type(self).__name__} no implementa rellenar().")


class PorMedia(EstrategiaImputacion):
    etiqueta = "media"

    def calcular(self, df, columna):
        valor = df[columna].mean()
        # Sin datos no hay con qué rellenar: se avisa en vez de dejar los nulos igual.
        if pd.isna(valor):
            raise ValueError(f"'{columna}' no tiene datos para calcular la media.")
        return {"valor": float(valor)}

    def rellenar(self, df, columna, parametros):
        df[columna] = df[columna].fillna(parametros["valor"])
        return df


class PorMediana(EstrategiaImputacion):
    etiqueta = "mediana"

    def calcular(self, df, columna):
        valor = df[columna].median()
        if pd.isna(valor):
            raise ValueError(f"'{columna}' no tiene datos para calcular la mediana.")
        return {"valor": float(valor)}

    def rellenar(self, df, columna, parametros):
        df[columna] = df[columna].fillna(parametros["valor"])
        return df


class PorModa(EstrategiaImputacion):
    etiqueta = "moda"

    def calcular(self, df, columna):
        modas = df[columna].mode(dropna=True)
        if modas.empty:
            raise ValueError(f"'{columna}' no tiene datos para calcular la moda.")
        return {"valor": modas.iloc[0]}  # con empate, el menor (como en la Fase 2)

    def rellenar(self, df, columna, parametros):
        df[columna] = df[columna].fillna(parametros["valor"])
        return df


class PorMedianaDeTramo(EstrategiaImputacion):
    """Mediana dentro de cada tramo. Si la fila no tiene tramo, queda nula.
    Marca las filas rellenadas en '<columna>_imputado'."""

    etiqueta = "mediana por tramo"

    def __init__(self, columna_tramo):
        self.columna_tramo = columna_tramo

    def calcular(self, df, columna):
        if self.columna_tramo not in df.columns:
            raise KeyError(f"'{self.columna_tramo}' no está en el conjunto.")
        medianas = df.groupby(self.columna_tramo)[columna].median().dropna()
        return {"medianas": medianas.to_dict()}

    def rellenar(self, df, columna, parametros):
        candidato = df[self.columna_tramo].map(parametros["medianas"])
        a_rellenar = df[columna].isna() & candidato.notna()
        df[columna] = df[columna].mask(a_rellenar, candidato)
        df[f"{columna}_imputado"] = a_rellenar.astype(int)
        return df


class ImputadorFlexible(Transformador):
    """Imputa una columna con la estrategia recibida (mediana por defecto)."""

    def __init__(self, columna, estrategia=None):
        super().__init__(columna)
        if estrategia is None:
            estrategia = PorMediana()
        if not isinstance(estrategia, EstrategiaImputacion):
            raise TypeError("La estrategia debe ser una EstrategiaImputacion.")
        self._estrategia = estrategia

    def aprender(self, df):
        return self._estrategia.calcular(df, self.columna)

    def aplicar(self, df):
        return self._estrategia.rellenar(df, self.columna, self._parametros)


def comparar_estrategias(df, columna, estrategias):
    """Tabla con el efecto de cada estrategia sobre la distribución de la columna."""
    original = df[columna]
    filas = [{
        "estrategia": "sin imputar",
        "n_validos": int(original.notna().sum()),
        "nulos_restantes": int(original.isna().sum()),
        "media": original.mean(),
        "desv_est": original.std(),
        "asimetria": original.skew(),
    }]
    for estrategia in estrategias:
        parametros = estrategia.calcular(df, columna)
        resultado = estrategia.rellenar(df.copy(), columna, parametros)[columna]
        filas.append({
            "estrategia": estrategia.etiqueta,
            "n_validos": int(resultado.notna().sum()),
            "nulos_restantes": int(resultado.isna().sum()),
            "media": resultado.mean(),
            "desv_est": resultado.std(),
            "asimetria": resultado.skew(),
        })

    tabla = pd.DataFrame(filas)
    referencia = tabla.loc[0, "desv_est"]
    tabla["cambio_desv_%"] = ((tabla["desv_est"] - referencia) / referencia * 100).round(2)
    return tabla.round({"media": 1, "desv_est": 1, "asimetria": 2})
