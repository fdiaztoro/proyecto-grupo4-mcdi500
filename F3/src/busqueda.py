"""
Funciones de busqueda sobre el conjunto de la ENS, usadas para
comparar dos formas de ubicar un registro dentro del DataFrame:
recorriendo fila por fila frente a acceder directamente por
posicion. Extraidas del notebook de la Formativa 3 (Fase 3).
"""

import time


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
