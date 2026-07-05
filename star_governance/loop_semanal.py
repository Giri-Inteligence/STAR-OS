"""
star_governance.loop_semanal

Camada determinística do Loop Semanal de Governança. Consolida payloads
históricos, registros de acompanhamento (Sprint 6.2) e status de
acompanhamento (Sprint 6.3) em um ciclo semanal em memória — sem
persistência, sem execução e sem automação.
"""

import copy
import hashlib
import json
from datetime import datetime, timezone

from star_governance.acompanhamento import (
    obter_dict_seguro,
    obter_lista_segura_governanca,
)
from star_governance.status_acompanhamento import (
    criar_snapshot_status_acompanhamento,
    gerar_leitura_status_acompanhamento,
)

VERSAO_ITEM_LOOP_GOVERNANCA = "6.4"
VERSAO_CICLO_LOOP_GOVERNANCA = "6.4"

CLASSIFICACOES_LOOP_PERMITIDAS = (
    "SEM_REGISTRO_OPERACIONAL",
    "REVISAO_DO_CICLO",
    "AGUARDANDO_EVIDENCIA",
    "AGUARDANDO_DECISAO",
    "DECISAO_REGISTRADA",
    "ENCERRADO",
    "SUSPENSO",
    "INCONSISTENTE",
)

PESOS_CLASSIFICACAO_LOOP = {
    "INCONSISTENTE": 1,
    "AGUARDANDO_DECISAO": 2,
    "AGUARDANDO_EVIDENCIA": 3,
    "DECISAO_REGISTRADA": 4,
    "REVISAO_DO_CICLO": 5,
    "SEM_REGISTRO_OPERACIONAL": 6,
    "SUSPENSO": 7,
    "ENCERRADO": 8,
}

LEITURAS_ITEM_LOOP = {
    "SEM_REGISTRO_OPERACIONAL": "Item sem registro operacional de acompanhamento.",
    "REVISAO_DO_CICLO": "Item em acompanhamento no ciclo.",
    "AGUARDANDO_EVIDENCIA": "Item aguarda evidência complementar.",
    "AGUARDANDO_DECISAO": "Item aguarda decisão operacional humana.",
    "DECISAO_REGISTRADA": "Item possui decisão operacional registrada.",
    "ENCERRADO": "Item encerrado no acompanhamento.",
    "SUSPENSO": "Item suspenso no acompanhamento.",
    "INCONSISTENTE": "Item com inconsistência de sequência de acompanhamento.",
}


def obter_classificacoes_loop_permitidas():
    return list(CLASSIFICACOES_LOOP_PERMITIDAS)


def obter_pesos_classificacao_loop():
    return dict(PESOS_CLASSIFICACAO_LOOP)


def gerar_timestamp_loop():
    return datetime.now(timezone.utc).isoformat()


def gerar_id_loop_deterministico(*partes):
    texto_partes = "|".join(str(parte) if parte is not None else "" for parte in partes)
    hash_completo = hashlib.sha256(texto_partes.encode("utf-8")).hexdigest()

    return hash_completo[:16].upper()


def classificar_item_loop(snapshot_status=None):
    snapshot_status = obter_dict_seguro(snapshot_status)

    avisos = []

    erros = snapshot_status.get("erros") or []
    transicoes_validas = snapshot_status.get("transicoes_validas", True)

    if erros or transicoes_validas is False:
        return {
            "classificacao_loop": "INCONSISTENTE",
            "entra_no_loop_ativo": True,
            "motivo": "Snapshot de status apresenta erros ou transições inválidas.",
            "avisos": avisos,
        }

    status_atual = snapshot_status.get("status_atual_acompanhamento", "")
    total_registros = snapshot_status.get("total_registros", 0)

    if status_atual == "NAO_INICIADO" and total_registros == 0:
        return {
            "classificacao_loop": "SEM_REGISTRO_OPERACIONAL",
            "entra_no_loop_ativo": True,
            "motivo": "Nenhum registro operacional de acompanhamento encontrado.",
            "avisos": avisos,
        }

    mapa_status_para_classificacao = {
        "EM_ACOMPANHAMENTO": ("REVISAO_DO_CICLO", True),
        "AGUARDANDO_EVIDENCIA": ("AGUARDANDO_EVIDENCIA", True),
        "AGUARDANDO_DECISAO": ("AGUARDANDO_DECISAO", True),
        "DECISAO_REGISTRADA": ("DECISAO_REGISTRADA", True),
        "ENCERRADO": ("ENCERRADO", False),
        "SUSPENSO": ("SUSPENSO", False),
    }

    if status_atual in mapa_status_para_classificacao:
        classificacao, entra_no_loop_ativo = mapa_status_para_classificacao[status_atual]

        return {
            "classificacao_loop": classificacao,
            "entra_no_loop_ativo": entra_no_loop_ativo,
            "motivo": f"Status atual de acompanhamento: {status_atual}.",
            "avisos": avisos,
        }

    if status_atual == "NAO_INICIADO":
        return {
            "classificacao_loop": "SEM_REGISTRO_OPERACIONAL",
            "entra_no_loop_ativo": True,
            "motivo": "Status atual de acompanhamento: NAO_INICIADO.",
            "avisos": avisos,
        }

    return {
        "classificacao_loop": "INCONSISTENTE",
        "entra_no_loop_ativo": True,
        "motivo": f"Status de acompanhamento não reconhecido: {status_atual!r}.",
        "avisos": avisos,
    }


def gerar_leitura_item_loop(item_loop=None):
    item_loop = obter_dict_seguro(item_loop)
    classificacao = item_loop.get("classificacao_loop", "")

    return LEITURAS_ITEM_LOOP.get(classificacao, LEITURAS_ITEM_LOOP["SEM_REGISTRO_OPERACIONAL"])


def criar_item_loop_governanca(payload_historico=None, registros_acompanhamento=None, contexto=None, criado_em=None):
    snapshot_status = criar_snapshot_status_acompanhamento(
        payload_historico=payload_historico, registros=registros_acompanhamento, contexto=contexto
    )
    leitura_status = gerar_leitura_status_acompanhamento(snapshot_status)
    classificacao_resultado = classificar_item_loop(snapshot_status)

    timestamp = criado_em if criado_em else gerar_timestamp_loop()

    item_loop_id = gerar_id_loop_deterministico(
        "ITEM_LOOP",
        snapshot_status.get("cliente_id", ""),
        snapshot_status.get("sessao_id", ""),
        snapshot_status.get("status_atual_acompanhamento", ""),
        classificacao_resultado["classificacao_loop"],
        timestamp,
    )

    item_loop = {
        "versao_item_loop_governanca": VERSAO_ITEM_LOOP_GOVERNANCA,
        "item_loop_id": item_loop_id,
        "cliente_id": snapshot_status.get("cliente_id", ""),
        "sessao_id": snapshot_status.get("sessao_id", ""),
        "nome_cliente": snapshot_status.get("nome_cliente", ""),
        "status_star": snapshot_status.get("status_star", ""),
        "status_conclusivo_geral": snapshot_status.get("status_conclusivo_geral", ""),
        "status_atual_acompanhamento": snapshot_status.get("status_atual_acompanhamento", ""),
        "classificacao_loop": classificacao_resultado["classificacao_loop"],
        "entra_no_loop_ativo": classificacao_resultado["entra_no_loop_ativo"],
        "total_registros": snapshot_status.get("total_registros", 0),
        "registro_id_atual": snapshot_status.get("registro_id_atual", ""),
        "transicoes_validas": snapshot_status.get("transicoes_validas", True),
        "erros": list(snapshot_status.get("erros") or []),
        "avisos": list(snapshot_status.get("avisos") or []) + list(classificacao_resultado.get("avisos") or []),
        "leitura_status": leitura_status,
        "leitura_loop": "",
        "snapshot_status": snapshot_status,
        "criado_em": timestamp,
    }

    item_loop["leitura_loop"] = gerar_leitura_item_loop(item_loop)

    json.dumps(item_loop)

    return item_loop


def ordenar_itens_loop(itens=None):
    itens_seguros = [item for item in obter_lista_segura_governanca(itens) if isinstance(item, dict)]

    def chave_ordenacao(item):
        classificacao = item.get("classificacao_loop", "")
        peso = PESOS_CLASSIFICACAO_LOOP.get(classificacao, PESOS_CLASSIFICACAO_LOOP["INCONSISTENTE"])

        return (peso, str(item.get("nome_cliente", "")), str(item.get("sessao_id", "")))

    return sorted(copy.deepcopy(itens_seguros), key=chave_ordenacao)


def gerar_resumo_loop_semanal(itens=None):
    itens_seguros = [item for item in obter_lista_segura_governanca(itens) if isinstance(item, dict)]

    resumo = {
        "total_itens": len(itens_seguros),
        "itens_ativos_no_loop": 0,
        "sem_registro_operacional": 0,
        "revisao_do_ciclo": 0,
        "aguardando_evidencia": 0,
        "aguardando_decisao": 0,
        "decisao_registrada": 0,
        "encerrado": 0,
        "suspenso": 0,
        "inconsistente": 0,
    }

    chave_por_classificacao = {
        "SEM_REGISTRO_OPERACIONAL": "sem_registro_operacional",
        "REVISAO_DO_CICLO": "revisao_do_ciclo",
        "AGUARDANDO_EVIDENCIA": "aguardando_evidencia",
        "AGUARDANDO_DECISAO": "aguardando_decisao",
        "DECISAO_REGISTRADA": "decisao_registrada",
        "ENCERRADO": "encerrado",
        "SUSPENSO": "suspenso",
        "INCONSISTENTE": "inconsistente",
    }

    for item in itens_seguros:
        classificacao = item.get("classificacao_loop", "")
        chave = chave_por_classificacao.get(classificacao, "inconsistente")
        resumo[chave] += 1

        if item.get("entra_no_loop_ativo"):
            resumo["itens_ativos_no_loop"] += 1

    return resumo


def criar_ciclo_loop_semanal(entradas=None, periodo_referencia="", origem="GOVERNANCA_MANUAL", criado_em=None):
    entradas_seguras = [entrada for entrada in obter_lista_segura_governanca(entradas) if isinstance(entrada, dict)]

    itens = []

    for entrada in entradas_seguras:
        item_loop = criar_item_loop_governanca(
            payload_historico=entrada.get("payload_historico"),
            registros_acompanhamento=entrada.get("registros_acompanhamento"),
            contexto=entrada.get("contexto"),
        )
        itens.append(item_loop)

    itens_ordenados = ordenar_itens_loop(itens)
    resumo_loop = gerar_resumo_loop_semanal(itens_ordenados)

    timestamp = criado_em if criado_em else gerar_timestamp_loop()

    ciclo_id = gerar_id_loop_deterministico(
        "CICLO_SEMANAL", periodo_referencia, origem, timestamp, len(itens_ordenados)
    )

    ciclo = {
        "versao_ciclo_loop_governanca": VERSAO_CICLO_LOOP_GOVERNANCA,
        "ciclo_id": ciclo_id,
        "tipo_ciclo": "SEMANAL",
        "periodo_referencia": str(periodo_referencia or ""),
        "origem": str(origem or ""),
        "criado_em": timestamp,
        "total_itens": len(itens_ordenados),
        "itens": itens_ordenados,
        "resumo_loop": resumo_loop,
    }

    json.dumps(ciclo)

    return ciclo


def validar_item_loop_governanca(item_loop=None):
    erros = []
    avisos = []

    if not isinstance(item_loop, dict):
        return {"valido": False, "erros": ["item_loop deve ser um dicionario."], "avisos": []}

    for campo in ("versao_item_loop_governanca", "item_loop_id", "cliente_id", "sessao_id",
                  "status_atual_acompanhamento", "classificacao_loop", "criado_em"):
        if not item_loop.get(campo):
            erros.append(f"Campo obrigatorio ausente ou vazio: {campo}.")

    classificacao_loop = item_loop.get("classificacao_loop", "")

    if classificacao_loop and classificacao_loop not in CLASSIFICACOES_LOOP_PERMITIDAS:
        erros.append(f"Classificacao de loop invalida: {classificacao_loop!r}.")

    try:
        json.dumps(item_loop)
    except Exception as exc:
        erros.append(f"item_loop nao e serializavel: {exc}")

    if classificacao_loop == "INCONSISTENTE" and not item_loop.get("erros"):
        avisos.append("Item classificado como INCONSISTENTE sem erros detalhados registrados.")

    if item_loop.get("entra_no_loop_ativo") is False and classificacao_loop not in ("ENCERRADO", "SUSPENSO"):
        avisos.append("Item fora do loop ativo com classificação diferente de ENCERRADO/SUSPENSO.")

    return {
        "valido": len(erros) == 0,
        "erros": erros,
        "avisos": avisos,
    }


def validar_ciclo_loop_semanal(ciclo=None):
    erros = []
    avisos = []

    if not isinstance(ciclo, dict):
        return {"valido": False, "erros": ["ciclo deve ser um dicionario."], "avisos": [], "total_itens": 0}

    for campo in ("versao_ciclo_loop_governanca", "ciclo_id", "tipo_ciclo", "criado_em"):
        if not ciclo.get(campo):
            erros.append(f"Campo obrigatorio ausente ou vazio: {campo}.")

    if ciclo.get("tipo_ciclo") not in (None, "", "SEMANAL"):
        erros.append(f"tipo_ciclo deveria ser SEMANAL, obtido {ciclo.get('tipo_ciclo')!r}.")
    elif not ciclo.get("tipo_ciclo"):
        erros.append("tipo_ciclo ausente ou vazio.")

    itens = ciclo.get("itens")

    if not isinstance(itens, list):
        erros.append("itens deveria ser uma lista.")
        itens = []

    total_itens_informado = ciclo.get("total_itens", 0)

    if total_itens_informado != len(itens):
        erros.append(
            f"total_itens ({total_itens_informado}) nao corresponde ao tamanho de itens ({len(itens)})."
        )

    if "resumo_loop" not in ciclo:
        erros.append("resumo_loop ausente.")

    if not itens:
        avisos.append("Ciclo semanal sem itens.")

    for item in itens:
        resultado_item = validar_item_loop_governanca(item)

        if not resultado_item["valido"]:
            erros.extend(resultado_item["erros"])

        avisos.extend(resultado_item["avisos"])

    try:
        json.dumps(ciclo)
    except Exception as exc:
        erros.append(f"ciclo nao e serializavel: {exc}")

    return {
        "valido": len(erros) == 0,
        "erros": erros,
        "avisos": avisos,
        "total_itens": len(itens),
    }


def formatar_item_loop_texto(item_loop=None):
    item_loop = obter_dict_seguro(item_loop)

    return [
        f"Cliente: {item_loop.get('nome_cliente', '')}",
        f"Sessão: {item_loop.get('sessao_id', '')}",
        f"Status STAR: {item_loop.get('status_star', '')}",
        f"Status atual do acompanhamento: {item_loop.get('status_atual_acompanhamento', '')}",
        f"Classificação no loop: {item_loop.get('classificacao_loop', '')}",
        f"Entra no loop ativo: {'SIM' if item_loop.get('entra_no_loop_ativo') else 'NAO'}",
        f"Leitura: {item_loop.get('leitura_loop', '')}",
    ]


def formatar_resumo_loop_texto(resumo=None):
    resumo = obter_dict_seguro(resumo)

    return [
        f"Total de itens: {resumo.get('total_itens', 0)}",
        f"Itens ativos no loop: {resumo.get('itens_ativos_no_loop', 0)}",
        f"Sem registro operacional: {resumo.get('sem_registro_operacional', 0)}",
        f"Em revisão do ciclo: {resumo.get('revisao_do_ciclo', 0)}",
        f"Aguardando evidência: {resumo.get('aguardando_evidencia', 0)}",
        f"Aguardando decisão: {resumo.get('aguardando_decisao', 0)}",
        f"Decisão registrada: {resumo.get('decisao_registrada', 0)}",
        f"Encerrados: {resumo.get('encerrado', 0)}",
        f"Suspensos: {resumo.get('suspenso', 0)}",
        f"Inconsistentes: {resumo.get('inconsistente', 0)}",
    ]


def formatar_validacao_loop_texto(resultado=None):
    resultado = obter_dict_seguro(resultado)

    linhas = [
        f"Ciclo válido: {'SIM' if resultado.get('valido') else 'NAO'}",
        f"Total de itens: {resultado.get('total_itens', 0)}",
        f"Erros: {len(resultado.get('erros') or [])}",
        f"Avisos: {len(resultado.get('avisos') or [])}",
    ]

    for erro in resultado.get("erros") or []:
        linhas.append(f"Erro: {erro}")

    for aviso in resultado.get("avisos") or []:
        linhas.append(f"Aviso: {aviso}")

    return linhas
