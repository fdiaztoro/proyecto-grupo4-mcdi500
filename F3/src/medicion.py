"""
Funciones de medicion de eficiencia (tiempo y memoria), reutilizadas
tanto en la Formativa 3 como en la Sumativa 2 sobre el pipeline
refactorizado a clases.
"""

import time
import tracemalloc


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