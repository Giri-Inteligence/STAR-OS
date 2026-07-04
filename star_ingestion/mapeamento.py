import re


MESES_PT = (
    "JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
    "JUL", "AGO", "SET", "OUT", "NOV", "DEZ",
    "JANEIRO", "FEVEREIRO", "MARÇO", "MARCO", "ABRIL", "MAIO", "JUNHO",
    "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
)


def normalizar_nome_coluna(coluna):
    return str(coluna).strip().upper()


def remover_duplicatas(lista):
    resultado = []
    vistos = set()

    for item in lista:
        chave = str(item)

        if chave not in vistos:
            resultado.append(item)
            vistos.add(chave)

    return resultado


def detectar_colunas_meses(colunas):
    meses = []

    for coluna in colunas:
        nome = normalizar_nome_coluna(coluna)

        tem_mes_texto = any(mes in nome for mes in MESES_PT)
        tem_formato_numerico = bool(
            re.search(r"\b(0?[1-9]|1[0-2])[/\-]\d{2,4}\b", nome)
        )

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
    palavras_chave = (
        "VENDEDOR",
        "VENDEDOR_STAR_ABA",
        "REPRESENTANTE",
        "REP",
        "CONSULTOR",
        "RESPONSAVEL",
        "RESPONSÁVEL"
    )

    for coluna in colunas:
        nome = normalizar_nome_coluna(coluna)

        if any(palavra in nome for palavra in palavras_chave):
            return coluna

    return None


def sugerir_coluna_cidade(colunas):
    palavras_chave = (
        "CIDADE",
        "CIDADE_STAR_ABA",
        "MUNICIPIO",
        "MUNICÍPIO",
        "LOCALIDADE",
        "REGIAO",
        "REGIÃO"
    )

    for coluna in colunas:
        nome = normalizar_nome_coluna(coluna)

        if any(palavra in nome for palavra in palavras_chave):
            return coluna

    return None


def montar_opcoes_cliente(colunas):
    meses = set(detectar_colunas_meses(colunas))

    termos_excluir = (
        "VENDEDOR", "VENDEDOR_STAR_ABA",
        "REPRESENTANTE", "REP", "CONSULTOR", "RESPONSAVEL", "RESPONSÁVEL",
        "CIDADE", "CIDADE_STAR_ABA",
        "MUNICIPIO", "MUNICÍPIO", "LOCALIDADE", "REGIAO", "REGIÃO",
        "SEGMENTO", "SEGMENTO_STAR",
        "FILIAL", "FILIAL_STAR"
    )

    termos_cliente = ("CLIENTE", "RAZAO", "RAZÃO", "NOME", "CONTA", "EMPRESA")

    candidatos = []
    outros = []

    for coluna in colunas:
        nome = normalizar_nome_coluna(coluna)

        if coluna in meses:
            continue

        if any(t in nome for t in termos_excluir):
            continue

        if any(t in nome for t in termos_cliente):
            candidatos.append(coluna)
        else:
            outros.append(coluna)

    opcoes = remover_duplicatas(candidatos + outros)

    return opcoes if opcoes else list(colunas)


def montar_opcoes_vendedor(colunas):
    meses = set(detectar_colunas_meses(colunas))

    termos_vendedor = (
        "VENDEDOR",
        "VENDEDOR_STAR_ABA",
        "REPRESENTANTE",
        "REP",
        "CONSULTOR",
        "RESPONSAVEL",
        "RESPONSÁVEL"
    )

    candidatos = []
    fallback = []

    for coluna in colunas:
        nome = normalizar_nome_coluna(coluna)

        if coluna in meses:
            continue

        if any(t in nome for t in termos_vendedor):
            candidatos.append(coluna)
        else:
            fallback.append(coluna)

    if candidatos:
        return ["Não usar"] + remover_duplicatas(candidatos)

    return ["Não usar"] + remover_duplicatas(fallback)


def montar_opcoes_cidade(colunas):
    meses = set(detectar_colunas_meses(colunas))

    termos_cidade = (
        "CIDADE",
        "CIDADE_STAR_ABA",
        "MUNICIPIO",
        "MUNICÍPIO",
        "LOCALIDADE",
        "REGIAO",
        "REGIÃO"
    )

    candidatos = []
    fallback = []

    for coluna in colunas:
        nome = normalizar_nome_coluna(coluna)

        if coluna in meses:
            continue

        if any(t in nome for t in termos_cidade):
            candidatos.append(coluna)
        else:
            fallback.append(coluna)

    if candidatos:
        return ["Não usar"] + remover_duplicatas(candidatos)

    return ["Não usar"] + remover_duplicatas(fallback)


def gerar_sugestoes_mapeamento(df):
    colunas = list(df.columns)

    return {
        "cliente": sugerir_coluna_cliente(colunas),
        "vendedor": sugerir_coluna_vendedor(colunas),
        "cidade": sugerir_coluna_cidade(colunas),
        "meses": detectar_colunas_meses(colunas),
        "colunas_disponiveis": colunas,
        "opcoes_cliente": montar_opcoes_cliente(colunas),
        "opcoes_vendedor": montar_opcoes_vendedor(colunas),
        "opcoes_cidade": montar_opcoes_cidade(colunas),
    }