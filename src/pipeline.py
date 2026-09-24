"""
Encadena los pasos del preprocesamiento de la ENS en un orden fijo.

Cada paso es una subclase de Transformador. El Pipeline no necesita
saber qué hace cada uno: le basta con que todos respondan a ajustar()
y transformar().
"""

import pandas as pd

from transformador import Transformador


class Pipeline:
    """Secuencia ordenada de pasos de preprocesamiento."""

    def __init__(self, pasos=None):
        self._pasos = []
        self._ajustado = False
        for paso in pasos or []:
            self.agregar(paso)

    def agregar(self, paso):
        """Suma un paso al final. Rechaza cualquier objeto que no sea Transformador."""
        if not isinstance(paso, Transformador):
            raise TypeError(
                f"Pipeline solo acepta Transformador; se recibió {type(paso).__name__}."
            )
        self._pasos.append(paso)
        self._ajustado = False  # un paso nuevo obliga a ajustar de nuevo
        return self

    def ajustar(self, df):
        """Ajusta cada paso sobre la salida del anterior, en orden."""
        intermedio = df
        for paso in self._pasos:
            intermedio = paso.ajustar_transformar(intermedio)
        self._ajustado = True
        return self

    def transformar(self, df):
        """Aplica todos los pasos con los parámetros ya calculados."""
        if not self._ajustado:
            raise RuntimeError("Pipeline: falta llamar a ajustar().")
        resultado = df
        for paso in self._pasos:
            resultado = paso.transformar(resultado)
        return resultado

    def ajustar_transformar(self, df):
        """Ajusta y transforma en una sola llamada sobre el mismo conjunto."""
        return self.ajustar(df).transformar(df)

    def resumen(self):
        """Tabla con el orden de los pasos y lo que calculó cada uno."""
        return pd.DataFrame([
            {"orden": i, "paso": paso.nombre, "parametros": paso.parametros}
            for i, paso in enumerate(self._pasos, start=1)
        ])

    def __len__(self):
        return len(self._pasos)

    def __repr__(self):
        estado = "ajustado" if self._ajustado else "sin ajustar"
        return f"Pipeline({len(self._pasos)} pasos, {estado})"