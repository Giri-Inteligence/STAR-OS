import copy

from star_intelligence.hipoteses import normalizar_status as _normalizar_texto_base


MAPA_STATUS_INVESTIGACAO = {
    "PENDENTE": "PENDENTE",
    "CONFIRMADA": "CONFIRMADA",
    "CONFIRMADO": "CONFIRMADA",
    "DESCARTADA": "DESCARTADA",
    "DESCARTADO": "DESCARTADA",
    "INCONCLUSIVA": "INCONCLUSIVA",
    "INCONCLUSIVO": "INCONCLUSIVA",
}


def normalizar_status_investigacao(status):
    texto = _normalizar_texto_base(status)

    return MAPA_STATUS_INVESTIGACAO.get(texto, "PENDENTE")


def criar_item_investigacao(
    id_item,
    pergunta,
    origem="PERGUNTA_VALIDACAO",
    status="PENDENTE",
    resposta="",
    evidencia="",
):
    return {
        "id_item": str(id_item) if id_item is not None else "",
        "origem": str(origem) if origem is not None else "",
        "pergunta": str(pergunta) if pergunta is not None else "",
        "status": normalizar_status_investigacao(status),
        "resposta": str(resposta) if resposta is not None else "",
        "evidencia": str(evidencia) if evidencia is not None else "",
    }


def criar_itens_a_partir_perguntas(perguntas):
    itens = []
    vistos = set()
    contador = 0

    for pergunta in perguntas or []:
        texto_pergunta = str(pergunta).strip() if pergunta is not None else ""

        if texto_pergunta == "" or texto_pergunta in vistos:
            continue

        vistos.add(texto_pergunta)
        contador += 1

        itens.append(criar_item_investigacao(
            id_item=f"INV_{contador:03d}",
            pergunta=texto_pergunta,
            origem="PERGUNTA_VALIDACAO",
            status="PENDENTE",
            resposta="",
            evidencia="",
        ))

    return itens


def criar_pacote_investigacao(cliente="", vendedor="", cidade="", pacote_hipoteses=None):
    perguntas = []

    if pacote_hipoteses:
        perguntas = pacote_hipoteses.get("perguntas_validacao", []) or []

    itens = criar_itens_a_partir_perguntas(perguntas)

    pacote = {
        "cliente": str(cliente) if cliente is not None else "",
        "vendedor": str(vendedor) if vendedor is not None else "",
        "cidade": str(cidade) if cidade is not None else "",
        "itens": itens,
    }

    pacote["resumo"] = resumir_investigacao(pacote)

    return pacote


def atualizar_item_investigacao(pacote, id_item, status=None, resposta=None, evidencia=None):
    try:
        pacote_copia = copy.deepcopy(pacote) if isinstance(pacote, dict) else {
            "cliente": "", "vendedor": "", "cidade": "", "itens": [],
        }

        for item in pacote_copia.get("itens", []):
            if item.get("id_item") == id_item:
                if status is not None:
                    item["status"] = normalizar_status_investigacao(status)
                if resposta is not None:
                    item["resposta"] = str(resposta)
                if evidencia is not None:
                    item["evidencia"] = str(evidencia)
                break

        pacote_copia["resumo"] = resumir_investigacao(pacote_copia)

        return pacote_copia
    except Exception:
        return copy.deepcopy(pacote) if isinstance(pacote, dict) else {
            "cliente": "", "vendedor": "", "cidade": "", "itens": [], "resumo": {},
        }


def resumir_investigacao(pacote):
    itens = (pacote or {}).get("itens", []) or []

    total_itens = len(itens)
    pendentes = sum(1 for item in itens if item.get("status") == "PENDENTE")
    confirmadas = sum(1 for item in itens if item.get("status") == "CONFIRMADA")
    descartadas = sum(1 for item in itens if item.get("status") == "DESCARTADA")
    inconclusivas = sum(1 for item in itens if item.get("status") == "INCONCLUSIVA")

    respondidas = sum(
        1 for item in itens
        if str(item.get("resposta", "")).strip() != "" or item.get("status") != "PENDENTE"
    )

    percentual_respondido = round((respondidas / total_itens) * 100, 2) if total_itens > 0 else 0.0

    if total_itens == 0:
        status_geral = "SEM ITENS DE INVESTIGACAO"
    elif pendentes == total_itens:
        status_geral = "NAO INICIADA"
    elif pendentes > 0 and respondidas > 0:
        status_geral = "EM ANDAMENTO"
    elif pendentes == 0 and inconclusivas > 0:
        status_geral = "CONCLUSAO PARCIAL"
    elif pendentes == 0:
        status_geral = "INVESTIGACAO REGISTRADA"
    else:
        status_geral = "EM ANDAMENTO"

    return {
        "total_itens": total_itens,
        "pendentes": pendentes,
        "confirmadas": confirmadas,
        "descartadas": descartadas,
        "inconclusivas": inconclusivas,
        "respondidas": respondidas,
        "percentual_respondido": percentual_respondido,
        "status_geral": status_geral,
    }


def gerar_leitura_investigacao(pacote):
    resumo = (pacote or {}).get("resumo") or resumir_investigacao(pacote)
    status_geral = resumo.get("status_geral", "")

    if status_geral == "SEM ITENS DE INVESTIGACAO":
        return "Não há itens de investigação para este cliente."

    if status_geral == "NAO INICIADA":
        return "Investigação ainda não iniciada."

    if status_geral == "EM ANDAMENTO":
        return "Investigação em andamento com respostas parciais."

    return "Investigação registrada, mas ainda exige leitura humana."


def formatar_resumo_investigacao(resumo):
    return [
        f"Itens de investigação: {resumo.get('total_itens', 0)}",
        f"Pendentes: {resumo.get('pendentes', 0)}",
        f"Confirmadas: {resumo.get('confirmadas', 0)}",
        f"Descartadas: {resumo.get('descartadas', 0)}",
        f"Inconclusivas: {resumo.get('inconclusivas', 0)}",
        f"Percentual respondido: {resumo.get('percentual_respondido', 0.0)}%",
        f"Status geral: {resumo.get('status_geral', '')}",
    ]
