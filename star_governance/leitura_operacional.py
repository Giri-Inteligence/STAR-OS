"""
star_governance.leitura_operacional

Camada determinística de leitura operacional de payloads de Governança
já consultados (registro de acompanhamento, snapshot de status, item de
loop, ciclo de loop e governança integrada). Gera uma interpretação
técnica, curta e não prescritiva — nunca recomenda ação, nunca cria
tarefa, agenda ou plano de ação. Não depende de Streamlit, sqlite3 ou
qualquer camada de persistência.
"""

TIPOS_PAYLOAD_LEITURA = (
    "REGISTRO_ACOMPANHAMENTO",
    "SNAPSHOT_STATUS",
    "ITEM_LOOP",
    "CICLO_LOOP",
    "GOVERNANCA_INTEGRADA",
)

CAMPOS_IDENTIFICADOR_POR_TIPO_LEITURA = {
    "REGISTRO_ACOMPANHAMENTO": "registro_id",
    "SNAPSHOT_STATUS": "snapshot_id",
    "ITEM_LOOP": "item_loop_id",
    "CICLO_LOOP": "ciclo_id",
    "GOVERNANCA_INTEGRADA": "governanca_id",
}

LEITURAS_CURTAS_POR_TIPO = {
    "REGISTRO_ACOMPANHAMENTO": "Registro de acompanhamento encontrado.",
    "SNAPSHOT_STATUS": "Snapshot de status encontrado.",
    "ITEM_LOOP": "Item de loop encontrado.",
    "CICLO_LOOP": "Ciclo de loop encontrado.",
    "GOVERNANCA_INTEGRADA": "Governança integrada encontrada.",
    "DESCONHECIDO": "Payload de governança não reconhecido.",
}

CAMINHOS_STATUS_LEITURA = (
    ("status_acompanhamento",),
    ("status_atual_acompanhamento",),
    ("dados_registro", "status_acompanhamento"),
    ("dados_registro_acompanhamento", "status_acompanhamento"),
    ("dados_snapshot", "status_atual_acompanhamento"),
    ("dados_snapshot_status", "status_atual"),
    ("snapshot_status", "status_atual_acompanhamento"),
    ("snapshot_status", "status_atual"),
    ("dados_item_loop", "status_atual_acompanhamento"),
    ("dados_item_loop", "status_acompanhamento"),
    ("item_loop", "status_atual_acompanhamento"),
    ("registro_acompanhamento", "status_acompanhamento"),
    ("dados_governanca_integrada", "status_atual"),
)

CAMINHOS_CLASSIFICACAO_LOOP_LEITURA = (
    ("classificacao_loop",),
    ("categoria_loop",),
    ("dados_item_loop", "classificacao_loop"),
    ("dados_item_loop", "categoria_loop"),
    ("dados_ciclo_loop", "classificacao_loop"),
    ("dados_ciclo_loop", "categoria_loop"),
    ("item_loop", "classificacao_loop"),
)


def obter_dict_seguro_leitura(valor):
    if isinstance(valor, dict):
        return dict(valor)

    return {}


def obter_lista_segura_leitura(valor):
    if isinstance(valor, list):
        return valor

    return []


def normalizar_tipo_payload_leitura(tipo):
    tipo_texto = str(tipo or "").strip().upper()

    if tipo_texto in TIPOS_PAYLOAD_LEITURA:
        return tipo_texto

    return "DESCONHECIDO"


def extrair_payload_de_linha_repositorio(item):
    item_seguro = obter_dict_seguro_leitura(item)

    payload_aninhado = item_seguro.get("payload")

    if isinstance(payload_aninhado, dict):
        return payload_aninhado

    if "tipo_payload_governanca" in item_seguro:
        return item_seguro

    return {}


def _buscar_valor_por_caminhos(payload, caminhos):
    for caminho in caminhos:
        valor_atual = payload

        for chave in caminho:
            valor_atual = obter_dict_seguro_leitura(valor_atual).get(chave) if isinstance(valor_atual, dict) else None

            if valor_atual is None:
                break

        if isinstance(valor_atual, str) and valor_atual:
            return valor_atual

    return ""


def extrair_identidade_leitura(payload):
    payload_seguro = obter_dict_seguro_leitura(payload)

    tipo = normalizar_tipo_payload_leitura(payload_seguro.get("tipo_payload_governanca", ""))
    campo_identificador = CAMPOS_IDENTIFICADOR_POR_TIPO_LEITURA.get(tipo)

    metadados = obter_dict_seguro_leitura(payload_seguro.get("metadados_persistencia"))

    return {
        "tipo_payload_governanca": tipo,
        "payload_id": str(payload_seguro.get(campo_identificador, "") or "") if campo_identificador else "",
        "cliente_id": str(payload_seguro.get("cliente_id", "") or ""),
        "sessao_id": str(payload_seguro.get("sessao_id", "") or ""),
        "nome_cliente": str(payload_seguro.get("nome_cliente", "") or ""),
        "origem": str(payload_seguro.get("origem", "") or metadados.get("origem", "") or ""),
        "criado_em": str(metadados.get("criado_em", "") or ""),
    }


def extrair_status_leitura(payload):
    payload_seguro = obter_dict_seguro_leitura(payload)

    return _buscar_valor_por_caminhos(payload_seguro, CAMINHOS_STATUS_LEITURA)


def extrair_classificacao_loop_leitura(payload):
    payload_seguro = obter_dict_seguro_leitura(payload)

    return _buscar_valor_por_caminhos(payload_seguro, CAMINHOS_CLASSIFICACAO_LOOP_LEITURA)


def criar_item_leitura_operacional(payload_ou_linha):
    payload = extrair_payload_de_linha_repositorio(payload_ou_linha)
    identidade = extrair_identidade_leitura(payload)

    status_acompanhamento = extrair_status_leitura(payload)
    classificacao_loop = extrair_classificacao_loop_leitura(payload)

    tipo = identidade["tipo_payload_governanca"]
    leitura_curta = LEITURAS_CURTAS_POR_TIPO.get(tipo, LEITURAS_CURTAS_POR_TIPO["DESCONHECIDO"])

    avisos = []

    if tipo == "DESCONHECIDO":
        avisos.append("Tipo de payload de governança não reconhecido.")

    if tipo == "CICLO_LOOP" and (not identidade["cliente_id"] or not identidade["sessao_id"]):
        avisos.append("Ciclo de loop sem identidade completa de cliente/sessão.")

    return {
        "tipo_payload_governanca": tipo,
        "payload_id": identidade["payload_id"],
        "cliente_id": identidade["cliente_id"],
        "sessao_id": identidade["sessao_id"],
        "nome_cliente": identidade["nome_cliente"],
        "origem": identidade["origem"],
        "criado_em": identidade["criado_em"],
        "status_acompanhamento": status_acompanhamento,
        "classificacao_loop": classificacao_loop,
        "leitura_curta": leitura_curta,
        "avisos": avisos,
    }


def gerar_resumo_quantitativo_leitura(itens_leitura):
    itens_seguros = [item for item in obter_lista_segura_leitura(itens_leitura) if isinstance(item, dict)]

    por_tipo = {}
    por_status = {}
    por_classificacao_loop = {}
    com_cliente_id = 0
    sem_cliente_id = 0
    com_sessao_id = 0
    sem_sessao_id = 0

    for item in itens_seguros:
        tipo = item.get("tipo_payload_governanca", "DESCONHECIDO")
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1

        status = item.get("status_acompanhamento", "")
        if status:
            por_status[status] = por_status.get(status, 0) + 1

        classificacao = item.get("classificacao_loop", "")
        if classificacao:
            por_classificacao_loop[classificacao] = por_classificacao_loop.get(classificacao, 0) + 1

        if item.get("cliente_id"):
            com_cliente_id += 1
        else:
            sem_cliente_id += 1

        if item.get("sessao_id"):
            com_sessao_id += 1
        else:
            sem_sessao_id += 1

    return {
        "total_payloads": len(itens_seguros),
        "por_tipo": por_tipo,
        "por_status": por_status,
        "por_classificacao_loop": por_classificacao_loop,
        "com_cliente_id": com_cliente_id,
        "sem_cliente_id": sem_cliente_id,
        "com_sessao_id": com_sessao_id,
        "sem_sessao_id": sem_sessao_id,
    }


def gerar_sintese_operacional_governanca(itens_leitura):
    itens_seguros = [item for item in obter_lista_segura_leitura(itens_leitura) if isinstance(item, dict)]

    tipos_presentes = {item.get("tipo_payload_governanca", "") for item in itens_seguros}

    itens_ciclo_loop = [item for item in itens_seguros if item.get("tipo_payload_governanca") == "CICLO_LOOP"]
    ciclo_loop_com_identidade = all(
        item.get("cliente_id") and item.get("sessao_id") for item in itens_ciclo_loop
    ) if itens_ciclo_loop else True

    consulta_completa_para_cliente_sessao = ciclo_loop_com_identidade

    status_identificados = sorted({item.get("status_acompanhamento", "") for item in itens_seguros if item.get("status_acompanhamento")})
    classificacoes_loop_identificadas = sorted(
        {item.get("classificacao_loop", "") for item in itens_seguros if item.get("classificacao_loop")}
    )

    avisos = []

    for item in itens_seguros:
        avisos.extend(item.get("avisos") or [])

    if not itens_seguros:
        leitura_sintetica = "Nenhuma governança salva foi encontrada para a consulta atual."
        avisos.append("Nenhum payload de governança informado.")
    elif not consulta_completa_para_cliente_sessao:
        leitura_sintetica = "Governança consultada, mas há payloads sem identidade completa de cliente/sessão."
    else:
        leitura_sintetica = "Governança consultada com payloads de acompanhamento e ciclo identificados."

    return {
        "tem_governanca": len(itens_seguros) > 0,
        "tem_registro_acompanhamento": "REGISTRO_ACOMPANHAMENTO" in tipos_presentes,
        "tem_snapshot_status": "SNAPSHOT_STATUS" in tipos_presentes,
        "tem_item_loop": "ITEM_LOOP" in tipos_presentes,
        "tem_ciclo_loop": "CICLO_LOOP" in tipos_presentes,
        "tem_governanca_integrada": "GOVERNANCA_INTEGRADA" in tipos_presentes,
        "ciclo_loop_com_identidade": ciclo_loop_com_identidade,
        "consulta_completa_para_cliente_sessao": consulta_completa_para_cliente_sessao,
        "status_identificados": status_identificados,
        "classificacoes_loop_identificadas": classificacoes_loop_identificadas,
        "leitura_sintetica": leitura_sintetica,
        "avisos": avisos,
    }


def gerar_leitura_operacional_governanca(payloads_ou_linhas=None):
    lista_segura = obter_lista_segura_leitura(payloads_ou_linhas)

    itens = [
        criar_item_leitura_operacional(entrada) for entrada in lista_segura if isinstance(entrada, dict)
    ]

    resumo_quantitativo = gerar_resumo_quantitativo_leitura(itens)
    sintese_operacional = gerar_sintese_operacional_governanca(itens)

    return {
        "valido": True,
        "total_payloads": len(itens),
        "itens": itens,
        "resumo_quantitativo": resumo_quantitativo,
        "sintese_operacional": sintese_operacional,
        "erros": [],
        "avisos": list(sintese_operacional.get("avisos") or []),
    }


def formatar_item_leitura_operacional_texto(item=None):
    item_seguro = obter_dict_seguro_leitura(item)

    return [
        f"Tipo: {item_seguro.get('tipo_payload_governanca', '')}",
        f"Payload ID: {item_seguro.get('payload_id', '')}",
        f"Cliente ID: {item_seguro.get('cliente_id', '')}",
        f"Sessão ID: {item_seguro.get('sessao_id', '')}",
        f"Leitura: {item_seguro.get('leitura_curta', '')}",
    ]


def formatar_leitura_operacional_governanca_texto(leitura=None):
    leitura_segura = obter_dict_seguro_leitura(leitura)
    sintese = obter_dict_seguro_leitura(leitura_segura.get("sintese_operacional"))

    linhas = [
        f"Total de payloads consultados: {leitura_segura.get('total_payloads', 0)}",
        f"Registro de acompanhamento: {'SIM' if sintese.get('tem_registro_acompanhamento') else 'NAO'}",
        f"Snapshot de status: {'SIM' if sintese.get('tem_snapshot_status') else 'NAO'}",
        f"Item de loop: {'SIM' if sintese.get('tem_item_loop') else 'NAO'}",
        f"Ciclo de loop: {'SIM' if sintese.get('tem_ciclo_loop') else 'NAO'}",
        f"Governança integrada: {'SIM' if sintese.get('tem_governanca_integrada') else 'NAO'}",
        f"CICLO_LOOP com identidade completa: {'SIM' if sintese.get('ciclo_loop_com_identidade') else 'NAO'}",
        f"Consulta completa para cliente/sessão: {'SIM' if sintese.get('consulta_completa_para_cliente_sessao') else 'NAO'}",
        f"Leitura sintética: {sintese.get('leitura_sintetica', '')}",
    ]

    for aviso in leitura_segura.get("avisos") or []:
        linhas.append(f"Aviso: {aviso}")

    return linhas
