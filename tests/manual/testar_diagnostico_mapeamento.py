"""
Teste manual simples do diagnostico de falhas de mapeamento
(star_ingestion/diagnostico_mapeamento.py). Executavel diretamente por
python, sem pytest.

Uso:
    python tests/manual/testar_diagnostico_mapeamento.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_ingestion.diagnostico_mapeamento import (
    diagnosticar_mapeamento,
    detectar_colunas_candidatas,
    formatar_diagnostico_mapeamento_texto,
)


def testar_caso_valido():
    df = pd.DataFrame({
        "NOME DO CLIENTE": ["Cliente A", "Cliente B"],
        "CIDADE": ["Sao Paulo", "Rio de Janeiro"],
        "VENDEDOR": ["Joao", "Maria"],
        "JAN/25": [100, 200],
        "FEV/25": [110, 210],
    })

    diagnostico = diagnosticar_mapeamento(
        df,
        cliente_col="NOME DO CLIENTE",
        vendedor_col="VENDEDOR",
        cidade_col="CIDADE",
        meses_col=["JAN/25", "FEV/25"],
    )

    assert diagnostico["ok"] is True
    assert diagnostico["erros"] == []

    print("caso valido: OK")


def testar_caso_sem_cliente():
    df = pd.DataFrame({
        "CIDADE": ["Sao Paulo", "Rio de Janeiro"],
        "VENDEDOR": ["Joao", "Maria"],
        "JAN/25": [100, 200],
    })

    diagnostico = diagnosticar_mapeamento(
        df,
        cliente_col=None,
        vendedor_col="VENDEDOR",
        cidade_col="CIDADE",
        meses_col=["JAN/25"],
    )

    assert diagnostico["ok"] is False
    assert any("cliente" in erro.lower() for erro in diagnostico["erros"])

    print("caso sem cliente: OK")


def testar_caso_sem_vendedor():
    df = pd.DataFrame({
        "NOME DO CLIENTE": ["Cliente A", "Cliente B"],
        "CIDADE": ["Sao Paulo", "Rio de Janeiro"],
        "JAN/25": [100, 200],
    })

    diagnostico = diagnosticar_mapeamento(
        df,
        cliente_col="NOME DO CLIENTE",
        vendedor_col=None,
        cidade_col="CIDADE",
        meses_col=["JAN/25"],
    )

    assert diagnostico["ok"] is False
    assert any("vendedor" in erro.lower() for erro in diagnostico["erros"])

    print("caso sem vendedor: OK")


def testar_caso_sem_meses():
    df = pd.DataFrame({
        "NOME DO CLIENTE": ["Cliente A", "Cliente B"],
        "CIDADE": ["Sao Paulo", "Rio de Janeiro"],
        "VENDEDOR": ["Joao", "Maria"],
    })

    diagnostico = diagnosticar_mapeamento(
        df,
        cliente_col="NOME DO CLIENTE",
        vendedor_col="VENDEDOR",
        cidade_col="CIDADE",
        meses_col=[],
    )

    assert diagnostico["ok"] is False
    assert any("mensal" in erro.lower() or "mes" in erro.lower() for erro in diagnostico["erros"])

    print("caso sem meses: OK")


def testar_caso_sem_cidade():
    df = pd.DataFrame({
        "NOME DO CLIENTE": ["Cliente A", "Cliente B"],
        "VENDEDOR": ["Joao", "Maria"],
        "JAN/25": [100, 200],
        "FEV/25": [110, 210],
    })

    diagnostico = diagnosticar_mapeamento(
        df,
        cliente_col="NOME DO CLIENTE",
        vendedor_col="VENDEDOR",
        cidade_col=None,
        meses_col=["JAN/25", "FEV/25"],
    )

    assert diagnostico["ok"] is True
    assert any("cidade" in aviso.lower() for aviso in diagnostico["avisos"])

    print("caso sem cidade: OK")


def testar_caso_nomes_alternativos():
    df = pd.DataFrame({
        "RAZÃO SOCIAL": ["Cliente A", "Cliente B"],
        "MUNICÍPIO": ["Sao Paulo", "Rio de Janeiro"],
        "REPRESENTANTE": ["Joao", "Maria"],
        "JANEIRO/25": [100, 200],
        "FEVEREIRO/25": [110, 210],
    })

    candidatos = detectar_colunas_candidatas(df)

    assert "RAZÃO SOCIAL" in candidatos["possiveis_clientes"]
    assert "MUNICÍPIO" in candidatos["possiveis_cidades"]
    assert "REPRESENTANTE" in candidatos["possiveis_vendedores"]
    assert "JANEIRO/25" in candidatos["possiveis_meses"]
    assert "FEVEREIRO/25" in candidatos["possiveis_meses"]

    diagnostico = diagnosticar_mapeamento(df, meses_col=[])
    linhas_texto = formatar_diagnostico_mapeamento_texto(diagnostico, candidatos=candidatos)

    assert any("Possíveis colunas de cliente" in linha for linha in linhas_texto)
    assert any("Possíveis colunas de vendedor" in linha for linha in linhas_texto)
    assert any("Possíveis colunas de cidade" in linha for linha in linhas_texto)
    assert any("Possíveis colunas de mês" in linha for linha in linhas_texto)

    print("caso nomes alternativos: OK")


if __name__ == "__main__":
    testar_caso_valido()
    testar_caso_sem_cliente()
    testar_caso_sem_vendedor()
    testar_caso_sem_meses()
    testar_caso_sem_cidade()
    testar_caso_nomes_alternativos()
    print("DIAGNOSTICO_MAPEAMENTO_OK")
