import re


MESES_PT = (
    "JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
    "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"
)


def normalizar_nome_coluna(coluna):
    return str(coluna).strip().upper()


def detectar_colunas_meses(colunas):
    meses = []

    for coluna in colunas:
        nome = normalizar_nome_coluna(coluna)

        tem_mes_texto = any(mes in nome for mes in MESES_PT)
        tem_formato_numerico = bool(re.search(r"\b(0?[1-9]|1[0-2])[/\-]\d{2,4}\b", nome))

        if tem_mes_texto or tem_formato_numerico:
            meses.append(coluna)

    return meses


def sugerir_coluna_cliente(colunas):
    palavras_chave = ("CLIENTE", "RAZAO", "RAZÃO", "NOME", "CONTA", "EMPRESA")

    for coluna in colunas:
        nome = normalizar_nome_coluna(coluna)

        if any(palavra in nome for palavra in palavras_chave):
            return coluna

    return None


def sugerir_coluna_vendedor(colunas):
    palavras_chave = ("VENDEDOR", "REPRESENTANTE", "REP", "CONSULTOR", "RESPONSAVEL", "RESPONSÁVEL")

    for coluna in colunas:
        nome = normalizar_nome_coluna(coluna)

        if any(palavra in nome for palavra in palavras_chave):
            return coluna

    return None


def sugerir_coluna_cidade(colunas):
    palavras_chave = ("CIDADE", "MUNICIPIO", "MUNICÍPIO", "LOCALIDADE", "REGIAO", "REGIÃO")

    for coluna in colunas:
        nome = normalizar_nome_coluna(coluna)

        if any(palavra in nome for palavra in palavras_chave):
            return coluna

    return None


def gerar_sugestoes_mapeamento(df):
    colunas = list(df.columns)

    return {
        "cliente": sugerir_coluna_cliente(colunas),
        "vendedor": sugerir_coluna_vendedor(colunas),
        "cidade": sugerir_coluna_cidade(colunas),
        "meses": detectar_colunas_meses(colunas),
        "colunas_disponiveis": colunas,
    }