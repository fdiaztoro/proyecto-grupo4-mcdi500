"""
Funciones de medicion de eficiencia (tiempo y memoria), reutilizadas
tanto en la Formativa 3 como en la Sumativa 2 sobre el pipeline
refactorizado a clases.
"""

import time
import tracemalloc
import timeit


def buscar_recorriendo(df, posicion_buscada):
    """Busca una fila recorriendo el DataFrame fila por fila."""
    for i, (idx, fila) in enumerate(df.iterrows()):
        if i == posicion_buscada:
            return fila
    return None


def buscar_por_indice(df, posicion_buscada):
    """Busca una fila accediendo directamente por su posicion."""
    try:
        return df.iloc[posicion_buscada]
    except IndexError:
        return None


def medir_tiempo(funcion, *args, repeticiones=5):
    """Ejecuta la funcion varias veces y devuelve el tiempo minimo."""
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion(*args)
        tiempos.append(time.perf_counter() - inicio)
    return min(tiempos), resultado


def medir_memoria(funcion, *args):
    """Mide la memoria maxima usada al ejecutar la funcion."""
    tracemalloc.start()
    resultado = funcion(*args)
    actual, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico, resultado




def buscar_iterrows_por_clave(df, clave, valor):
    """Busqueda real: recorre hasta encontrar la clave (no una posicion)."""
    for _, fila in df.iterrows():
        if fila[clave] == valor:
            return fila
    return None


def buscar_vectorizado(df, clave, valor):
    """Busqueda con mascara booleana vectorizada: O(n), sin iterrows."""
    resultado = df[df[clave] == valor]
    return resultado.iloc[0] if len(resultado) > 0 else None


def construir_indice_pandas(df, clave):
    """Costo de construccion usando set_index de pandas."""
    return df.set_index(clave)


def construir_indice_dict(df, clave):
    """Costo de construccion usando un diccionario nativo de Python.

    Se evita iterrows(): cada iteracion de iterrows crea una Serie por
    fila, lo que encarece la construccion sin necesidad. dict(zip(...))
    empareja las claves con los registros ya extraidos por to_dict(),
    evitando ese costo por fila.
    """
    claves = df[clave]
    filas = df.to_dict("records")
    return dict(zip(claves, filas))


def buscar_indexado_pandas(df_indexado, valor):
    """Busqueda O(1) sobre un indice ya construido con pandas."""
    try:
        return df_indexado.loc[valor]
    except KeyError:
        return None


def buscar_indexado_dict(indice_dict, valor):
    """Busqueda O(1) sobre un diccionario ya construido."""
    return indice_dict.get(valor)

def medir_tiempo_timeit(funcion, *args, numero=20, repeticiones=5):
    """
    Mide el tiempo promedio por llamada utilizando timeit.

    Ejecuta varios bloques de mediciones y devuelve el mejor tiempo
    promedio por ejecución, reduciendo el efecto de variaciones
    externas del sistema.
    """
    tiempos = timeit.repeat(
        lambda: funcion(*args),
        number=numero,
        repeat=repeticiones
    )

    return min(tiempos) / numero