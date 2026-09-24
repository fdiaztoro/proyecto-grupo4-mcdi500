class Transformador:
    """Clase base: lo que todos los pasos del pipeline comparten.

    Esta clase NO se usa directamente. Su trabajo es definir el contrato:
    que metodos tendra todo paso del pipeline y como se controla su estado.
    Las clases hijas solo completan lo que cambia de un paso a otro.
    """

    def __init__(self, columna):
        # Atributo publico: cualquiera puede leerlo y cambiarlo
        self.columna = columna

        # Atributos con guion bajo: por convencion, INTERNOS.
        self._parametros = {}       # lo que el paso aprende del conjunto
        self._ajustado = False      # controla que no se transforme antes de ajustar

    @property
    def nombre(self):
        return f"{type(self).__name__}({self.columna})"

    @property
    def parametros(self):
        # Copia defensiva: quien lee esto no puede modificar el estado interno
        return dict(self._parametros)

    def ajustar(self, df):
        """Aprende los parametros del conjunto que recibe."""
        if self.columna not in df.columns:
            raise KeyError(f"{self.nombre}: la columna no existe en el conjunto.")

        self._parametros = self.aprender(df)
        self._ajustado = True
        return self

    def transformar(self, df):
        """Aplica la transformacion usando lo aprendido en ajustar()."""
        if not self._ajustado:
            raise RuntimeError(f"{self.nombre}: hay que ajustar antes de transformar.")

        return self.aplicar(df.copy())

    def ajustar_transformar(self, df):
        """Atajo: aprender y aplicar sobre el mismo conjunto."""
        return self.ajustar(df).transformar(df)

    def aprender(self, df):
        """Calcula y devuelve los parametros. Lo implementa cada clase hija."""
        raise NotImplementedError("Cada clase hija debe implementar aprender().")

    def aplicar(self, df):
        """Aplica la transformacion. Lo implementa cada clase hija."""
        raise NotImplementedError("Cada clase hija debe implementar aplicar().")