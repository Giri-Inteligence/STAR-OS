import re
import unicodedata


MESES_NOME_PARA_NUMERO = {
    "JAN": 1, "JANEIRO": 1,
    "FEV": 2, "FEVEREIRO": 2,
    "MAR": 3, "MARCO": 3,
    "ABR": 4, "ABRIL": 4,
    "MAI": 5, "MAIO": 5,
    "JUN": 6, "JUNHO": 6,
    "JUL": 7, "JULHO": 7,
    "AGO": 8, "AGOSTO": 8,
    "SET": 9, "SETEMBRO": 9,
    "OUT": 10, "OUTUBRO": 10,
    "NOV": 11, "NOVEMBRO": 11,
    "DEZ": 12, "DEZEMBRO": 12,
}

TERMOS_BLOQUEADOS = ("TOTAL", "SUBTOTAL", "CLIENTE", "VENDEDOR", "CIDADE")

_NOMES_MESES_REGEX = "|".join(sorted(MESES_NOME_PARA_NUMERO.keys(), key=len, reverse=True))

PADRAO_MES_TEXTO = re.compile(r"\b(" + _NOMES_MESES_REGEX + r")\b[\s/-]*(\d{2,4})\b")
PADRAO_MES_ANO_NUMERICO = re.compile(r"\b(0?[1-9]|1[0-2])[/-](\d{2,4})\b")
PADRAO_ANO_MES_NUMERICO = re.compile(r"\b(\d{4})[/-](0?[1-9]|1[0-2])\b")


def normalizar_texto_coluna(nome):
    texto = " ".join(str(nome).strip().upper().split())
    texto_decomposto = unicodedata.normalize("NFKD", texto)

    return "".join(c for c in texto_decomposto if not unicodedata.combining(c))


def _ano_completo(ano_texto):
    ano = int(ano_texto)

    if ano < 100:
        return 2000 + ano

    return ano


def _montar_periodo(coluna_original, mes, ano):
    if not 1 <= mes <= 12:
        return None

    return {
        "coluna_original": coluna_original,
        "mes": mes,
        "ano": ano,
        "periodo": f"{ano:04d}-{mes:02d}",
        "rotulo": f"{mes:02d}/{ano:04d}",
    }


def extrair_periodo_mes(nome_coluna):
    texto = normalizar_texto_coluna(nome_coluna)

    if texto in TERMOS_BLOQUEADOS:
        return None

    match_texto = PADRAO_MES_TEXTO.search(texto)

    if match_texto:
        mes = MESES_NOME_PARA_NUMERO[match_texto.group(1)]
        ano = _ano_completo(match_texto.group(2))

        return _montar_periodo(nome_coluna, mes, ano)

    match_mes_ano = PADRAO_MES_ANO_NUMERICO.search(texto)

    if match_mes_ano:
        mes = int(match_mes_ano.group(1))
        ano = _ano_completo(match_mes_ano.group(2))

        return _montar_periodo(nome_coluna, mes, ano)

    match_ano_mes = PADRAO_ANO_MES_NUMERICO.search(texto)

    if match_ano_mes:
        ano = _ano_completo(match_ano_mes.group(1))
        mes = int(match_ano_mes.group(2))

        return _montar_periodo(nome_coluna, mes, ano)

    return None


def ordenar_colunas_mensais(meses_col, metadados):
    mapa_periodo = {item["coluna_original"]: (item["ano"], item["mes"]) for item in metadados}

    return sorted(meses_col, key=lambda coluna: mapa_periodo.get(coluna, (9999, 99)))


def detectar_colunas_mensais_avancado(df):
    colunas = list(df.columns)

    metadados = []
    avisos = []
    duplicados = []
    colunas_por_periodo = {}

    for coluna in colunas:
        periodo_info = extrair_periodo_mes(coluna)

        if periodo_info is None:
            continue

        metadados.append(periodo_info)
        colunas_por_periodo.setdefault(periodo_info["periodo"], []).append(coluna)

    for periodo, colunas_periodo in colunas_por_periodo.items():
        if len(colunas_periodo) > 1:
            duplicados.append({"periodo": periodo, "colunas": colunas_periodo})
            nomes = " e ".join(str(c) for c in colunas_periodo)
            rotulo_periodo = f"{periodo[5:7]}/{periodo[:4]}"
            avisos.append(f"período duplicado {rotulo_periodo} nas colunas {nomes}.")

    meses_col = ordenar_colunas_mensais([item["coluna_original"] for item in metadados], metadados)

    return {
        "meses_col": meses_col,
        "metadados": metadados,
        "avisos": avisos,
        "duplicados": duplicados,
    }


def formatar_resumo_normalizacao_meses(resultado):
    linhas = []

    meses_col = resultado.get("meses_col", [])
    metadados = resultado.get("metadados", [])

    linhas.append(f"Meses reconhecidos: {len(meses_col)}")

    if meses_col:
        mapa = {item["coluna_original"]: item["rotulo"] for item in metadados}
        linhas.append(f"Primeiro mês reconhecido: {mapa[meses_col[0]]}")
        linhas.append(f"Último mês reconhecido: {mapa[meses_col[-1]]}")

    for aviso in resultado.get("avisos", []):
        linhas.append(f"Aviso: {aviso}")

    return linhas
