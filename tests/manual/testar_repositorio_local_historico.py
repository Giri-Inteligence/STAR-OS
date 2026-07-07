"""
Teste manual simples do Repositorio Local do Historico Investigativo
(star_persistence/repositorio_local.py). Executavel diretamente por python,
sem pytest. Usa apenas tempfile.TemporaryDirectory para o banco SQLite de
teste, removido ao final. Nao usa IA, nao chama API externa, nao consome
token, nao cria banco permanente no repositorio.

Uso:
    python tests/manual/testar_repositorio_local_historico.py
"""

import json
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_persistence.contrato_historico import criar_payload_historico_investigativo
from star_persistence.repositorio_local import (
    TABELAS_ESPERADAS,
    obter_conexao,
    inicializar_schema,
    verificar_schema,
    sessao_existe,
    salvar_payload_historico,
    carregar_payload_por_sessao,
    listar_sessoes_cliente,
    listar_clientes_investigados,
    contar_registros_repositorio,
    remover_sessao_teste,
    formatar_resumo_repositorio,
)

TERMOS_FRASE_PROIBIDOS = (
    "automaticamente",
    "executar tarefa",
    "criar tarefa",
    "enviar mensagem",
    "acionar agente",
    "causa raiz confirmada",
    "plano de acao",
)
TERMOS_PALAVRA_PROIBIDOS = (r"\bia\b", r"\btoken\b", r"\bapi\b")
EXTENSOES_PERSISTENCIA_PROIBIDAS = (".db", ".sqlite", ".sqlite3", ".json")


def _termo_proibido_encontrado(texto):
    texto_lower = texto.lower()

    for termo in TERMOS_FRASE_PROIBIDOS:
        if termo in texto_lower:
            return termo

    for padrao in TERMOS_PALAVRA_PROIBIDOS:
        if re.search(padrao, texto_lower):
            return padrao

    return None


def _construir_payload_teste():
    linha_star = {
        "status_star": "ALERTA",
        "curva": "A",
        "media_lp": 1000.0,
        "media_cp": 500.0,
        "meses_sem_compra": 2,
        "erosao_star": 0.5,
        "meta": 1200.0,
        "acao": "Contatar cliente",
    }
    itens = [
        {
            "origem": "PRECO",
            "pergunta": "Houve reajuste de preco?",
            "status": "CONFIRMADA",
            "resposta": "Sim",
            "evidencia": "Cliente confirmou reajuste",
        },
        {
            "origem": "CONCORRENCIA",
            "pergunta": "Ha concorrencia nova na regiao?",
            "status": "PENDENTE",
            "resposta": "",
            "evidencia": "",
        },
    ]
    pacote_investigativo = {
        "status_star": "ALERTA",
        "curva": "A",
        "nivel_prioridade": "ALTA",
        "tipo_prioridade": "URGENTE",
        "resumo_hipotese": "Possivel perda por preco",
        "resumo_investigacao": {"total_itens": 2},
        "maturidade_investigacao": "PARCIAL",
        "leitura_consolidada": "Investigacao em andamento",
    }
    conclusao_investigativa = {
        "leitura_conclusao": "Aguardando mais evidencias",
        "resumo_conclusao": {
            "status_conclusivo_geral": "PARCIAL",
            "hipoteses_confirmadas": 1,
            "hipoteses_descartadas": 0,
            "hipoteses_inconclusivas": 0,
            "pendentes_validacao": 1,
            "respostas_sem_classificacao": 0,
        },
    }

    return criar_payload_historico_investigativo(
        nome_cliente="Empresa Alfa Ltda",
        vendedor="Joao",
        cidade="Curitiba",
        linha_star=linha_star,
        itens_investigativos=itens,
        pacote_investigativo=pacote_investigativo,
        conclusao_investigativa=conclusao_investigativa,
        arquivo_origem_nome="planilha.xlsx",
        usuario_responsavel="consultor",
    )


def testar_obter_conexao(db_path):
    try:
        obter_conexao("")
        raise AssertionError("obter_conexao deveria levantar ValueError para db_path vazio")
    except ValueError:
        pass

    conexao = obter_conexao(db_path)
    try:
        cursor = conexao.execute("PRAGMA foreign_keys")
        valor = cursor.fetchone()[0]
        assert valor == 1, "foreign_keys deveria estar ativo (ON)"
    finally:
        conexao.close()

    print("1. obter_conexao: OK")


def testar_inicializar_schema(db_path):
    resultado = inicializar_schema(db_path)

    assert resultado["ok"] is True
    assert set(resultado["tabelas"]) == set(TABELAS_ESPERADAS)
    assert resultado["db_path"] == str(db_path)

    print("2. inicializar_schema: OK")


def testar_verificar_schema(db_path):
    resultado = verificar_schema(db_path)

    assert resultado["ok"] is True
    assert set(resultado["tabelas_encontradas"]) == set(TABELAS_ESPERADAS)
    assert resultado["tabelas_faltantes"] == []

    print("3. verificar_schema: OK")


def testar_construir_payload():
    payload = _construir_payload_teste()

    assert isinstance(payload, dict)
    assert len(payload["itens_investigativos"]) == 2

    print("4. construir payload de teste com 2 itens: OK")

    return payload


def testar_salvar_payload_historico(db_path, payload):
    resultado = salvar_payload_historico(db_path, payload)

    assert resultado["ok"] is True, resultado
    assert resultado["itens_salvos"] == 2
    assert resultado["sessao_id"] != ""
    assert resultado["cliente_id"] != ""
    assert resultado["erro"] == ""

    print("5. salvar_payload_historico (primeiro salvamento): OK")

    return resultado


def testar_contar_registros_repositorio(db_path):
    contagens = contar_registros_repositorio(db_path)

    assert contagens["clientes_investigados"] == 1
    assert contagens["sessoes_investigativas"] == 1
    assert contagens["snapshots_star"] == 1
    assert contagens["itens_investigativos"] == 2
    assert contagens["pacotes_investigativos"] == 1
    assert contagens["conclusoes_investigativas"] == 1
    assert contagens["metadados_execucao"] == 1
    assert contagens["payloads_historico"] == 1

    print("6. contar_registros_repositorio: OK")

    return contagens


def testar_sessao_existe(db_path, sessao_id):
    assert sessao_existe(db_path, sessao_id) is True
    assert sessao_existe(db_path, "SESSAO_INEXISTENTE") is False

    print("7. sessao_existe: OK")


def testar_carregar_payload_por_sessao(db_path, sessao_id):
    resultado = carregar_payload_por_sessao(db_path, sessao_id)

    assert resultado["ok"] is True
    assert resultado["sessao_id"] == sessao_id
    assert resultado["payload"]["sessao"]["sessao_id"] == sessao_id
    assert resultado["erro"] == ""

    resultado_inexistente = carregar_payload_por_sessao(db_path, "SESSAO_INEXISTENTE")
    assert resultado_inexistente["ok"] is False
    assert resultado_inexistente["erro"] == "SESSAO_NAO_ENCONTRADA"

    print("8. carregar_payload_por_sessao: OK")


def testar_bloqueio_sobrescrita(db_path, payload):
    resultado = salvar_payload_historico(db_path, payload, permitir_atualizacao=False)

    assert resultado["ok"] is False
    assert resultado["erro"] == "SESSAO_JA_EXISTE"

    print("9. bloqueio de sobrescrita silenciosa: OK")


def testar_atualizacao_explicita(db_path, payload, sessao_id):
    resultado = salvar_payload_historico(db_path, payload, permitir_atualizacao=True)

    assert resultado["ok"] is True, resultado
    assert resultado["sessao_id"] == sessao_id
    assert resultado["itens_salvos"] == 2

    contagens = contar_registros_repositorio(db_path)
    assert contagens["sessoes_investigativas"] == 1, "sessao nao deveria duplicar"
    assert contagens["clientes_investigados"] == 1
    assert contagens["payloads_historico"] == 1, "payloads_historico deveria continuar 1 para a mesma sessao"
    assert contagens["itens_investigativos"] == 2

    print("10. atualizacao explicita (permitir_atualizacao=True) sem duplicar: OK")


def testar_listar_sessoes_cliente(db_path, cliente_id, sessao_id):
    sessoes = listar_sessoes_cliente(db_path, cliente_id)

    assert isinstance(sessoes, list)
    assert len(sessoes) == 1
    assert sessoes[0]["sessao_id"] == sessao_id
    assert sessoes[0]["cliente_id"] == cliente_id
    assert "payload_json" not in sessoes[0]

    print("11. listar_sessoes_cliente: OK")


def testar_listar_clientes_investigados(db_path, cliente_id):
    clientes = listar_clientes_investigados(db_path)

    assert isinstance(clientes, list)
    assert len(clientes) == 1
    assert clientes[0]["cliente_id"] == cliente_id
    assert clientes[0]["total_sessoes"] == 1

    print("12. listar_clientes_investigados: OK")


def testar_formatar_resumo_repositorio(contagens):
    linhas = formatar_resumo_repositorio(contagens)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Clientes investigados:") for linha in linhas)
    assert any(linha.startswith("Itens investigativos:") for linha in linhas)
    assert any(linha.startswith("Payloads") for linha in linhas)

    print("13. formatar_resumo_repositorio: OK")


def testar_remover_sessao_teste(db_path, sessao_id, cliente_id):
    resultado = remover_sessao_teste(db_path, sessao_id)

    assert resultado["ok"] is True
    assert resultado["sessao_id"] == sessao_id

    contagens = contar_registros_repositorio(db_path)
    assert contagens["sessoes_investigativas"] == 0
    assert contagens["snapshots_star"] == 0
    assert contagens["itens_investigativos"] == 0
    assert contagens["pacotes_investigativos"] == 0
    assert contagens["conclusoes_investigativas"] == 0
    assert contagens["metadados_execucao"] == 0
    assert contagens["payloads_historico"] == 0
    assert contagens["clientes_investigados"] == 1, "cliente nao deveria ser removido automaticamente"

    print("14. remover_sessao_teste (cliente permanece, restante removido): OK")


def testar_seguranca_arquitetural(db_path, payload):
    textos = [json.dumps(payload)]

    for item in payload.get("itens_investigativos", []):
        textos.append(item.get("pergunta", ""))
        textos.append(item.get("resposta", ""))
        textos.append(item.get("evidencia_textual", ""))

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    pasta_scratch = os.path.dirname(os.path.abspath(__file__))
    pasta_raiz = os.path.abspath(os.path.join(pasta_scratch, "..", ".."))

    for pasta in (
        pasta_scratch,
        pasta_raiz,
        os.path.join(pasta_raiz, "star_persistence"),
        os.path.join(pasta_raiz, "star_core"),
        os.path.join(pasta_raiz, "star_ingestion"),
        os.path.join(pasta_raiz, "star_intelligence"),
    ):
        for nome_arquivo in os.listdir(pasta):
            for extensao in EXTENSOES_PERSISTENCIA_PROIBIDAS:
                if nome_arquivo.lower().endswith(extensao):
                    raise AssertionError(f"arquivo de persistencia funcional encontrado: {nome_arquivo}")

    assert not os.path.exists(db_path), "o banco de teste deveria ter sido removido com o TemporaryDirectory"

    print("15. seguranca arquitetural (nenhum banco/artefato permanente, nenhum termo proibido): OK")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho_banco = str(Path(tmpdir) / "historico_teste.sqlite")

        testar_obter_conexao(caminho_banco)
        testar_inicializar_schema(caminho_banco)
        testar_verificar_schema(caminho_banco)

        payload_teste = testar_construir_payload()
        resultado_salvar = testar_salvar_payload_historico(caminho_banco, payload_teste)

        sessao_id_teste = resultado_salvar["sessao_id"]
        cliente_id_teste = resultado_salvar["cliente_id"]

        testar_contar_registros_repositorio(caminho_banco)
        testar_sessao_existe(caminho_banco, sessao_id_teste)
        testar_carregar_payload_por_sessao(caminho_banco, sessao_id_teste)
        testar_bloqueio_sobrescrita(caminho_banco, payload_teste)
        testar_atualizacao_explicita(caminho_banco, payload_teste, sessao_id_teste)
        testar_listar_sessoes_cliente(caminho_banco, cliente_id_teste, sessao_id_teste)
        testar_listar_clientes_investigados(caminho_banco, cliente_id_teste)

        contagens_finais = contar_registros_repositorio(caminho_banco)
        testar_formatar_resumo_repositorio(contagens_finais)
        testar_remover_sessao_teste(caminho_banco, sessao_id_teste, cliente_id_teste)

    testar_seguranca_arquitetural(caminho_banco, payload_teste)

    print("REPOSITORIO_LOCAL_HISTORICO_OK")
