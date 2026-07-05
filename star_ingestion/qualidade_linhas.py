import unicodedata

import pandas as pd


TERMOS_RESIDUAIS_EXATOS = {
    "",
    "-", "—", "–",
    "NAN", "NONE", "NULL",
    "NAO INFORMADO", "SEM CLIENTE",
    "CLIENTE", "NOME DO CLIENTE", "RAZAO SOCIAL", "EMPRESA", "CONTA",
    "TOTAL", "TOTAL GERAL", "SUBTOTAL", "SOMA",
}


def normalizar_texto_linha(valor):
    if valor is None:
        return ""

    if isinstance(valor, float) and valor != valor:
        return ""

    texto = " ".join(str(valor).strip().upper().split())

    if texto == "":
        return ""

    texto_decomposto = unicodedata.normalize("NFKD", texto)

    return "".join(c for c in texto_decomposto if not unicodedata.combining(c))


def cliente_residual_obvio(valor_cliente):
    texto = normalizar_texto_linha(valor_cliente)

    return texto in TERMOS_RESIDUAIS_EXATOS


def linha_tem_venda(row, meses_col):
    for coluna in meses_col or []:
        if coluna not in row.index:
            continue

        try:
            valor = float(row[coluna])
        except (TypeError, ValueError):
            continue

        if valor > 0:
            return True

    return False


def classificar_linhas_base(df, cliente_col, vendedor_col, meses_col):
    df_trabalho = df.copy()
    meses_col = meses_col or []

    mensagens = []
    avisos = []
    removidas = []

    linhas_entrada = len(df_trabalho)

    if cliente_col and cliente_col in df_trabalho.columns:
        mascara_residual = df_trabalho[cliente_col].apply(cliente_residual_obvio)
    else:
        mascara_residual = pd.Series([False] * linhas_entrada, index=df_trabalho.index)

    for indice, linha in df_trabalho[mascara_residual].iterrows():
        valor_cliente = linha[cliente_col] if cliente_col in df_trabalho.columns else None
        removidas.append({
            "indice": indice,
            "cliente": valor_cliente,
            "motivo": "identidade de cliente residual ou invalida",
        })

    linhas_removidas = int(mascara_residual.sum())
    df_filtrado = df_trabalho[~mascara_residual].reset_index(drop=True)

    if linhas_removidas > 0:
        mensagens.append(
            f"{linhas_removidas} linha(s) removida(s) por identidade de cliente residual ou invalida."
        )

    clientes_zerados_preservados = 0
    clientes_com_venda_parcial_preservados = 0
    linhas_cliente_sem_vendedor = 0
    linhas_sem_venda = 0

    for _, linha in df_filtrado.iterrows():
        if linha_tem_venda(linha, meses_col):
            clientes_com_venda_parcial_preservados += 1
        else:
            clientes_zerados_preservados += 1
            linhas_sem_venda += 1

        if vendedor_col and vendedor_col in df_filtrado.columns:
            if normalizar_texto_linha(linha[vendedor_col]) == "":
                linhas_cliente_sem_vendedor += 1

    if linhas_cliente_sem_vendedor > 0:
        avisos.append(
            f"{linhas_cliente_sem_vendedor} linha(s) possui(em) cliente preenchido, mas vendedor ausente."
        )

    return {
        "df": df_filtrado,
        "mensagens": mensagens,
        "avisos": avisos,
        "removidas": removidas,
        "estatisticas": {
            "linhas_entrada": linhas_entrada,
            "linhas_saida": len(df_filtrado),
            "linhas_removidas": linhas_removidas,
            "clientes_zerados_preservados": clientes_zerados_preservados,
            "clientes_com_venda_parcial_preservados": clientes_com_venda_parcial_preservados,
            "linhas_cliente_sem_vendedor": linhas_cliente_sem_vendedor,
            "linhas_sem_venda": linhas_sem_venda,
        },
    }


def formatar_resumo_qualidade_linhas(resultado):
    estatisticas = resultado.get("estatisticas", {})
    linhas = []

    linhas.append(f"Linhas analisadas: {estatisticas.get('linhas_entrada', 0)}")
    linhas.append(f"Linhas removidas como resíduo: {estatisticas.get('linhas_removidas', 0)}")
    linhas.append(f"Clientes zerados preservados: {estatisticas.get('clientes_zerados_preservados', 0)}")
    linhas.append(
        f"Clientes com venda parcial preservados: {estatisticas.get('clientes_com_venda_parcial_preservados', 0)}"
    )

    linhas_sem_vendedor = estatisticas.get("linhas_cliente_sem_vendedor", 0)

    if linhas_sem_vendedor > 0:
        linhas.append(
            f"Aviso: {linhas_sem_vendedor} linha(s) possui(em) cliente preenchido, mas vendedor ausente."
        )

    return linhas
