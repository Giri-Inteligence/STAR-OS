"""
star_governance.status_acompanhamento

Camada determinística de estado e transição do Registro de
Acompanhamento Operacional (Sprint 6.2). Avalia, valida e interpreta o
status de continuidade da investigação em memória — sem persistência,
sem execução e sem automação.
"""

import json

from star_governance.acompanhamento import (
    obter_dict_seguro,
    obter_lista_segura_governanca,
    normalizar_status_acompanhamento,
    validar_registro_acompanhamento,
    extrair_contexto_payload_historico,
)

VERSAO_SNAPSHOT_STATUS_GOVERNANCA = "6.3"

STATUS_ACOMPANHAMENTO_PERMITIDOS = (
    "NAO_INICIADO",
    "EM_ACOMPANHAMENTO",
    "AGUARDANDO_EVIDENCIA",
    "AGUARDANDO_DECISAO",
    "DECISAO_REGISTRADA",
    "ENCERRADO",
    "SUSPENSO",
)

STATUS_FINAIS = ("ENCERRADO",)

TRANSICOES_STATUS_PERMITIDAS = {
    "NAO_INICIADO": [
        "NAO_INICIADO", "EM_ACOMPANHAMENTO", "AGUARDANDO_EVIDENCIA",
        "AGUARDANDO_DECISAO", "SUSPENSO", "ENCERRADO",
    ],
    "EM_ACOMPANHAMENTO": [
        "EM_ACOMPANHAMENTO", "AGUARDANDO_EVIDENCIA", "AGUARDANDO_DECISAO",
        "DECISAO_REGISTRADA", "ENCERRADO", "SUSPENSO",
    ],
    "AGUARDANDO_EVIDENCIA": [
        "AGUARDANDO_EVIDENCIA", "EM_ACOMPANHAMENTO", "AGUARDANDO_DECISAO",
        "DECISAO_REGISTRADA", "ENCERRADO", "SUSPENSO",
    ],
    "AGUARDANDO_DECISAO": [
        "AGUARDANDO_DECISAO", "EM_ACOMPANHAMENTO", "DECISAO_REGISTRADA",
        "ENCERRADO", "SUSPENSO",
    ],
    "DECISAO_REGISTRADA": [
        "DECISAO_REGISTRADA", "EM_ACOMPANHAMENTO", "ENCERRADO", "SUSPENSO",
    ],
    "ENCERRADO": ["ENCERRADO"],
    "SUSPENSO": ["SUSPENSO", "EM_ACOMPANHAMENTO", "ENCERRADO"],
}

LEITURAS_STATUS_SNAPSHOT = {
    "NAO_INICIADO": "Acompanhamento sem registros operacionais.",
    "EM_ACOMPANHAMENTO": "Acompanhamento em curso.",
    "AGUARDANDO_EVIDENCIA": "Acompanhamento aguarda evidência complementar.",
    "AGUARDANDO_DECISAO": "Acompanhamento aguarda decisão operacional humana.",
    "DECISAO_REGISTRADA": "Decisão operacional registrada.",
    "ENCERRADO": "Acompanhamento encerrado.",
    "SUSPENSO": "Acompanhamento suspenso.",
}


def obter_status_acompanhamento_permitidos():
    return list(STATUS_ACOMPANHAMENTO_PERMITIDOS)


def obter_transicoes_status_permitidas():
    return {status: list(destinos) for status, destinos in TRANSICOES_STATUS_PERMITIDAS.items()}


def status_eh_final(status):
    return normalizar_status_acompanhamento(status) in STATUS_FINAIS


def status_exige_evidencia(status):
    return normalizar_status_acompanhamento(status) == "AGUARDANDO_EVIDENCIA"


def status_exige_decisao(status):
    return normalizar_status_acompanhamento(status) in ("AGUARDANDO_DECISAO", "DECISAO_REGISTRADA")


def avaliar_transicao_status(status_atual, status_novo, contexto=None):
    contexto = obter_dict_seguro(contexto)

    status_atual_normalizado = normalizar_status_acompanhamento(status_atual)
    status_novo_normalizado = normalizar_status_acompanhamento(status_novo)

    erros = []
    avisos = []

    permitir_reabertura = bool(contexto.get("permitir_reabertura"))

    if status_atual_normalizado == "ENCERRADO" and status_novo_normalizado != "ENCERRADO":
        if not permitir_reabertura:
            erros.append("Transição bloqueada: status ENCERRADO é final e não permite reabertura sem autorização explícita.")
        elif status_novo_normalizado != "EM_ACOMPANHAMENTO":
            erros.append("Reabertura de ENCERRADO só é permitida para EM_ACOMPANHAMENTO.")
    else:
        destinos_permitidos = TRANSICOES_STATUS_PERMITIDAS.get(status_atual_normalizado, [])
        if status_novo_normalizado not in destinos_permitidos:
            erros.append(
                f"Transição não permitida: {status_atual_normalizado} → {status_novo_normalizado}."
            )

    if status_novo_normalizado == "AGUARDANDO_EVIDENCIA" and not contexto.get("evidencia_complementar"):
        avisos.append("Status AGUARDANDO_EVIDENCIA sem evidência complementar informada no contexto.")

    if status_novo_normalizado == "DECISAO_REGISTRADA" and not contexto.get("decisao_operacional"):
        avisos.append("Status DECISAO_REGISTRADA sem decisão operacional informada no contexto.")

    if status_novo_normalizado == "AGUARDANDO_DECISAO":
        avisos.append("Status AGUARDANDO_DECISAO depende de decisão operacional humana.")

    return {
        "permitida": len(erros) == 0,
        "status_atual": status_atual_normalizado,
        "status_novo": status_novo_normalizado,
        "erros": erros,
        "avisos": avisos,
    }


def sugerir_status_conceituais_permitidos(status_atual, contexto=None):
    contexto = obter_dict_seguro(contexto)
    status_atual_normalizado = normalizar_status_acompanhamento(status_atual)

    avisos = []

    if status_atual_normalizado == "ENCERRADO":
        if contexto.get("permitir_reabertura"):
            status_permitidos = ["ENCERRADO", "EM_ACOMPANHAMENTO"]
        else:
            status_permitidos = ["ENCERRADO"]
    else:
        status_permitidos = list(TRANSICOES_STATUS_PERMITIDAS.get(status_atual_normalizado, []))

    return {
        "status_atual": status_atual_normalizado,
        "status_permitidos": status_permitidos,
        "avisos": avisos,
    }


def ordenar_registros_por_criado_em(registros=None):
    registros_seguros = [
        registro for registro in obter_lista_segura_governanca(registros) if isinstance(registro, dict)
    ]

    com_data = [registro for registro in registros_seguros if registro.get("criado_em")]
    sem_data = [registro for registro in registros_seguros if not registro.get("criado_em")]

    com_data_ordenados = sorted(com_data, key=lambda registro: registro.get("criado_em", ""))

    return com_data_ordenados + sem_data


def obter_status_atual_acompanhamento(registros=None):
    registros_ordenados = ordenar_registros_por_criado_em(registros)

    if not registros_ordenados:
        return {"status_atual": "NAO_INICIADO", "registro_id_atual": "", "total_registros_considerados": 0}

    ultimo_registro = registros_ordenados[-1]
    status_atual = normalizar_status_acompanhamento(ultimo_registro.get("status_acompanhamento", ""))

    return {
        "status_atual": status_atual,
        "registro_id_atual": str(ultimo_registro.get("registro_id", "") or ""),
        "total_registros_considerados": len(registros_ordenados),
    }


def validar_consistencia_status_acompanhamento(registros=None, contexto=None):
    registros_ordenados = ordenar_registros_por_criado_em(registros)

    erros = []
    avisos = []
    transicoes_avaliadas = 0

    if not registros_ordenados:
        return {
            "valido": True,
            "erros": [],
            "avisos": ["Nenhum registro de acompanhamento informado."],
            "total_registros": 0,
            "transicoes_avaliadas": 0,
        }

    for registro in registros_ordenados:
        resultado_validacao = validar_registro_acompanhamento(registro)

        if not resultado_validacao["valido"]:
            erros.extend(resultado_validacao["erros"])

        avisos.extend(resultado_validacao["avisos"])

    for indice in range(1, len(registros_ordenados)):
        status_anterior = registros_ordenados[indice - 1].get("status_acompanhamento", "")
        status_seguinte = registros_ordenados[indice].get("status_acompanhamento", "")

        resultado_transicao = avaliar_transicao_status(status_anterior, status_seguinte, contexto)
        transicoes_avaliadas += 1

        if not resultado_transicao["permitida"]:
            erros.extend(resultado_transicao["erros"])

        avisos.extend(resultado_transicao["avisos"])

    return {
        "valido": len(erros) == 0,
        "erros": erros,
        "avisos": avisos,
        "total_registros": len(registros_ordenados),
        "transicoes_avaliadas": transicoes_avaliadas,
    }


def criar_snapshot_status_acompanhamento(payload_historico=None, registros=None, contexto=None):
    contexto_payload = extrair_contexto_payload_historico(payload_historico)
    status_atual_info = obter_status_atual_acompanhamento(registros)
    validacao_consistencia = validar_consistencia_status_acompanhamento(registros, contexto)
    sugestao_status = sugerir_status_conceituais_permitidos(status_atual_info["status_atual"], contexto)

    snapshot = {
        "versao_snapshot_status_governanca": VERSAO_SNAPSHOT_STATUS_GOVERNANCA,
        "cliente_id": contexto_payload["cliente_id"],
        "sessao_id": contexto_payload["sessao_id"],
        "nome_cliente": contexto_payload["nome_cliente"],
        "status_star": contexto_payload["status_star"],
        "status_conclusivo_geral": contexto_payload["status_conclusivo_geral"],
        "status_atual_acompanhamento": status_atual_info["status_atual"],
        "registro_id_atual": status_atual_info["registro_id_atual"],
        "total_registros": status_atual_info["total_registros_considerados"],
        "transicoes_validas": validacao_consistencia["valido"],
        "erros": list(validacao_consistencia["erros"]),
        "avisos": list(validacao_consistencia["avisos"]),
        "status_permitidos_a_partir_do_atual": list(sugestao_status["status_permitidos"]),
    }

    json.dumps(snapshot)

    return snapshot


def gerar_leitura_status_acompanhamento(snapshot=None):
    snapshot = obter_dict_seguro(snapshot)
    status_atual = normalizar_status_acompanhamento(snapshot.get("status_atual_acompanhamento", ""))

    return LEITURAS_STATUS_SNAPSHOT.get(status_atual, LEITURAS_STATUS_SNAPSHOT["NAO_INICIADO"])


def formatar_snapshot_status_texto(snapshot=None):
    snapshot = obter_dict_seguro(snapshot)

    return [
        f"Cliente: {snapshot.get('nome_cliente', '')}",
        f"Sessão: {snapshot.get('sessao_id', '')}",
        f"Status STAR: {snapshot.get('status_star', '')}",
        f"Status conclusivo: {snapshot.get('status_conclusivo_geral', '')}",
        f"Status atual do acompanhamento: {snapshot.get('status_atual_acompanhamento', '')}",
        f"Total de registros: {snapshot.get('total_registros', 0)}",
        f"Transições válidas: {'SIM' if snapshot.get('transicoes_validas') else 'NAO'}",
        f"Leitura: {gerar_leitura_status_acompanhamento(snapshot)}",
    ]


def formatar_validacao_status_texto(resultado=None):
    resultado = obter_dict_seguro(resultado)

    linhas = [
        f"Sequência válida: {'SIM' if resultado.get('valido') else 'NAO'}",
        f"Total de registros: {resultado.get('total_registros', 0)}",
        f"Transições avaliadas: {resultado.get('transicoes_avaliadas', 0)}",
        f"Erros: {len(resultado.get('erros') or [])}",
        f"Avisos: {len(resultado.get('avisos') or [])}",
    ]

    for erro in resultado.get("erros") or []:
        linhas.append(f"Erro: {erro}")

    for aviso in resultado.get("avisos") or []:
        linhas.append(f"Aviso: {aviso}")

    return linhas
