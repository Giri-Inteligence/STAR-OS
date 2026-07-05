"""
Teste manual simples da qualidade de linhas
(star_ingestion/qualidade_linhas.py). Executavel diretamente por python,
sem pytest.

Uso:
    python tests/manual/testar_qualidade_linhas.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_ingestion.qualidade_linhas import (
    cliente_residual_obvio,
    linha_tem_venda,
    classificar_linhas_base,
)


def testar_cliente_residual_obvio():
    residuais = ["", "-", "TOTAL", "TOTAL GERAL", "SUBTOTAL", "NOME DO CLIENTE", "SEM CLIENTE", "não informado"]

    for valor in residuais:
        assert cliente_residual_obvio(valor) is True, f"{valor!r} deveria ser residual"

    reais = ["Total Distribuidora Ltda", "Total Service Comércio", "Empresa Zero Ltda", "Mercado Central"]

    for valor in reais:
        assert cliente_residual_obvio(valor) is False, f"{valor!r} nao deveria ser residual"

    print("cliente_residual_obvio: OK")


def testar_linha_tem_venda():
    linha_com_venda = pd.Series({"JAN/25": 0, "FEV/25": 100})
    assert linha_tem_venda(linha_com_venda, ["JAN/25", "FEV/25"]) is True

    linha_sem_venda = pd.Series({"JAN/25": 0, "FEV/25": 0})
    assert linha_tem_venda(linha_sem_venda, ["JAN/25", "FEV/25"]) is False

    print("linha_tem_venda: OK")


def testar_preserva_cliente_zerado():
    df = pd.DataFrame({
        "NOME DO CLIENTE": ["Empresa Zero Ltda"],
        "VENDEDOR": ["João"],
        "JAN/25": [0.0],
        "FEV/25": [0.0],
    })

    resultado = classificar_linhas_base(df, "NOME DO CLIENTE", "VENDEDOR", ["JAN/25", "FEV/25"])

    assert len(resultado["df"]) == 1
    assert resultado["estatisticas"]["clientes_zerados_preservados"] == 1
    assert resultado["estatisticas"]["linhas_removidas"] == 0

    print("preserva cliente zerado real: OK")


def testar_preserva_cliente_venda_parcial():
    df = pd.DataFrame({
        "NOME DO CLIENTE": ["Cliente Compra Parcial Ltda"],
        "VENDEDOR": ["Maria"],
        "JAN/25": [0.0],
        "FEV/25": [0.0],
        "MAR/25": [1500.0],
        "ABR/25": [0.0],
    })

    resultado = classificar_linhas_base(df, "NOME DO CLIENTE", "VENDEDOR", ["JAN/25", "FEV/25", "MAR/25", "ABR/25"])

    assert len(resultado["df"]) == 1
    assert resultado["estatisticas"]["clientes_com_venda_parcial_preservados"] == 1
    assert resultado["estatisticas"]["linhas_removidas"] == 0

    print("preserva cliente com venda parcial: OK")


def testar_remove_residuos_evidentes():
    df = pd.DataFrame({
        "NOME DO CLIENTE": ["TOTAL", "", "-", "Empresa Real Ltda"],
        "VENDEDOR": ["Joao"] * 4,
        "JAN/25": [0.0, 0.0, 0.0, 1000.0],
    })

    resultado = classificar_linhas_base(df, "NOME DO CLIENTE", "VENDEDOR", ["JAN/25"])

    assert list(resultado["df"]["NOME DO CLIENTE"]) == ["Empresa Real Ltda"]
    assert resultado["estatisticas"]["linhas_removidas"] == 3
    assert len(resultado["removidas"]) == 3

    print("remove residuos evidentes: OK")


def testar_preserva_total_distribuidora():
    df = pd.DataFrame({
        "NOME DO CLIENTE": ["TOTAL", "SUBTOTAL", "Total Distribuidora Ltda"],
        "VENDEDOR": ["Joao"] * 3,
        "JAN/25": [0.0, 0.0, 5000.0],
    })

    resultado = classificar_linhas_base(df, "NOME DO CLIENTE", "VENDEDOR", ["JAN/25"])

    assert list(resultado["df"]["NOME DO CLIENTE"]) == ["Total Distribuidora Ltda"]

    print("preserva Total Distribuidora Ltda: OK")


def testar_avisa_cliente_sem_vendedor():
    df = pd.DataFrame({
        "NOME DO CLIENTE": ["Cliente Sem Vendedor Ltda"],
        "VENDEDOR": [""],
        "JAN/25": [100.0],
    })

    resultado = classificar_linhas_base(df, "NOME DO CLIENTE", "VENDEDOR", ["JAN/25"])

    assert len(resultado["df"]) == 1
    assert resultado["estatisticas"]["linhas_cliente_sem_vendedor"] == 1
    assert len(resultado["avisos"]) >= 1

    print("avisa cliente sem vendedor: OK")


if __name__ == "__main__":
    testar_cliente_residual_obvio()
    testar_linha_tem_venda()
    testar_preserva_cliente_zerado()
    testar_preserva_cliente_venda_parcial()
    testar_remove_residuos_evidentes()
    testar_preserva_total_distribuidora()
    testar_avisa_cliente_sem_vendedor()
    print("QUALIDADE_LINHAS_OK")
