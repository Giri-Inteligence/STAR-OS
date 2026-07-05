import pandas as pd

from star_ingestion.normalizacao_valores import normalizar_valor_monetario


def _limpar_valor_monetario(valor):
    if pd.isna(valor):
        return None

    return normalizar_valor_monetario(valor)


def validar_colunas_obrigatorias(clie_col, vend_col, meses_col, df):
    erros = []

    if not clie_col:
        erros.append("Coluna de cliente nao foi informada.")
    elif clie_col not in df.columns:
        erros.append(f"Coluna de cliente '{clie_col}' nao existe na planilha.")

    if not vend_col:
        erros.append("Coluna de vendedor nao foi informada.")
    elif vend_col not in df.columns:
        erros.append(f"Coluna de vendedor '{vend_col}' nao existe na planilha.")

    if not meses_col:
        erros.append("Nenhuma coluna de faturamento mensal foi informada.")
    else:
        faltantes = [c for c in meses_col if c not in df.columns]

        if faltantes:
            nomes = ", ".join(str(c) for c in faltantes)
            erros.append(f"Coluna(s) de mes nao encontrada(s) na planilha: {nomes}.")

    return len(erros) == 0, erros


def validar_colunas_mensais(meses_col, df):
    erros = []

    if not meses_col:
        return False, ["Nenhuma coluna de faturamento mensal foi informada."]

    faltantes = [c for c in meses_col if c not in df.columns]

    if faltantes:
        nomes = ", ".join(str(c) for c in faltantes)
        erros.append(f"Coluna(s) de mes nao encontrada(s) na planilha: {nomes}.")
        return False, erros

    colunas_com_numero_valido = []

    for coluna in meses_col:
        valores_limpos = df[coluna].apply(_limpar_valor_monetario)
        numeros = pd.to_numeric(valores_limpos, errors="coerce")

        if numeros.notna().sum() > 0:
            colunas_com_numero_valido.append(coluna)

    if not colunas_com_numero_valido:
        erros.append(
            "Nenhuma das colunas de faturamento mensal contem valores numericos validos "
            "apos limpar moeda, pontos, virgulas e espacos."
        )

    return len(erros) == 0, erros


def validar_base_minima(df, clie_col, vend_col, meses_col):
    erros = []

    if df is None or df.empty:
        return False, ["A planilha esta vazia."]

    valido_colunas, erros_colunas = validar_colunas_obrigatorias(clie_col, vend_col, meses_col, df)
    erros.extend(erros_colunas)

    valido_meses, erros_meses = validar_colunas_mensais(meses_col, df)

    for erro in erros_meses:
        if erro not in erros:
            erros.append(erro)

    if not valido_colunas or not valido_meses:
        return False, erros

    clientes = df[clie_col].astype(str).str.strip()
    tem_cliente = df[clie_col].notna() & (clientes != "") & (clientes.str.upper() != "NAN")

    if not tem_cliente.any():
        erros.append("Nao existe nenhuma linha com cliente preenchido.")

    tem_venda = False

    for coluna in meses_col:
        valores_limpos = df[coluna].apply(_limpar_valor_monetario)
        numeros = pd.to_numeric(valores_limpos, errors="coerce").fillna(0)

        if (numeros != 0).any():
            tem_venda = True
            break

    if not tem_venda:
        erros.append("Nao existe nenhuma linha com venda registrada em algum mes.")

    return len(erros) == 0, erros
