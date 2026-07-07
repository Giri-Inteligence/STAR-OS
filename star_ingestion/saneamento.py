TERMOS_TOTAL_SUBTOTAL = ("TOTAL", "TOTAL GERAL", "SUBTOTAL", "SOMA")


def remover_linhas_colunas_vazias(df):
    relatorio_saneamento = []
    df_saneado = df.copy()

    linhas_antes = len(df_saneado)
    df_saneado = df_saneado.dropna(how="all").reset_index(drop=True)
    linhas_removidas = linhas_antes - len(df_saneado)

    if linhas_removidas > 0:
        relatorio_saneamento.append(f"{linhas_removidas} linha(s) totalmente vazia(s) removida(s).")

    colunas_antes = df_saneado.shape[1]
    df_saneado = df_saneado.dropna(axis=1, how="all")
    colunas_removidas = colunas_antes - df_saneado.shape[1]

    if colunas_removidas > 0:
        relatorio_saneamento.append(f"{colunas_removidas} coluna(s) totalmente vazia(s) removida(s).")

    return df_saneado, relatorio_saneamento


def remover_cabecalhos_repetidos(df):
    relatorio_saneamento = []
    df_saneado = df.copy()

    colunas_normalizadas = [str(c).strip().upper() for c in df_saneado.columns]
    total_colunas = len(colunas_normalizadas)

    if total_colunas == 0 or len(df_saneado) == 0:
        return df_saneado, relatorio_saneamento

    def linha_parece_cabecalho(linha):
        valores = [str(v).strip().upper() for v in linha.values]
        iguais = sum(1 for valor, coluna in zip(valores, colunas_normalizadas) if coluna and valor == coluna)
        return iguais >= max(2, total_colunas // 2)

    mascara = df_saneado.apply(linha_parece_cabecalho, axis=1)
    linhas_removidas = int(mascara.sum())

    if linhas_removidas > 0:
        df_saneado = df_saneado[~mascara].reset_index(drop=True)
        relatorio_saneamento.append(f"{linhas_removidas} linha(s) de cabecalho repetido removida(s).")

    return df_saneado, relatorio_saneamento


def remover_linhas_total_subtotal(df, coluna_cliente):
    relatorio_saneamento = []
    df_saneado = df.copy()

    if not coluna_cliente or coluna_cliente not in df_saneado.columns:
        return df_saneado, relatorio_saneamento

    valores = df_saneado[coluna_cliente].astype(str).str.strip().str.upper().str.rstrip(":")
    mascara = valores.isin(TERMOS_TOTAL_SUBTOTAL)
    linhas_removidas = int(mascara.sum())

    if linhas_removidas > 0:
        df_saneado = df_saneado[~mascara].reset_index(drop=True)
        relatorio_saneamento.append(
            f"{linhas_removidas} linha(s) de total/subtotal removida(s) da coluna de cliente."
        )

    return df_saneado, relatorio_saneamento
