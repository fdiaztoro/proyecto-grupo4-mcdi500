import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from transformadores import (
    CodificadorOneHot,
    EscaladorEstandar,
    EliminadorColumna,
    ConvertidorEntero,
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
        
def test_codificador_codigo_desconocido_al_transformar():
    df_ajuste = pd.DataFrame({
        "Sexo": [1, 2, 1, 2]
    })

    df_nuevo = pd.DataFrame({
        "Sexo": [1, 2, 9]
    })

    codificador = CodificadorOneHot("Sexo")
    codificador.ajustar(df_ajuste)

    with pytest.raises(ValueError):
        codificador.transformar(df_nuevo)

def test_codificador_una_sola_categoria_presente():
    df = pd.DataFrame({
        "Sexo": [1, 1, 1]
    })

    codificador = CodificadorOneHot("Sexo")
    resultado = codificador.ajustar_transformar(df)

    assert resultado["Sexo_Hombre"].tolist() == [1, 1, 1]
    assert resultado["Sexo_Mujer"].tolist() == [0, 0, 0]

def test_escalador_mantiene_nulos():
    df = pd.DataFrame({
        "Edad": [20.0, 30.0, None, 40.0, 50.0]
    })

    escalador = EscaladorEstandar("Edad")
    resultado = escalador.ajustar_transformar(df)

    assert resultado["Edad"].isna().sum() == 1

    valores_validos = resultado["Edad"].dropna()

    assert abs(valores_validos.mean()) < 1e-10
    assert abs(valores_validos.std(ddof=0) - 1) < 1e-10
    
def test_escalador_columna_completamente_nula():
    df = pd.DataFrame({
        "Edad": [None, None, None]
    })

    escalador = EscaladorEstandar("Edad")

    with pytest.raises(ValueError):
        escalador.ajustar(df)
        
def test_codificador_nombres_di3():
    """Verifica los nombres esperados para las categorías de di3."""
    df = pd.DataFrame({
        "di3": [1, 2, 3]
    })

    codificador = CodificadorOneHot("di3")
    resultado = codificador.ajustar_transformar(df)

    columnas_esperadas = {
        "di3_Si",
        "di3_No",
        "di3_No_recuerda",
    }

    assert columnas_esperadas.issubset(resultado.columns)
    assert "di3" not in resultado.columns


def test_codificador_nombres_dis2():
    """Verifica los nombres esperados para las categorías de dis2."""
    df = pd.DataFrame({
        "dis2": [1, 2, 3, 4]
    })

    codificador = CodificadorOneHot("dis2")
    resultado = codificador.ajustar_transformar(df)

    columnas_esperadas = {
        "dis2_Si_una_vez",
        "dis2_Si_mas_de_una_vez",
        "dis2_Nunca",
        "dis2_No_recuerda",
    }

    assert columnas_esperadas.issubset(resultado.columns)
    assert "dis2" not in resultado.columns

def test_eliminador_columna():
    """Verifica que EliminadorColumna elimine la columna indicada."""
    df = pd.DataFrame({
        "IdEncuesta": [1, 2, 3],
        "Edad": [20, 30, 40],
    })

    eliminador = EliminadorColumna("IdEncuesta")
    resultado = eliminador.ajustar_transformar(df)

    assert "IdEncuesta" not in resultado.columns
    assert "Edad" in resultado.columns


def test_convertidor_entero_con_nulos():
    """Verifica que ConvertidorEntero rechace columnas con nulos."""
    df = pd.DataFrame({
        "HTA": [1.0, None, 0.0]
    })

    convertidor = ConvertidorEntero("HTA")

    with pytest.raises(ValueError):
        convertidor.ajustar(df)
