"""
Gera planilhas Excel para testar manualmente a qualidade de linhas
(star_ingestion/qualidade_linhas.py): clientes reais zerados, linhas
residuais evidentes, misturas e clientes com compra parcial/esporadica.

Uso:
    python tests/manual/gerar_planilhas_qualidade_linhas.py
"""

import os

import pandas as pd


VENDEDORES = ["Joao", "Maria", "Pedro"]

CIDADES = [
    "Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre",
    "Recife", "Salvador", "Fortaleza", "Manaus", "Goiania",
]

MESES_6 = ["JAN/25", "FEV/25", "MAR/25", "ABR/25", "MAI/25", "JUN/25"]

MESES_18 = [
    "JAN/25", "FEV/25", "MAR/25", "ABR/25", "MAI/25", "JUN/25",
    "JUL/25", "AGO/25", "SET/25", "OUT/25", "NOV/25", "DEZ/25",
    "JAN/26", "FEV/26", "MAR/26", "ABR/26", "MAI/26", "JUN/26",
]

PASTA_SAIDA = os.path.join(os.path.dirname(__file__), "qualidade_linhas")


def _salvar(df, nome_arquivo):
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

    with pd.ExcelWriter(caminho, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Consolidado", index=False)

    return caminho


def gerar_clientes_zerados_validos():
    dados = {"NOME DO CLIENTE": [], "CIDADE": [], "VENDEDOR": []}

    for mes in MESES_6:
        dados[mes] = []

    for i in range(12):
        dados["NOME DO CLIENTE"].append(f"Cliente Teste {i + 1:02d} Ltda")
        dados["CIDADE"].append(CIDADES[i % len(CIDADES)])
        dados["VENDEDOR"].append(VENDEDORES[i % len(VENDEDORES)])

        if i % 3 == 0:
            vendas = [0.0] * len(MESES_6)
        else:
            base = 4000 + i * 500
            vendas = [base + j * 100 for j in range(len(MESES_6))]

        for mes, valor in zip(MESES_6, vendas):
            dados[mes].append(valor)

    df = pd.DataFrame(dados)

    return _salvar(df, "clientes_zerados_validos.xlsx")


def gerar_linhas_residuais_obvias():
    dados = {"NOME DO CLIENTE": [], "CIDADE": [], "VENDEDOR": []}

    for mes in MESES_6:
        dados[mes] = []

    for i in range(10):
        dados["NOME DO CLIENTE"].append(f"Cliente Teste {i + 1:02d} Ltda")
        dados["CIDADE"].append(CIDADES[i % len(CIDADES)])
        dados["VENDEDOR"].append(VENDEDORES[i % len(VENDEDORES)])

        base = 3000 + i * 400
        for mes, valor in zip(MESES_6, [base + j * 80 for j in range(len(MESES_6))]):
            dados[mes].append(valor)

    linhas_residuais = [
        ("TOTAL", None, None),
        ("TOTAL GERAL", None, None),
        ("SUBTOTAL", None, None),
        ("-", None, None),
        (None, None, None),
        ("NOME DO CLIENTE", None, None),
    ]

    for cliente, cidade, vendedor in linhas_residuais:
        dados["NOME DO CLIENTE"].append(cliente)
        dados["CIDADE"].append(cidade)
        dados["VENDEDOR"].append(vendedor)

        for mes in MESES_6:
            dados[mes].append(0.0)

    df = pd.DataFrame(dados)

    return _salvar(df, "linhas_residuais_obvias.xlsx")


def gerar_misto_zero_residuo():
    dados = {"NOME DO CLIENTE": [], "CIDADE": [], "VENDEDOR": []}

    for mes in MESES_6:
        dados[mes] = []

    clientes_reais = [
        ("Cliente Venda Normal 01 Ltda", [5000, 5200, 4900, 5300, 5400, 5100]),
        ("Cliente Venda Normal 02 Ltda", [7000, 6900, 7100, 7200, 6800, 7300]),
        ("Cliente Zerado 01 Ltda", [0, 0, 0, 0, 0, 0]),
        ("Cliente Zerado 02 Ltda", [0, 0, 0, 0, 0, 0]),
        ("Cliente Venda Normal 03 Ltda", [3000, 3100, 2900, 3200, 3300, 3050]),
        ("Total Distribuidora Ltda", [8000, 8100, 7900, 8200, 8300, 8050]),
        ("Cliente Venda Normal 04 Ltda", [4500, 4600, 4400, 4700, 4800, 4550]),
        ("Cliente Zerado 03 Ltda", [0, 0, 0, 0, 0, 0]),
        ("Cliente Venda Normal 05 Ltda", [6000, 6100, 5900, 6200, 6300, 6050]),
        ("Cliente Venda Normal 06 Ltda", [2500, 2600, 2400, 2700, 2800, 2550]),
    ]

    for i, (cliente, vendas) in enumerate(clientes_reais):
        dados["NOME DO CLIENTE"].append(cliente)
        dados["CIDADE"].append(CIDADES[i % len(CIDADES)])
        dados["VENDEDOR"].append(VENDEDORES[i % len(VENDEDORES)])

        for mes, valor in zip(MESES_6, vendas):
            dados[mes].append(float(valor))

    linhas_residuais = ["TOTAL", "SUBTOTAL", "-"]

    for cliente in linhas_residuais:
        dados["NOME DO CLIENTE"].append(cliente)
        dados["CIDADE"].append(None)
        dados["VENDEDOR"].append(None)

        for mes in MESES_6:
            dados[mes].append(0.0)

    df = pd.DataFrame(dados)

    return _salvar(df, "misto_zero_residuo.xlsx")


def gerar_base_parcial_vendedor_ausente():
    dados = {"NOME DO CLIENTE": [], "CIDADE": [], "VENDEDOR": []}

    for mes in MESES_6:
        dados[mes] = []

    for i in range(12):
        dados["NOME DO CLIENTE"].append(f"Cliente Teste {i + 1:02d} Ltda")
        dados["CIDADE"].append(CIDADES[i % len(CIDADES)])

        if i % 4 == 3:
            dados["VENDEDOR"].append(None)
        else:
            dados["VENDEDOR"].append(VENDEDORES[i % len(VENDEDORES)])

        base = 4000 + i * 300
        for mes, valor in zip(MESES_6, [base + j * 90 for j in range(len(MESES_6))]):
            dados[mes].append(float(valor))

    df = pd.DataFrame(dados)

    return _salvar(df, "base_parcial_vendedor_ausente.xlsx")


def gerar_cliente_compra_parcial():
    dados = {"NOME DO CLIENTE": [], "CIDADE": [], "VENDEDOR": []}

    for mes in MESES_18:
        dados[mes] = []

    def linha_zero():
        return [0.0] * len(MESES_18)

    def linha_um_mes(indice_mes, valor):
        vendas = [0.0] * len(MESES_18)
        vendas[indice_mes] = valor
        return vendas

    def linha_tres_meses(indices, valor):
        vendas = [0.0] * len(MESES_18)
        for indice in indices:
            vendas[indice] = valor
        return vendas

    def linha_esporadica():
        vendas = [0.0] * len(MESES_18)
        for indice in (2, 7, 13):
            vendas[indice] = 1800.0
        return vendas

    clientes = [
        ("Cliente Todos Meses Zerados Ltda", linha_zero()),
        ("Cliente Apenas Um Mes Ltda", linha_um_mes(0, 2500.0)),
        ("Cliente Tres Meses Venda Ltda", linha_tres_meses([0, 1, 2], 1200.0)),
        ("Cliente Quinze Zerados Um Preenchido Ltda", linha_um_mes(17, 3000.0)),
        ("Cliente Compra Esporadica Ltda", linha_esporadica()),
        ("Cliente Venda Constante 01 Ltda", [3000.0 + i * 50 for i in range(len(MESES_18))]),
        ("Cliente Venda Constante 02 Ltda", [4000.0 + i * 40 for i in range(len(MESES_18))]),
        ("Cliente Apenas Ultimo Mes Ltda", linha_um_mes(17, 1500.0)),
        ("Cliente Primeiro Mes Apenas Ltda", linha_um_mes(0, 1700.0)),
        ("Cliente Meio do Periodo Ltda", linha_um_mes(9, 2200.0)),
        ("Cliente Dois Meses Intercalados Ltda", linha_tres_meses([3, 12], 1300.0)),
        ("Cliente Zerado Recente Ltda", linha_zero()),
    ]

    for i, (cliente, vendas) in enumerate(clientes):
        dados["NOME DO CLIENTE"].append(cliente)
        dados["CIDADE"].append(CIDADES[i % len(CIDADES)])
        dados["VENDEDOR"].append(VENDEDORES[i % len(VENDEDORES)])

        for mes, valor in zip(MESES_18, vendas):
            dados[mes].append(valor)

    df = pd.DataFrame(dados)

    return _salvar(df, "cliente_compra_parcial.xlsx")


def gerar_planilhas_qualidade_linhas():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    caminhos = [
        gerar_clientes_zerados_validos(),
        gerar_linhas_residuais_obvias(),
        gerar_misto_zero_residuo(),
        gerar_base_parcial_vendedor_ausente(),
        gerar_cliente_compra_parcial(),
    ]

    return caminhos


if __name__ == "__main__":
    for caminho in gerar_planilhas_qualidade_linhas():
        print(f"Planilha de qualidade de linhas gerada em: {caminho}")
