"""
Clase base del pipeline de preprocesamiento de la ENS 2016-2017.

Cada paso de limpieza de la Fase 2 (imputar, codificar, escalar) pasa
a ser una subclase de Transformador. La subclase decide qué calcular
y cómo usarlo; esta clase se encarga del orden de uso y de los errores.
"""


class Transformador:
    """Interfaz común para los pasos del pipeline.

    Uso esperado: primero ajustar() con el conjunto de referencia y
    después transformar() con cualquier conjunto, usando siempre lo
    calculado en el ajuste.
    """

    def __init__(self, columna):
        self.columna = columna
        # Estado interno: se modifica solo desde los métodos de la clase
        self._parametros = {}
        self._ajustado = False

    @property
    def nombre(self):
        """Etiqueta legible del paso, útil en resúmenes y mensajes."""
        return f"{type(self).__name__}({self.columna})"

    @property
    def parametros(self):
        """Valores calculados en el ajuste. Se entrega una copia para
        que nadie altere el estado del paso desde fuera."""
        return dict(self._parametros)

    def ajustar(self, df):
        """Calcula los parámetros del paso a partir de df."""
        if self.columna not in df.columns:
            raise KeyError(f"{self.nombre}: '{self.columna}' no está en el conjunto.")
        self._parametros = self.aprender(df)
        self._ajustado = True
        return self

    def transformar(self, df):
        """Aplica el paso sobre una copia de df con los parámetros ya calculados."""
        if not self._ajustado:
            raise RuntimeError(f"{self.nombre}: falta llamar a ajustar().")
        return self.aplicar(df.copy())

    def ajustar_transformar(self, df):
        """Ajusta y transforma en una sola llamada sobre el mismo conjunto."""
        return self.ajustar(df).transformar(df)

    def aprender(self, df):
        """Cada subclase define qué calcula. Devuelve un diccionario."""
        raise NotImplementedError(f"{type(self).__name__} no implementa aprender().")

    def aplicar(self, df):
        """Cada subclase define cómo usa lo calculado. Devuelve un DataFrame."""
        raise NotImplementedError(f"{type(self).__name__} no implementa aplicar().")

    def __repr__(self):
        estado = "ajustado" if self._ajustado else "sin ajustar"
        return f"{self.nombre} [{estado}]"