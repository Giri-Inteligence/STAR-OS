"""
star_persistence.contrato_governanca

Contrato determinístico para representar payloads persistíveis de
Governança (Registro de Acompanhamento, Snapshot de Status, Item de
Loop, Ciclo de Loop e Governança Integrada). Define estrutura
serializável e validável para futura persistência — não salva nada,
não cria banco, não cria tabela e não altera o schema SQLite.
"""

import json
import unicodedata

from star_persistence.contrato_historico import (
    garantir_json_serializavel,
    gerar_id_deterministico,
    gerar_timestamp_iso,
)

VERSAO_PAYLOAD_GOVERNANCA = "7.2"
VERSAO_CONTRATO_PERSISTENCIA_GOVERNANCA = "7.2"

TIPOS_PAYLOAD_GOVERNANCA = (
    "REGISTRO_ACOMPANHAMENTO",
    "SNAPSHOT_STATUS",
    "ITEM_LOOP",
    "CICLO_LOOP",
    "GOVERNANCA_INTEGRADA",
)

MAPA_TIPO_PAYLOAD_GOVERNANCA = {
    "REGISTRO": "REGISTRO_ACOMPANHAMENTO",
    "REGISTRO ACOMPANHAMENTO": "REGISTRO_ACOMPANHAMENTO",
    "REGISTRO_ACOMPANHAMENTO": "REGISTRO_ACOMPANHAMENTO",
    "SNAPSHOT": "SNAPSHOT_STATUS",
    "SNAPSHOT STATUS": "SNAPSHOT_STATUS",
    "SNAPSHOT_STATUS": "SNAPSHOT_STATUS",
    "ITEM": "ITEM_LOOP",
    "ITEM LOOP": "ITEM_LOOP",
    "ITEM_LOOP": "ITEM_LOOP",
    "CICLO": "CICLO_LOOP",
    "CICLO LOOP": "CICLO_LOOP",
    "CICLO_LOOP": "CICLO_LOOP",
    "GOVERNANCA": "GOVERNANCA_INTEGRADA",
    "GOVERNANCA INTEGRADA": "GOVERNANCA_INTEGRADA",
    "GOVERNANCA_INTEGRADA": "GOVERNANCA_INTEGRADA",
}


def _normalizar_texto_para_mapa_governanca(valor):
    if valor is None:
        return ""

    if isinstance(valor, float) and valor != valor:
        return ""

    texto = " ".join(str(valor).strip().upper().split())

    if texto == "":
        return ""

    texto_decomposto = unicodedata.normalize("NFKD", texto)

    return "".join(caractere for caractere in texto_decomposto if not unicodedata.combining(caractere))


def obter_dict_seguro_governanca(valor):
    if isinstance(valor, dict):
        return valor

    return {}


def obter_lista_segura_contrato_governanca(valor):
    if valor is None:
        return []

    if isinstance(valor, list):
        return valor

    if isinstance(valor, tuple):
        return list(valor)

    return [valor]


def normalizar_tipo_payload_governanca(tipo):
    texto = _normalizar_texto_para_mapa_governanca(tipo)

    return MAPA_TIPO_PAYLOAD_GOVERNANCA.get(texto, "GOVERNANCA_INTEGRADA")


def criar_metadados_persistencia_governanca(
    origem="GOVERNANCA_MANUAL", usuario_registro="", criado_em=None, versao_contrato="7.2"
):
    timestamp = gerar_timestamp_iso(criado_em)

    return {
        "versao_contrato_persistencia_governanca": str(versao_contrato or VERSAO_CONTRATO_PERSISTENCIA_GOVERNANCA),
        "origem": str(origem or ""),
        "usuario_registro": str(usuario_registro or ""),
        "criado_em": timestamp,
        "atualizado_em": timestamp,
        "persistido": False,
        "persistencia_habilitada": False,
        "observacao_contrato": "Contrato de persistencia da governanca — nenhum dado e salvo nesta fase.",
    }


def criar_snapshot_id_deterministico(snapshot_status=None):
    snapshot = obter_dict_seguro_governanca(snapshot_status)

    return gerar_id_deterministico(
        "SNAPSHOT_STATUS",
        [
            snapshot.get("cliente_id", ""),
            snapshot.get("sessao_id", ""),
            snapshot.get("status_atual_acompanhamento", ""),
            snapshot.get("registro_id_atual", ""),
            str(snapshot.get("total_registros", 0)),
        ],
    )


CHAVES_LISTA_ITENS_CICLO = ("itens", "itens_loop", "itens_governanca", "lista_itens")
CHAVES_SUBESTRUTURA_ITEM = (
    "snapshot_status", "dados_snapshot", "dados_item_loop", "item_loop", "contexto", "cliente", "sessao",
)


def _buscar_identificadores_em_item_loop(item):
    item = obter_dict_seguro_governanca(item)

    cliente_id = item.get("cliente_id", "")
    sessao_id = item.get("sessao_id", "")
    nome_cliente = item.get("nome_cliente", "")

    if cliente_id and sessao_id and nome_cliente:
        return cliente_id, sessao_id, nome_cliente

    for chave in CHAVES_SUBESTRUTURA_ITEM:
        substrutura = obter_dict_seguro_governanca(item.get(chave))

        if not substrutura:
            continue

        cliente_id = cliente_id or substrutura.get("cliente_id", "")
        sessao_id = sessao_id or substrutura.get("sessao_id", "")
        nome_cliente = nome_cliente or substrutura.get("nome_cliente", "")

    return cliente_id, sessao_id, nome_cliente


def _buscar_identificadores_em_ciclo(ciclo):
    ciclo = obter_dict_seguro_governanca(ciclo)

    cliente_id = ciclo.get("cliente_id", "")
    sessao_id = ciclo.get("sessao_id", "")
    nome_cliente = ciclo.get("nome_cliente", "")

    if cliente_id and sessao_id and nome_cliente:
        return cliente_id, sessao_id, nome_cliente

    for chave_lista in CHAVES_LISTA_ITENS_CICLO:
        itens = ciclo.get(chave_lista)

        if not isinstance(itens, list):
            continue

        for item in itens:
            if not isinstance(item, dict):
                continue

            cliente_id_item, sessao_id_item, nome_cliente_item = _buscar_identificadores_em_item_loop(item)

            cliente_id = cliente_id or cliente_id_item
            sessao_id = sessao_id or sessao_id_item
            nome_cliente = nome_cliente or nome_cliente_item

            if cliente_id and sessao_id and nome_cliente:
                return cliente_id, sessao_id, nome_cliente

    return cliente_id, sessao_id, nome_cliente


def extrair_identificadores_governanca(
    registro_acompanhamento=None, snapshot_status=None, item_loop=None, ciclo_loop=None
):
    registro = obter_dict_seguro_governanca(registro_acompanhamento)
    snapshot = obter_dict_seguro_governanca(snapshot_status)
    item = obter_dict_seguro_governanca(item_loop)
    ciclo = obter_dict_seguro_governanca(ciclo_loop)

    snapshot_efetivo = snapshot if snapshot else obter_dict_seguro_governanca(item.get("snapshot_status"))

    cliente_id_ciclo, sessao_id_ciclo, nome_cliente_ciclo = _buscar_identificadores_em_ciclo(ciclo)

    cliente_id = (
        item.get("cliente_id") or snapshot_efetivo.get("cliente_id") or registro.get("cliente_id")
        or cliente_id_ciclo or ""
    )
    sessao_id = (
        item.get("sessao_id") or snapshot_efetivo.get("sessao_id") or registro.get("sessao_id")
        or sessao_id_ciclo or ""
    )
    nome_cliente = (
        item.get("nome_cliente") or snapshot_efetivo.get("nome_cliente") or registro.get("nome_cliente")
        or nome_cliente_ciclo or ""
    )
    status_star = item.get("status_star") or snapshot_efetivo.get("status_star") or ""
    status_conclusivo_geral = (
        item.get("status_conclusivo_geral") or snapshot_efetivo.get("status_conclusivo_geral") or ""
    )
    status_atual_acompanhamento = (
        item.get("status_atual_acompanhamento") or snapshot_efetivo.get("status_atual_acompanhamento") or ""
    )

    return {
        "cliente_id": str(cliente_id or ""),
        "sessao_id": str(sessao_id or ""),
        "nome_cliente": str(nome_cliente or ""),
        "registro_id": str(registro.get("registro_id", "") or ""),
        "snapshot_id": criar_snapshot_id_deterministico(snapshot_efetivo) if snapshot_efetivo else "",
        "item_loop_id": str(item.get("item_loop_id", "") or ""),
        "ciclo_id": str(ciclo.get("ciclo_id", "") or ""),
        "status_star": str(status_star or ""),
        "status_conclusivo_geral": str(status_conclusivo_geral or ""),
        "status_atual_acompanhamento": str(status_atual_acompanhamento or ""),
        "classificacao_loop": str(item.get("classificacao_loop", "") or ""),
    }


def criar_payload_registro_acompanhamento_persistivel(registro_acompanhamento=None, metadados=None):
    registro = obter_dict_seguro_governanca(registro_acompanhamento)
    identificadores = extrair_identificadores_governanca(registro_acompanhamento=registro)
    metadados_efetivos = metadados if metadados else criar_metadados_persistencia_governanca()

    payload = {
        "tipo_payload_governanca": "REGISTRO_ACOMPANHAMENTO",
        "versao_payload_governanca": VERSAO_PAYLOAD_GOVERNANCA,
        "registro_id": identificadores["registro_id"],
        "cliente_id": identificadores["cliente_id"],
        "sessao_id": identificadores["sessao_id"],
        "nome_cliente": identificadores["nome_cliente"],
        "dados_registro": garantir_json_serializavel(registro),
        "metadados_persistencia": metadados_efetivos,
    }

    json.dumps(payload)

    return payload


def criar_payload_snapshot_status_persistivel(snapshot_status=None, metadados=None):
    snapshot = obter_dict_seguro_governanca(snapshot_status)
    identificadores = extrair_identificadores_governanca(snapshot_status=snapshot)
    metadados_efetivos = metadados if metadados else criar_metadados_persistencia_governanca()

    payload = {
        "tipo_payload_governanca": "SNAPSHOT_STATUS",
        "versao_payload_governanca": VERSAO_PAYLOAD_GOVERNANCA,
        "snapshot_id": identificadores["snapshot_id"],
        "cliente_id": identificadores["cliente_id"],
        "sessao_id": identificadores["sessao_id"],
        "nome_cliente": identificadores["nome_cliente"],
        "status_atual_acompanhamento": identificadores["status_atual_acompanhamento"],
        "dados_snapshot": garantir_json_serializavel(snapshot),
        "metadados_persistencia": metadados_efetivos,
    }

    json.dumps(payload)

    return payload


def criar_payload_item_loop_persistivel(item_loop=None, metadados=None):
    item = obter_dict_seguro_governanca(item_loop)
    identificadores = extrair_identificadores_governanca(item_loop=item)
    metadados_efetivos = metadados if metadados else criar_metadados_persistencia_governanca()

    payload = {
        "tipo_payload_governanca": "ITEM_LOOP",
        "versao_payload_governanca": VERSAO_PAYLOAD_GOVERNANCA,
        "item_loop_id": identificadores["item_loop_id"],
        "cliente_id": identificadores["cliente_id"],
        "sessao_id": identificadores["sessao_id"],
        "nome_cliente": identificadores["nome_cliente"],
        "classificacao_loop": identificadores["classificacao_loop"],
        "entra_no_loop_ativo": bool(item.get("entra_no_loop_ativo", False)),
        "dados_item_loop": garantir_json_serializavel(item),
        "metadados_persistencia": metadados_efetivos,
    }

    json.dumps(payload)

    return payload


def criar_payload_ciclo_loop_persistivel(ciclo_loop=None, metadados=None):
    ciclo = obter_dict_seguro_governanca(ciclo_loop)
    identificadores = extrair_identificadores_governanca(ciclo_loop=ciclo)
    metadados_efetivos = metadados if metadados else criar_metadados_persistencia_governanca()

    payload = {
        "tipo_payload_governanca": "CICLO_LOOP",
        "versao_payload_governanca": VERSAO_PAYLOAD_GOVERNANCA,
        "ciclo_id": identificadores["ciclo_id"],
        "cliente_id": identificadores["cliente_id"],
        "sessao_id": identificadores["sessao_id"],
        "nome_cliente": identificadores["nome_cliente"],
        "tipo_ciclo": str(ciclo.get("tipo_ciclo", "") or ""),
        "periodo_referencia": str(ciclo.get("periodo_referencia", "") or ""),
        "origem": str(ciclo.get("origem", "") or ""),
        "total_itens": int(ciclo.get("total_itens", 0) or 0),
        "dados_ciclo_loop": garantir_json_serializavel(ciclo),
        "metadados_persistencia": metadados_efetivos,
    }

    json.dumps(payload)

    return payload


def criar_payload_governanca_integrada(
    registro_acompanhamento=None, snapshot_status=None, item_loop=None, ciclo_loop=None, metadados=None
):
    registro = obter_dict_seguro_governanca(registro_acompanhamento)
    snapshot = obter_dict_seguro_governanca(snapshot_status)
    item = obter_dict_seguro_governanca(item_loop)
    ciclo = obter_dict_seguro_governanca(ciclo_loop)

    identificadores = extrair_identificadores_governanca(
        registro_acompanhamento=registro, snapshot_status=snapshot, item_loop=item, ciclo_loop=ciclo
    )
    metadados_efetivos = metadados if metadados else criar_metadados_persistencia_governanca()

    governanca_id = gerar_id_deterministico(
        "GOVERNANCA_INTEGRADA",
        [
            identificadores["cliente_id"],
            identificadores["sessao_id"],
            identificadores["registro_id"],
            identificadores["snapshot_id"],
            identificadores["item_loop_id"],
            identificadores["ciclo_id"],
        ],
    )

    payload = {
        "tipo_payload_governanca": "GOVERNANCA_INTEGRADA",
        "versao_payload_governanca": VERSAO_PAYLOAD_GOVERNANCA,
        "governanca_id": governanca_id,
        "cliente_id": identificadores["cliente_id"],
        "sessao_id": identificadores["sessao_id"],
        "nome_cliente": identificadores["nome_cliente"],
        "registro_acompanhamento": garantir_json_serializavel(registro),
        "snapshot_status": garantir_json_serializavel(snapshot),
        "item_loop": garantir_json_serializavel(item),
        "ciclo_loop": garantir_json_serializavel(ciclo),
        "referencias": {
            "registro_id": identificadores["registro_id"],
            "snapshot_id": identificadores["snapshot_id"],
            "item_loop_id": identificadores["item_loop_id"],
            "ciclo_id": identificadores["ciclo_id"],
        },
        "metadados_persistencia": metadados_efetivos,
    }

    json.dumps(payload)

    return payload


def validar_payload_governanca(payload=None):
    erros = []
    avisos = []

    if not isinstance(payload, dict):
        return {"valido": False, "erros": ["payload deve ser um dicionario."], "avisos": []}

    tipo_payload = payload.get("tipo_payload_governanca", "")

    if not tipo_payload:
        erros.append("tipo_payload_governanca ausente.")
    elif tipo_payload not in TIPOS_PAYLOAD_GOVERNANCA:
        erros.append(f"tipo_payload_governanca invalido: {tipo_payload!r}.")

    if not payload.get("versao_payload_governanca"):
        erros.append("versao_payload_governanca ausente.")

    metadados = payload.get("metadados_persistencia")

    if not isinstance(metadados, dict):
        erros.append("metadados_persistencia ausente.")
    else:
        if metadados.get("persistido") is True:
            erros.append("Payload marcado como persistido=True — Sprint 7.2 nao deve persistir.")

        if metadados.get("persistencia_habilitada") is True:
            erros.append("Payload marcado como persistencia_habilitada=True — Sprint 7.2 nao habilita persistencia.")

    try:
        json.dumps(garantir_json_serializavel(payload))
    except Exception as exc:
        erros.append(f"Payload nao e serializavel: {exc}")

    campos_obrigatorios_por_tipo = {
        "REGISTRO_ACOMPANHAMENTO": "registro_id",
        "SNAPSHOT_STATUS": "snapshot_id",
        "ITEM_LOOP": "item_loop_id",
        "CICLO_LOOP": "ciclo_id",
        "GOVERNANCA_INTEGRADA": "governanca_id",
    }

    campo_obrigatorio = campos_obrigatorios_por_tipo.get(tipo_payload)

    if campo_obrigatorio and not payload.get(campo_obrigatorio):
        erros.append(f"Campo obrigatorio ausente ou vazio para {tipo_payload}: {campo_obrigatorio}.")

    if not payload.get("cliente_id"):
        avisos.append("cliente_id ausente.")

    if not payload.get("sessao_id"):
        avisos.append("sessao_id ausente.")

    return {
        "valido": len(erros) == 0,
        "erros": erros,
        "avisos": avisos,
    }


def validar_payloads_governanca(payloads=None):
    payloads_seguros = obter_lista_segura_contrato_governanca(payloads)

    erros = []
    avisos = []
    payloads_validos = 0
    payloads_invalidos = 0

    if not payloads_seguros:
        return {
            "valido": True,
            "total_payloads": 0,
            "payloads_validos": 0,
            "payloads_invalidos": 0,
            "erros": [],
            "avisos": ["Nenhum payload de governanca informado."],
        }

    for payload in payloads_seguros:
        resultado = validar_payload_governanca(payload)

        if resultado["valido"]:
            payloads_validos += 1
        else:
            payloads_invalidos += 1
            erros.extend(resultado["erros"])

        avisos.extend(resultado["avisos"])

    return {
        "valido": payloads_invalidos == 0,
        "total_payloads": len(payloads_seguros),
        "payloads_validos": payloads_validos,
        "payloads_invalidos": payloads_invalidos,
        "erros": erros,
        "avisos": avisos,
    }


def formatar_validacao_payload_governanca_texto(resultado=None):
    resultado = obter_dict_seguro_governanca(resultado)

    linhas = [
        f"Payload válido: {'SIM' if resultado.get('valido') else 'NAO'}",
        f"Erros: {len(resultado.get('erros') or [])}",
        f"Avisos: {len(resultado.get('avisos') or [])}",
    ]

    for erro in resultado.get("erros") or []:
        linhas.append(f"Erro: {erro}")

    for aviso in resultado.get("avisos") or []:
        linhas.append(f"Aviso: {aviso}")

    return linhas


def formatar_payload_governanca_resumo_texto(payload=None):
    payload = obter_dict_seguro_governanca(payload)
    metadados = obter_dict_seguro_governanca(payload.get("metadados_persistencia"))

    return [
        f"Tipo de payload: {payload.get('tipo_payload_governanca', '')}",
        f"Versão do payload: {payload.get('versao_payload_governanca', '')}",
        f"Cliente: {payload.get('nome_cliente', '')}",
        f"Sessão: {payload.get('sessao_id', '')}",
        f"Persistido: {'SIM' if metadados.get('persistido') else 'NAO'}",
        f"Persistência habilitada: {'SIM' if metadados.get('persistencia_habilitada') else 'NAO'}",
    ]
