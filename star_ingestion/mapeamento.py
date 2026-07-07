import re


MESES_PT = (
    "JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
    "JUL", "AGO", "SET", "OUT", "NOV", "DEZ",
    "JANEIRO", "FEVEREIRO", "MARÇO", "MARCO", "ABRIL", "MAIO", "JUNHO",
    "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
)

# Termos usados para reconhecer cada campo estrutural. Propositalmente sem
# palavras genericas como "NOME" isoladas, pois isso combinava com colunas
# erradas (ex.: "NOME DA CIDADE" sendo sugerida como coluna de cliente).
TERMOS_CLIENTE = ("CLIENTE", "RAZAO", "RAZÃO", "CONTA", "EMPRESA")
TERMOS_VENDEDOR = ("VENDEDOR", "REPRESENTANTE", "CONSULTOR", "RESPONSAVEL", "RESPONSÁVEL")
TERMOS_CIDADE = ("CIDADE", "MUNICIPIO", "MUNICÍPIO", "REGIAO", "REGIÃO", "LOCALIDADE")
TERMOS_ESTRUTURAIS_EXTRA = ("SEGMENTO", "FILIAL")


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


def _tem_termo(nome, termos):
    return any(termo in nome for termo in termos)


def _colunas_validas_para_cliente(colunas):
    meses = set(detectar_colunas_meses(colunas))
    termos_excluir = TERMOS_VENDEDOR + TERMOS_CIDADE + TERMOS_ESTRUTURAIS_EXTRA

    return [
        coluna for coluna in colunas
        if coluna not in meses and not _tem_termo(normalizar_nome_coluna(coluna), termos_excluir)
    ]


def _colunas_validas_para_vendedor(colunas):
    meses = set(detectar_colunas_meses(colunas))
    termos_excluir = TERMOS_CLIENTE + TERMOS_CIDADE + TERMOS_ESTRUTURAIS_EXTRA

    return [
        coluna for coluna in colunas
        if coluna not in meses and not _tem_termo(normalizar_nome_coluna(coluna), termos_excluir)
    ]


def _colunas_validas_para_cidade(colunas):
    meses = set(detectar_colunas_meses(colunas))
    termos_excluir = TERMOS_CLIENTE + TERMOS_VENDEDOR + TERMOS_ESTRUTURAIS_EXTRA

    return [
        coluna for coluna in colunas
        if coluna not in meses and not _tem_termo(normalizar_nome_coluna(coluna), termos_excluir)
    ]


def sugerir_coluna_cliente(colunas):
    candidatas = _colunas_validas_para_cliente(colunas)

    for termo in TERMOS_CLIENTE:
        for coluna in candidatas:
            if termo in normalizar_nome_coluna(coluna):
                return coluna

    return None


def sugerir_coluna_vendedor(colunas):
    candidatas = _colunas_validas_para_vendedor(colunas)

    for termo in TERMOS_VENDEDOR:
        for coluna in candidatas:
            if termo in normalizar_nome_coluna(coluna):
                return coluna

    return None


def sugerir_coluna_cidade(colunas):
    candidatas = _colunas_validas_para_cidade(colunas)

    for termo in TERMOS_CIDADE:
        for coluna in candidatas:
            if termo in normalizar_nome_coluna(coluna):
                return coluna

    return None


def montar_opcoes_cliente(colunas):
    validas = _colunas_validas_para_cliente(colunas)

    prioritarias = [c for c in validas if _tem_termo(normalizar_nome_coluna(c), TERMOS_CLIENTE)]
    outras = [c for c in validas if c not in prioritarias]

    opcoes = remover_duplicatas(prioritarias + outras)

    if opcoes:
        return opcoes

    # Nunca deixar o campo obrigatorio de cliente sem nenhuma opcao: cai para
    # todas as colunas que nao sejam de mes e, em ultimo caso, todas as colunas.
    meses = set(detectar_colunas_meses(colunas))
    sem_meses = [c for c in colunas if c not in meses]

    return sem_meses if sem_meses else list(colunas)


def montar_opcoes_vendedor(colunas):
    validas = _colunas_validas_para_vendedor(colunas)

    prioritarias = [c for c in validas if _tem_termo(normalizar_nome_coluna(c), TERMOS_VENDEDOR)]
    outras = [c for c in validas if c not in prioritarias]

    opcoes = remover_duplicatas(prioritarias + outras)

    return ["Não usar"] + opcoes


def montar_opcoes_cidade(colunas):
    validas = _colunas_validas_para_cidade(colunas)

    prioritarias = [c for c in validas if _tem_termo(normalizar_nome_coluna(c), TERMOS_CIDADE)]
    outras = [c for c in validas if c not in prioritarias]

    opcoes = remover_duplicatas(prioritarias + outras)

    return ["Não usar"] + opcoes


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
