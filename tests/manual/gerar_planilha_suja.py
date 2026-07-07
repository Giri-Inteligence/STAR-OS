"""
Gera uma planilha Excel propositalmente suja para testar, de forma manual,
o saneamento leve implementado em star_ingestion/saneamento.py.

Uso:
    python tests/manual/gerar_planilha_suja.py
"""

import os

import pandas as pd


COLUNAS = [
    "NOME DO CLIENTE",
    "CIDADE",
    "VENDEDOR",
    "JANEIRO/25",
    "FEVEREIRO/25",
    "MARÇO/25",
    "ABRIL/25",
    "MAIO/25",
    "JUNHO/25",
]

CAMINHO_SAIDA = os.path.join(os.path.dirname(__file__), "planilha_suja_star.xlsx")


def _cliente(nome, cidade, vendedor, vendas):
    linha = [nome, cidade, vendedor] + list(vendas)
    return dict(zip(COLUNAS, linha))


def montar_linhas():
    linhas = []

    # 10 clientes validos, com vendedores e cidades variados
    linhas.append(_cliente("Comercial Aurora Ltda", "Sao Paulo", "Joao", [12000, 13500, 11800, 14200, 15000, 13900]))
    linhas.append(_cliente("Distribuidora Bela Vista", "Rio de Janeiro", "Maria", [8000, 8200, 7900, 8600, 9000, 8700]))
    linhas.append(_cliente("Mercado Central Ltda", "Belo Horizonte", "Pedro", [5000, 5300, 4800, 5100, 5600, 5400]))
    linhas.append(_cliente("Casa do Construtor Sul", "Curitiba", "Joao", [21000, 19800, 20500, 22000, 21500, 23000]))
    linhas.append(_cliente("Armazem Boa Esperanca", "Porto Alegre", "Maria", [3000, 3100, 2900, 3200, 3300, 3150]))

    # linha suja 3: repete o cabecalho dentro da tabela
    linhas.append(dict(zip(COLUNAS, COLUNAS)))

    linhas.append(_cliente("Ferragens Nova Era", "Recife", "Pedro", [9500, 9700, 9200, 9800, 10100, 9900]))
    linhas.append(_cliente("Comercio Vale Verde", "Salvador", "Joao", [6700, 6900, 6500, 7000, 7200, 6950]))
    linhas.append(_cliente("Distribuidora Estrela Ltda", "Fortaleza", "Maria", [15200, 14800, 15500, 16000, 15700, 16200]))
    linhas.append(_cliente("Mercearia Sao Jose", "Manaus", "Pedro", [2400, 2500, 2300, 2600, 2700, 2550]))
    linhas.append(_cliente("Atacado Rio Grande", "Goiania", "Joao", [11000, 11500, 10800, 11700, 12000, 11900]))

    # cliente real com "Total" no nome: NAO pode ser removido pelo saneamento
    linhas.append(_cliente("Total Distribuidora Ltda", "Brasilia", "Maria", [18000, 17500, 18200, 18700, 19000, 18600]))

    # linha suja 1: totalmente vazia
    linhas.append({coluna: None for coluna in COLUNAS})

    # linha suja 4: NOME DO CLIENTE = TOTAL
    linha_total = {coluna: None for coluna in COLUNAS}
    linha_total["NOME DO CLIENTE"] = "TOTAL"
    linhas.append(linha_total)

    # linha suja 5: NOME DO CLIENTE = SUBTOTAL
    linha_subtotal = {coluna: None for coluna in COLUNAS}
    linha_subtotal["NOME DO CLIENTE"] = "SUBTOTAL"
    linhas.append(linha_subtotal)

    return linhas


def gerar_planilha_suja():
    linhas = montar_linhas()
    df = pd.DataFrame(linhas, columns=COLUNAS)

    # linha suja 2: coluna totalmente vazia
    df["OBSERVACAO"] = None

    with pd.ExcelWriter(CAMINHO_SAIDA, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Consolidado", index=False)

    return CAMINHO_SAIDA


if __name__ == "__main__":
    caminho = gerar_planilha_suja()
    print(f"Planilha suja gerada em: {caminho}")
