"""
Teste manual simples da normalizacao avancada de valores monetarios
(star_ingestion/normalizacao_valores.py). Executavel diretamente por python,
sem pytest.

Uso:
    python tests/manual/testar_normalizacao_valores.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_ingestion.normalizacao_valores import (
    normalizar_valor_monetario,
    normalizar_colunas_monetarias,
)


def testar_formatos_validos():
    casos = [
        (10000, 10000.0),
        (10000.50, 10000.5),
        ("10000,50", 10000.5),
        ("10.000", 10000.0),
        ("10.000,00", 10000.0),
        ("R$ 10.000,00", 10000.0),
        ("R$10.000,00", 10000.0),
        ("10,000.50", 10000.5),
        ("1.234.567,89", 1234567.89),
        ("1,234,567.89", 1234567.89),
    ]

    for valor, esperado in casos:
        resultado = normalizar_valor_monetario(valor)
        assert resultado == esperado, f"{valor!r}: esperado {esperado}, obtido {resultado}"

    print("formatos validos: OK")


def testar_formatos_invalidos_ou_vazios():
    casos = [None, "", "-", "—", "–", "R$ -", "abc", "não informado"]

    for valor in casos:
        resultado = normalizar_valor_monetario(valor)
        assert resultado is None, f"{valor!r}: esperado None, obtido {resultado}"

    print("formatos invalidos ou vazios: OK")


def testar_normalizar_colunas_monetarias():
    df = pd.DataFrame({
        "NOME DO CLIENTE": ["A", "B", "C", "D", "E", "F"],
        "VENDEDOR": ["Joao"] * 6,
        "JAN/25": [10000, "R$ 10.000,00", "10,000.50", "-", "", "abc"],
        "FEV/25": [1000, 2000, 3000, 4000, 5000, 6000],
    })
    df_copia_original = df.copy()

    resultado = normalizar_colunas_monetarias(df, ["JAN/25", "FEV/25"])

    assert df.equals(df_copia_original), "o DataFrame original nao deveria ser alterado"

    df_normalizado = resultado["df"]
    assert df_normalizado["JAN/25"].tolist() == [10000.0, 10000.0, 10000.5, 0.0, 0.0, 0.0]
    assert all(isinstance(v, float) for v in df_normalizado["JAN/25"])
    assert all(isinstance(v, float) for v in df_normalizado["FEV/25"])

    estatisticas = resultado["estatisticas"]
    assert estatisticas["valores_convertidos"] == 9
    assert estatisticas["valores_vazios_ou_hifen"] == 2
    assert estatisticas["valores_invalidos"] == 1
    assert estatisticas["colunas_processadas"] == 2
    assert estatisticas["colunas_ausentes"] == []

    print("normalizar_colunas_monetarias: OK")


if __name__ == "__main__":
    testar_formatos_validos()
    testar_formatos_invalidos_ou_vazios()
    testar_normalizar_colunas_monetarias()
    print("NORMALIZACAO_VALORES_OK")
