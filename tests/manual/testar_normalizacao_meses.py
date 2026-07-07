"""
Teste manual simples da normalizacao avancada de meses
(star_ingestion/normalizacao_meses.py). Executavel diretamente por python,
sem pytest.

Uso:
    python tests/manual/testar_normalizacao_meses.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_ingestion.normalizacao_meses import (
    normalizar_texto_coluna,
    extrair_periodo_mes,
    detectar_colunas_mensais_avancado,
)


def testar_normalizar_texto_coluna():
    assert normalizar_texto_coluna(" Março 2025 ") == "MARCO 2025"
    assert normalizar_texto_coluna("Responsável") == "RESPONSAVEL"

    print("normalizar_texto_coluna: OK")


def testar_formatos_validos():
    casos = [
        ("JAN/25", 1, 2025),
        ("JANEIRO/25", 1, 2025),
        ("Janeiro 2025", 1, 2025),
        ("JAN 2025", 1, 2025),
        ("01/25", 1, 2025),
        ("1/25", 1, 2025),
        ("01/2025", 1, 2025),
        ("2025-01", 1, 2025),
        ("VENDAS JAN/25", 1, 2025),
        ("FATURAMENTO 01/2025", 1, 2025),
        ("RECEITA MARÇO 2025", 3, 2025),
    ]

    for coluna, mes_esperado, ano_esperado in casos:
        resultado = extrair_periodo_mes(coluna)

        assert resultado is not None, f"{coluna!r} deveria ser reconhecida"
        assert resultado["mes"] == mes_esperado, f"{coluna!r}: mes {resultado['mes']} != {mes_esperado}"
        assert resultado["ano"] == ano_esperado, f"{coluna!r}: ano {resultado['ano']} != {ano_esperado}"

    print("formatos validos: OK")


def testar_formatos_invalidos():
    casos = ["TOTAL", "SUBTOTAL", "CLIENTE", "VENDEDOR", "CIDADE", "00/25", "13/25", "99/9999"]

    for coluna in casos:
        resultado = extrair_periodo_mes(coluna)
        assert resultado is None, f"{coluna!r} nao deveria ser reconhecida, mas retornou {resultado}"

    print("formatos invalidos: OK")


def testar_deteccao_fora_de_ordem():
    df = pd.DataFrame(columns=["NOME DO CLIENTE", "VENDEDOR", "MAR/25", "JAN/25", "FEV/25"])
    resultado = detectar_colunas_mensais_avancado(df)

    assert resultado["meses_col"] == ["JAN/25", "FEV/25", "MAR/25"], resultado["meses_col"]

    print("deteccao fora de ordem: OK")


def testar_duplicados():
    df = pd.DataFrame(columns=["NOME DO CLIENTE", "VENDEDOR", "JAN/25", "JANEIRO/25", "FEV/25"])
    resultado = detectar_colunas_mensais_avancado(df)

    assert len(resultado["duplicados"]) == 1
    assert resultado["duplicados"][0]["periodo"] == "2025-01"
    assert set(resultado["duplicados"][0]["colunas"]) == {"JAN/25", "JANEIRO/25"}
    assert len(resultado["avisos"]) == 1
    # duplicidade nao bloqueia: as colunas continuam presentes em meses_col
    assert "JAN/25" in resultado["meses_col"]
    assert "JANEIRO/25" in resultado["meses_col"]

    print("duplicados: OK")


if __name__ == "__main__":
    testar_normalizar_texto_coluna()
    testar_formatos_validos()
    testar_formatos_invalidos()
    testar_deteccao_fora_de_ordem()
    testar_duplicados()
    print("NORMALIZACAO_MESES_OK")
