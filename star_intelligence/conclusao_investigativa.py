from star_intelligence.hipoteses import normalizar_status as _normalizar_texto_base
from star_intelligence.investigacao import normalizar_status_investigacao
from star_intelligence.pacote_investigativo import obter_lista_segura


MAPA_CLASSIFICACAO_CONCLUSIVA = {
    "CONFIRMADO": "HIPOTESE CONFIRMADA",
    "CONFIRMADA": "HIPOTESE CONFIRMADA",
    "DESCARTADO": "HIPOTESE DESCARTADA",
    "DESCARTADA": "HIPOTESE DESCARTADA",
    "INCONCLUSIVO": "HIPOTESE INCONCLUSIVA",
    "INCONCLUSIVA": "HIPOTESE INCONCLUSIVA",
    "PENDENTE": "PENDENTE DE VALIDACAO",
    "RESPOSTA SEM CLASSIFICACAO": "RESPOSTA SEM CLASSIFICACAO",
}

LEITURAS_POR_CLASSIFICACAO = {
    "HIPOTESE CONFIRMADA": "Item investigativo marcado como confirmado.",
    "HIPOTESE DESCARTADA": "Item investigativo marcado como descartado.",
    "HIPOTESE INCONCLUSIVA": "Item investigativo ainda inconclusivo.",
    "PENDENTE DE VALIDACAO": "Item ainda pendente de validação.",
    "RESPOSTA SEM CLASSIFICACAO": "Item possui resposta ou evidência, mas ainda sem classificação conclusiva.",
}

MAPA_LEITURA_CONCLUSAO = {
    "SEM ITENS INVESTIGATIVOS": "Ainda não há itens investigativos para classificar.",
    "SEM VALIDACAO INICIADA": "A validação ainda não foi iniciada.",
    "RESPOSTAS SEM CLASSIFICACAO": "Existem respostas registradas sem classificação conclusiva.",
    "CLASSIFICACAO PARCIAL": "A classificação investigativa está parcial.",
    "CLASSIFICACAO CONCLUIDA COM INCONCLUSIVOS": "A classificação foi concluída, mas existem itens inconclusivos.",
    "CLASSIFICACAO CONCLUIDA": "A classificação investigativa foi registrada, mas ainda depende de interpretação humana.",
    "CLASSIFICACAO EM ANDAMENTO": "A classificação investigativa foi registrada, mas ainda depende de interpretação humana.",
}


def normalizar_classificacao_conclusiva(valor):
    texto = _normalizar_texto_base(valor)

    return MAPA_CLASSIFICACAO_CONCLUSIVA.get(texto, "PENDENTE DE VALIDACAO")


def classificar_item_investigativo(item):
    item = item or {}

    resposta = str(item.get("resposta", "") or "")
    evidencia = str(item.get("evidencia", "") or "")
    status_investigativo = normalizar_status_investigacao(item.get("status"))

    tem_resposta = resposta.strip() != ""
    tem_evidencia = evidencia.strip() != ""

    if status_investigativo == "CONFIRMADA":
        classificacao = "HIPOTESE CONFIRMADA"
    elif status_investigativo == "DESCARTADA":
        classificacao = "HIPOTESE DESCARTADA"
    elif status_investigativo == "INCONCLUSIVA":
        classificacao = "HIPOTESE INCONCLUSIVA"
    elif tem_resposta or tem_evidencia:
        classificacao = "RESPOSTA SEM CLASSIFICACAO"
    else:
        classificacao = "PENDENTE DE VALIDACAO"

    return {
        "id_item": item.get("id_item", ""),
        "pergunta": item.get("pergunta", ""),
        "status_investigativo": status_investigativo,
        "resposta": resposta,
        "evidencia": evidencia,
        "classificacao_conclusiva": classificacao,
        "tem_resposta": tem_resposta,
        "tem_evidencia": tem_evidencia,
        "leitura_item": LEITURAS_POR_CLASSIFICACAO.get(classificacao, ""),
    }


def classificar_itens_investigativos(itens):
    resultado = []

    for item in obter_lista_segura(itens):
        if not isinstance(item, dict):
            continue

        resultado.append(classificar_item_investigativo(item))

    return resultado


def resumir_conclusao_investigativa(classificacoes):
    classificacoes = obter_lista_segura(classificacoes)

    total_itens = len(classificacoes)
    hipoteses_confirmadas = sum(
        1 for c in classificacoes if c.get("classificacao_conclusiva") == "HIPOTESE CONFIRMADA"
    )
    hipoteses_descartadas = sum(
        1 for c in classificacoes if c.get("classificacao_conclusiva") == "HIPOTESE DESCARTADA"
    )
    hipoteses_inconclusivas = sum(
        1 for c in classificacoes if c.get("classificacao_conclusiva") == "HIPOTESE INCONCLUSIVA"
    )
    pendentes_validacao = sum(
        1 for c in classificacoes if c.get("classificacao_conclusiva") == "PENDENTE DE VALIDACAO"
    )
    respostas_sem_classificacao = sum(
        1 for c in classificacoes if c.get("classificacao_conclusiva") == "RESPOSTA SEM CLASSIFICACAO"
    )
    itens_com_resposta = sum(1 for c in classificacoes if c.get("tem_resposta"))
    itens_com_evidencia = sum(1 for c in classificacoes if c.get("tem_evidencia"))

    classificados = hipoteses_confirmadas + hipoteses_descartadas + hipoteses_inconclusivas
    percentual_classificado = round((classificados / total_itens) * 100, 2) if total_itens > 0 else 0.0

    if total_itens == 0:
        status_geral = "SEM ITENS INVESTIGATIVOS"
    elif (
        hipoteses_confirmadas == 0
        and hipoteses_descartadas == 0
        and hipoteses_inconclusivas == 0
        and pendentes_validacao == total_itens
    ):
        status_geral = "SEM VALIDACAO INICIADA"
    elif respostas_sem_classificacao > 0 and percentual_classificado == 0:
        status_geral = "RESPOSTAS SEM CLASSIFICACAO"
    elif 0 < percentual_classificado < 100:
        status_geral = "CLASSIFICACAO PARCIAL"
    elif percentual_classificado == 100 and hipoteses_inconclusivas > 0:
        status_geral = "CLASSIFICACAO CONCLUIDA COM INCONCLUSIVOS"
    elif percentual_classificado == 100:
        status_geral = "CLASSIFICACAO CONCLUIDA"
    else:
        status_geral = "CLASSIFICACAO EM ANDAMENTO"

    return {
        "total_itens": total_itens,
        "hipoteses_confirmadas": hipoteses_confirmadas,
        "hipoteses_descartadas": hipoteses_descartadas,
        "hipoteses_inconclusivas": hipoteses_inconclusivas,
        "pendentes_validacao": pendentes_validacao,
        "respostas_sem_classificacao": respostas_sem_classificacao,
        "itens_com_resposta": itens_com_resposta,
        "itens_com_evidencia": itens_com_evidencia,
        "percentual_classificado": percentual_classificado,
        "status_conclusivo_geral": status_geral,
    }


def gerar_leitura_conclusao_investigativa(resumo):
    status_geral = (resumo or {}).get("status_conclusivo_geral", "")

    return MAPA_LEITURA_CONCLUSAO.get(
        status_geral,
        "A classificação investigativa foi registrada, mas ainda depende de interpretação humana.",
    )


def gerar_conclusao_investigativa(pacote_investigativo=None):
    pacote_investigativo = pacote_investigativo or {}

    itens = obter_lista_segura(pacote_investigativo.get("itens_investigativos"))
    classificacoes = classificar_itens_investigativos(itens)
    resumo_conclusao = resumir_conclusao_investigativa(classificacoes)
    leitura_conclusao = gerar_leitura_conclusao_investigativa(resumo_conclusao)

    return {
        "cliente": pacote_investigativo.get("cliente", ""),
        "status_star": pacote_investigativo.get("status_star", ""),
        "nivel_prioridade": pacote_investigativo.get("nivel_prioridade", ""),
        "tipo_prioridade": pacote_investigativo.get("tipo_prioridade", ""),
        "classificacoes": classificacoes,
        "resumo_conclusao": resumo_conclusao,
        "leitura_conclusao": leitura_conclusao,
        "hipoteses_confirmadas": [
            c for c in classificacoes if c.get("classificacao_conclusiva") == "HIPOTESE CONFIRMADA"
        ],
        "hipoteses_descartadas": [
            c for c in classificacoes if c.get("classificacao_conclusiva") == "HIPOTESE DESCARTADA"
        ],
        "hipoteses_inconclusivas": [
            c for c in classificacoes if c.get("classificacao_conclusiva") == "HIPOTESE INCONCLUSIVA"
        ],
        "pendentes_validacao": [
            c for c in classificacoes if c.get("classificacao_conclusiva") == "PENDENTE DE VALIDACAO"
        ],
        "respostas_sem_classificacao": [
            c for c in classificacoes if c.get("classificacao_conclusiva") == "RESPOSTA SEM CLASSIFICACAO"
        ],
    }


def formatar_conclusao_investigativa_texto(conclusao):
    conclusao = conclusao or {}
    resumo = conclusao.get("resumo_conclusao") or {}

    return [
        f"Cliente: {conclusao.get('cliente', '')}",
        f"Status STAR: {conclusao.get('status_star', '')}",
        f"Nível de prioridade: {conclusao.get('nivel_prioridade', '')}",
        f"Hipóteses confirmadas: {resumo.get('hipoteses_confirmadas', 0)}",
        f"Hipóteses descartadas: {resumo.get('hipoteses_descartadas', 0)}",
        f"Hipóteses inconclusivas: {resumo.get('hipoteses_inconclusivas', 0)}",
        f"Pendentes de validação: {resumo.get('pendentes_validacao', 0)}",
        f"Respostas sem classificação: {resumo.get('respostas_sem_classificacao', 0)}",
        f"Status conclusivo geral: {resumo.get('status_conclusivo_geral', '')}",
        f"Leitura conclusiva: {conclusao.get('leitura_conclusao', '')}",
    ]


def gerar_tabela_conclusao(conclusao):
    conclusao = conclusao or {}
    classificacoes = conclusao.get("classificacoes") or []

    tabela = []

    for item in classificacoes:
        tabela.append({
            "ID": item.get("id_item", ""),
            "Pergunta": item.get("pergunta", ""),
            "Status investigativo": item.get("status_investigativo", ""),
            "Classificação conclusiva": item.get("classificacao_conclusiva", ""),
            "Resposta": item.get("resposta", ""),
            "Evidência": item.get("evidencia", ""),
            "Leitura do item": item.get("leitura_item", ""),
        })

    return tabela
