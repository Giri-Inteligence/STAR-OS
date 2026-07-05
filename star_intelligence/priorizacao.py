PONTOS_CURVA = {"A": 30, "B": 20, "C": 10}

PONTOS_STATUS = {
    "QUEDA ACENTUADA": 40,
    "QUEDA": 30,
    "INATIVO": 35,
    "ESTAVEL": 10,
    "CRESCIMENTO": 5,
    "CRESCIMENTO ACENTUADO": 0,
}

ORDEM_CURVA = {"A": 0, "B": 1, "C": 2}


def obter_valor_numerico(row, coluna, padrao=0.0):
    try:
        if coluna not in row.index:
            return padrao

        valor = row[coluna]

        if valor is None:
            return padrao

        if isinstance(valor, float) and valor != valor:
            return padrao

        texto = str(valor).strip()

        if texto == "":
            return padrao

        return float(valor)
    except Exception:
        return padrao


def obter_texto(row, coluna, padrao=""):
    try:
        if coluna not in row.index:
            return padrao

        valor = row[coluna]

        if valor is None:
            return padrao

        if isinstance(valor, float) and valor != valor:
            return padrao

        texto = str(valor).strip()

        return texto if texto != "" else padrao
    except Exception:
        return padrao


def _normalizar_rotulo(texto):
    return str(texto).strip().upper()


def calcular_pontuacao_prioridade(row):
    pontuacao = 0.0

    curva = _normalizar_rotulo(obter_texto(row, "CURVA"))
    pontuacao += PONTOS_CURVA.get(curva, 0)

    status = _normalizar_rotulo(obter_texto(row, "STATUS"))
    pontuacao += PONTOS_STATUS.get(status, 0)

    meses_sem_compra = obter_valor_numerico(row, "MESES_SEM_COMPRA", 0.0)

    if meses_sem_compra >= 6:
        pontuacao += 25
    elif meses_sem_compra >= 3:
        pontuacao += 15
    elif meses_sem_compra >= 1:
        pontuacao += 5

    erosao = obter_valor_numerico(row, "EROSAO STAR", 0.0)

    if 0 <= erosao <= 10:
        pontuacao += erosao * 3
    elif erosao > 10:
        pontuacao += 30

    media_lp = obter_valor_numerico(row, "MEDIA LP", 0.0)
    media_cp = obter_valor_numerico(row, "MEDIA CP", 0.0)

    if media_lp > 0:
        if media_cp <= 0:
            pontuacao += 20
        elif media_cp < media_lp * 0.5:
            pontuacao += 15
        elif media_cp < media_lp * 0.8:
            pontuacao += 8

    return pontuacao


def classificar_nivel_prioridade(pontuacao):
    if pontuacao >= 90:
        return "P1 CRITICA"

    if pontuacao >= 70:
        return "P2 ALTA"

    if pontuacao >= 45:
        return "P3 MEDIA"

    return "P4 MONITORAMENTO"


def definir_tipo_prioridade(row):
    status = _normalizar_rotulo(obter_texto(row, "STATUS"))
    erosao = obter_valor_numerico(row, "EROSAO STAR", 0.0)

    if status == "INATIVO":
        return "REATIVACAO"

    if status in ("QUEDA ACENTUADA", "QUEDA"):
        return "PRESERVACAO"

    if status == "ESTAVEL" and erosao >= 5:
        return "INVESTIGACAO"

    if status in ("CRESCIMENTO", "CRESCIMENTO ACENTUADO"):
        return "EXPANSAO CONTROLADA"

    return "MONITORAMENTO"


def gerar_motivos_prioridade(row):
    motivos = []

    curva = _normalizar_rotulo(obter_texto(row, "CURVA"))

    if curva == "A":
        motivos.append("Cliente curva A.")

    status = _normalizar_rotulo(obter_texto(row, "STATUS"))

    if status == "QUEDA ACENTUADA":
        motivos.append("Status em queda acentuada.")
    elif status == "QUEDA":
        motivos.append("Status em queda.")
    elif status == "INATIVO":
        motivos.append("Cliente inativo.")

    meses_sem_compra = obter_valor_numerico(row, "MESES_SEM_COMPRA", 0.0)

    if meses_sem_compra >= 3:
        motivos.append("Alta quantidade de meses sem compra.")

    erosao = obter_valor_numerico(row, "EROSAO STAR", 0.0)

    if erosao >= 5:
        motivos.append("Erosão STAR elevada.")

    media_lp = obter_valor_numerico(row, "MEDIA LP", 0.0)
    media_cp = obter_valor_numerico(row, "MEDIA CP", 0.0)

    if media_lp > 0 and media_cp < media_lp:
        motivos.append("Média de curto prazo abaixo da média de longo prazo.")

    return motivos


def gerar_fila_prioridade(df_star):
    df_prioridade = df_star.copy()

    df_prioridade["PONTUACAO_PRIORIDADE"] = df_prioridade.apply(calcular_pontuacao_prioridade, axis=1)
    df_prioridade["NIVEL_PRIORIDADE"] = df_prioridade["PONTUACAO_PRIORIDADE"].apply(classificar_nivel_prioridade)
    df_prioridade["TIPO_PRIORIDADE"] = df_prioridade.apply(definir_tipo_prioridade, axis=1)
    df_prioridade["MOTIVOS_PRIORIDADE"] = df_prioridade.apply(gerar_motivos_prioridade, axis=1)

    if "CURVA" in df_prioridade.columns:
        chave_curva = df_prioridade["CURVA"].apply(lambda v: ORDEM_CURVA.get(_normalizar_rotulo(v), 3))
    else:
        chave_curva = 3

    df_prioridade["_ORDEM_CURVA_TEMP"] = chave_curva

    colunas_ordenacao = ["PONTUACAO_PRIORIDADE", "_ORDEM_CURVA_TEMP"]
    ascendente = [False, True]

    if "EROSAO STAR" in df_prioridade.columns:
        colunas_ordenacao.append("EROSAO STAR")
        ascendente.append(False)

    if "MESES_SEM_COMPRA" in df_prioridade.columns:
        colunas_ordenacao.append("MESES_SEM_COMPRA")
        ascendente.append(False)

    df_prioridade = (
        df_prioridade
        .sort_values(by=colunas_ordenacao, ascending=ascendente)
        .drop(columns=["_ORDEM_CURVA_TEMP"])
        .reset_index(drop=True)
    )

    return df_prioridade


def resumir_fila_prioridade(df_prioridade):
    contagem = df_prioridade["NIVEL_PRIORIDADE"].value_counts()

    return {
        "total_clientes": len(df_prioridade),
        "p1_critica": int(contagem.get("P1 CRITICA", 0)),
        "p2_alta": int(contagem.get("P2 ALTA", 0)),
        "p3_media": int(contagem.get("P3 MEDIA", 0)),
        "p4_monitoramento": int(contagem.get("P4 MONITORAMENTO", 0)),
    }


def formatar_resumo_fila_prioridade(resumo):
    return [
        f"Clientes na fila de prioridade: {resumo.get('total_clientes', 0)}",
        f"P1 crítica: {resumo.get('p1_critica', 0)}",
        f"P2 alta: {resumo.get('p2_alta', 0)}",
        f"P3 média: {resumo.get('p3_media', 0)}",
        f"P4 monitoramento: {resumo.get('p4_monitoramento', 0)}",
    ]
