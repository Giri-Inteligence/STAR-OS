import hashlib
import json
import math
import unicodedata
from datetime import datetime, timezone

from star_intelligence.pacote_investigativo import obter_lista_segura


MAPA_STATUS_SESSAO = {
    "ABERTA": "ABERTA",
    "EM ANDAMENTO": "EM_ANDAMENTO",
    "EM_ANDAMENTO": "EM_ANDAMENTO",
    "CONCLUIDA": "CONCLUIDA",
    "ARQUIVADA": "ARQUIVADA",
}


def _normalizar_texto_basico(valor):
    if valor is None:
        return ""

    if isinstance(valor, float) and valor != valor:
        return ""

    texto = " ".join(str(valor).strip().upper().split())

    if texto == "":
        return ""

    texto_decomposto = unicodedata.normalize("NFKD", texto)

    return "".join(c for c in texto_decomposto if not unicodedata.combining(c))


def _obter_campo(fonte, chave, padrao=""):
    if fonte is None:
        return padrao

    try:
        valor = fonte.get(chave, padrao)
    except AttributeError:
        try:
            valor = fonte[chave]
        except Exception:
            return padrao
    except Exception:
        return padrao

    if valor is None:
        return padrao

    if isinstance(valor, float) and valor != valor:
        return padrao

    return valor


def _obter_texto_campo(fonte, chave, padrao=""):
    valor = _obter_campo(fonte, chave, padrao)
    texto = str(valor).strip() if valor is not None else ""

    return texto if texto != "" else padrao


def _obter_numero_campo(fonte, chave, padrao=0.0):
    valor = _obter_campo(fonte, chave, padrao)

    try:
        numero = float(valor)

        if numero != numero:
            return padrao

        return numero
    except (TypeError, ValueError):
        return padrao


def limpar_valor_serializavel(valor):
    try:
        if valor is None:
            return None

        if isinstance(valor, bool):
            return valor

        if isinstance(valor, int):
            return valor

        if isinstance(valor, float):
            if math.isnan(valor) or math.isinf(valor):
                return None
            return valor

        if isinstance(valor, str):
            return valor

        if isinstance(valor, (list, tuple)):
            return [limpar_valor_serializavel(item) for item in valor]

        if isinstance(valor, dict):
            return {str(chave): limpar_valor_serializavel(item) for chave, item in valor.items()}

        return str(valor)
    except Exception:
        return None


def garantir_json_serializavel(payload):
    try:
        limpo = limpar_valor_serializavel(payload)
        json.dumps(limpo)

        return limpo
    except Exception:
        return {
            "erro_serializacao": True,
            "payload_original_tipo": str(type(payload)),
        }


def _normalizar_partes_para_hash(partes):
    if partes is None:
        return ""

    if isinstance(partes, dict):
        itens = sorted(partes.items(), key=lambda par: str(par[0]))
        return "|".join(f"{chave}={valor}" for chave, valor in itens)

    if isinstance(partes, (list, tuple)):
        return "|".join(str(item) for item in partes)

    return str(partes)


def gerar_id_deterministico(prefixo, partes):
    prefixo_normalizado = str(prefixo).strip().upper() if prefixo else "ID"

    texto_partes = _normalizar_partes_para_hash(partes)

    hash_completo = hashlib.sha256(texto_partes.encode("utf-8")).hexdigest()
    hash_curto = hash_completo[:12].upper()

    return f"{prefixo_normalizado}_{hash_curto}"


def gerar_timestamp_iso(valor=None):
    try:
        if valor is None:
            return datetime.now(timezone.utc).isoformat()

        if isinstance(valor, str):
            return valor if valor.strip() != "" else datetime.now(timezone.utc).isoformat()

        if hasattr(valor, "isoformat"):
            return valor.isoformat()

        return str(valor)
    except Exception:
        return str(valor) if valor is not None else ""


def normalizar_status_sessao(status):
    texto = _normalizar_texto_basico(status)

    return MAPA_STATUS_SESSAO.get(texto, "ABERTA")


def criar_cliente_investigado(
    nome_cliente="",
    vendedor="",
    cidade="",
    origem_cliente_coluna="",
    origem_vendedor_coluna="",
    origem_cidade_coluna="",
    criado_em=None,
):
    timestamp = gerar_timestamp_iso(criado_em)

    cliente_id = gerar_id_deterministico("CLIENTE", [nome_cliente or "", vendedor or "", cidade or ""])

    return {
        "cliente_id": cliente_id,
        "nome_cliente": str(nome_cliente or ""),
        "vendedor": str(vendedor or ""),
        "cidade": str(cidade or ""),
        "origem_cliente_coluna": str(origem_cliente_coluna or ""),
        "origem_vendedor_coluna": str(origem_vendedor_coluna or ""),
        "origem_cidade_coluna": str(origem_cidade_coluna or ""),
        "criado_em": timestamp,
        "atualizado_em": timestamp,
    }


def criar_sessao_investigativa(
    cliente_id="",
    origem="STREAMLIT_SESSION",
    usuario_responsavel="",
    status_sessao="ABERTA",
    versao_modelo="5.2",
    criado_em=None,
):
    timestamp = gerar_timestamp_iso(criado_em)
    status_normalizado = normalizar_status_sessao(status_sessao)

    sessao_id = gerar_id_deterministico(
        "SESSAO", [cliente_id or "", origem or "", usuario_responsavel or "", timestamp]
    )

    return {
        "sessao_id": sessao_id,
        "cliente_id": str(cliente_id or ""),
        "data_sessao": timestamp,
        "origem": str(origem or ""),
        "usuario_responsavel": str(usuario_responsavel or ""),
        "status_sessao": status_normalizado,
        "versao_modelo": str(versao_modelo or ""),
        "criado_em": timestamp,
        "atualizado_em": timestamp,
    }


def criar_snapshot_star(linha_star=None, sessao_id="", cliente_id="", criado_em=None):
    timestamp = gerar_timestamp_iso(criado_em)
    linha_star = linha_star if linha_star is not None else {}

    snapshot_id = gerar_id_deterministico("SNAPSHOT", [sessao_id or "", cliente_id or "", timestamp])

    return {
        "snapshot_id": snapshot_id,
        "sessao_id": str(sessao_id or ""),
        "cliente_id": str(cliente_id or ""),
        "status_star": _obter_texto_campo(linha_star, "STATUS"),
        "curva": _obter_texto_campo(linha_star, "CURVA"),
        "media_lp": _obter_numero_campo(linha_star, "MEDIA LP"),
        "media_cp": _obter_numero_campo(linha_star, "MEDIA CP"),
        "meses_sem_compra": _obter_numero_campo(linha_star, "MESES_SEM_COMPRA"),
        "erosao_star": _obter_numero_campo(linha_star, "EROSAO STAR"),
        "meta": _obter_numero_campo(linha_star, "META"),
        "acao": _obter_texto_campo(linha_star, "ACAO"),
        "criado_em": timestamp,
    }


def criar_itens_investigativos_payload(itens=None, sessao_id="", criado_em=None):
    timestamp = gerar_timestamp_iso(criado_em)
    payload_itens = []

    for item in obter_lista_segura(itens):
        if not isinstance(item, dict):
            continue

        id_item = item.get("id_item", "")
        pergunta = item.get("pergunta", "")

        item_id = gerar_id_deterministico("ITEM", [sessao_id or "", id_item or "", pergunta or ""])

        payload_itens.append({
            "item_id": item_id,
            "sessao_id": str(sessao_id or ""),
            "origem": str(item.get("origem", "") or ""),
            "pergunta": str(pergunta or ""),
            "status_investigativo": str(item.get("status", "") or ""),
            "resposta": str(item.get("resposta", "") or ""),
            "evidencia_textual": str(item.get("evidencia", "") or ""),
            "criado_em": timestamp,
            "atualizado_em": timestamp,
        })

    return payload_itens


def criar_pacote_investigativo_payload(pacote_investigativo=None, sessao_id="", cliente_id="", criado_em=None):
    timestamp = gerar_timestamp_iso(criado_em)
    pacote_investigativo = pacote_investigativo if isinstance(pacote_investigativo, dict) else {}

    pacote_id = gerar_id_deterministico("PACOTE", [sessao_id or "", cliente_id or "", timestamp])

    return {
        "pacote_id": pacote_id,
        "sessao_id": str(sessao_id or ""),
        "cliente_id": str(cliente_id or ""),
        "status_star": str(pacote_investigativo.get("status_star", "") or ""),
        "curva": str(pacote_investigativo.get("curva", "") or ""),
        "nivel_prioridade": str(pacote_investigativo.get("nivel_prioridade", "") or ""),
        "tipo_prioridade": str(pacote_investigativo.get("tipo_prioridade", "") or ""),
        "resumo_hipotese": str(pacote_investigativo.get("resumo_hipotese", "") or ""),
        "resumo_investigacao": dict(pacote_investigativo.get("resumo_investigacao") or {}),
        "maturidade_investigacao": str(pacote_investigativo.get("maturidade_investigacao", "") or ""),
        "leitura_consolidada": str(pacote_investigativo.get("leitura_consolidada", "") or ""),
        "criado_em": timestamp,
    }


def criar_conclusao_investigativa_payload(conclusao_investigativa=None, pacote_id="", sessao_id="", criado_em=None):
    timestamp = gerar_timestamp_iso(criado_em)
    conclusao_investigativa = conclusao_investigativa if isinstance(conclusao_investigativa, dict) else {}

    resumo = conclusao_investigativa.get("resumo_conclusao") or {}

    conclusao_id = gerar_id_deterministico("CONCLUSAO", [pacote_id or "", sessao_id or "", timestamp])

    return {
        "conclusao_id": conclusao_id,
        "pacote_id": str(pacote_id or ""),
        "sessao_id": str(sessao_id or ""),
        "status_conclusivo_geral": str(resumo.get("status_conclusivo_geral", "") or ""),
        "leitura_conclusao": str(conclusao_investigativa.get("leitura_conclusao", "") or ""),
        "hipoteses_confirmadas_count": int(resumo.get("hipoteses_confirmadas", 0) or 0),
        "hipoteses_descartadas_count": int(resumo.get("hipoteses_descartadas", 0) or 0),
        "hipoteses_inconclusivas_count": int(resumo.get("hipoteses_inconclusivas", 0) or 0),
        "pendentes_validacao_count": int(resumo.get("pendentes_validacao", 0) or 0),
        "respostas_sem_classificacao_count": int(resumo.get("respostas_sem_classificacao", 0) or 0),
        "criado_em": timestamp,
    }


def criar_metadados_execucao(
    sessao_id="",
    arquivo_origem_nome="",
    data_upload=None,
    versao_star_os="",
    versao_modelo_persistencia="5.2",
    ambiente="LOCAL",
    observacoes="",
):
    timestamp_upload = gerar_timestamp_iso(data_upload)

    execucao_id = gerar_id_deterministico(
        "EXECUCAO", [sessao_id or "", arquivo_origem_nome or "", timestamp_upload]
    )

    return {
        "execucao_id": execucao_id,
        "sessao_id": str(sessao_id or ""),
        "arquivo_origem_nome": str(arquivo_origem_nome or ""),
        "data_upload": timestamp_upload,
        "versao_star_os": str(versao_star_os or ""),
        "versao_modelo_persistencia": str(versao_modelo_persistencia or ""),
        "ambiente": str(ambiente or ""),
        "observacoes": str(observacoes or ""),
    }


def criar_payload_historico_investigativo(
    nome_cliente="",
    vendedor="",
    cidade="",
    origem_cliente_coluna="",
    origem_vendedor_coluna="",
    origem_cidade_coluna="",
    linha_star=None,
    itens_investigativos=None,
    pacote_investigativo=None,
    conclusao_investigativa=None,
    arquivo_origem_nome="",
    usuario_responsavel="",
    criado_em=None,
):
    timestamp = gerar_timestamp_iso(criado_em)

    cliente_payload = criar_cliente_investigado(
        nome_cliente=nome_cliente,
        vendedor=vendedor,
        cidade=cidade,
        origem_cliente_coluna=origem_cliente_coluna,
        origem_vendedor_coluna=origem_vendedor_coluna,
        origem_cidade_coluna=origem_cidade_coluna,
        criado_em=timestamp,
    )

    sessao_payload = criar_sessao_investigativa(
        cliente_id=cliente_payload["cliente_id"],
        usuario_responsavel=usuario_responsavel,
        criado_em=timestamp,
    )

    snapshot_payload = criar_snapshot_star(
        linha_star=linha_star,
        sessao_id=sessao_payload["sessao_id"],
        cliente_id=cliente_payload["cliente_id"],
        criado_em=timestamp,
    )

    itens_payload = criar_itens_investigativos_payload(
        itens=itens_investigativos,
        sessao_id=sessao_payload["sessao_id"],
        criado_em=timestamp,
    )

    pacote_payload = criar_pacote_investigativo_payload(
        pacote_investigativo=pacote_investigativo,
        sessao_id=sessao_payload["sessao_id"],
        cliente_id=cliente_payload["cliente_id"],
        criado_em=timestamp,
    )

    conclusao_payload = criar_conclusao_investigativa_payload(
        conclusao_investigativa=conclusao_investigativa,
        pacote_id=pacote_payload["pacote_id"],
        sessao_id=sessao_payload["sessao_id"],
        criado_em=timestamp,
    )

    metadados_payload = criar_metadados_execucao(
        sessao_id=sessao_payload["sessao_id"],
        arquivo_origem_nome=arquivo_origem_nome,
        data_upload=timestamp,
    )

    payload = {
        "versao_contrato": "5.2",
        "cliente": cliente_payload,
        "sessao": sessao_payload,
        "snapshot_star": snapshot_payload,
        "itens_investigativos": itens_payload,
        "pacote_investigativo": pacote_payload,
        "conclusao_investigativa": conclusao_payload,
        "metadados_execucao": metadados_payload,
    }

    return garantir_json_serializavel(payload)


def validar_payload_historico(payload):
    try:
        erros = []
        avisos = []

        if not isinstance(payload, dict):
            return {"valido": False, "erros": ["payload nao e um dicionario."], "avisos": []}

        if "versao_contrato" not in payload:
            erros.append("versao_contrato ausente.")

        cliente = payload.get("cliente")
        if not isinstance(cliente, dict):
            erros.append("cliente ausente ou invalido.")
        elif not cliente.get("cliente_id"):
            erros.append("cliente.cliente_id ausente.")

        sessao = payload.get("sessao")
        if not isinstance(sessao, dict):
            erros.append("sessao ausente ou invalida.")
        elif not sessao.get("sessao_id"):
            erros.append("sessao.sessao_id ausente.")

        if not isinstance(payload.get("snapshot_star"), dict):
            erros.append("snapshot_star ausente ou invalido.")

        itens = payload.get("itens_investigativos")
        if not isinstance(itens, list):
            erros.append("itens_investigativos nao e uma lista.")
        elif len(itens) == 0:
            avisos.append("Nenhum item investigativo informado.")

        if not isinstance(payload.get("pacote_investigativo"), dict):
            erros.append("pacote_investigativo ausente ou invalido.")

        if not isinstance(payload.get("conclusao_investigativa"), dict):
            erros.append("conclusao_investigativa ausente ou invalido.")

        metadados = payload.get("metadados_execucao")
        if not isinstance(metadados, dict):
            erros.append("metadados_execucao ausente ou invalido.")
        elif not metadados.get("arquivo_origem_nome"):
            avisos.append("Nenhum arquivo_origem_nome informado.")

        try:
            json.dumps(payload)
        except Exception:
            erros.append("payload nao e serializavel com json.dumps.")

        return {
            "valido": len(erros) == 0,
            "erros": erros,
            "avisos": avisos,
        }
    except Exception:
        return {"valido": False, "erros": ["falha inesperada ao validar payload."], "avisos": []}


def formatar_validacao_payload_texto(resultado):
    resultado = resultado or {}

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
