"""
Gera planilhas Excel com formatos avancados de colunas mensais (texto,
numericos variados, com prefixo, fora de ordem e parcialmente invalidos),
para testar manualmente star_ingestion/normalizacao_meses.py.

Uso:
    python tests/manual/gerar_planilhas_meses_avancados.py
"""

import os

import pandas as pd


VENDEDORES = ["Joao", "Maria", "Pedro"]

CIDADES = [
    "Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre",
    "Recife", "Salvador", "Fortaleza", "Manaus", "Goiania",
]

PASTA_SAIDA = os.path.join(os.path.dirname(__file__), "meses_avancados")


def _salvar(df, nome_arquivo):
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

    with pd.ExcelWriter(caminho, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Consolidado", index=False)

    return caminho


def _valores_venda(indice, quantidade):
    base = 5000 + indice * 750
    return [base + i * 120 for i in range(quantidade)]


def _montar_base(colunas_meses):
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

        for mes, valor in zip(colunas_meses, _valores_venda(i, len(colunas_meses))):
            dados[mes].append(valor)

    return pd.DataFrame(dados)


def gerar_meses_texto_variado():
    colunas = ["Janeiro 2025", "Fevereiro 2025", "Março 2025", "Abril 2025", "Maio 2025", "Junho 2025"]
    df = _montar_base(colunas)

    return _salvar(df, "meses_texto_variado.xlsx")


def gerar_meses_numericos_variados():
    colunas = ["1/25", "02/25", "03/2025", "2025-04", "2025/05", "06/25"]
    df = _montar_base(colunas)

    return _salvar(df, "meses_numericos_variados.xlsx")


def gerar_meses_com_prefixo():
    colunas = [
        "VENDAS JAN/25", "FATURAMENTO FEV/25", "RECEITA MARÇO 2025",
        "VENDAS ABRIL 2025", "FATURAMENTO MAIO/25", "RECEITA JUNHO/25",
    ]
    df = _montar_base(colunas)

    return _salvar(df, "meses_com_prefixo.xlsx")


def gerar_meses_fora_ordem():
    colunas = ["MAR/25", "JAN/25", "JUN/25", "FEV/25", "MAI/25", "ABR/25"]
    df = _montar_base(colunas)

    return _salvar(df, "meses_fora_ordem.xlsx")


def gerar_meses_invalidos_parciais():
    colunas = ["JAN/25", "13/25", "TOTAL", "FEV/25", "00/25", "MARÇO 2025"]
    df = _montar_base(colunas)

    return _salvar(df, "meses_invalidos_parciais.xlsx")


def gerar_planilhas_meses_avancados():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    caminhos = [
        gerar_meses_texto_variado(),
        gerar_meses_numericos_variados(),
        gerar_meses_com_prefixo(),
        gerar_meses_fora_ordem(),
        gerar_meses_invalidos_parciais(),
    ]

    return caminhos


if __name__ == "__main__":
    for caminho in gerar_planilhas_meses_avancados():
        print(f"Planilha de meses avancados gerada em: {caminho}")
