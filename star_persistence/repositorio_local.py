import json
import sqlite3

from star_persistence.contrato_historico import (
    garantir_json_serializavel,
    validar_payload_historico,
    gerar_timestamp_iso,
)


TABELAS_ESPERADAS = (
    "clientes_investigados",
    "sessoes_investigativas",
    "snapshots_star",
    "itens_investigativos",
    "pacotes_investigativos",
    "conclusoes_investigativas",
    "metadados_execucao",
    "payloads_historico",
)

SCHEMA_SQL = (
    """
    CREATE TABLE IF NOT EXISTS clientes_investigados (
        cliente_id TEXT PRIMARY KEY,
        nome_cliente TEXT,
        vendedor TEXT,
        cidade TEXT,
        origem_cliente_coluna TEXT,
        origem_vendedor_coluna TEXT,
        origem_cidade_coluna TEXT,
        criado_em TEXT,
        atualizado_em TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sessoes_investigativas (
        sessao_id TEXT PRIMARY KEY,
        cliente_id TEXT NOT NULL,
        data_sessao TEXT,
        origem TEXT,
        usuario_responsavel TEXT,
        status_sessao TEXT,
        versao_modelo TEXT,
        criado_em TEXT,
        atualizado_em TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes_investigados(cliente_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS snapshots_star (
        snapshot_id TEXT PRIMARY KEY,
        sessao_id TEXT NOT NULL,
        cliente_id TEXT NOT NULL,
        status_star TEXT,
        curva TEXT,
        media_lp REAL,
        media_cp REAL,
        meses_sem_compra REAL,
        erosao_star REAL,
        meta REAL,
        acao TEXT,
        criado_em TEXT,
        FOREIGN KEY(sessao_id) REFERENCES sessoes_investigativas(sessao_id),
        FOREIGN KEY(cliente_id) REFERENCES clientes_investigados(cliente_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS itens_investigativos (
        item_id TEXT PRIMARY KEY,
        sessao_id TEXT NOT NULL,
        origem TEXT,
        pergunta TEXT,
        status_investigativo TEXT,
        resposta TEXT,
        evidencia_textual TEXT,
        criado_em TEXT,
        atualizado_em TEXT,
        FOREIGN KEY(sessao_id) REFERENCES sessoes_investigativas(sessao_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS pacotes_investigativos (
        pacote_id TEXT PRIMARY KEY,
        sessao_id TEXT NOT NULL,
        cliente_id TEXT NOT NULL,
        status_star TEXT,
        curva TEXT,
        nivel_prioridade TEXT,
        tipo_prioridade TEXT,
        resumo_hipotese TEXT,
        resumo_investigacao_json TEXT,
        maturidade_investigacao TEXT,
        leitura_consolidada TEXT,
        criado_em TEXT,
        FOREIGN KEY(sessao_id) REFERENCES sessoes_investigativas(sessao_id),
        FOREIGN KEY(cliente_id) REFERENCES clientes_investigados(cliente_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS conclusoes_investigativas (
        conclusao_id TEXT PRIMARY KEY,
        pacote_id TEXT NOT NULL,
        sessao_id TEXT NOT NULL,
        status_conclusivo_geral TEXT,
        leitura_conclusao TEXT,
        hipoteses_confirmadas_count INTEGER,
        hipoteses_descartadas_count INTEGER,
        hipoteses_inconclusivas_count INTEGER,
        pendentes_validacao_count INTEGER,
        respostas_sem_classificacao_count INTEGER,
        criado_em TEXT,
        FOREIGN KEY(pacote_id) REFERENCES pacotes_investigativos(pacote_id),
        FOREIGN KEY(sessao_id) REFERENCES sessoes_investigativas(sessao_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS metadados_execucao (
        execucao_id TEXT PRIMARY KEY,
        sessao_id TEXT NOT NULL,
        arquivo_origem_nome TEXT,
        data_upload TEXT,
        versao_star_os TEXT,
        versao_modelo_persistencia TEXT,
        ambiente TEXT,
        observacoes TEXT,
        FOREIGN KEY(sessao_id) REFERENCES sessoes_investigativas(sessao_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS payloads_historico (
        sessao_id TEXT PRIMARY KEY,
        payload_json TEXT NOT NULL,
        salvo_em TEXT,
        FOREIGN KEY(sessao_id) REFERENCES sessoes_investigativas(sessao_id)
    )
    """,
)


def obter_conexao(db_path):
    if not db_path:
        raise ValueError("db_path e obrigatorio para abrir conexao com o repositorio local.")

    conexao = sqlite3.connect(str(db_path))
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def inicializar_schema(db_path):
    conexao = obter_conexao(db_path)

    try:
        for comando in SCHEMA_SQL:
            conexao.execute(comando)
        conexao.commit()
    finally:
        conexao.close()

    return {
        "ok": True,
        "tabelas": list(TABELAS_ESPERADAS),
        "db_path": str(db_path),
    }


def verificar_schema(db_path):
    conexao = obter_conexao(db_path)

    try:
        cursor = conexao.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas_no_banco = {linha["name"] for linha in cursor.fetchall()}
    finally:
        conexao.close()

    tabelas_encontradas = [tabela for tabela in TABELAS_ESPERADAS if tabela in tabelas_no_banco]
    tabelas_faltantes = [tabela for tabela in TABELAS_ESPERADAS if tabela not in tabelas_no_banco]

    return {
        "ok": len(tabelas_faltantes) == 0,
        "tabelas_encontradas": tabelas_encontradas,
        "tabelas_faltantes": tabelas_faltantes,
    }


def sessao_existe(db_path, sessao_id):
    if not sessao_id:
        return False

    conexao = obter_conexao(db_path)

    try:
        cursor = conexao.execute("SELECT 1 FROM sessoes_investigativas WHERE sessao_id = ?", (sessao_id,))
        return cursor.fetchone() is not None
    except sqlite3.OperationalError:
        return False
    finally:
        conexao.close()


def salvar_payload_historico(db_path, payload, permitir_atualizacao=False):
    validacao = validar_payload_historico(payload)

    if not validacao.get("valido"):
        return {
            "ok": False,
            "sessao_id": "",
            "cliente_id": "",
            "itens_salvos": 0,
            "erro": "PAYLOAD_INVALIDO: " + "; ".join(validacao.get("erros") or []),
        }

    payload_limpo = garantir_json_serializavel(payload)

    cliente = payload_limpo.get("cliente") or {}
    sessao = payload_limpo.get("sessao") or {}
    snapshot = payload_limpo.get("snapshot_star") or {}
    itens = payload_limpo.get("itens_investigativos") or []
    pacote = payload_limpo.get("pacote_investigativo") or {}
    conclusao = payload_limpo.get("conclusao_investigativa") or {}
    metadados = payload_limpo.get("metadados_execucao") or {}

    sessao_id = sessao.get("sessao_id", "")
    cliente_id = cliente.get("cliente_id", "")

    inicializar_schema(db_path)

    if sessao_existe(db_path, sessao_id) and not permitir_atualizacao:
        return {
            "ok": False,
            "sessao_id": sessao_id,
            "cliente_id": cliente_id,
            "itens_salvos": 0,
            "erro": "SESSAO_JA_EXISTE",
        }

    conexao = obter_conexao(db_path)
    itens_salvos = 0

    try:
        conexao.execute(
            """
            INSERT INTO clientes_investigados (
                cliente_id, nome_cliente, vendedor, cidade,
                origem_cliente_coluna, origem_vendedor_coluna, origem_cidade_coluna,
                criado_em, atualizado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(cliente_id) DO UPDATE SET
                nome_cliente=excluded.nome_cliente,
                vendedor=excluded.vendedor,
                cidade=excluded.cidade,
                origem_cliente_coluna=excluded.origem_cliente_coluna,
                origem_vendedor_coluna=excluded.origem_vendedor_coluna,
                origem_cidade_coluna=excluded.origem_cidade_coluna,
                atualizado_em=excluded.atualizado_em
            """,
            (
                cliente_id,
                cliente.get("nome_cliente", ""),
                cliente.get("vendedor", ""),
                cliente.get("cidade", ""),
                cliente.get("origem_cliente_coluna", ""),
                cliente.get("origem_vendedor_coluna", ""),
                cliente.get("origem_cidade_coluna", ""),
                cliente.get("criado_em", ""),
                cliente.get("atualizado_em", ""),
            ),
        )

        conexao.execute(
            """
            INSERT INTO sessoes_investigativas (
                sessao_id, cliente_id, data_sessao, origem, usuario_responsavel,
                status_sessao, versao_modelo, criado_em, atualizado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(sessao_id) DO UPDATE SET
                cliente_id=excluded.cliente_id,
                data_sessao=excluded.data_sessao,
                origem=excluded.origem,
                usuario_responsavel=excluded.usuario_responsavel,
                status_sessao=excluded.status_sessao,
                versao_modelo=excluded.versao_modelo,
                atualizado_em=excluded.atualizado_em
            """,
            (
                sessao_id,
                cliente_id,
                sessao.get("data_sessao", ""),
                sessao.get("origem", ""),
                sessao.get("usuario_responsavel", ""),
                sessao.get("status_sessao", ""),
                sessao.get("versao_modelo", ""),
                sessao.get("criado_em", ""),
                sessao.get("atualizado_em", ""),
            ),
        )

        conexao.execute("DELETE FROM snapshots_star WHERE sessao_id = ?", (sessao_id,))
        conexao.execute(
            """
            INSERT INTO snapshots_star (
                snapshot_id, sessao_id, cliente_id, status_star, curva,
                media_lp, media_cp, meses_sem_compra, erosao_star, meta, acao, criado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot.get("snapshot_id", ""),
                sessao_id,
                cliente_id,
                snapshot.get("status_star", ""),
                snapshot.get("curva", ""),
                snapshot.get("media_lp", 0.0),
                snapshot.get("media_cp", 0.0),
                snapshot.get("meses_sem_compra", 0.0),
                snapshot.get("erosao_star", 0.0),
                snapshot.get("meta", 0.0),
                snapshot.get("acao", ""),
                snapshot.get("criado_em", ""),
            ),
        )

        conexao.execute("DELETE FROM itens_investigativos WHERE sessao_id = ?", (sessao_id,))

        for item in itens:
            conexao.execute(
                """
                INSERT INTO itens_investigativos (
                    item_id, sessao_id, origem, pergunta, status_investigativo,
                    resposta, evidencia_textual, criado_em, atualizado_em
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.get("item_id", ""),
                    sessao_id,
                    item.get("origem", ""),
                    item.get("pergunta", ""),
                    item.get("status_investigativo", ""),
                    item.get("resposta", ""),
                    item.get("evidencia_textual", ""),
                    item.get("criado_em", ""),
                    item.get("atualizado_em", ""),
                ),
            )
            itens_salvos += 1

        conexao.execute("DELETE FROM conclusoes_investigativas WHERE sessao_id = ?", (sessao_id,))
        conexao.execute("DELETE FROM pacotes_investigativos WHERE sessao_id = ?", (sessao_id,))
        conexao.execute(
            """
            INSERT INTO pacotes_investigativos (
                pacote_id, sessao_id, cliente_id, status_star, curva,
                nivel_prioridade, tipo_prioridade, resumo_hipotese,
                resumo_investigacao_json, maturidade_investigacao, leitura_consolidada, criado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pacote.get("pacote_id", ""),
                sessao_id,
                cliente_id,
                pacote.get("status_star", ""),
                pacote.get("curva", ""),
                pacote.get("nivel_prioridade", ""),
                pacote.get("tipo_prioridade", ""),
                pacote.get("resumo_hipotese", ""),
                json.dumps(pacote.get("resumo_investigacao") or {}),
                pacote.get("maturidade_investigacao", ""),
                pacote.get("leitura_consolidada", ""),
                pacote.get("criado_em", ""),
            ),
        )

        conexao.execute(
            """
            INSERT INTO conclusoes_investigativas (
                conclusao_id, pacote_id, sessao_id, status_conclusivo_geral, leitura_conclusao,
                hipoteses_confirmadas_count, hipoteses_descartadas_count, hipoteses_inconclusivas_count,
                pendentes_validacao_count, respostas_sem_classificacao_count, criado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                conclusao.get("conclusao_id", ""),
                conclusao.get("pacote_id", ""),
                sessao_id,
                conclusao.get("status_conclusivo_geral", ""),
                conclusao.get("leitura_conclusao", ""),
                conclusao.get("hipoteses_confirmadas_count", 0),
                conclusao.get("hipoteses_descartadas_count", 0),
                conclusao.get("hipoteses_inconclusivas_count", 0),
                conclusao.get("pendentes_validacao_count", 0),
                conclusao.get("respostas_sem_classificacao_count", 0),
                conclusao.get("criado_em", ""),
            ),
        )

        conexao.execute("DELETE FROM metadados_execucao WHERE sessao_id = ?", (sessao_id,))
        conexao.execute(
            """
            INSERT INTO metadados_execucao (
                execucao_id, sessao_id, arquivo_origem_nome, data_upload,
                versao_star_os, versao_modelo_persistencia, ambiente, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                metadados.get("execucao_id", ""),
                sessao_id,
                metadados.get("arquivo_origem_nome", ""),
                metadados.get("data_upload", ""),
                metadados.get("versao_star_os", ""),
                metadados.get("versao_modelo_persistencia", ""),
                metadados.get("ambiente", ""),
                metadados.get("observacoes", ""),
            ),
        )

        conexao.execute(
            "INSERT OR REPLACE INTO payloads_historico (sessao_id, payload_json, salvo_em) VALUES (?, ?, ?)",
            (sessao_id, json.dumps(payload_limpo), gerar_timestamp_iso()),
        )

        conexao.commit()
    except Exception as exc:
        conexao.rollback()

        return {
            "ok": False,
            "sessao_id": sessao_id,
            "cliente_id": cliente_id,
            "itens_salvos": 0,
            "erro": f"ERRO_AO_SALVAR: {exc}",
        }
    finally:
        conexao.close()

    return {
        "ok": True,
        "sessao_id": sessao_id,
        "cliente_id": cliente_id,
        "itens_salvos": itens_salvos,
        "erro": "",
    }


def carregar_payload_por_sessao(db_path, sessao_id):
    if not sessao_id:
        return {"ok": False, "sessao_id": sessao_id or "", "payload": {}, "erro": "SESSAO_NAO_ENCONTRADA"}

    try:
        conexao = obter_conexao(db_path)
    except Exception as exc:
        return {"ok": False, "sessao_id": sessao_id, "payload": {}, "erro": f"ERRO_AO_ABRIR_BANCO: {exc}"}

    try:
        cursor = conexao.execute("SELECT payload_json FROM payloads_historico WHERE sessao_id = ?", (sessao_id,))
        linha = cursor.fetchone()
    except sqlite3.OperationalError:
        linha = None
    finally:
        conexao.close()

    if linha is None:
        return {"ok": False, "sessao_id": sessao_id, "payload": {}, "erro": "SESSAO_NAO_ENCONTRADA"}

    try:
        payload = json.loads(linha["payload_json"])
    except Exception as exc:
        return {"ok": False, "sessao_id": sessao_id, "payload": {}, "erro": f"ERRO_AO_DECODIFICAR: {exc}"}

    return {"ok": True, "sessao_id": sessao_id, "payload": payload, "erro": ""}


def listar_sessoes_cliente(db_path, cliente_id):
    if not cliente_id:
        return []

    try:
        conexao = obter_conexao(db_path)
    except Exception:
        return []

    try:
        cursor = conexao.execute(
            """
            SELECT
                s.sessao_id AS sessao_id,
                s.cliente_id AS cliente_id,
                s.data_sessao AS data_sessao,
                s.status_sessao AS status_sessao,
                s.usuario_responsavel AS usuario_responsavel,
                s.criado_em AS criado_em,
                s.atualizado_em AS atualizado_em,
                m.arquivo_origem_nome AS arquivo_origem_nome
            FROM sessoes_investigativas s
            LEFT JOIN metadados_execucao m ON m.sessao_id = s.sessao_id
            WHERE s.cliente_id = ?
            ORDER BY s.criado_em DESC
            """,
            (cliente_id,),
        )
        linhas = cursor.fetchall()
    except sqlite3.OperationalError:
        linhas = []
    finally:
        conexao.close()

    return [dict(linha) for linha in linhas]


def listar_clientes_investigados(db_path):
    try:
        conexao = obter_conexao(db_path)
    except Exception:
        return []

    try:
        cursor = conexao.execute(
            """
            SELECT
                c.cliente_id AS cliente_id,
                c.nome_cliente AS nome_cliente,
                c.vendedor AS vendedor,
                c.cidade AS cidade,
                COUNT(s.sessao_id) AS total_sessoes,
                MAX(s.criado_em) AS ultima_sessao_em
            FROM clientes_investigados c
            LEFT JOIN sessoes_investigativas s ON s.cliente_id = c.cliente_id
            GROUP BY c.cliente_id, c.nome_cliente, c.vendedor, c.cidade
            ORDER BY ultima_sessao_em DESC
            """
        )
        linhas = cursor.fetchall()
    except sqlite3.OperationalError:
        linhas = []
    finally:
        conexao.close()

    return [dict(linha) for linha in linhas]


def contar_registros_repositorio(db_path):
    contagens = {tabela: 0 for tabela in TABELAS_ESPERADAS}

    try:
        conexao = obter_conexao(db_path)
    except Exception:
        return contagens

    try:
        for tabela in TABELAS_ESPERADAS:
            try:
                cursor = conexao.execute(f"SELECT COUNT(*) AS total FROM {tabela}")
                linha = cursor.fetchone()
                contagens[tabela] = linha["total"] if linha else 0
            except sqlite3.OperationalError:
                contagens[tabela] = 0
    finally:
        conexao.close()

    return contagens


def remover_sessao_teste(db_path, sessao_id):
    if not sessao_id:
        return {"ok": False, "sessao_id": sessao_id or ""}

    try:
        conexao = obter_conexao(db_path)
    except Exception:
        return {"ok": False, "sessao_id": sessao_id}

    try:
        conexao.execute("DELETE FROM payloads_historico WHERE sessao_id = ?", (sessao_id,))
        conexao.execute("DELETE FROM metadados_execucao WHERE sessao_id = ?", (sessao_id,))
        conexao.execute("DELETE FROM conclusoes_investigativas WHERE sessao_id = ?", (sessao_id,))
        conexao.execute("DELETE FROM pacotes_investigativos WHERE sessao_id = ?", (sessao_id,))
        conexao.execute("DELETE FROM itens_investigativos WHERE sessao_id = ?", (sessao_id,))
        conexao.execute("DELETE FROM snapshots_star WHERE sessao_id = ?", (sessao_id,))
        conexao.execute("DELETE FROM sessoes_investigativas WHERE sessao_id = ?", (sessao_id,))
        conexao.commit()
        ok = True
    except Exception:
        conexao.rollback()
        ok = False
    finally:
        conexao.close()

    return {"ok": ok, "sessao_id": sessao_id}


def formatar_resumo_repositorio(contagens):
    contagens = contagens or {}

    return [
        f"Clientes investigados: {contagens.get('clientes_investigados', 0)}",
        f"Sessões investigativas: {contagens.get('sessoes_investigativas', 0)}",
        f"Itens investigativos: {contagens.get('itens_investigativos', 0)}",
        f"Payloads históricos: {contagens.get('payloads_historico', 0)}",
    ]
