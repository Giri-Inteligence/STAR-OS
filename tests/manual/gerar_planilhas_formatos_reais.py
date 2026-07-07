"""
Gera planilhas Excel com variacoes reais de nomes de colunas e formatos de
valores, comuns em exportacoes de ERP/CRM/controles internos, para testar
manualmente o mapeamento guiado e a validacao (star_ingestion/mapeamento.py
e star_ingestion/validacao.py).

Uso:
    python tests/manual/gerar_planilhas_formatos_reais.py
"""

import os

import pandas as pd


MESES_TEXTO = ["JANEIRO/25", "FEVEREIRO/25", "MARÇO/25", "ABRIL/25", "MAIO/25", "JUNHO/25"]
MESES_NUMERICOS = ["01/25", "02/25", "03/25", "04/25", "05/25", "06/25"]

VENDEDORES = ["Joao", "Maria", "Pedro"]

CIDADES = [
    "Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre",
    "Recife", "Salvador", "Fortaleza", "Manaus", "Goiania",
]

PASTA_SAIDA = os.path.join(os.path.dirname(__file__), "formatos_reais")


def _salvar(df, nome_arquivo):
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

    with pd.ExcelWriter(caminho, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Consolidado", index=False)

    return caminho


def _valores_venda(indice):
    base = 5000 + indice * 750
    return [base + i * 120 for i in range(len(MESES_TEXTO))]


def gerar_planilha_estrutural(nome_cliente_col, nome_cidade_col, nome_vendedor_col, nome_arquivo):
    dados = {
        nome_cliente_col: [],
        nome_cidade_col: [],
        nome_vendedor_col: [],
    }

    for mes in MESES_TEXTO:
        dados[mes] = []

    for i in range(10):
        dados[nome_cliente_col].append(f"Cliente Teste {i + 1:02d} Ltda")
        dados[nome_cidade_col].append(CIDADES[i % len(CIDADES)])
        dados[nome_vendedor_col].append(VENDEDORES[i % len(VENDEDORES)])

        for mes, valor in zip(MESES_TEXTO, _valores_venda(i)):
            dados[mes].append(valor)

    df = pd.DataFrame(dados)

    return _salvar(df, nome_arquivo)


def gerar_razao_representante_municipio():
    return gerar_planilha_estrutural(
        "RAZÃO SOCIAL", "MUNICÍPIO", "REPRESENTANTE",
        "razao_representante_municipio.xlsx",
    )


def gerar_empresa_consultor_regiao():
    return gerar_planilha_estrutural(
        "EMPRESA", "REGIÃO", "CONSULTOR",
        "empresa_consultor_regiao.xlsx",
    )


def gerar_conta_responsavel_localidade():
    return gerar_planilha_estrutural(
        "CONTA", "LOCALIDADE", "RESPONSÁVEL",
        "conta_responsavel_localidade.xlsx",
    )


def gerar_meses_numericos():
    dados = {
        "NOME DO CLIENTE": [],
        "CIDADE": [],
        "VENDEDOR": [],
    }

    for mes in MESES_NUMERICOS:
        dados[mes] = []

    for i in range(10):
        dados["NOME DO CLIENTE"].append(f"Cliente Teste {i + 1:02d} Ltda")
        dados["CIDADE"].append(CIDADES[i % len(CIDADES)])
        dados["VENDEDOR"].append(VENDEDORES[i % len(VENDEDORES)])

        for mes, valor in zip(MESES_NUMERICOS, _valores_venda(i)):
            dados[mes].append(valor)

    df = pd.DataFrame(dados)

    return _salvar(df, "meses_numericos.xlsx")


def gerar_valores_monetarios():
    # Formatos variados de valor que uma planilha real de cliente costuma trazer.
    formatos = [10000, 10000.50, "R$ 10.000,00", "10.000,00", None, "-"]

    dados = {
        "NOME DO CLIENTE": [],
        "CIDADE": [],
        "VENDEDOR": [],
    }

    for mes in MESES_TEXTO:
        dados[mes] = []

    for i in range(10):
        dados["NOME DO CLIENTE"].append(f"Cliente Teste {i + 1:02d} Ltda")
        dados["CIDADE"].append(CIDADES[i % len(CIDADES)])
        dados["VENDEDOR"].append(VENDEDORES[i % len(VENDEDORES)])

        for j, mes in enumerate(MESES_TEXTO):
            valor = formatos[(i + j) % len(formatos)]
            dados[mes].append(valor)

    df = pd.DataFrame(dados)

    return _salvar(df, "valores_monetarios.xlsx")


def gerar_planilhas_formatos_reais():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    caminhos = [
        gerar_razao_representante_municipio(),
        gerar_empresa_consultor_regiao(),
        gerar_conta_responsavel_localidade(),
        gerar_meses_numericos(),
        gerar_valores_monetarios(),
    ]

    return caminhos


if __name__ == "__main__":
    for caminho in gerar_planilhas_formatos_reais():
        print(f"Planilha de formato real gerada em: {caminho}")
