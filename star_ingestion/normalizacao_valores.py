import re


SIMBOLOS_MONETARIOS = re.compile(r"(?i)r\$|brl")
CARACTERES_VAZIOS = {"-", "—", "–", "--"}
PADRAO_NUMERICO = re.compile(r"-?[0-9.,]+")


def _limpar_texto(valor):
    texto = str(valor).strip()
    texto = SIMBOLOS_MONETARIOS.sub("", texto)
    texto = re.sub(r"\s+", "", texto)

    return texto


def _converter_texto_numerico(texto):
    tem_virgula = "," in texto
    tem_ponto = "." in texto

    if tem_virgula and tem_ponto:
        pos_virgula = texto.rfind(",")
        pos_ponto = texto.rfind(".")

        if pos_virgula > pos_ponto:
            texto = texto.replace(".", "").replace(",", ".")
        else:
            texto = texto.replace(",", "")

    elif tem_virgula:
        partes = texto.split(",")

        if len(partes) == 2 and len(partes[1]) in (1, 2):
            texto = partes[0] + "." + partes[1]
        else:
            texto = texto.replace(",", "")

    elif tem_ponto:
        partes = texto.split(".")

        if len(partes) == 2 and len(partes[1]) in (1, 2):
            texto = partes[0] + "." + partes[1]
        else:
            texto = texto.replace(".", "")

    try:
        return float(texto)
    except ValueError:
        return None


def normalizar_valor_monetario(valor):
    if valor is None:
        return None

    if isinstance(valor, float) and valor != valor:
        return None

    if isinstance(valor, (int, float)):
        return float(valor)

    texto = _limpar_texto(valor)

    if texto == "" or texto in CARACTERES_VAZIOS:
        return None

    if not PADRAO_NUMERICO.fullmatch(texto):
        return None

    return _converter_texto_numerico(texto)


def _classificar_valor(valor):
    if valor is None:
        return 0.0, "vazio_ou_hifen"

    if isinstance(valor, float) and valor != valor:
        return 0.0, "vazio_ou_hifen"

    if isinstance(valor, (int, float)):
        return float(valor), "convertido"

    texto = _limpar_texto(valor)

    if texto == "" or texto in CARACTERES_VAZIOS:
        return 0.0, "vazio_ou_hifen"

    numero = normalizar_valor_monetario(valor)

    if numero is None:
        return 0.0, "invalido"

    return numero, "convertido"


def normalizar_colunas_monetarias(df, meses_col):
    df_normalizado = df.copy()

    colunas_processadas = 0
    valores_convertidos = 0
    valores_vazios_ou_hifen = 0
    valores_invalidos = 0
    colunas_ausentes = []

    for coluna in meses_col or []:
        if coluna not in df_normalizado.columns:
            colunas_ausentes.append(coluna)
            continue

        colunas_processadas += 1
        valores_finais = []

        for valor in df_normalizado[coluna]:
            valor_final, categoria = _classificar_valor(valor)
            valores_finais.append(valor_final)

            if categoria == "convertido":
                valores_convertidos += 1
            elif categoria == "vazio_ou_hifen":
                valores_vazios_ou_hifen += 1
            else:
                valores_invalidos += 1

        df_normalizado[coluna] = valores_finais

    mensagens = [
        f"{colunas_processadas} coluna(s) monetaria(s) processada(s).",
        f"{valores_convertidos} valor(es) convertido(s) com sucesso.",
        f"{valores_vazios_ou_hifen} valor(es) vazio(s) ou hifen tratado(s) como 0.",
    ]

    avisos = []

    if valores_invalidos > 0:
        avisos.append(f"{valores_invalidos} valor(es) invalido(s) foram tratados como 0.")

    if colunas_ausentes:
        nomes = ", ".join(str(c) for c in colunas_ausentes)
        avisos.append(f"Coluna(s) de mes ausente(s) na base: {nomes}.")

    return {
        "df": df_normalizado,
        "mensagens": mensagens,
        "avisos": avisos,
        "estatisticas": {
            "colunas_processadas": colunas_processadas,
            "valores_convertidos": valores_convertidos,
            "valores_vazios_ou_hifen": valores_vazios_ou_hifen,
            "valores_invalidos": valores_invalidos,
            "colunas_ausentes": colunas_ausentes,
        },
    }


def formatar_resumo_normalizacao_valores(resultado):
    estatisticas = resultado.get("estatisticas", {})
    linhas = []

    linhas.append(f"Colunas monetárias processadas: {estatisticas.get('colunas_processadas', 0)}")
    linhas.append(f"Valores convertidos com sucesso: {estatisticas.get('valores_convertidos', 0)}")
    linhas.append(f"Valores vazios ou hífen tratados como 0: {estatisticas.get('valores_vazios_ou_hifen', 0)}")

    valores_invalidos = estatisticas.get("valores_invalidos", 0)

    if valores_invalidos > 0:
        linhas.append(f"Aviso: {valores_invalidos} valores inválidos foram tratados como 0.")

    colunas_ausentes = estatisticas.get("colunas_ausentes", [])

    if colunas_ausentes:
        nomes = ", ".join(str(c) for c in colunas_ausentes)
        linhas.append(f"Aviso: coluna(s) de mês ausente(s) na base: {nomes}.")

    return linhas
