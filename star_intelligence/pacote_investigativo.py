from star_intelligence.investigacao import resumir_investigacao, gerar_leitura_investigacao


STATUS_INVESTIGATIVOS_VALIDOS = ("PENDENTE", "CONFIRMADA", "DESCARTADA", "INCONCLUSIVA")

MAPA_LEITURA_CONSOLIDADA = {
    "SEM INVESTIGACAO": "Pacote sem itens investigativos disponíveis.",
    "NAO INICIADA": "Pacote ainda sem investigação registrada.",
    "INICIAL": "Pacote com investigação inicial e evidências parciais.",
    "PARCIAL": "Pacote com investigação parcialmente consolidada.",
    "CONSOLIDADA COM PENDENCIAS": "Pacote consolidado, mas ainda dependente de leitura humana.",
    "CONSOLIDADA": "Pacote consolidado, mas ainda dependente de leitura humana.",
}


def obter_lista_segura(valor):
    try:
        if isinstance(valor, list):
            return valor

        if isinstance(valor, tuple):
            return list(valor)

        if valor is None:
            return []

        if isinstance(valor, str) and valor.strip() == "":
            return []

        return [valor]
    except Exception:
        return []


def contar_itens_por_status(itens):
    contagem = {status: 0 for status in STATUS_INVESTIGATIVOS_VALIDOS}

    for item in obter_lista_segura(itens):
        try:
            status = item.get("status") if isinstance(item, dict) else None
        except Exception:
            status = None

        if status not in STATUS_INVESTIGATIVOS_VALIDOS:
            status = "PENDENTE"

        contagem[status] += 1

    return contagem


def extrair_evidencias_registradas(itens):
    resultado = []

    for item in obter_lista_segura(itens):
        if not isinstance(item, dict):
            continue

        resposta = str(item.get("resposta", "") or "").strip()
        evidencia = str(item.get("evidencia", "") or "").strip()

        if resposta == "" and evidencia == "":
            continue

        resultado.append({
            "id_item": item.get("id_item", ""),
            "pergunta": item.get("pergunta", ""),
            "status": item.get("status", "PENDENTE"),
            "resposta": item.get("resposta", ""),
            "evidencia": item.get("evidencia", ""),
        })

    return resultado


def classificar_maturidade_investigacao(resumo_investigacao):
    resumo = resumo_investigacao or {}

    total_itens = resumo.get("total_itens", 0)
    percentual_respondido = resumo.get("percentual_respondido", 0.0)
    inconclusivas = resumo.get("inconclusivas", 0)

    if total_itens == 0:
        return "SEM INVESTIGACAO"

    if percentual_respondido == 0:
        return "NAO INICIADA"

    if 0 < percentual_respondido < 50:
        return "INICIAL"

    if 50 <= percentual_respondido < 100:
        return "PARCIAL"

    if percentual_respondido == 100 and inconclusivas > 0:
        return "CONSOLIDADA COM PENDENCIAS"

    if percentual_respondido == 100:
        return "CONSOLIDADA"

    return "INICIAL"


def gerar_leitura_consolidada_pacote(pacote):
    maturidade = (pacote or {}).get("maturidade_investigacao", "")

    return MAPA_LEITURA_CONSOLIDADA.get(maturidade, "Pacote sem itens investigativos disponíveis.")


def gerar_pacote_investigativo_cliente(raio_x=None, pacote_hipoteses=None, recomendacoes=None, pacote_investigacao=None):
    raio_x = raio_x or {}
    pacote_hipoteses = pacote_hipoteses or {}
    recomendacoes = recomendacoes or {}
    pacote_investigacao = pacote_investigacao or {}

    itens_investigativos = list(obter_lista_segura(pacote_investigacao.get("itens")))

    resumo_investigacao = pacote_investigacao.get("resumo")

    if not resumo_investigacao:
        resumo_investigacao = resumir_investigacao(pacote_investigacao)

    contagem_status_investigativo = contar_itens_por_status(itens_investigativos)
    evidencias_registradas = extrair_evidencias_registradas(itens_investigativos)
    maturidade_investigacao = classificar_maturidade_investigacao(resumo_investigacao)

    leitura_investigacao = pacote_investigacao.get("leitura_investigacao") or gerar_leitura_investigacao(
        pacote_investigacao
    )

    pacote = {
        "cliente": raio_x.get("cliente", ""),
        "vendedor": raio_x.get("vendedor", ""),
        "cidade": raio_x.get("cidade", ""),
        "curva": raio_x.get("curva", ""),
        "status_star": raio_x.get("status", ""),
        "nivel_prioridade": raio_x.get("nivel_prioridade", ""),
        "tipo_prioridade": raio_x.get("tipo_prioridade", ""),
        "leitura_operacional": raio_x.get("leitura_operacional", ""),
        "resumo_hipotese": pacote_hipoteses.get("resumo_hipotese", ""),
        "hipoteses_status": list(obter_lista_segura(pacote_hipoteses.get("hipoteses_status"))),
        "hipoteses_sinais": list(obter_lista_segura(pacote_hipoteses.get("hipoteses_sinais"))),
        "perguntas_validacao": list(obter_lista_segura(pacote_hipoteses.get("perguntas_validacao"))),
        "recomendacoes": dict(recomendacoes) if isinstance(recomendacoes, dict) else {},
        "itens_investigativos": itens_investigativos,
        "resumo_investigacao": dict(resumo_investigacao) if isinstance(resumo_investigacao, dict) else {},
        "contagem_status_investigativo": contagem_status_investigativo,
        "evidencias_registradas": evidencias_registradas,
        "maturidade_investigacao": maturidade_investigacao,
        "leitura_investigacao": leitura_investigacao,
    }

    pacote["leitura_consolidada"] = gerar_leitura_consolidada_pacote(pacote)

    return pacote


def formatar_pacote_investigativo_texto(pacote):
    pacote = pacote or {}

    return [
        f"Cliente: {pacote.get('cliente', '')}",
        f"Vendedor: {pacote.get('vendedor', '')}",
        f"Cidade: {pacote.get('cidade', '')}",
        f"Curva: {pacote.get('curva', '')}",
        f"Status STAR: {pacote.get('status_star', '')}",
        f"Nível de prioridade: {pacote.get('nivel_prioridade', '')}",
        f"Resumo da hipótese: {pacote.get('resumo_hipotese', '')}",
        f"Itens investigativos: {len(pacote.get('itens_investigativos') or [])}",
        f"Maturidade da investigação: {pacote.get('maturidade_investigacao', '')}",
        f"Leitura consolidada: {pacote.get('leitura_consolidada', '')}",
    ]


def gerar_tabela_evidencias(pacote):
    pacote = pacote or {}
    evidencias = pacote.get("evidencias_registradas") or []

    tabela = []

    for item in evidencias:
        tabela.append({
            "ID": item.get("id_item", ""),
            "Pergunta": item.get("pergunta", ""),
            "Status": item.get("status", ""),
            "Resposta": item.get("resposta", ""),
            "Evidência": item.get("evidencia", ""),
        })

    return tabela
