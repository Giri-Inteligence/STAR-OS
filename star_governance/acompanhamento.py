"""
star_governance.acompanhamento

Contrato determinístico do Registro de Acompanhamento Operacional.
Representa, em memória, a continuidade de uma investigação já salva no
Histórico Investigativo (Sprint 5) — sem persistência, sem execução e
sem automação. Usa apenas biblioteca padrão do Python além das funções
utilitárias já existentes em star_persistence.contrato_historico.
"""

import json
import unicodedata

from star_persistence.contrato_historico import (
    garantir_json_serializavel,
    gerar_id_deterministico,
    gerar_timestamp_iso,
)

VERSAO_CONTRATO_GOVERNANCA = "6.2"

ESTADOS_ACOMPANHAMENTO = (
    "NAO_INICIADO",
    "EM_ACOMPANHAMENTO",
    "AGUARDANDO_EVIDENCIA",
    "AGUARDANDO_DECISAO",
    "DECISAO_REGISTRADA",
    "ENCERRADO",
    "SUSPENSO",
)

TIPOS_ACOMPANHAMENTO = (
    "OBSERVACAO",
    "RETORNO",
    "COMPLEMENTO_EVIDENCIA",
    "REVISAO",
    "DECISAO_OPERACIONAL",
    "PENDENCIA_INVESTIGATIVA",
)

MAPA_STATUS_ACOMPANHAMENTO = {
    "NAO INICIADO": "NAO_INICIADO",
    "NAO_INICIADO": "NAO_INICIADO",
    "EM ACOMPANHAMENTO": "EM_ACOMPANHAMENTO",
    "EM_ACOMPANHAMENTO": "EM_ACOMPANHAMENTO",
    "AGUARDANDO EVIDENCIA": "AGUARDANDO_EVIDENCIA",
    "AGUARDANDO_EVIDENCIA": "AGUARDANDO_EVIDENCIA",
    "AGUARDANDO DECISAO": "AGUARDANDO_DECISAO",
    "AGUARDANDO_DECISAO": "AGUARDANDO_DECISAO",
    "DECISAO REGISTRADA": "DECISAO_REGISTRADA",
    "DECISAO_REGISTRADA": "DECISAO_REGISTRADA",
    "ENCERRADO": "ENCERRADO",
    "ENCERRADA": "ENCERRADO",
    "SUSPENSO": "SUSPENSO",
    "SUSPENSA": "SUSPENSO",
}

MAPA_TIPO_ACOMPANHAMENTO = {
    "OBSERVACAO": "OBSERVACAO",
    "RETORNO": "RETORNO",
    "COMPLEMENTO EVIDENCIA": "COMPLEMENTO_EVIDENCIA",
    "COMPLEMENTO_EVIDENCIA": "COMPLEMENTO_EVIDENCIA",
    "REVISAO": "REVISAO",
    "DECISAO OPERACIONAL": "DECISAO_OPERACIONAL",
    "DECISAO_OPERACIONAL": "DECISAO_OPERACIONAL",
    "PENDENCIA INVESTIGATIVA": "PENDENCIA_INVESTIGATIVA",
    "PENDENCIA_INVESTIGATIVA": "PENDENCIA_INVESTIGATIVA",
}

LEITURAS_POR_STATUS = {
    "NAO_INICIADO": "Acompanhamento ainda não iniciado.",
    "EM_ACOMPANHAMENTO": "Acompanhamento em curso, com registro de observação.",
    "AGUARDANDO_EVIDENCIA": "Acompanhamento aguarda evidência complementar.",
    "AGUARDANDO_DECISAO": "Acompanhamento aguarda decisão operacional humana.",
    "DECISAO_REGISTRADA": "Decisão operacional registrada para continuidade da governança.",
    "ENCERRADO": "Acompanhamento encerrado.",
    "SUSPENSO": "Acompanhamento suspenso.",
}


def _normalizar_texto_para_mapa(valor):
    if valor is None:
        return ""

    if isinstance(valor, float) and valor != valor:
        return ""

    texto = " ".join(str(valor).strip().upper().split())

    if texto == "":
        return ""

    texto_decomposto = unicodedata.normalize("NFKD", texto)

    return "".join(caractere for caractere in texto_decomposto if not unicodedata.combining(caractere))


def obter_dict_seguro(valor):
    if isinstance(valor, dict):
        return valor

    return {}


def obter_lista_segura_governanca(valor):
    if valor is None:
        return []

    if isinstance(valor, list):
        return valor

    if isinstance(valor, tuple):
        return list(valor)

    return [valor]


def normalizar_status_acompanhamento(status):
    texto = _normalizar_texto_para_mapa(status)

    return MAPA_STATUS_ACOMPANHAMENTO.get(texto, "NAO_INICIADO")


def normalizar_tipo_acompanhamento(tipo):
    texto = _normalizar_texto_para_mapa(tipo)

    return MAPA_TIPO_ACOMPANHAMENTO.get(texto, "OBSERVACAO")


def extrair_contexto_payload_historico(payload_historico=None):
    payload_historico = obter_dict_seguro(payload_historico)

    cliente = obter_dict_seguro(payload_historico.get("cliente"))
    sessao = obter_dict_seguro(payload_historico.get("sessao"))
    snapshot = obter_dict_seguro(payload_historico.get("snapshot_star"))
    itens = obter_lista_segura_governanca(payload_historico.get("itens_investigativos"))
    pacote = obter_dict_seguro(payload_historico.get("pacote_investigativo"))
    conclusao = obter_dict_seguro(payload_historico.get("conclusao_investigativa"))

    return {
        "cliente_id": str(cliente.get("cliente_id", "") or ""),
        "sessao_id": str(sessao.get("sessao_id", "") or ""),
        "nome_cliente": str(cliente.get("nome_cliente", "") or ""),
        "vendedor": str(cliente.get("vendedor", "") or ""),
        "cidade": str(cliente.get("cidade", "") or ""),
        "status_star": str(snapshot.get("status_star", "") or ""),
        "curva": str(snapshot.get("curva", "") or ""),
        "status_conclusivo_geral": str(conclusao.get("status_conclusivo_geral", "") or ""),
        "leitura_conclusao": str(conclusao.get("leitura_conclusao", "") or ""),
        "total_itens_investigativos": len(itens),
        "pacote_id": str(pacote.get("pacote_id", "") or ""),
        "conclusao_id": str(conclusao.get("conclusao_id", "") or ""),
    }


def criar_registro_acompanhamento(
    payload_historico=None,
    tipo_acompanhamento="OBSERVACAO",
    status_acompanhamento="NAO_INICIADO",
    observacao_acompanhamento="",
    evidencia_complementar="",
    decisao_operacional="",
    origem="GOVERNANCA_MANUAL",
    usuario_registro="",
    criado_em=None,
):
    contexto = extrair_contexto_payload_historico(payload_historico)
    timestamp = gerar_timestamp_iso(criado_em)

    tipo_normalizado = normalizar_tipo_acompanhamento(tipo_acompanhamento)
    status_normalizado = normalizar_status_acompanhamento(status_acompanhamento)

    observacao_texto = str(observacao_acompanhamento or "")
    evidencia_texto = str(evidencia_complementar or "")
    decisao_texto = str(decisao_operacional or "")

    registro_id = gerar_id_deterministico(
        "ACOMPANHAMENTO",
        [
            contexto["cliente_id"],
            contexto["sessao_id"],
            tipo_normalizado,
            status_normalizado,
            observacao_texto,
            timestamp,
        ],
    )

    registro = {
        "versao_contrato_governanca": VERSAO_CONTRATO_GOVERNANCA,
        "registro_id": registro_id,
        "cliente_id": contexto["cliente_id"],
        "sessao_id": contexto["sessao_id"],
        "nome_cliente": contexto["nome_cliente"],
        "vendedor": contexto["vendedor"],
        "cidade": contexto["cidade"],
        "status_star": contexto["status_star"],
        "curva": contexto["curva"],
        "status_conclusivo_geral": contexto["status_conclusivo_geral"],
        "leitura_conclusao": contexto["leitura_conclusao"],
        "tipo_acompanhamento": tipo_normalizado,
        "status_acompanhamento": status_normalizado,
        "observacao_acompanhamento": observacao_texto,
        "evidencia_complementar": evidencia_texto,
        "decisao_operacional": decisao_texto,
        "origem": str(origem or ""),
        "usuario_registro": str(usuario_registro or ""),
        "criado_em": timestamp,
        "atualizado_em": timestamp,
        "referencias": {
            "pacote_id": contexto["pacote_id"],
            "conclusao_id": contexto["conclusao_id"],
            "total_itens_investigativos": contexto["total_itens_investigativos"],
        },
    }

    return garantir_json_serializavel(registro)


def validar_registro_acompanhamento(registro=None):
    erros = []
    avisos = []

    if not isinstance(registro, dict):
        return {"valido": False, "erros": ["registro deve ser um dicionario."], "avisos": []}

    for campo in ("versao_contrato_governanca", "registro_id", "cliente_id", "sessao_id",
                  "tipo_acompanhamento", "status_acompanhamento", "criado_em"):
        if not registro.get(campo):
            erros.append(f"Campo obrigatorio ausente ou vazio: {campo}.")

    try:
        json.dumps(garantir_json_serializavel(registro))
    except Exception as exc:
        erros.append(f"Registro nao e serializavel: {exc}")

    observacao = registro.get("observacao_acompanhamento", "") if isinstance(registro, dict) else ""
    evidencia = registro.get("evidencia_complementar", "") if isinstance(registro, dict) else ""
    decisao = registro.get("decisao_operacional", "") if isinstance(registro, dict) else ""

    if not observacao and not evidencia and not decisao:
        avisos.append("Registro sem observação, evidência complementar ou decisão operacional.")

    status_acompanhamento = registro.get("status_acompanhamento", "") if isinstance(registro, dict) else ""

    if status_acompanhamento == "DECISAO_REGISTRADA" and not decisao:
        avisos.append("Status DECISAO_REGISTRADA sem decisão operacional registrada.")

    if status_acompanhamento == "AGUARDANDO_EVIDENCIA" and not evidencia:
        avisos.append("Status AGUARDANDO_EVIDENCIA sem evidência complementar registrada.")

    return {
        "valido": len(erros) == 0,
        "erros": erros,
        "avisos": avisos,
    }


def gerar_leitura_acompanhamento(registro=None):
    registro = obter_dict_seguro(registro)
    status_acompanhamento = normalizar_status_acompanhamento(registro.get("status_acompanhamento", ""))

    return LEITURAS_POR_STATUS.get(status_acompanhamento, LEITURAS_POR_STATUS["NAO_INICIADO"])


def gerar_pacote_acompanhamento_operacional(payload_historico=None, registros=None):
    contexto = extrair_contexto_payload_historico(payload_historico)
    registros_seguros = [
        registro for registro in obter_lista_segura_governanca(registros) if isinstance(registro, dict)
    ]

    resumo_acompanhamento = {
        "nao_iniciado": 0,
        "em_acompanhamento": 0,
        "aguardando_evidencia": 0,
        "aguardando_decisao": 0,
        "decisao_registrada": 0,
        "encerrado": 0,
        "suspenso": 0,
    }

    chave_por_status = {
        "NAO_INICIADO": "nao_iniciado",
        "EM_ACOMPANHAMENTO": "em_acompanhamento",
        "AGUARDANDO_EVIDENCIA": "aguardando_evidencia",
        "AGUARDANDO_DECISAO": "aguardando_decisao",
        "DECISAO_REGISTRADA": "decisao_registrada",
        "ENCERRADO": "encerrado",
        "SUSPENSO": "suspenso",
    }

    for registro in registros_seguros:
        status_normalizado = normalizar_status_acompanhamento(registro.get("status_acompanhamento", ""))
        chave = chave_por_status.get(status_normalizado, "nao_iniciado")
        resumo_acompanhamento[chave] += 1

    pacote = {
        "versao_pacote_governanca": VERSAO_CONTRATO_GOVERNANCA,
        "cliente_id": contexto["cliente_id"],
        "sessao_id": contexto["sessao_id"],
        "nome_cliente": contexto["nome_cliente"],
        "status_star": contexto["status_star"],
        "status_conclusivo_geral": contexto["status_conclusivo_geral"],
        "total_registros": len(registros_seguros),
        "registros": list(registros_seguros),
        "resumo_acompanhamento": resumo_acompanhamento,
    }

    return garantir_json_serializavel(pacote)


def formatar_registro_acompanhamento_texto(registro=None):
    registro = obter_dict_seguro(registro)

    return [
        f"Cliente: {registro.get('nome_cliente', '')}",
        f"Sessão: {registro.get('sessao_id', '')}",
        f"Tipo de acompanhamento: {registro.get('tipo_acompanhamento', '')}",
        f"Status de acompanhamento: {registro.get('status_acompanhamento', '')}",
        f"Observação: {registro.get('observacao_acompanhamento', '')}",
        f"Leitura: {gerar_leitura_acompanhamento(registro)}",
    ]


def formatar_validacao_acompanhamento_texto(resultado=None):
    resultado = obter_dict_seguro(resultado)

    linhas = [
        f"Registro válido: {'SIM' if resultado.get('valido') else 'NAO'}",
        f"Erros: {len(resultado.get('erros') or [])}",
        f"Avisos: {len(resultado.get('avisos') or [])}",
    ]

    for erro in resultado.get("erros") or []:
        linhas.append(f"Erro: {erro}")

    for aviso in resultado.get("avisos") or []:
        linhas.append(f"Aviso: {aviso}")

    return linhas
