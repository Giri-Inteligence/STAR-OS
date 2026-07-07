import unicodedata

from star_intelligence.priorizacao import obter_valor_numerico, obter_texto


HIPOTESES_POR_STATUS = {
    "INATIVO": [
        "Possível interrupção completa da compra.",
        "Possível substituição por concorrente.",
        "Possível perda de relacionamento comercial.",
        "Possível mudança de necessidade, operação ou demanda do cliente.",
        "Possível cliente cadastrado, mas sem ativação comercial recente.",
    ],
    "QUEDA ACENTUADA": [
        "Possível perda relevante de volume.",
        "Possível perda de frequência de compra.",
        "Possível redução de mix.",
        "Possível entrada de concorrente.",
        "Possível problema de atendimento, preço, entrega ou relacionamento.",
    ],
    "QUEDA": [
        "Possível deterioração gradual da carteira.",
        "Possível espaçamento de compras.",
        "Possível redução parcial de volume ou mix.",
        "Possível queda de demanda do cliente.",
        "Possível perda de atenção comercial sobre a conta.",
    ],
    "ESTAVEL": [
        "Possível manutenção do padrão histórico de compra.",
        "Possível carteira sem variação relevante no curto prazo.",
        "Possível estabilidade aparente que ainda exige leitura de erosão e recência.",
    ],
    "CRESCIMENTO": [
        "Possível aumento de volume ou frequência.",
        "Possível expansão de mix.",
        "Possível maior aderência comercial recente.",
        "Possível oportunidade de preservar o crescimento sem assumir estabilidade definitiva.",
    ],
    "CRESCIMENTO ACENTUADO": [
        "Possível crescimento relevante no curto prazo.",
        "Possível evento pontual de compra acima do padrão.",
        "Possível expansão de relacionamento comercial.",
        "Possível oportunidade de investigar se o crescimento é recorrente ou episódico.",
    ],
}

PERGUNTAS_INATIVO = [
    "O cliente ainda está ativo e comprando nesta categoria?",
    "Quando foi o último contato comercial relevante com este cliente?",
    "Existe informação de compra com concorrente?",
    "Houve problema de atendimento, entrega, preço ou relacionamento?",
    "O cliente deixou de comprar por perda de demanda ou por perda comercial?",
]

PERGUNTAS_QUEDA = [
    "A queda ocorreu por volume, frequência ou mix?",
    "O cliente reduziu a compra em todos os itens ou apenas em algumas categorias?",
    "Houve mudança de decisor, comprador ou operação?",
    "Existe concorrente atuando neste cliente?",
    "O vendedor manteve cadência recente de contato?",
]

PERGUNTAS_ESTAVEL_EROSAO = [
    "A estabilidade é real ou esconde perda de mix?",
    "O cliente mantém frequência e volume consistentes?",
    "Existe concentração em poucos produtos?",
    "Há sinais de queda em itens estratégicos?",
]

PERGUNTAS_CRESCIMENTO = [
    "O crescimento é recorrente ou pontual?",
    "O crescimento veio de aumento de volume, frequência ou mix?",
    "Existe oportunidade de consolidar o novo patamar?",
    "O cliente aumentou compra por demanda real ou evento específico?",
]

PERGUNTAS_GERAIS = [
    "Qual evidência confirma ou refuta esta hipótese?",
    "O que o vendedor sabe que ainda não aparece nos dados?",
    "Qual foi a última interação comercial registrada?",
]


def normalizar_status(status):
    if status is None:
        return ""

    if isinstance(status, float) and status != status:
        return ""

    texto = " ".join(str(status).strip().upper().split())

    if texto == "":
        return ""

    texto_decomposto = unicodedata.normalize("NFKD", texto)

    return "".join(c for c in texto_decomposto if not unicodedata.combining(c))


def _remover_duplicatas(itens):
    vistos = set()
    resultado = []

    for item in itens:
        if item not in vistos:
            resultado.append(item)
            vistos.add(item)

    return resultado


def gerar_hipoteses_por_status(row):
    status = normalizar_status(obter_texto(row, "STATUS"))

    return list(
        HIPOTESES_POR_STATUS.get(status, ["Status não reconhecido para hipótese operacional específica."])
    )


def gerar_hipoteses_por_sinais(row):
    hipoteses = []

    curva = normalizar_status(obter_texto(row, "CURVA"))
    status = normalizar_status(obter_texto(row, "STATUS"))

    if curva == "A" and status in ("QUEDA", "QUEDA ACENTUADA"):
        hipoteses.append("Por ser curva A, a queda pode representar risco relevante de receita.")

    meses_sem_compra = obter_valor_numerico(row, "MESES_SEM_COMPRA", 0.0)

    if meses_sem_compra >= 6:
        hipoteses.append(
            "Longo período sem compra pode indicar ruptura de relacionamento, perda de demanda "
            "ou substituição por fornecedor."
        )
    elif 3 <= meses_sem_compra < 6:
        hipoteses.append("Período intermediário sem compra pode indicar risco de afastamento comercial.")

    erosao = obter_valor_numerico(row, "EROSAO STAR", 0.0)

    if erosao >= 7:
        hipoteses.append("Erosão elevada pode indicar deterioração forte da relação comercial.")
    elif 5 <= erosao < 7:
        hipoteses.append("Erosão moderada pode indicar deterioração silenciosa.")

    media_lp = obter_valor_numerico(row, "MEDIA LP", 0.0)
    media_cp = obter_valor_numerico(row, "MEDIA CP", 0.0)

    if media_lp > 0 and media_cp <= 0:
        hipoteses.append("Curto prazo zerado com histórico anterior pode indicar interrupção recente de compra.")
    elif media_lp > 0 and media_cp < media_lp * 0.5:
        hipoteses.append(
            "Média de curto prazo muito abaixo da média de longo prazo pode indicar perda de volume ou frequência."
        )

    nivel_prioridade = normalizar_status(obter_texto(row, "NIVEL_PRIORIDADE"))

    if nivel_prioridade == "P1 CRITICA":
        hipoteses.append("Prioridade crítica reforça a necessidade de investigação no ritual comercial.")

    tipo_prioridade = normalizar_status(obter_texto(row, "TIPO_PRIORIDADE"))

    if tipo_prioridade == "REATIVACAO":
        hipoteses.append("A natureza da prioridade sugere hipótese de reativação.")
    elif tipo_prioridade == "PRESERVACAO":
        hipoteses.append("A natureza da prioridade sugere hipótese de preservação de receita.")

    return _remover_duplicatas(hipoteses)


def gerar_perguntas_validacao(row):
    status = normalizar_status(obter_texto(row, "STATUS"))
    erosao = obter_valor_numerico(row, "EROSAO STAR", 0.0)

    perguntas = []

    if status == "INATIVO":
        perguntas.extend(PERGUNTAS_INATIVO)
    elif status in ("QUEDA", "QUEDA ACENTUADA"):
        perguntas.extend(PERGUNTAS_QUEDA)
    elif status == "ESTAVEL" and erosao >= 5:
        perguntas.extend(PERGUNTAS_ESTAVEL_EROSAO)
    elif status in ("CRESCIMENTO", "CRESCIMENTO ACENTUADO"):
        perguntas.extend(PERGUNTAS_CRESCIMENTO)

    perguntas.extend(PERGUNTAS_GERAIS)

    return _remover_duplicatas(perguntas)


def gerar_alertas_investigacao(row):
    alertas = []

    curva = normalizar_status(obter_texto(row, "CURVA"))
    status = normalizar_status(obter_texto(row, "STATUS"))

    if curva == "A" and status in ("QUEDA", "QUEDA ACENTUADA"):
        alertas.append("Cliente curva A com queda exige atenção na governança comercial.")

    if status == "INATIVO":
        alertas.append("Cliente inativo com histórico anterior não deve desaparecer da carteira.")

    erosao = obter_valor_numerico(row, "EROSAO STAR", 0.0)

    if erosao >= 7:
        alertas.append("Erosão elevada exige validação de causa antes de recomendação.")

    if status == "CRESCIMENTO ACENTUADO":
        alertas.append("Crescimento acentuado pode ser pontual e deve ser interpretado com cautela.")

    return _remover_duplicatas(alertas)


def gerar_hipoteses_cliente(row):
    status = normalizar_status(obter_texto(row, "STATUS"))
    erosao = obter_valor_numerico(row, "EROSAO STAR", 0.0)

    if status == "INATIVO":
        resumo = "Cliente com hipóteses de reativação a validar."
    elif status in ("QUEDA", "QUEDA ACENTUADA"):
        resumo = "Cliente com hipóteses de preservação de receita a investigar."
    elif status == "ESTAVEL" and erosao >= 5:
        resumo = "Cliente com estabilidade aparente e sinais que exigem leitura complementar."
    elif status in ("CRESCIMENTO", "CRESCIMENTO ACENTUADO"):
        resumo = "Cliente em crescimento que exige validação de recorrência."
    else:
        resumo = "Cliente em monitoramento sem hipótese crítica inicial."

    return {
        "hipoteses_status": _remover_duplicatas(gerar_hipoteses_por_status(row)),
        "hipoteses_sinais": _remover_duplicatas(gerar_hipoteses_por_sinais(row)),
        "perguntas_validacao": _remover_duplicatas(gerar_perguntas_validacao(row)),
        "alertas_investigacao": _remover_duplicatas(gerar_alertas_investigacao(row)),
        "resumo_hipotese": resumo,
    }


def formatar_hipoteses_texto(pacote):
    linhas = [f"Resumo: {pacote.get('resumo_hipotese', '')}"]

    for hipotese in pacote.get("hipoteses_status", []):
        linhas.append(f"Hipótese por status: {hipotese}")

    for hipotese in pacote.get("hipoteses_sinais", []):
        linhas.append(f"Hipótese por sinais: {hipotese}")

    for pergunta in pacote.get("perguntas_validacao", []):
        linhas.append(f"Pergunta de validação: {pergunta}")

    for alerta in pacote.get("alertas_investigacao", []):
        linhas.append(f"Alerta: {alerta}")

    return linhas
