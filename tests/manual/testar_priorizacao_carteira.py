"""
Teste manual simples da fila de prioridade da carteira
(star_intelligence/priorizacao.py). Executavel diretamente por python,
sem pytest.

Uso:
    python tests/manual/testar_priorizacao_carteira.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_intelligence.priorizacao import (
    calcular_pontuacao_prioridade,
    classificar_nivel_prioridade,
    definir_tipo_prioridade,
    gerar_motivos_prioridade,
    gerar_fila_prioridade,
    resumir_fila_prioridade,
)


def testar_pontuacao_caso_critico():
    row = pd.Series({
        "CURVA": "A",
        "STATUS": "QUEDA ACENTUADA",
        "MESES_SEM_COMPRA": 6,
        "EROSAO STAR": 8,
        "MEDIA LP": 10000,
        "MEDIA CP": 3000,
    })

    pontuacao = calcular_pontuacao_prioridade(row)
    nivel = classificar_nivel_prioridade(pontuacao)

    assert nivel == "P1 CRITICA", f"esperado P1 CRITICA, obtido {nivel} (pontuacao {pontuacao})"

    print("pontuacao caso critico: OK")


def testar_pontuacao_caso_monitoramento():
    row = pd.Series({
        "CURVA": "C",
        "STATUS": "CRESCIMENTO",
        "MESES_SEM_COMPRA": 0,
        "EROSAO STAR": 0,
        "MEDIA LP": 1000,
        "MEDIA CP": 1500,
    })

    pontuacao = calcular_pontuacao_prioridade(row)
    nivel = classificar_nivel_prioridade(pontuacao)

    assert nivel == "P4 MONITORAMENTO", f"esperado P4 MONITORAMENTO, obtido {nivel} (pontuacao {pontuacao})"

    print("pontuacao caso monitoramento: OK")


def testar_definir_tipo_prioridade():
    casos = [
        ({"STATUS": "INATIVO"}, "REATIVACAO"),
        ({"STATUS": "QUEDA"}, "PRESERVACAO"),
        ({"STATUS": "QUEDA ACENTUADA"}, "PRESERVACAO"),
        ({"STATUS": "ESTAVEL", "EROSAO STAR": 5}, "INVESTIGACAO"),
        ({"STATUS": "CRESCIMENTO"}, "EXPANSAO CONTROLADA"),
    ]

    for dados, esperado in casos:
        resultado = definir_tipo_prioridade(pd.Series(dados))
        assert resultado == esperado, f"{dados}: esperado {esperado}, obtido {resultado}"

    print("definir_tipo_prioridade: OK")


def testar_gerar_motivos_prioridade():
    assert "Cliente curva A." in gerar_motivos_prioridade(pd.Series({"CURVA": "A"}))
    assert len(gerar_motivos_prioridade(pd.Series({"STATUS": "QUEDA"}))) > 0
    assert len(gerar_motivos_prioridade(pd.Series({"MESES_SEM_COMPRA": 5}))) > 0
    assert len(gerar_motivos_prioridade(pd.Series({"EROSAO STAR": 7}))) > 0

    print("gerar_motivos_prioridade: OK")


def testar_gerar_fila_prioridade():
    df = pd.DataFrame([
        {"CLIENTE": "Cliente Critico", "VENDEDOR": "Joao", "CURVA": "A", "STATUS": "QUEDA ACENTUADA",
         "MESES_SEM_COMPRA": 6, "EROSAO STAR": 8, "MEDIA LP": 10000, "MEDIA CP": 3000},
        {"CLIENTE": "Cliente Monitoramento", "VENDEDOR": "Maria", "CURVA": "C", "STATUS": "CRESCIMENTO",
         "MESES_SEM_COMPRA": 0, "EROSAO STAR": 0, "MEDIA LP": 1000, "MEDIA CP": 1500},
        {"CLIENTE": "Cliente Medio", "VENDEDOR": "Pedro", "CURVA": "B", "STATUS": "ESTAVEL",
         "MESES_SEM_COMPRA": 2, "EROSAO STAR": 3, "MEDIA LP": 5000, "MEDIA CP": 4500},
        {"CLIENTE": "Cliente Alto", "VENDEDOR": "Joao", "CURVA": "A", "STATUS": "INATIVO",
         "MESES_SEM_COMPRA": 8, "EROSAO STAR": 2, "MEDIA LP": 7000, "MEDIA CP": 0},
        {"CLIENTE": "Cliente Investigacao", "VENDEDOR": "Maria", "CURVA": "B", "STATUS": "ESTAVEL",
         "MESES_SEM_COMPRA": 1, "EROSAO STAR": 6, "MEDIA LP": 4000, "MEDIA CP": 3900},
    ])
    df_copia_original = df.copy()

    df_fila = gerar_fila_prioridade(df)

    assert df.equals(df_copia_original), "o DataFrame original nao deveria ser alterado"

    for coluna in ("PONTUACAO_PRIORIDADE", "NIVEL_PRIORIDADE", "TIPO_PRIORIDADE", "MOTIVOS_PRIORIDADE"):
        assert coluna in df_fila.columns, f"{coluna} nao foi criada"

    assert len(df_fila) == len(df), "nenhum cliente deveria ser removido"

    pontuacoes = df_fila["PONTUACAO_PRIORIDADE"].tolist()
    assert pontuacoes == sorted(pontuacoes, reverse=True), "a fila deveria estar ordenada de forma decrescente"

    assert df_fila.iloc[0]["CLIENTE"] == "Cliente Critico", "o cliente mais critico deveria aparecer primeiro"

    print("gerar_fila_prioridade: OK")

    return df_fila


def testar_resumir_fila_prioridade(df_fila):
    resumo = resumir_fila_prioridade(df_fila)

    soma = resumo["p1_critica"] + resumo["p2_alta"] + resumo["p3_media"] + resumo["p4_monitoramento"]
    assert soma == resumo["total_clientes"], f"soma {soma} deveria ser igual a total_clientes {resumo['total_clientes']}"

    print("resumir_fila_prioridade: OK")


if __name__ == "__main__":
    testar_pontuacao_caso_critico()
    testar_pontuacao_caso_monitoramento()
    testar_definir_tipo_prioridade()
    testar_gerar_motivos_prioridade()
    fila = testar_gerar_fila_prioridade()
    testar_resumir_fila_prioridade(fila)
    print("PRIORIZACAO_CARTEIRA_OK")
