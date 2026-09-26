"""
Pruebas por clase del pipeline de preprocesamiento de la ENS 2016-2017.

¿Para qué sirve este archivo?
Para comprobar que cada clase del pipeline, por separado, se comporta bien.
Cada prueba usa una tabla pequeña escrita a mano, donde el resultado correcto
se puede calcular de memoria.

Los tres escenarios de prueba, en simple:
  - normal:    el uso esperado, con datos comunes.
  - límite:    situaciones extremas pero válidas (una columna sin nulos, un solo
               dato, un pipeline vacío...). No deben fallar ni dar resultados raros.
  - excepción: entradas incorrectas. Deben fallar con un error claro.

Clases probadas (13), agrupadas por archivo y en el mismo orden en que aparecen
en el informe de ejecutar_pruebas():
  - transformador.py:   Transformador (clase base).
  - imputadores.py:     MarcadorNoRespuesta, EliminadorFilasNulas, PorMedia,
                        PorMediana, PorModa, PorMedianaDeTramo, ImputadorFlexible.
  - transformadores.py: EliminadorColumna, ConvertidorEntero, CodificadorOneHot,
                        EscaladorEstandar.
  - pipeline.py:        Pipeline.

Cómo se ejecuta (en ambos casos src/ debe estar en sys.path antes de importar):
  - Desde el notebook: ejecutar_pruebas() devuelve un informe en tabla, con una
    fila por prueba (clase, escenario, prueba, estado y detalle).
  - Con pytest: tests/test_casos_por_clase.py agrega las rutas y las ejecuta.
    El nombre de este archivo no empieza con "test_", así pytest no lo recoge
    dos veces.

La validación del resultado sobre el conjunto real y la comparación con la
Fase 2 no están aquí: viven en src/validador.py.
"""

import numpy as np
import pandas as pd

from imputadores import (
    EliminadorFilasNulas, ImputadorFlexible, MarcadorNoRespuesta,
    PorMedia, PorMediana, PorMedianaDeTramo, PorModa,
)
from pipeline import Pipeline
from transformador import Transformador
from transformadores import (
    CodificadorOneHot, ConvertidorEntero, EliminadorColumna, EscaladorEstandar,
)


# Los tres tipos de prueba que existen.
ESCENARIOS = ("normal", "limite", "excepcion")
# Lista donde el decorador @prueba anota cada prueba; ejecutar_pruebas() la recorre.
PRUEBAS = []


def prueba(clase, escenario):
    """Decorador: registra la función de abajo como una prueba de `clase`.

    En simple: se escribe @prueba("Pipeline", "limite") encima de una función y
    queda anotada en la lista PRUEBAS. Después ejecutar_pruebas() las corre todas.

    - clase: nombre de la clase que se está probando (sirve para ordenar el informe).
    - escenario: "normal", "limite" o "excepcion".

    La primera línea del docstring de cada prueba es la descripción que sale en el informe.
    """
    if escenario not in ESCENARIOS:
        raise ValueError(f"Escenario '{escenario}' no válido. Use uno de {ESCENARIOS}.")

    def registrar(funcion):
        """Anota la función en PRUEBAS y la devuelve sin cambios."""
        PRUEBAS.append({
            "clase": clase,
            "escenario": escenario,
            "prueba": (funcion.__doc__ or funcion.__name__).strip().splitlines()[0],
            "funcion": funcion,
        })
        return funcion

    return registrar


def _debe_lanzar(tipo_error, accion, contiene=None):
    """Comprueba que `accion` lance `tipo_error`; devuelve el mensaje capturado.

    En simple: sirve para las pruebas de "excepción", donde lo correcto es que
    algo falle. La prueba pasa si aparece el error esperado y falla si no falla
    nada o si el mensaje no dice lo que se esperaba.

    - tipo_error: el tipo de error que debe aparecer (por ejemplo KeyError).
    - accion: función sin argumentos que hace la operación que debe fallar.
    - contiene: texto que debe aparecer en el mensaje del error (opcional).
    """
    try:
        accion()
    except tipo_error as error:
        if contiene is not None:
            assert contiene in str(error), f"El mensaje no menciona '{contiene}': {error}"
        return f"{type(error).__name__}: {error}"
    raise AssertionError(f"No lanzó {tipo_error.__name__}")


def _rellenar(estrategia, datos, columna):
    """Aplica una estrategia de imputación directamente, sin pasar por el Transformador.

    En simple: atajo para probar PorMedia, PorMediana o PorModa por sí solas.
    Primero calcula con qué valor rellenar y luego rellena los nulos. Trabaja
    sobre una copia, así que los datos originales no se modifican.
    """
    parametros = estrategia.calcular(datos, columna)
    return estrategia.rellenar(datos.copy(), columna, parametros)


class _PasoDoblador(Transformador):
    """Subclase mínima para probar la clase base sin depender de un paso real.

    En simple: es un paso de mentira que multiplica una columna por 2. La clase
    base Transformador no se puede probar sola (le faltan aprender y aplicar),
    así que se crea este paso mínimo que las completa.
    """

    def aprender(self, df):
        """Lo que "aprende" el paso: el número por el que multiplicará (siempre 2)."""
        return {"factor": 2}

    def aplicar(self, df):
        """Multiplica la columna por el factor aprendido y devuelve los datos."""
        df[self.columna] = df[self.columna] * self._parametros["factor"]
        return df


# ---------------------------------------------------------------------------
# Transformador (clase base)
# ---------------------------------------------------------------------------

@prueba("Transformador", "normal")
def _transformador_normal():
    """Ajustar devuelve el mismo paso, guarda lo aprendido y transformar lo aplica.

    En simple: se crea un paso que duplica la columna x. Se ajusta con [1, 2, 3],
    se comprueba que aprendió el factor 2 y que al transformar queda [2, 4, 6].
    """
    datos = pd.DataFrame({"x": [1, 2, 3]})
    paso = _PasoDoblador("x")
    assert paso.ajustar(datos) is paso, "ajustar() debe devolver el propio paso"
    assert paso.parametros == {"factor": 2}
    assert paso.transformar(datos)["x"].tolist() == [2, 4, 6]
    assert repr(paso).endswith("[ajustado]")


@prueba("Transformador", "limite")
def _transformador_parametros_copia():
    """parametros entrega una copia: modificarla no altera el estado interno.

    En simple: si alguien cambia lo que devuelve `parametros`, el paso no debe
    cambiar por dentro. Se intenta poner factor = 99 y se comprueba que sigue en 2.
    """
    paso = _PasoDoblador("x").ajustar(pd.DataFrame({"x": [1]}))
    paso.parametros["factor"] = 99
    assert paso.parametros["factor"] == 2


@prueba("Transformador", "limite")
def _transformador_no_modifica_entrada():
    """transformar trabaja sobre una copia y deja intacto el DataFrame de entrada.

    En simple: se transforman unos datos y después se comprueba que la tabla
    original quedó exactamente igual que antes.
    """
    datos = pd.DataFrame({"x": [1, 2, 3]})
    original = datos.copy()
    _PasoDoblador("x").ajustar_transformar(datos)
    assert datos.equals(original)


@prueba("Transformador", "excepcion")
def _transformador_sin_ajustar():
    """transformar antes de ajustar lanza RuntimeError.

    En simple: se intenta transformar sin haber ajustado antes. Debe fallar con
    RuntimeError, porque el paso todavía no aprendió nada.
    """
    datos = pd.DataFrame({"x": [1]})
    return _debe_lanzar(RuntimeError, lambda: _PasoDoblador("x").transformar(datos), "ajustar")


@prueba("Transformador", "excepcion")
def _transformador_columna_inexistente():
    """Ajustar con una columna que no existe lanza KeyError.

    En simple: si el paso apunta a una columna que no está en los datos, debe
    fallar al ajustar con KeyError. Este control vive en la clase base, así que
    todas las clases hijas lo heredan sin escribirlo de nuevo.
    """
    datos = pd.DataFrame({"x": [1]})
    return _debe_lanzar(KeyError, lambda: _PasoDoblador("otra").ajustar(datos), "no está")


@prueba("Transformador", "excepcion")
def _transformador_base_sin_aprender():
    """La clase base no se usa sola: sin aprender() lanza NotImplementedError.

    En simple: la clase base es solo un molde. Usarla directamente debe fallar
    con NotImplementedError, porque le falta el método aprender().
    """
    datos = pd.DataFrame({"x": [1]})
    return _debe_lanzar(NotImplementedError, lambda: Transformador("x").ajustar(datos), "aprender")


@prueba("Transformador", "excepcion")
def _transformador_parametros_solo_lectura():
    """parametros no se puede reasignar desde fuera (AttributeError).

    En simple: `parametros` solo se puede leer. Intentar asignarle un valor
    desde fuera debe fallar con AttributeError.
    """
    paso = _PasoDoblador("x").ajustar(pd.DataFrame({"x": [1]}))

    def reasignar():
        """Intenta reemplazar los parámetros desde fuera (debe fallar)."""
        paso.parametros = {"factor": -1}

    return _debe_lanzar(AttributeError, reasignar)


# ---------------------------------------------------------------------------
# MarcadorNoRespuesta
# ---------------------------------------------------------------------------

@prueba("MarcadorNoRespuesta", "normal")
def _marcador_normal():
    """Pasa los códigos -8888 y -9999 a nulo y anota quién no respondió.

    En simple: en la columna ingreso, -9999 y -8888 significan "no responde".
    Deben quedar como nulos, y una columna nueva (ingreso_no_responde) marca
    con 1 a quiénes traían el código.
    """
    datos = pd.DataFrame({"ingreso": [100, -9999, 200, -8888, 300]})
    salida = MarcadorNoRespuesta("ingreso").ajustar_transformar(datos)
    assert salida["ingreso"].isna().tolist() == [False, True, False, True, False]
    assert salida["ingreso_no_responde"].tolist() == [0, 1, 0, 1, 0]
    assert salida["ingreso"].dropna().tolist() == [100.0, 200.0, 300.0]


@prueba("MarcadorNoRespuesta", "limite")
def _marcador_sin_codigos():
    """Sin códigos presentes no cambia ningún valor y la bandera queda en cero.

    En simple: si ningún valor es un código de no respuesta, los datos quedan
    iguales y la columna ingreso_no_responde queda toda en 0.
    """
    datos = pd.DataFrame({"ingreso": [100, 200, 300]})
    salida = MarcadorNoRespuesta("ingreso").ajustar_transformar(datos)
    assert salida["ingreso"].tolist() == [100.0, 200.0, 300.0]
    assert salida["ingreso_no_responde"].sum() == 0


@prueba("MarcadorNoRespuesta", "limite")
def _marcador_nulo_previo():
    """Un nulo que ya venía en los datos no cuenta como no respuesta.

    En simple: un valor que ya estaba vacío antes NO se marca como "no
    respondió". Solo cuenta el que traía el código -9999.
    """
    datos = pd.DataFrame({"ingreso": [100.0, np.nan, -9999.0]})
    salida = MarcadorNoRespuesta("ingreso").ajustar_transformar(datos)
    assert salida["ingreso_no_responde"].tolist() == [0, 0, 1]
    assert salida["ingreso"].isna().sum() == 2


@prueba("MarcadorNoRespuesta", "excepcion")
def _marcador_columna_inexistente():
    """Una columna que no existe lanza KeyError.

    En simple: pedir marcar una columna que no está en los datos debe fallar
    con KeyError.
    """
    datos = pd.DataFrame({"ingreso": [100]})
    return _debe_lanzar(KeyError, lambda: MarcadorNoRespuesta("otra").ajustar(datos), "no está")


# ---------------------------------------------------------------------------
# EliminadorFilasNulas
# ---------------------------------------------------------------------------

@prueba("EliminadorFilasNulas", "normal")
def _eliminador_normal():
    """Quita las filas con nulo en la columna y renumera el índice.

    En simple: de 4 personas, una tiene HTA vacío. Debe quedar sin esa fila
    (3 filas) y con los índices renumerados 0, 1, 2.
    """
    datos = pd.DataFrame({"HTA": [0.0, 1.0, np.nan, 0.0], "edad": [30, 40, 50, 60]})
    salida = EliminadorFilasNulas("HTA").ajustar_transformar(datos)
    assert len(salida) == 3 and salida["HTA"].isna().sum() == 0
    assert salida.index.tolist() == [0, 1, 2], "el índice debe renumerarse"
    assert salida["edad"].tolist() == [30, 40, 60]


@prueba("EliminadorFilasNulas", "limite")
def _eliminador_sin_nulos():
    """Sin nulos en la columna devuelve los mismos datos.

    En simple: si nadie tiene HTA vacío, no hay nada que eliminar y la tabla
    queda igual.
    """
    datos = pd.DataFrame({"HTA": [0.0, 1.0], "edad": [30, 40]})
    assert EliminadorFilasNulas("HTA").ajustar_transformar(datos).equals(datos)


@prueba("EliminadorFilasNulas", "limite")
def _eliminador_todo_nulo():
    """Si todas las filas son nulas queda un DataFrame vacío con sus columnas.

    En simple: si todas las filas tienen la columna vacía, se eliminan todas.
    Queda una tabla sin filas, pero conserva sus columnas.
    """
    datos = pd.DataFrame({"HTA": [np.nan, np.nan], "edad": [30, 40]})
    salida = EliminadorFilasNulas("HTA").ajustar_transformar(datos)
    assert len(salida) == 0 and list(salida.columns) == ["HTA", "edad"]


@prueba("EliminadorFilasNulas", "limite")
def _eliminador_solo_mira_su_columna():
    """Los nulos de otras columnas no provocan que se elimine la fila.

    En simple: la fila se elimina solo si el vacío está en la columna indicada
    (HTA). Un vacío en otra columna no cuenta.
    """
    datos = pd.DataFrame({"HTA": [1.0, np.nan], "otra": [np.nan, 2.0]})
    salida = EliminadorFilasNulas("HTA").ajustar_transformar(datos)
    assert len(salida) == 1 and salida["otra"].isna().sum() == 1


@prueba("EliminadorFilasNulas", "excepcion")
def _eliminador_columna_inexistente():
    """Una columna que no existe lanza KeyError.

    En simple: indicar una columna que no está en los datos debe fallar con
    KeyError.
    """
    datos = pd.DataFrame({"HTA": [1.0]})
    return _debe_lanzar(KeyError, lambda: EliminadorFilasNulas("otra").ajustar(datos), "no está")


# ---------------------------------------------------------------------------
# Estrategias de imputación: PorMedia, PorMediana, PorModa
# ---------------------------------------------------------------------------

@prueba("PorMedia", "normal")
def _media_normal():
    """Rellena los nulos con la media de los datos presentes.

    En simple: con [10, vacío, 20, 30] la media es 20, y el vacío se rellena con 20.
    """
    datos = pd.DataFrame({"x": [10.0, np.nan, 20.0, 30.0]})
    assert _rellenar(PorMedia(), datos, "x")["x"].tolist() == [10.0, 20.0, 20.0, 30.0]


@prueba("PorMedia", "limite")
def _media_un_solo_dato():
    """Con un único dato válido, la media es ese dato.

    En simple: si solo hay un dato (7), la media es 7 y todos los vacíos se
    rellenan con 7.
    """
    datos = pd.DataFrame({"x": [7.0, np.nan, np.nan]})
    assert _rellenar(PorMedia(), datos, "x")["x"].tolist() == [7.0, 7.0, 7.0]


@prueba("PorMedia", "excepcion")
def _media_sin_datos():
    """Una columna sin ningún dato lanza ValueError.

    En simple: si la columna está completamente vacía no hay con qué calcular
    la media. Debe fallar con ValueError.
    """
    datos = pd.DataFrame({"x": [np.nan, np.nan]})
    return _debe_lanzar(ValueError, lambda: PorMedia().calcular(datos, "x"), "no tiene datos")


@prueba("PorMediana", "normal")
def _mediana_normal():
    """Rellena los nulos con la mediana de los datos presentes.

    En simple: con [10, vacío, 20, 60] la mediana es 20 (el valor del medio), y
    el vacío se rellena con 20.
    """
    datos = pd.DataFrame({"x": [10.0, np.nan, 20.0, 60.0]})
    assert _rellenar(PorMediana(), datos, "x")["x"].tolist() == [10.0, 20.0, 20.0, 60.0]


@prueba("PorMediana", "limite")
def _mediana_cantidad_par():
    """Con cantidad par de datos, la mediana es el promedio de los dos centrales.

    En simple: con [1, 2, 3, 4] hay dos valores en el medio (2 y 3). La mediana
    es su promedio: 2,5.
    """
    datos = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0, np.nan]})
    assert _rellenar(PorMediana(), datos, "x")["x"].iloc[-1] == 2.5


@prueba("PorMediana", "excepcion")
def _mediana_sin_datos():
    """Una columna sin ningún dato lanza ValueError.

    En simple: si la columna está completamente vacía no hay con qué calcular
    la mediana. Debe fallar con ValueError.
    """
    datos = pd.DataFrame({"x": [np.nan, np.nan]})
    return _debe_lanzar(ValueError, lambda: PorMediana().calcular(datos, "x"), "no tiene datos")


@prueba("PorModa", "normal")
def _moda_normal():
    """Rellena los nulos con el valor más frecuente.

    En simple: con [1, 2, 2, vacío, 2, 1] el valor que más se repite es 2, y el
    vacío se rellena con 2.
    """
    datos = pd.DataFrame({"x": [1.0, 2.0, 2.0, np.nan, 2.0, 1.0]})
    assert _rellenar(PorModa(), datos, "x")["x"].tolist() == [1.0, 2.0, 2.0, 2.0, 2.0, 1.0]


@prueba("PorModa", "limite")
def _moda_empate():
    """Con empate entre valores, se elige el menor (igual que en la Fase 2).

    En simple: con [1, 1, 2, 2] hay empate entre 1 y 2. Se elige el menor (1),
    como hizo la Fase 2.
    """
    datos = pd.DataFrame({"x": [1.0, 1.0, 2.0, 2.0, np.nan]})
    assert _rellenar(PorModa(), datos, "x")["x"].iloc[-1] == 1.0


@prueba("PorModa", "excepcion")
def _moda_sin_datos():
    """Una columna sin ningún dato lanza ValueError.

    En simple: si la columna está completamente vacía no hay valor más
    frecuente que calcular. Debe fallar con ValueError.
    """
    datos = pd.DataFrame({"x": [np.nan, np.nan]})
    return _debe_lanzar(ValueError, lambda: PorModa().calcular(datos, "x"), "no tiene datos")


# ---------------------------------------------------------------------------
# PorMedianaDeTramo
# ---------------------------------------------------------------------------

def _imputar_por_tramo(datos):
    """Atajo: imputa la columna "monto" con la mediana de su "tramo" y devuelve el resultado.

    En simple: agrupa las filas por la columna "tramo" y rellena cada vacío de
    "monto" con la mediana de su propio tramo. Además crea la columna
    "monto_imputado", que marca con 1 las filas rellenadas.
    """
    return ImputadorFlexible("monto", PorMedianaDeTramo("tramo")).ajustar_transformar(datos)


@prueba("PorMedianaDeTramo", "normal")
def _tramo_normal():
    """Rellena con la mediana de su propio tramo y marca solo las filas rellenadas.

    En simple: hay dos tramos. En el tramo 1 los montos son 10 y 20 (mediana 15);
    en el tramo 2 son 100 y 300 (mediana 200). Cada vacío se rellena con la
    mediana de su tramo, y monto_imputado marca con 1 solo esas dos filas.
    """
    datos = pd.DataFrame({"tramo": [1, 1, 1, 2, 2, 2],
                          "monto": [10.0, 20.0, np.nan, 100.0, np.nan, 300.0]})
    salida = _imputar_por_tramo(datos)
    assert salida["monto"].tolist() == [10.0, 20.0, 15.0, 100.0, 200.0, 300.0]
    assert salida["monto_imputado"].tolist() == [0, 0, 1, 0, 1, 0]


@prueba("PorMedianaDeTramo", "limite")
def _tramo_fila_sin_tramo():
    """Una fila sin tramo queda nula y no se marca como imputada.

    En simple: si una fila no tiene tramo, no se sabe con qué mediana
    rellenarla. Queda vacía y no se marca como imputada.
    """
    datos = pd.DataFrame({"tramo": [1.0, 1.0, np.nan], "monto": [10.0, np.nan, np.nan]})
    salida = _imputar_por_tramo(datos)
    assert salida["monto"].isna().tolist() == [False, False, True]
    assert salida["monto_imputado"].tolist() == [0, 1, 0]


@prueba("PorMedianaDeTramo", "limite")
def _tramo_sin_ningun_valor():
    """Si un tramo no tiene ningún monto, sus filas quedan nulas y sin marca.

    En simple: el tramo 2 no tiene ni un monto conocido, así que no hay mediana
    con qué rellenar. Sus filas quedan vacías (sin inventar un valor) y no se
    marcan como imputadas. El tramo 1 sí se rellena con su mediana (10).
    """
    datos = pd.DataFrame({"tramo": [1, 1, 2, 2], "monto": [10.0, np.nan, np.nan, np.nan]})
    salida = _imputar_por_tramo(datos)
    assert salida["monto"].isna().tolist() == [False, False, True, True]
    assert salida["monto"].iloc[1] == 10.0
    assert salida["monto_imputado"].tolist() == [0, 1, 0, 0]


@prueba("PorMedianaDeTramo", "excepcion")
def _tramo_columna_inexistente():
    """Si la columna de tramo no existe lanza KeyError.

    En simple: si los datos no tienen la columna "tramo", no se puede agrupar.
    Debe fallar con KeyError.
    """
    datos = pd.DataFrame({"monto": [10.0, np.nan]})
    paso = ImputadorFlexible("monto", PorMedianaDeTramo("tramo"))
    return _debe_lanzar(KeyError, lambda: paso.ajustar(datos), "no está")


# ---------------------------------------------------------------------------
# ImputadorFlexible
# ---------------------------------------------------------------------------

@prueba("ImputadorFlexible", "normal")
def _imputador_por_defecto():
    """Sin estrategia usa la mediana y la deja guardada en sus parámetros.

    En simple: si no se indica estrategia, se usa la mediana. Con
    [20, vacío, 30, 40] la mediana es 30, y ese valor queda guardado en los
    parámetros del paso.
    """
    datos = pd.DataFrame({"IMC": [20.0, np.nan, 30.0, 40.0]})
    paso = ImputadorFlexible("IMC")
    assert paso.ajustar_transformar(datos)["IMC"].tolist() == [20.0, 30.0, 30.0, 40.0]
    assert paso.parametros == {"valor": 30.0}


@prueba("ImputadorFlexible", "normal")
def _imputador_polimorfismo():
    """Con cualquier estrategia se usa la misma llamada y no quedan nulos.

    En simple: el imputador se usa igual con media, mediana o moda (misma
    llamada). En los tres casos el vacío debe quedar relleno.
    """
    datos = pd.DataFrame({"x": [1.0, 2.0, 2.0, np.nan, 5.0]})
    for estrategia in (PorMedia(), PorMediana(), PorModa()):
        salida = ImputadorFlexible("x", estrategia).ajustar_transformar(datos)
        assert salida["x"].isna().sum() == 0, f"quedaron nulos con {estrategia.etiqueta}"


@prueba("ImputadorFlexible", "limite")
def _imputador_sin_nulos():
    """Una columna sin ningún nulo no se altera.

    En simple: si no hay vacíos no hay nada que rellenar. Los valores deben
    quedar exactamente iguales (es el primer caso límite del cuaderno del curso).
    """
    datos = pd.DataFrame({"IMC": [25.0, 30.0, 35.0]})
    assert ImputadorFlexible("IMC").ajustar_transformar(datos)["IMC"].tolist() == [25.0, 30.0, 35.0]


@prueba("ImputadorFlexible", "limite")
def _imputador_sin_fuga():
    """Aprende en entrenamiento y aplica a prueba con el valor del entrenamiento.

    En simple: el valor de relleno se calcula con los datos de entrenamiento
    (mediana 20) y se aplica a los de prueba. No debe usar los valores de prueba
    (1000 y 2000): eso sería "espiar" datos que no debería conocer (fuga de datos).
    """
    entrenamiento = pd.DataFrame({"x": [10.0, 20.0, 30.0]})
    prueba_ = pd.DataFrame({"x": [np.nan, 1000.0, 2000.0]})
    paso = ImputadorFlexible("x").ajustar(entrenamiento)
    assert paso.transformar(prueba_)["x"].iloc[0] == 20.0, "debe usar la mediana del entrenamiento"


@prueba("ImputadorFlexible", "excepcion")
def _imputador_estrategia_invalida():
    """Una estrategia que no es EstrategiaImputacion lanza TypeError.

    En simple: la estrategia debe ser una de las clases de imputación. Pasar el
    texto "mediana" debe fallar con TypeError.
    """
    return _debe_lanzar(TypeError, lambda: ImputadorFlexible("x", "mediana"), "EstrategiaImputacion")


@prueba("ImputadorFlexible", "excepcion")
def _imputador_columna_sin_datos():
    """Ajustar sobre una columna sin ningún dato lanza ValueError.

    En simple: si la columna está completamente vacía no hay con qué calcular
    el valor de relleno. Debe fallar con ValueError.
    """
    datos = pd.DataFrame({"x": [np.nan, np.nan]})
    return _debe_lanzar(ValueError, lambda: ImputadorFlexible("x").ajustar(datos), "no tiene datos")


# ---------------------------------------------------------------------------
# EliminadorColumna
# ---------------------------------------------------------------------------

@prueba("EliminadorColumna", "normal")
def _quitar_columna_normal():
    """Quita la columna indicada y deja intactas las demás y todas las filas.

    En simple: IdEncuesta no forma parte del conjunto final. Debe desaparecer,
    y la columna Edad y las 3 filas deben quedar exactamente como estaban.
    """
    datos = pd.DataFrame({"IdEncuesta": [1, 2, 3], "Edad": [20, 30, 40]})
    salida = EliminadorColumna("IdEncuesta").ajustar_transformar(datos)
    assert list(salida.columns) == ["Edad"]
    assert salida["Edad"].tolist() == [20, 30, 40]


@prueba("EliminadorColumna", "limite")
def _quitar_columna_unica():
    """Si es la única columna, queda una tabla sin columnas pero con sus filas.

    En simple: al quitar la única columna que hay, la tabla se queda sin
    columnas, pero conserva sus 2 filas. No debe fallar.
    """
    datos = pd.DataFrame({"IdEncuesta": [1, 2]})
    assert EliminadorColumna("IdEncuesta").ajustar_transformar(datos).shape == (2, 0)


@prueba("EliminadorColumna", "excepcion")
def _quitar_columna_inexistente():
    """Una columna que no existe lanza KeyError.

    En simple: pedir eliminar una columna que no está en los datos debe fallar
    con KeyError, en vez de seguir como si nada.
    """
    datos = pd.DataFrame({"Edad": [20]})
    return _debe_lanzar(KeyError, lambda: EliminadorColumna("IdEncuesta").ajustar(datos), "no está")


# ---------------------------------------------------------------------------
# ConvertidorEntero
# ---------------------------------------------------------------------------

@prueba("ConvertidorEntero", "normal")
def _convertidor_normal():
    """Convierte una columna decimal sin nulos a entero, con los mismos valores.

    En simple: HTA llega como 1.0 y 0.0 (decimales). Debe quedar como números
    enteros (1 y 0), igual que en el archivo de la Fase 2.
    """
    datos = pd.DataFrame({"HTA": [1.0, 0.0, 1.0]})
    salida = ConvertidorEntero("HTA").ajustar_transformar(datos)
    assert pd.api.types.is_integer_dtype(salida["HTA"])
    assert salida["HTA"].tolist() == [1, 0, 1]


@prueba("ConvertidorEntero", "limite")
def _convertidor_ya_entero():
    """Una columna que ya es entera queda igual.

    En simple: si GPAQ ya viene como entero, convertirla otra vez no debe
    cambiar ni sus valores ni su tipo.
    """
    datos = pd.DataFrame({"GPAQ": [1, 2, 3]})
    salida = ConvertidorEntero("GPAQ").ajustar_transformar(datos)
    assert salida.equals(datos)


@prueba("ConvertidorEntero", "excepcion")
def _convertidor_con_nulos():
    """Una columna con nulos lanza ValueError al ajustar.

    En simple: un vacío no se puede escribir como número entero. Por eso el
    paso debe negarse al ajustar, con ValueError, en vez de fallar más adelante.
    """
    datos = pd.DataFrame({"HTA": [1.0, np.nan, 0.0]})
    return _debe_lanzar(ValueError, lambda: ConvertidorEntero("HTA").ajustar(datos), "tiene nulos")


# ---------------------------------------------------------------------------
# CodificadorOneHot
# ---------------------------------------------------------------------------

@prueba("CodificadorOneHot", "normal")
def _onehot_normal():
    """Crea una columna 0/1 por categoría, quita la original y conserva las demás.

    En simple: Sexo (1 = Hombre, 2 = Mujer) se convierte en dos columnas,
    Sexo_Hombre y Sexo_Mujer, con un 1 donde corresponde. La columna Sexo
    desaparece y la columna Edad queda igual.
    """
    datos = pd.DataFrame({"Sexo": [1, 2, 2, 1], "Edad": [30, 40, 50, 60]})
    paso = CodificadorOneHot("Sexo")
    salida = paso.ajustar_transformar(datos)
    assert list(salida.columns) == ["Edad", "Sexo_Hombre", "Sexo_Mujer"]
    assert salida["Sexo_Hombre"].tolist() == [1, 0, 0, 1]
    assert salida["Sexo_Mujer"].tolist() == [0, 1, 1, 0]
    assert paso.parametros == {"categorias": {1: "Hombre", 2: "Mujer"}}


@prueba("CodificadorOneHot", "limite")
def _onehot_una_sola_categoria():
    """Con una sola categoría presente se generan igual todas las columnas.

    En simple: si todos son de zona urbana, igual deben aparecer Zona_Urbano y
    Zona_Rural (esta última en 0). Las categorías salen del libro de códigos de
    la ENS, no de los datos, así el conjunto final siempre tiene las mismas
    columnas. (En el cuaderno del curso, en cambio, sale una sola columna.)
    """
    datos = pd.DataFrame({"Zona": [1, 1, 1]})
    salida = CodificadorOneHot("Zona").ajustar_transformar(datos)
    assert list(salida.columns) == ["Zona_Urbano", "Zona_Rural"]
    assert salida["Zona_Urbano"].tolist() == [1, 1, 1]
    assert salida["Zona_Rural"].tolist() == [0, 0, 0]


@prueba("CodificadorOneHot", "limite")
def _onehot_esquema_estable_en_prueba():
    """Ajustado con un conjunto, a otro con menos categorías le da las mismas columnas.

    En simple: se ajusta con las tres respuestas de di3 y se transforma un
    conjunto donde todos respondieron "No". Deben salir igual las tres columnas
    (di3_Si, di3_No, di3_No_recuerda), para que entrenamiento y prueba tengan
    exactamente el mismo esquema.
    """
    entrenamiento = pd.DataFrame({"di3": [1, 2, 3]})
    prueba_ = pd.DataFrame({"di3": [2, 2]})
    salida = CodificadorOneHot("di3").ajustar(entrenamiento).transformar(prueba_)
    assert list(salida.columns) == ["di3_Si", "di3_No", "di3_No_recuerda"]
    assert salida["di3_No"].tolist() == [1, 1]


@prueba("CodificadorOneHot", "excepcion")
def _onehot_codigo_desconocido_al_ajustar():
    """Un código que no está en el libro de códigos lanza ValueError al ajustar.

    En simple: Sexo solo admite 1 y 2. Si aparece un 9, el paso debe fallar con
    ValueError en vez de ignorarlo en silencio.
    """
    datos = pd.DataFrame({"Sexo": [1, 2, 9]})
    return _debe_lanzar(ValueError, lambda: CodificadorOneHot("Sexo").ajustar(datos), "no reconocidos")


@prueba("CodificadorOneHot", "excepcion")
def _onehot_codigo_desconocido_al_transformar():
    """Un código nuevo que aparece solo al transformar también lanza ValueError.

    En simple: se ajusta con 1 y 2, y después llega un conjunto con un 9. En el
    cuaderno del curso esa categoría nueva se ignora; aquí se decidió rechazarla
    con ValueError, para no perder personas sin aviso.
    """
    paso = CodificadorOneHot("Sexo").ajustar(pd.DataFrame({"Sexo": [1, 2]}))
    nuevos = pd.DataFrame({"Sexo": [1, 9]})
    return _debe_lanzar(ValueError, lambda: paso.transformar(nuevos), "durante la transformación")


@prueba("CodificadorOneHot", "excepcion")
def _onehot_columna_sin_mapeo():
    """Una columna sin categorías definidas lanza ValueError.

    En simple: el codificador solo sabe codificar las columnas que tienen su
    libro de códigos (Sexo, Zona, di3 y dis2). Pedirle que codifique Edad debe
    fallar con ValueError.
    """
    datos = pd.DataFrame({"Edad": [30, 40]})
    return _debe_lanzar(ValueError, lambda: CodificadorOneHot("Edad").ajustar(datos), "no existe un mapeo")


# ---------------------------------------------------------------------------
# EscaladorEstandar
# ---------------------------------------------------------------------------

@prueba("EscaladorEstandar", "normal")
def _escalador_normal():
    """Deja la columna con media 0 y desviación 1, y guarda la media y la desviación.

    En simple: con [20, 30, 40, 50] la media es 35 y la desviación es la raíz
    de 125 (desviación poblacional, ddof=0, como StandardScaler en la Fase 2).
    Después de escalar, la columna debe tener media 0 y desviación 1.
    """
    datos = pd.DataFrame({"Edad": [20.0, 30.0, 40.0, 50.0]})
    paso = EscaladorEstandar("Edad")
    salida = paso.ajustar_transformar(datos)
    assert np.isclose(paso.parametros["media"], 35.0)
    assert np.isclose(paso.parametros["desviacion"], np.sqrt(125))
    assert np.isclose(salida["Edad"].mean(), 0.0)
    assert np.isclose(salida["Edad"].std(ddof=0), 1.0)


@prueba("EscaladorEstandar", "limite")
def _escalador_conserva_nulos():
    """Los nulos se conservan y no entran en el cálculo de la media ni la desviación.

    En simple: as27 tiene vacíos que se dejaron a propósito. El escalador debe
    dejarlos vacíos y escalar solo los valores presentes (media 0 y desviación
    1 entre ellos).
    """
    datos = pd.DataFrame({"as27": [20.0, 30.0, np.nan, 40.0, 50.0]})
    salida = EscaladorEstandar("as27").ajustar_transformar(datos)
    assert salida["as27"].isna().tolist() == [False, False, True, False, False]
    presentes = salida["as27"].dropna()
    assert np.isclose(presentes.mean(), 0.0) and np.isclose(presentes.std(ddof=0), 1.0)


@prueba("EscaladorEstandar", "limite")
def _escalador_sin_fuga():
    """Aprende en entrenamiento y aplica a prueba la media y desviación del entrenamiento.

    En simple: con [0, 10] aprende media 5 y desviación 5. Al escalar otro
    conjunto [5, 15] debe usar esos mismos valores y dar [0, 2]. Si diera
    media 0 en la prueba, estaría "espiando" datos que no debía conocer.
    """
    entrenamiento = pd.DataFrame({"IMC": [0.0, 10.0]})
    prueba_ = pd.DataFrame({"IMC": [5.0, 15.0]})
    salida = EscaladorEstandar("IMC").ajustar(entrenamiento).transformar(prueba_)
    assert np.allclose(salida["IMC"].tolist(), [0.0, 2.0])


@prueba("EscaladorEstandar", "excepcion")
def _escalador_varianza_cero():
    """Una columna constante (desviación cero) lanza ValueError.

    En simple: si todos tienen el mismo valor, la desviación es 0 y escalar
    obligaría a dividir por cero. En el cuaderno del curso eso devuelve ceros;
    aquí se decidió avisar con ValueError, porque una columna constante no
    aporta información y conviene revisarla.
    """
    datos = pd.DataFrame({"Edad": [50.0, 50.0, 50.0]})
    return _debe_lanzar(ValueError, lambda: EscaladorEstandar("Edad").ajustar(datos), "desviación estándar")


@prueba("EscaladorEstandar", "excepcion")
def _escalador_sin_datos():
    """Una columna sin ningún dato lanza ValueError.

    En simple: si la columna está completamente vacía no hay media ni
    desviación que calcular. Debe fallar con ValueError.
    """
    datos = pd.DataFrame({"Edad": [np.nan, np.nan]})
    return _debe_lanzar(ValueError, lambda: EscaladorEstandar("Edad").ajustar(datos), "desviación estándar")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def _datos_pipeline():
    """Tabla pequeña de ejemplo (5 personas) para las pruebas del Pipeline.

    Tiene un código -9999 en ingreso, un vacío en HTA y un vacío en IMC.
    """
    return pd.DataFrame({
        "ingreso": [100, -9999, 200, 300, 400],
        "HTA": [0.0, 1.0, np.nan, 0.0, 1.0],
        "IMC": [20.0, np.nan, 30.0, 40.0, 50.0],
    })


def _pasos_pipeline():
    """Los tres pasos de ejemplo, en orden: marcar no respuesta, quitar filas sin HTA e imputar IMC."""
    return [MarcadorNoRespuesta("ingreso"), EliminadorFilasNulas("HTA"), ImputadorFlexible("IMC")]


@prueba("Pipeline", "normal")
def _pipeline_normal():
    """Encadena los pasos en orden: marca, elimina filas e imputa.

    En simple: se encadenan tres pasos sobre 5 personas: marcar el código -9999,
    eliminar la fila sin HTA e imputar el IMC vacío con la mediana. Deben quedar
    4 filas, sin vacíos en IMC y con 1 persona marcada como "no respuesta".
    """
    datos = _datos_pipeline()
    pipe = Pipeline(_pasos_pipeline())
    salida = pipe.ajustar(datos).transformar(datos)
    assert len(pipe) == 3
    assert pipe.resumen()["paso"].tolist() == [
        "MarcadorNoRespuesta(ingreso)", "EliminadorFilasNulas(HTA)", "ImputadorFlexible(IMC)"]
    assert len(salida) == 4, "debe quedar sin la fila con HTA nulo"
    assert salida["IMC"].tolist() == [20.0, 40.0, 40.0, 50.0]
    assert salida["ingreso_no_responde"].sum() == 1


@prueba("Pipeline", "limite")
def _pipeline_vacio():
    """Un pipeline sin pasos devuelve los datos sin cambios.

    En simple: un pipeline sin pasos no hace nada; devuelve los datos tal cual.
    """
    datos = _datos_pipeline()
    assert Pipeline().ajustar(datos).transformar(datos).equals(datos)


@prueba("Pipeline", "limite")
def _pipeline_paso_nuevo_exige_reajustar():
    """Agregar un paso después de ajustar obliga a ajustar de nuevo.

    En simple: si después de ajustar se agrega un paso, el pipeline ya no está
    listo. Pedir transformar debe fallar con un RuntimeError del propio Pipeline.
    """
    datos = _datos_pipeline()
    pipe = Pipeline([EliminadorFilasNulas("HTA")]).ajustar(datos)
    pipe.agregar(ImputadorFlexible("IMC"))
    return _debe_lanzar(RuntimeError, lambda: pipe.transformar(datos), "Pipeline:")


@prueba("Pipeline", "limite")
def _pipeline_no_modifica_entrada():
    """Ajustar y transformar dejan intacto el DataFrame de entrada.

    En simple: después de pasar los datos por los tres pasos, la tabla original
    debe seguir exactamente igual (con su -9999 y sus vacíos). Si cambiara, un
    segundo uso de esos datos daría otro resultado.
    """
    datos = _datos_pipeline()
    original = datos.copy()
    Pipeline(_pasos_pipeline()).ajustar(datos).transformar(datos)
    assert datos.equals(original)


@prueba("Pipeline", "excepcion")
def _pipeline_agregar_no_transformador():
    """Agregar algo que no es un Transformador lanza TypeError.

    En simple: al pipeline solo se le pueden agregar Transformadores. Agregar un
    texto debe fallar con TypeError.
    """
    return _debe_lanzar(TypeError, lambda: Pipeline().agregar("texto"), "Transformador")


@prueba("Pipeline", "excepcion")
def _pipeline_sin_ajustar():
    """transformar antes de ajustar lanza RuntimeError.

    En simple: pedir transformar sin haber ajustado el pipeline debe fallar con
    RuntimeError del propio Pipeline (no de alguno de sus pasos).
    """
    datos = _datos_pipeline()
    return _debe_lanzar(RuntimeError, lambda: Pipeline(_pasos_pipeline()).transformar(datos), "Pipeline:")


@prueba("Pipeline", "excepcion")
def _pipeline_paso_columna_inexistente():
    """Un paso que apunta a una columna inexistente detiene el ajuste con KeyError.

    En simple: si uno de los pasos pide una columna que no existe, el pipeline
    debe detenerse al ajustar y el mensaje debe nombrar al paso que falló.
    """
    datos = _datos_pipeline()
    pipe = Pipeline([EliminadorFilasNulas("HTA"), ImputadorFlexible("no_existe")])
    return _debe_lanzar(KeyError, lambda: pipe.ajustar(datos), "ImputadorFlexible(no_existe)")


# ---------------------------------------------------------------------------
# Ejecutor de las pruebas
# ---------------------------------------------------------------------------

def ejecutar_pruebas(clases=None, escenarios=None, estricto=True):
    """Ejecuta las pruebas registradas y devuelve un informe con una fila por prueba.

    En simple: corre todas las pruebas registradas con @prueba, una por una, anota
    si cada una salió bien y entrega una tabla con las columnas clase, escenario,
    prueba, estado y detalle.

    - clases: lista de nombres para correr solo esas clases (por defecto, todas).
    - escenarios: lista para correr solo esos escenarios (por defecto, todos).
    - estricto: si es True y alguna prueba no pasa, lanza AssertionError con el
      resumen; si es False, solo informa y devuelve la tabla.

    Estados posibles: OK (pasó), FALLA (una comprobación no se cumplió) y
    ERROR (ocurrió algo inesperado dentro de la prueba).
    """
    filas = []
    for registro in PRUEBAS:
        if clases and registro["clase"] not in clases:
            continue
        if escenarios and registro["escenario"] not in escenarios:
            continue
        try:
            detalle, estado = registro["funcion"]() or "", "OK"
        except AssertionError as error:
            detalle, estado = str(error) or "aserción sin mensaje", "FALLA"
        except Exception as error:
            detalle, estado = f"{type(error).__name__}: {error}", "ERROR"
        filas.append({"clase": registro["clase"], "escenario": registro["escenario"],
                      "prueba": registro["prueba"], "estado": estado, "detalle": detalle})

    informe = pd.DataFrame(filas, columns=["clase", "escenario", "prueba", "estado", "detalle"])
    con_problemas = informe[informe["estado"] != "OK"]
    print(f"{len(informe)} pruebas: {len(informe) - len(con_problemas)} OK, "
          f"{len(con_problemas)} con problemas")
    if estricto and len(con_problemas):
        raise AssertionError("Pruebas con problemas:\n" + con_problemas.to_string(index=False))
    return informe
