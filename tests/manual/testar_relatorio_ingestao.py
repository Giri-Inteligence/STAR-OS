"""
Teste manual simples do relatorio estruturado de ingestao
(star_ingestion/relatorio.py). Executavel diretamente por python, sem pytest.

Uso:
    python tests/manual/testar_relatorio_ingestao.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_ingestion.relatorio import (
    criar_relatorio_ingestao,
    registrar_estado_inicial,
    registrar_estado_final,
    registrar_mapeamento,
    adicionar_saneamento,
    adicionar_avisos,
    adicionar_erros,
    marcar_processado,
    formatar_relatorio_texto,
)


def testar_fluxo_processado():
    df_inicial = pd.DataFrame({
        "NOME DO CLIENTE": ["Cliente A", "Cliente B", None],
        "VENDEDOR": ["Joao", "Maria", None],
        "JANEIRO/25": [100, 200, None],
        "FEVEREIRO/25": [110, 210, None],
    })

    relatorio = criar_relatorio_ingestao()
    registrar_estado_inicial(relatorio, df_inicial)

    adicionar_saneamento(relatorio, ["1 linha(s) totalmente vazia(s) removida(s)."])

    df_final = df_inicial.dropna(how="all").reset_index(drop=True)
    df_final = df_final[df_final["NOME DO CLIENTE"].notna()].reset_index(drop=True)

    registrar_mapeamento(
        relatorio,
        cliente_col="NOME DO CLIENTE",
        vendedor_col="VENDEDOR",
        cidade_col=None,
        meses_col=["JANEIRO/25", "FEVEREIRO/25"],
    )

    registrar_estado_final(relatorio, df_final)
    marcar_processado(relatorio)

    assert relatorio["status"] == "PROCESSADO", relatorio["status"]
    assert relatorio["bloqueado"] is False
    assert relatorio["linhas_iniciais"] == 3
    assert relatorio["colunas_iniciais"] == 4
    assert relatorio["linhas_finais"] == 2
    assert relatorio["cliente_col"] == "NOME DO CLIENTE"
    assert relatorio["vendedor_col"] == "VENDEDOR"
    assert len(relatorio["meses_col"]) == 2

    linhas_texto = formatar_relatorio_texto(relatorio)
    assert any("PROCESSADO" in linha for linha in linhas_texto)
    assert any("Saneamento:" in linha for linha in linhas_texto)

    print("teste fluxo processado: OK")


def testar_fluxo_bloqueado():
    relatorio = criar_relatorio_ingestao()

    df = pd.DataFrame({"NOME DO CLIENTE": [None, None]})
    registrar_estado_inicial(relatorio, df)

    adicionar_avisos(relatorio, ["Coluna de cidade nao informada."])
    adicionar_erros(relatorio, ["Cliente nao informado."])

    assert relatorio["status"] == "BLOQUEADO"
    assert relatorio["bloqueado"] is True

    marcar_processado(relatorio)

    assert relatorio["status"] == "BLOQUEADO"
    assert relatorio["bloqueado"] is True

    linhas_texto = formatar_relatorio_texto(relatorio)
    assert any("BLOQUEADO" in linha for linha in linhas_texto)
    assert any("Erro:" in linha for linha in linhas_texto)
    assert any("Aviso:" in linha for linha in linhas_texto)

    print("teste fluxo bloqueado: OK")


if __name__ == "__main__":
    testar_fluxo_processado()
    testar_fluxo_bloqueado()
    print("RELATORIO_INGESTAO_OK")
