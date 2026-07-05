from star_intelligence.priorizacao import obter_valor_numerico, obter_texto


def _normalizar(texto):
    return str(texto).strip().upper()


def calcular_variacao_media(media_lp, media_cp):
    try:
        media_lp = float(media_lp)
        media_cp = float(media_cp)
    except (TypeError, ValueError):
        return None

    if media_lp <= 0:
        return None

    return round(((media_cp - media_lp) / media_lp) * 100, 2)


def classificar_sinal_variacao(media_lp, media_cp):
    try:
        media_lp = float(media_lp)
    except (TypeError, ValueError):
        media_lp = 0.0

    try:
        media_cp = float(media_cp)
    except (TypeError, ValueError):
        media_cp = 0.0

    if media_lp <= 0 and media_cp <= 0:
        return "SEM HISTORICO DE COMPRA"

    if media_lp <= 0 and media_cp > 0:
        return "COMPRA RECENTE SEM BASE HISTORICA"

    if media_cp <= 0 and media_lp > 0:
        return "CURTO PRAZO ZERADO"

    if media_cp < media_lp * 0.5:
        return "FORTE REDUCAO"

    if media_cp < media_lp * 0.8:
        return "REDUCAO"

    if media_cp <= media_lp * 1.2:
        return "ESTABILIDADE RELATIVA"

    if media_cp > media_lp * 1.2:
        return "CRESCIMENTO"

    return "NAO CLASSIFICADO"


def gerar_sinais_operacionais_cliente(row):
    sinais = []

    curva = _normalizar(obter_texto(row, "CURVA"))

    if curva == "A":
        sinais.append("Cliente de alta relevância na carteira.")

    status = _normalizar(obter_texto(row, "STATUS"))

    if status == "QUEDA ACENTUADA":
        sinais.append("Cliente em queda acentuada.")
    elif status == "QUEDA":
        sinais.append("Cliente em queda.")
    elif status == "INATIVO":
        sinais.append("Cliente inativo.")

    meses_sem_compra = obter_valor_numerico(row, "MESES_SEM_COMPRA", 0.0)

    if meses_sem_compra >= 1:
        sinais.append("Cliente com meses sem compra.")

    if meses_sem_compra >= 6:
        sinais.append("Cliente com longo período sem compra.")

    erosao = obter_valor_numerico(row, "EROSAO STAR", 0.0)

    if erosao >= 7:
        sinais.append("Erosão STAR elevada.")
    elif erosao >= 5:
        sinais.append("Erosão STAR moderada.")

    media_lp = obter_valor_numerico(row, "MEDIA LP", 0.0)
    media_cp = obter_valor_numerico(row, "MEDIA CP", 0.0)

    if media_lp > 0 and media_cp <= 0:
        sinais.append("Curto prazo zerado com histórico anterior.")
    elif media_lp > 0 and media_cp < media_lp:
        sinais.append("Curto prazo abaixo do longo prazo.")

    nivel_prioridade = _normalizar(obter_texto(row, "NIVEL_PRIORIDADE"))

    if nivel_prioridade == "P1 CRITICA":
        sinais.append("Cliente em prioridade crítica.")
    elif nivel_prioridade == "P2 ALTA":
        sinais.append("Cliente em prioridade alta.")

    return sinais


def gerar_leitura_operacional_cliente(row):
    status = _normalizar(obter_texto(row, "STATUS"))
    curva = _normalizar(obter_texto(row, "CURVA"))
    erosao = obter_valor_numerico(row, "EROSAO STAR", 0.0)

    if status == "INATIVO":
        return "Cliente inativo que deve ser observado na rotina comercial."

    if status == "QUEDA ACENTUADA" and curva == "A":
        return "Cliente relevante com forte sinal de deterioração operacional."

    if status in ("QUEDA", "QUEDA ACENTUADA"):
        return "Cliente com sinal de queda e necessidade de atenção operacional."

    if status == "ESTAVEL" and erosao >= 5:
        return "Cliente aparentemente estável, mas com sinal de erosão a investigar."

    if status in ("CRESCIMENTO", "CRESCIMENTO ACENTUADO"):
        return "Cliente em crescimento, sem sinal crítico imediato."

    return "Cliente deve ser mantido em monitoramento."


def gerar_raio_x_cliente(row, cliente_col, vendedor_col=None, cidade_col=None):
    cliente = obter_texto(row, cliente_col)
    vendedor = obter_texto(row, vendedor_col) if vendedor_col else ""
    cidade = obter_texto(row, cidade_col) if cidade_col else ""

    curva = obter_texto(row, "CURVA")
    status = obter_texto(row, "STATUS")

    media_lp = obter_valor_numerico(row, "MEDIA LP", 0.0)
    media_cp = obter_valor_numerico(row, "MEDIA CP", 0.0)

    return {
        "cliente": cliente,
        "vendedor": vendedor,
        "cidade": cidade,
        "curva": curva,
        "status": status,
        "media_lp": media_lp,
        "media_cp": media_cp,
        "variacao_media_percentual": calcular_variacao_media(media_lp, media_cp),
        "sinal_variacao": classificar_sinal_variacao(media_lp, media_cp),
        "meses_sem_compra": obter_valor_numerico(row, "MESES_SEM_COMPRA", 0.0),
        "erosao_star": obter_valor_numerico(row, "EROSAO STAR", 0.0),
        "meta": obter_valor_numerico(row, "META", 0.0),
        "acao_star": obter_texto(row, "ACAO"),
        "pontuacao_prioridade": obter_valor_numerico(row, "PONTUACAO_PRIORIDADE", 0.0),
        "nivel_prioridade": obter_texto(row, "NIVEL_PRIORIDADE"),
        "tipo_prioridade": obter_texto(row, "TIPO_PRIORIDADE"),
        "sinais_operacionais": gerar_sinais_operacionais_cliente(row),
        "leitura_operacional": gerar_leitura_operacional_cliente(row),
    }


def formatar_raio_x_texto(raio_x):
    linhas = [
        f"Cliente: {raio_x.get('cliente', '')}",
        f"Vendedor: {raio_x.get('vendedor', '')}",
        f"Cidade: {raio_x.get('cidade', '')}",
        f"Curva: {raio_x.get('curva', '')}",
        f"Status STAR: {raio_x.get('status', '')}",
        f"Média LP: {raio_x.get('media_lp', 0.0)}",
        f"Média CP: {raio_x.get('media_cp', 0.0)}",
    ]

    variacao = raio_x.get("variacao_media_percentual")
    linhas.append(
        f"Variação média: {variacao}%" if variacao is not None else "Variação média: sem base para cálculo"
    )

    linhas.append(f"Sinal de variação: {raio_x.get('sinal_variacao', '')}")
    linhas.append(f"Meses sem compra: {raio_x.get('meses_sem_compra', 0.0)}")
    linhas.append(f"Erosão STAR: {raio_x.get('erosao_star', 0.0)}")
    linhas.append(f"Nível de prioridade: {raio_x.get('nivel_prioridade', '')}")
    linhas.append(f"Tipo de prioridade: {raio_x.get('tipo_prioridade', '')}")
    linhas.append(f"Leitura operacional: {raio_x.get('leitura_operacional', '')}")

    return linhas
