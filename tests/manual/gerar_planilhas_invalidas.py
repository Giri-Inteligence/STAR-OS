"""
Gera planilhas Excel propositalmente invalidas, para testar manualmente se o
STAR OS bloqueia bases sem a estrutura minima exigida
(star_ingestion/validacao.py).

Uso:
    python tests/manual/gerar_planilhas_invalidas.py
"""

import os

import pandas as pd


MESES = ["JANEIRO/25", "FEVEREIRO/25", "MARÇO/25", "ABRIL/25", "MAIO/25", "JUNHO/25"]

PASTA_SAIDA = os.path.join(os.path.dirname(__file__), "invalidas")


def _salvar(df, nome_arquivo):
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

    with pd.ExcelWriter(caminho, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Consolidado", index=False)

    return caminho


def gerar_sem_cliente():
    # Tem CIDADE, VENDEDOR e meses, mas nenhuma coluna de nome de cliente.
    dados = {
        "CIDADE": ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte"],
        "VENDEDOR": ["Joao", "Maria", "Pedro"],
    }

    for mes in MESES:
        dados[mes] = [1000, 1200, 900]

    df = pd.DataFrame(dados)

    return _salvar(df, "sem_cliente.xlsx")


def gerar_sem_vendedor():
    # Tem NOME DO CLIENTE, CIDADE e meses, mas nenhuma coluna de vendedor.
    dados = {
        "NOME DO CLIENTE": ["Comercial Aurora Ltda", "Distribuidora Bela Vista", "Mercado Central Ltda"],
        "CIDADE": ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte"],
    }

    for mes in MESES:
        dados[mes] = [1000, 1200, 900]

    df = pd.DataFrame(dados)

    return _salvar(df, "sem_vendedor.xlsx")


def gerar_sem_meses():
    # Tem NOME DO CLIENTE, CIDADE e VENDEDOR, mas nenhuma coluna mensal.
    dados = {
        "NOME DO CLIENTE": ["Comercial Aurora Ltda", "Distribuidora Bela Vista", "Mercado Central Ltda"],
        "CIDADE": ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte"],
        "VENDEDOR": ["Joao", "Maria", "Pedro"],
    }

    df = pd.DataFrame(dados)

    return _salvar(df, "sem_meses.xlsx")


def gerar_cliente_vazio():
    # Tem todas as colunas minimas, mas NOME DO CLIENTE totalmente vazio.
    dados = {
        "NOME DO CLIENTE": [None, None, None],
        "CIDADE": ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte"],
        "VENDEDOR": ["Joao", "Maria", "Pedro"],
    }

    for mes in MESES:
        dados[mes] = [1000, 1200, 900]

    df = pd.DataFrame(dados)

    return _salvar(df, "cliente_vazio.xlsx")


def gerar_base_vazia():
    # Tem as colunas minimas, mas nenhuma linha de dados.
    colunas = ["NOME DO CLIENTE", "CIDADE", "VENDEDOR"] + MESES
    df = pd.DataFrame(columns=colunas)

    return _salvar(df, "base_vazia.xlsx")


def gerar_meses_invalidos():
    # Tem todas as colunas minimas, mas os valores dos meses sao todos invalidos.
    dados = {
        "NOME DO CLIENTE": ["Comercial Aurora Ltda", "Distribuidora Bela Vista", "Mercado Central Ltda"],
        "CIDADE": ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte"],
        "VENDEDOR": ["Joao", "Maria", "Pedro"],
    }

    valores_invalidos = ["erro", "abc", "sem dado"]

    for mes in MESES:
        dados[mes] = valores_invalidos

    df = pd.DataFrame(dados)

    return _salvar(df, "meses_invalidos.xlsx")


def gerar_planilhas_invalidas():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    caminhos = [
        gerar_sem_cliente(),
        gerar_sem_vendedor(),
        gerar_sem_meses(),
        gerar_cliente_vazio(),
        gerar_base_vazia(),
        gerar_meses_invalidos(),
    ]

    return caminhos


if __name__ == "__main__":
    for caminho in gerar_planilhas_invalidas():
        print(f"Planilha invalida gerada em: {caminho}")
