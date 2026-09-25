import pandas as pd
import pytest

from src.transformadores import (
    CodificadorOneHot,
    EscaladorEstandar,
)

def test_codificador_onehot_sexo():
    """Verifica la codificación correcta de la variable Sexo."""

    df = pd.DataFrame({
        "Sexo": [1, 2, 2, 1]
    })

    codificador = CodificadorOneHot("Sexo")
    resultado = codificador.ajustar_transformar(df)

    assert resultado["Sexo_Hombre"].tolist() == [1, 0, 0, 1]
    assert resultado["Sexo_Mujer"].tolist() == [0, 1, 1, 0]
    assert "Sexo" not in resultado.columns


def test_codificador_codigo_desconocido():
    """Verifica que un código categórico desconocido genere error."""

    df = pd.DataFrame({
        "Sexo": [1, 2, 9]
    })

    codificador = CodificadorOneHot("Sexo")

    with pytest.raises(ValueError):
        codificador.ajustar(df)


def test_transformar_sin_ajustar():
    """Verifica que no se pueda transformar antes de ajustar."""

    df = pd.DataFrame({
        "Sexo": [1, 2]
    })

    codificador = CodificadorOneHot("Sexo")

    with pytest.raises(RuntimeError):
        codificador.transformar(df)


def test_escalador_estandar():
    """Verifica media 0 y desviación estándar 1."""

    df = pd.DataFrame({
        "Edad": [20, 30, 40, 50]
    })

    escalador = EscaladorEstandar("Edad")
    resultado = escalador.ajustar_transformar(df)

    media = resultado["Edad"].mean()
    desviacion = resultado["Edad"].std(ddof=0)

    assert abs(media) < 1e-10
    assert abs(desviacion - 1) < 1e-10


def test_escalador_desviacion_cero():
    """Verifica que una variable constante genere error."""

    df = pd.DataFrame({
        "Edad": [30, 30, 30, 30]
    })

    escalador = EscaladorEstandar("Edad")

    with pytest.raises(ValueError):
        escalador.ajustar(df)