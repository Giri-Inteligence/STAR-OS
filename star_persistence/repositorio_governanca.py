"""
star_persistence.repositorio_governanca

Repositório local SQLite controlado para persistir payloads de
Governança (Sprint 7.3), validados pelo contrato da Sprint 7.2. Cria
schema próprio de governança, separado do schema do Histórico
Investigativo (Sprint 5.3) — não altera nem consulta aquele schema.
Nenhum banco é criado automaticamente no import; a criação do schema
exige chamada explícita com caminho de banco informado.
"""

import json
import sqlite3
from pathlib import Path

from star_persistence.contrato_governanca import (
    validar_payload_governanca,
    normalizar_tipo_payload_governanca,
)
from star_persistence.contrato_historico import (
    garantir_json_serializavel,
    gerar_timestamp_iso,
)

VERSAO_SCHEMA_GOVERNANCA = "7.3"

TIPOS_PAYLOAD_GOVERNANCA_ESPERADOS = (
    "REGISTRO_ACOMPANHAMENTO",
    "SNAPSHOT_STATUS",
    "ITEM_LOOP",
    "CICLO_LOOP",
    "GOVERNANCA_INTEGRADA",
)

CAMPOS_IDENTIFICADOR_POR_TIPO = {
    "REGISTRO_ACOMPANHAMENTO": "registro_id",
    "SNAPSHOT_STATUS": "snapshot_id",
    "ITEM_LOOP": "item_loop_id",
    "CICLO_LOOP": "ciclo_id",
    "GOVERNANCA_INTEGRADA": "governanca_id",
}

SCHEMA_SQL_GOVERNANCA = (
    """
    CREATE TABLE IF NOT EXISTS governanca_schema_info (
        chave TEXT PRIMARY KEY,
        valor TEXT NOT NULL,
        criado_em TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS governanca_payloads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_payload_governanca TEXT NOT NULL,
        payload_id TEXT NOT NULL,
        cliente_id TEXT,
        sessao_id TEXT,
        nome_cliente TEXT,
        origem TEXT,
        criado_em_payload TEXT,
        criado_em_repositorio TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        UNIQUE(tipo_payload_governanca, payload_id)
    )
    """,
)


def normalizar_caminho_banco_governanca(caminho_banco):
    if not caminho_banco:
        return None

    return Path(caminho_banco)


def obter_conexao_governanca(caminho_banco):
    caminho_normalizado = normalizar_caminho_banco_governanca(caminho_banco)

    if caminho_normalizado is None:
        raise ValueError("caminho_banco e obrigatorio para abrir conexao com o repositorio de governanca.")

    caminho_normalizado.parent.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(str(caminho_normalizado))
    conexao.row_factory = sqlite3.Row

    return conexao


def inicializar_schema_governanca(caminho_banco):
    resultado = {
        "inicializado": False,
        "caminho_banco": str(caminho_banco or ""),
        "tabelas": [],
        "erros": [],
        "avisos": [],
    }

    conexao = obter_conexao_governanca(caminho_banco)

    try:
        for comando in SCHEMA_SQL_GOVERNANCA:
            conexao.execute(comando)

        conexao.execute(
            "INSERT OR REPLACE INTO governanca_schema_info (chave, valor, criado_em) VALUES (?, ?, ?)",
            ("schema", "GOVERNANCA_LOCAL", gerar_timestamp_iso()),
        )
        conexao.execute(
            "INSERT OR REPLACE INTO governanca_schema_info (chave, valor, criado_em) VALUES (?, ?, ?)",
            ("versao_schema_governanca", VERSAO_SCHEMA_GOVERNANCA, gerar_timestamp_iso()),
        )

        conexao.commit()

        resultado["inicializado"] = True
        resultado["tabelas"] = ["governanca_schema_info", "governanca_payloads"]
    except Exception as exc:
        conexao.rollback()
        resultado["erros"].append(f"Erro ao inicializar schema: {exc}")
    finally:
        conexao.close()

    return resultado


def verificar_schema_governanca(caminho_banco):
    resultado = {
        "valido": False,
        "caminho_banco": str(caminho_banco or ""),
        "tabelas_encontradas": [],
        "tabelas_ausentes": [],
        "erros": [],
        "avisos": [],
    }

    tabelas_esperadas = ("governanca_schema_info", "governanca_payloads")

    try:
        conexao = obter_conexao_governanca(caminho_banco)
    except Exception as exc:
        resultado["erros"].append(f"Erro ao abrir banco: {exc}")
        resultado["tabelas_ausentes"] = list(tabelas_esperadas)
        return resultado

    try:
        cursor = conexao.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas_no_banco = {linha["name"] for linha in cursor.fetchall()}
    except sqlite3.OperationalError as exc:
        resultado["erros"].append(f"Erro ao consultar schema: {exc}")
        tabelas_no_banco = set()
    finally:
        conexao.close()

    tabelas_encontradas = [tabela for tabela in tabelas_esperadas if tabela in tabelas_no_banco]
    tabelas_ausentes = [tabela for tabela in tabelas_esperadas if tabela not in tabelas_no_banco]

    resultado["tabelas_encontradas"] = tabelas_encontradas
    resultado["tabelas_ausentes"] = tabelas_ausentes
    resultado["valido"] = len(tabelas_ausentes) == 0

    return resultado


def extrair_payload_id_governanca(payload):
    if not isinstance(payload, dict):
        return ""

    tipo_payload = payload.get("tipo_payload_governanca", "")
    campo_identificador = CAMPOS_IDENTIFICADOR_POR_TIPO.get(tipo_payload)

    if not campo_identificador:
        return ""

    return str(payload.get(campo_identificador, "") or "")


def preparar_linha_payload_governanca(payload):
    resultado_validacao = validar_payload_governanca(payload)

    resultado = {
        "valido": resultado_validacao["valido"],
        "linha": {},
        "erros": list(resultado_validacao["erros"]),
        "avisos": list(resultado_validacao["avisos"]),
    }

    if not resultado["valido"]:
        return resultado

    payload_limpo = garantir_json_serializavel(payload)
    tipo_payload = normalizar_tipo_payload_governanca(payload.get("tipo_payload_governanca", ""))
    payload_id = extrair_payload_id_governanca(payload)

    metadados = payload.get("metadados_persistencia") or {}

    resultado["linha"] = {
        "tipo_payload_governanca": tipo_payload,
        "payload_id": payload_id,
        "cliente_id": str(payload.get("cliente_id", "") or ""),
        "sessao_id": str(payload.get("sessao_id", "") or ""),
        "nome_cliente": str(payload.get("nome_cliente", "") or ""),
        "origem": str(metadados.get("origem", "") or ""),
        "criado_em_payload": str(metadados.get("criado_em", "") or ""),
        "criado_em_repositorio": gerar_timestamp_iso(),
        "payload_json": json.dumps(payload_limpo, ensure_ascii=False, sort_keys=True),
    }

    return resultado


def payload_governanca_existe(caminho_banco, tipo_payload_governanca, payload_id):
    if not tipo_payload_governanca or not payload_id:
        return False

    tipo_normalizado = normalizar_tipo_payload_governanca(tipo_payload_governanca)

    try:
        conexao = obter_conexao_governanca(caminho_banco)
    except Exception:
        return False

    try:
        cursor = conexao.execute(
            "SELECT 1 FROM governanca_payloads WHERE tipo_payload_governanca = ? AND payload_id = ?",
            (tipo_normalizado, payload_id),
        )
        return cursor.fetchone() is not None
    except sqlite3.OperationalError:
        return False
    finally:
        conexao.close()


def salvar_payload_governanca(caminho_banco, payload, sobrescrever=False):
    resultado = {
        "salvo": False,
        "duplicado": False,
        "tipo_payload_governanca": "",
        "payload_id": "",
        "caminho_banco": str(caminho_banco or ""),
        "erros": [],
        "avisos": [],
    }

    preparo = preparar_linha_payload_governanca(payload)

    if not preparo["valido"]:
        resultado["erros"] = preparo["erros"]
        resultado["avisos"] = preparo["avisos"]
        return resultado

    linha = preparo["linha"]
    resultado["tipo_payload_governanca"] = linha["tipo_payload_governanca"]
    resultado["payload_id"] = linha["payload_id"]
    resultado["avisos"] = list(preparo["avisos"])

    inicializar_schema_governanca(caminho_banco)

    ja_existe = payload_governanca_existe(caminho_banco, linha["tipo_payload_governanca"], linha["payload_id"])

    if ja_existe and not sobrescrever:
        resultado["duplicado"] = True
        resultado["avisos"].append("Payload ja existe no repositorio e nao foi sobrescrito.")
        return resultado

    conexao = obter_conexao_governanca(caminho_banco)

    try:
        conexao.execute(
            """
            INSERT OR REPLACE INTO governanca_payloads (
                tipo_payload_governanca, payload_id, cliente_id, sessao_id, nome_cliente,
                origem, criado_em_payload, criado_em_repositorio, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                linha["tipo_payload_governanca"],
                linha["payload_id"],
                linha["cliente_id"],
                linha["sessao_id"],
                linha["nome_cliente"],
                linha["origem"],
                linha["criado_em_payload"],
                linha["criado_em_repositorio"],
                linha["payload_json"],
            ),
        )
        conexao.commit()
        resultado["salvo"] = True
    except Exception as exc:
        conexao.rollback()
        resultado["erros"].append(f"Erro ao salvar payload: {exc}")
    finally:
        conexao.close()

    return resultado


def carregar_payload_governanca(caminho_banco, tipo_payload_governanca, payload_id):
    tipo_normalizado = normalizar_tipo_payload_governanca(tipo_payload_governanca) if tipo_payload_governanca else ""

    resultado = {
        "encontrado": False,
        "payload": {},
        "tipo_payload_governanca": tipo_normalizado,
        "payload_id": str(payload_id or ""),
        "erros": [],
        "avisos": [],
    }

    if not tipo_normalizado or not payload_id:
        resultado["avisos"].append("tipo_payload_governanca ou payload_id ausente.")
        return resultado

    try:
        conexao = obter_conexao_governanca(caminho_banco)
    except Exception as exc:
        resultado["erros"].append(f"Erro ao abrir banco: {exc}")
        return resultado

    try:
        cursor = conexao.execute(
            "SELECT payload_json FROM governanca_payloads WHERE tipo_payload_governanca = ? AND payload_id = ?",
            (tipo_normalizado, payload_id),
        )
        linha = cursor.fetchone()
    except sqlite3.OperationalError as exc:
        resultado["erros"].append(f"Erro ao consultar payload: {exc}")
        linha = None
    finally:
        conexao.close()

    if linha is None:
        return resultado

    try:
        resultado["payload"] = json.loads(linha["payload_json"])
        resultado["encontrado"] = True
    except Exception as exc:
        resultado["erros"].append(f"Erro ao decodificar payload: {exc}")

    return resultado


def listar_payloads_governanca(caminho_banco, tipo_payload_governanca=None, cliente_id=None, sessao_id=None, limite=100):
    condicoes = []
    parametros = []

    if tipo_payload_governanca:
        condicoes.append("tipo_payload_governanca = ?")
        parametros.append(normalizar_tipo_payload_governanca(tipo_payload_governanca))

    if cliente_id:
        condicoes.append("cliente_id = ?")
        parametros.append(cliente_id)

    if sessao_id:
        condicoes.append("sessao_id = ?")
        parametros.append(sessao_id)

    clausula_where = f"WHERE {' AND '.join(condicoes)}" if condicoes else ""

    try:
        conexao = obter_conexao_governanca(caminho_banco)
    except Exception:
        return []

    try:
        cursor = conexao.execute(
            f"""
            SELECT tipo_payload_governanca, payload_id, cliente_id, sessao_id, nome_cliente,
                   origem, criado_em_payload, criado_em_repositorio, payload_json
            FROM governanca_payloads
            {clausula_where}
            ORDER BY criado_em_repositorio DESC
            LIMIT ?
            """,
            (*parametros, int(limite or 100)),
        )
        linhas = cursor.fetchall()
    except sqlite3.OperationalError:
        linhas = []
    finally:
        conexao.close()

    resultado = []

    for linha in linhas:
        try:
            payload_decodificado = json.loads(linha["payload_json"])
        except Exception:
            payload_decodificado = {}

        resultado.append(
            {
                "tipo_payload_governanca": linha["tipo_payload_governanca"],
                "payload_id": linha["payload_id"],
                "cliente_id": linha["cliente_id"],
                "sessao_id": linha["sessao_id"],
                "nome_cliente": linha["nome_cliente"],
                "origem": linha["origem"],
                "criado_em_payload": linha["criado_em_payload"],
                "criado_em_repositorio": linha["criado_em_repositorio"],
                "payload": payload_decodificado,
            }
        )

    return resultado


def salvar_lote_payloads_governanca(caminho_banco, payloads=None, sobrescrever=False):
    payloads_seguros = payloads if isinstance(payloads, list) else ([] if payloads is None else [payloads])

    resultado = {
        "total_payloads": len(payloads_seguros),
        "salvos": 0,
        "duplicados": 0,
        "invalidos": 0,
        "erros": [],
        "avisos": [],
    }

    for payload in payloads_seguros:
        resultado_individual = salvar_payload_governanca(caminho_banco, payload, sobrescrever=sobrescrever)

        if resultado_individual["salvo"]:
            resultado["salvos"] += 1
        elif resultado_individual["duplicado"]:
            resultado["duplicados"] += 1
        else:
            resultado["invalidos"] += 1

        resultado["erros"].extend(resultado_individual["erros"])
        resultado["avisos"].extend(resultado_individual["avisos"])

    return resultado


def contar_registros_repositorio_governanca(caminho_banco):
    resultado = {
        "total_payloads": 0,
        "por_tipo": {tipo: 0 for tipo in TIPOS_PAYLOAD_GOVERNANCA_ESPERADOS},
        "erros": [],
        "avisos": [],
    }

    try:
        conexao = obter_conexao_governanca(caminho_banco)
    except Exception:
        resultado["avisos"].append("Banco de governanca nao existe ou nao pode ser aberto.")
        return resultado

    try:
        cursor = conexao.execute(
            "SELECT tipo_payload_governanca, COUNT(*) AS total FROM governanca_payloads GROUP BY tipo_payload_governanca"
        )
        linhas = cursor.fetchall()

        for linha in linhas:
            tipo = linha["tipo_payload_governanca"]

            if tipo in resultado["por_tipo"]:
                resultado["por_tipo"][tipo] = linha["total"]

            resultado["total_payloads"] += linha["total"]
    except sqlite3.OperationalError:
        resultado["avisos"].append("Schema de governanca ainda nao inicializado.")
    finally:
        conexao.close()

    return resultado


def validar_integridade_repositorio_governanca(caminho_banco):
    resultado = {
        "valido": True,
        "total_payloads": 0,
        "payloads_validos": 0,
        "payloads_invalidos": 0,
        "erros": [],
        "avisos": [],
    }

    payloads = listar_payloads_governanca(caminho_banco, limite=100000)

    if not payloads:
        resultado["avisos"].append("Repositorio de governanca sem payloads.")
        return resultado

    resultado["total_payloads"] = len(payloads)

    for registro in payloads:
        payload = registro.get("payload")
        resultado_validacao = validar_payload_governanca(payload)

        if resultado_validacao["valido"]:
            resultado["payloads_validos"] += 1
        else:
            resultado["payloads_invalidos"] += 1
            resultado["erros"].extend(resultado_validacao["erros"])

    resultado["valido"] = resultado["payloads_invalidos"] == 0

    return resultado


def formatar_resumo_repositorio_governanca(resumo=None):
    resumo = resumo or {}
    por_tipo = resumo.get("por_tipo") or {}

    return [
        f"Total de payloads: {resumo.get('total_payloads', 0)}",
        f"Registros de acompanhamento: {por_tipo.get('REGISTRO_ACOMPANHAMENTO', 0)}",
        f"Snapshots de status: {por_tipo.get('SNAPSHOT_STATUS', 0)}",
        f"Itens de loop: {por_tipo.get('ITEM_LOOP', 0)}",
        f"Ciclos de loop: {por_tipo.get('CICLO_LOOP', 0)}",
        f"Governanças integradas: {por_tipo.get('GOVERNANCA_INTEGRADA', 0)}",
    ]


def formatar_validacao_repositorio_governanca(resultado=None):
    resultado = resultado or {}

    linhas = [
        f"Repositório válido: {'SIM' if resultado.get('valido') else 'NAO'}",
        f"Total de payloads: {resultado.get('total_payloads', 0)}",
        f"Payloads válidos: {resultado.get('payloads_validos', 0)}",
        f"Payloads inválidos: {resultado.get('payloads_invalidos', 0)}",
        f"Erros: {len(resultado.get('erros') or [])}",
        f"Avisos: {len(resultado.get('avisos') or [])}",
    ]

    for erro in resultado.get("erros") or []:
        linhas.append(f"Erro: {erro}")

    for aviso in resultado.get("avisos") or []:
        linhas.append(f"Aviso: {aviso}")

    return linhas
