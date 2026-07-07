"""
Gera planilhas Excel com formatos avancados de valores monetarios
(brasileiro, americano, misto, vazios/hifen e parcialmente invalidos), para
testar manualmente star_ingestion/normalizacao_valores.py.

Uso:
    python tests/manual/gerar_planilhas_valores_avancados.py
"""

import os

import pandas as pd


VENDEDORES = ["Joao", "Maria", "Pedro"]

CIDADES = [
    "Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre",
    "Recife", "Salvador", "Fortaleza", "Manaus", "Goiania",
]

PASTA_SAIDA = os.path.join(os.path.dirname(__file__), "valores_avancados")

COLUNAS_MESES_PADRAO = ["JAN/25", "FEV/25", "MAR/25", "ABR/25", "MAI/25", "JUN/25"]


def _salvar(df, nome_arquivo):
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

    with pd.ExcelWriter(caminho, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Consolidado", index=False)

    return caminho


def _montar_base(colunas_meses, valores_padrao):
    dados = {
        "NOME DO CLIENTE": [],
        "CIDADE": [],
        "VENDEDOR": [],
    }

    for mes in colunas_meses:
        dados[mes] = []

    for i in range(10):
        dados["NOME DO CLIENTE"].append(f"Cliente Teste {i + 1:02d} Ltda")
        dados["CIDADE"].append(CIDADES[i % len(CIDADES)])
        dados["VENDEDOR"].append(VENDEDORES[i % len(VENDEDORES)])

        for j, mes in enumerate(colunas_meses):
            dados[mes].append(valores_padrao[(i + j) % len(valores_padrao)])

    return pd.DataFrame(dados)


def gerar_valores_brasileiros():
    valores = ["R$ 10.000,00", "10.000,00", "1.234.567,89", "10000,50"]
    df = _montar_base(COLUNAS_MESES_PADRAO, valores)

    return _salvar(df, "valores_brasileiros.xlsx")


def gerar_valores_americanos():
    valores = ["10,000.50", "1,234,567.89", "10000.50", "10000"]
    df = _montar_base(COLUNAS_MESES_PADRAO, valores)

    return _salvar(df, "valores_americanos.xlsx")


def gerar_valores_mistos():
    colunas = ["Janeiro 2025", "FEV/25", "FATURAMENTO MARÇO 2025", "2025-04", "MAIO/25", "RECEITA JUNHO/25"]
    valores = ["R$ 10.000,00", "10,000.50", "10000,50", "10000.50", "10.000"]
    df = _montar_base(colunas, valores)

    return _salvar(df, "valores_mistos.xlsx")


def gerar_valores_vazios_hifen():
    valores = [10000, 12000, "", "-", "—", "R$ -"]
    df = _montar_base(COLUNAS_MESES_PADRAO, valores)

    return _salvar(df, "valores_vazios_hifen.xlsx")


def gerar_valores_invalidos_parciais():
    valores = [10000, 12000, "abc", "não informado", "erro", "-"]
    df = _montar_base(COLUNAS_MESES_PADRAO, valores)

    return _salvar(df, "valores_invalidos_parciais.xlsx")


def gerar_planilhas_valores_avancados():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    caminhos = [
        gerar_valores_brasileiros(),
        gerar_valores_americanos(),
        gerar_valores_mistos(),
        gerar_valores_vazios_hifen(),
        gerar_valores_invalidos_parciais(),
    ]

    return caminhos


if __name__ == "__main__":
    for caminho in gerar_planilhas_valores_avancados():
        print(f"Planilha de valores avancados gerada em: {caminho}")
