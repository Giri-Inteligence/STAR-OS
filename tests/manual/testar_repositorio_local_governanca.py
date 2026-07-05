"""
Teste manual simples do Repositorio Local de Governanca
(star_persistence/repositorio_governanca.py). Executavel diretamente por
python, sem pytest. Usa apenas tempfile.TemporaryDirectory para o banco
SQLite de teste, removido ao final. Nao usa IA, nao chama API externa,
nao consome token, nao cria banco permanente no repositorio.

Uso:
    python tests/manual/testar_repositorio_local_governanca.py
"""

import copy
import json
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_governance.acompanhamento import criar_registro_acompanhamento
from star_governance.status_acompanhamento import criar_snapshot_status_acompanhamento
from star_governance.loop_semanal import criar_item_loop_governanca, criar_ciclo_loop_semanal

from star_persistence.contrato_governanca import (
    criar_payload_registro_acompanhamento_persistivel,
    criar_payload_snapshot_status_persistivel,
    criar_payload_item_loop_persistivel,
    criar_payload_ciclo_loop_persistivel,
    criar_payload_governanca_integrada,
)
from star_persistence.repositorio_governanca import (
    normalizar_caminho_banco_governanca,
    inicializar_schema_governanca,
    verificar_schema_governanca,
    preparar_linha_payload_governanca,
    salvar_payload_governanca,
    carregar_payload_governanca,
    listar_payloads_governanca,
    salvar_lote_payloads_governanca,
    contar_registros_repositorio_governanca,
    validar_integridade_repositorio_governanca,
    formatar_resumo_repositorio_governanca,
    formatar_validacao_repositorio_governanca,
)

TERMOS_FRASE_PROIBIDOS = (
    "tarefa criada",
    "plano de acao criado",
    "agenda criada",
    "calendario criado",
    "mensagem enviada",
    "agente acionado",
    "ia acionada",
    "api externa",
    "causa raiz confirmada",
    "recomendado",
    "deve fazer",
)
TERMOS_PALAVRA_PROIBIDOS = (r"\btoken\b",)
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


def _construir_payload_historico_simulado(sufixo="1"):
    return {
        "versao_contrato": "5.2",
        "cliente": {
            "cliente_id": f"CLIENTE_TESTE{sufixo}",
            "nome_cliente": f"Empresa Alfa {sufixo}",
            "vendedor": "Joao",
            "cidade": "Curitiba",
        },
        "sessao": {"sessao_id": f"SESSAO_TESTE{sufixo}"},
        "snapshot_star": {"status_star": "ALERTA", "curva": "A"},
        "itens_investigativos": [
            {"item_id": "ITEM_1", "pergunta": "Houve reajuste de preco?"},
        ],
        "pacote_investigativo": {"pacote_id": f"PACOTE_TESTE{sufixo}"},
        "conclusao_investigativa": {
            "conclusao_id": f"CONCLUSAO_TESTE{sufixo}",
            "status_conclusivo_geral": "PARCIAL",
            "leitura_conclusao": "Aguardando mais evidencias",
        },
    }


def _construir_payloads_governanca(sufixo="1"):
    payload_historico = _construir_payload_historico_simulado(sufixo)

    registro = criar_registro_acompanhamento(
        payload_historico=payload_historico, status_acompanhamento="EM_ACOMPANHAMENTO",
        observacao_acompanhamento=f"Retorno {sufixo}.",
    )
    snapshot = criar_snapshot_status_acompanhamento(payload_historico=payload_historico, registros=[registro])
    item_loop = criar_item_loop_governanca(payload_historico=payload_historico, registros_acompanhamento=[registro])
    ciclo_loop = criar_ciclo_loop_semanal(
        entradas=[{"payload_historico": payload_historico, "registros_acompanhamento": [registro]}],
        periodo_referencia=f"2026-W2{sufixo}",
    )

    payload_registro = criar_payload_registro_acompanhamento_persistivel(registro)
    payload_snapshot = criar_payload_snapshot_status_persistivel(snapshot)
    payload_item = criar_payload_item_loop_persistivel(item_loop)
    payload_ciclo = criar_payload_ciclo_loop_persistivel(ciclo_loop)
    payload_integrado = criar_payload_governanca_integrada(
        registro_acompanhamento=registro, snapshot_status=snapshot, item_loop=item_loop, ciclo_loop=ciclo_loop
    )

    return {
        "payload_historico": payload_historico,
        "registro": registro,
        "snapshot": snapshot,
        "item_loop": item_loop,
        "ciclo_loop": ciclo_loop,
        "payload_registro": payload_registro,
        "payload_snapshot": payload_snapshot,
        "payload_item": payload_item,
        "payload_ciclo": payload_ciclo,
        "payload_integrado": payload_integrado,
    }


def testar_normalizar_caminho_banco_governanca(db_path):
    assert normalizar_caminho_banco_governanca(db_path) == Path(db_path)
    assert normalizar_caminho_banco_governanca(Path(db_path)) == Path(db_path)
    assert normalizar_caminho_banco_governanca("") is None
    assert normalizar_caminho_banco_governanca(None) is None

    print("1. normalizar_caminho_banco_governanca: OK")


def testar_inicializar_schema_governanca(db_path):
    resultado = inicializar_schema_governanca(db_path)

    assert resultado["inicializado"] is True
    assert "governanca_schema_info" in resultado["tabelas"]
    assert "governanca_payloads" in resultado["tabelas"]

    print("2. inicializar_schema_governanca: OK")


def testar_verificar_schema_governanca(db_path, db_path_sem_schema):
    resultado_valido = verificar_schema_governanca(db_path)
    assert resultado_valido["valido"] is True

    resultado_sem_schema = verificar_schema_governanca(db_path_sem_schema)
    assert resultado_sem_schema["valido"] is False
    assert len(resultado_sem_schema["tabelas_ausentes"]) > 0

    print("3. verificar_schema_governanca: OK")


def testar_preparar_linha_payload_governanca(payload_registro):
    payload_copia = copy.deepcopy(payload_registro)

    resultado_valido = preparar_linha_payload_governanca(payload_registro)

    assert payload_registro == payload_copia, "payload nao deveria ser alterado"
    assert resultado_valido["valido"] is True
    assert isinstance(resultado_valido["linha"]["payload_json"], str)
    json.loads(resultado_valido["linha"]["payload_json"])

    resultado_invalido = preparar_linha_payload_governanca({"algo": "errado"})
    assert resultado_invalido["valido"] is False
    assert resultado_invalido["linha"] == {}

    print("4. preparar_linha_payload_governanca: OK")


def testar_salvar_payload_governanca(db_path, payload_registro):
    payload_copia = copy.deepcopy(payload_registro)

    resultado = salvar_payload_governanca(db_path, payload_registro)
    assert payload_registro == payload_copia, "payload nao deveria ser alterado"
    assert resultado["salvo"] is True

    resultado_invalido = salvar_payload_governanca(db_path, {"algo": "errado"})
    assert resultado_invalido["salvo"] is False

    resultado_duplicado = salvar_payload_governanca(db_path, payload_registro, sobrescrever=False)
    assert resultado_duplicado["salvo"] is False
    assert resultado_duplicado["duplicado"] is True

    resultado_sobrescrito = salvar_payload_governanca(db_path, payload_registro, sobrescrever=True)
    assert resultado_sobrescrito["salvo"] is True

    print("5. salvar_payload_governanca: OK")


def testar_carregar_payload_governanca(db_path, payload_registro):
    resultado = carregar_payload_governanca(
        db_path, "REGISTRO_ACOMPANHAMENTO", payload_registro["registro_id"]
    )

    assert resultado["encontrado"] is True
    assert resultado["tipo_payload_governanca"] == "REGISTRO_ACOMPANHAMENTO"
    assert resultado["payload_id"] == payload_registro["registro_id"]

    resultado_inexistente = carregar_payload_governanca(db_path, "REGISTRO_ACOMPANHAMENTO", "INEXISTENTE")
    assert resultado_inexistente["encontrado"] is False

    print("6. carregar_payload_governanca: OK")


def testar_listar_payloads_governanca(db_path, payload_registro):
    listagem_por_tipo = listar_payloads_governanca(db_path, tipo_payload_governanca="REGISTRO_ACOMPANHAMENTO")
    assert len(listagem_por_tipo) >= 1
    assert listagem_por_tipo[0]["payload"]["registro_id"] == payload_registro["registro_id"]

    listagem_por_cliente = listar_payloads_governanca(db_path, cliente_id=payload_registro["cliente_id"])
    assert len(listagem_por_cliente) >= 1

    listagem_por_sessao = listar_payloads_governanca(db_path, sessao_id=payload_registro["sessao_id"])
    assert len(listagem_por_sessao) >= 1

    listagem_limitada = listar_payloads_governanca(db_path, limite=1)
    assert len(listagem_limitada) <= 1

    print("7. listar_payloads_governanca: OK")


def testar_salvar_lote_payloads_governanca(db_path, payloads_governanca):
    lote = [
        payloads_governanca["payload_snapshot"],
        payloads_governanca["payload_item"],
        payloads_governanca["payload_ciclo"],
        {"algo": "errado"},
    ]
    lote_copia = copy.deepcopy(lote)

    resultado = salvar_lote_payloads_governanca(db_path, lote, sobrescrever=True)

    assert lote == lote_copia, "payloads originais nao deveriam ser alterados"
    assert resultado["total_payloads"] == 4
    assert resultado["salvos"] == 3
    assert resultado["invalidos"] == 1

    print("8. salvar_lote_payloads_governanca: OK")


def testar_listar_ciclo_loop_por_cliente_sessao(db_path, payloads_governanca):
    payload_ciclo = payloads_governanca["payload_ciclo"]

    assert payload_ciclo["cliente_id"] != "", "payload_ciclo deveria ter cliente_id apos a correcao da Sprint 8.2"
    assert payload_ciclo["sessao_id"] != "", "payload_ciclo deveria ter sessao_id apos a correcao da Sprint 8.2"

    listagem_ciclo_por_cliente = listar_payloads_governanca(
        db_path, tipo_payload_governanca="CICLO_LOOP", cliente_id=payload_ciclo["cliente_id"]
    )
    assert len(listagem_ciclo_por_cliente) >= 1, "CICLO_LOOP deveria aparecer na listagem filtrada por cliente_id"
    assert listagem_ciclo_por_cliente[0]["payload"]["ciclo_id"] == payload_ciclo["ciclo_id"]

    listagem_ciclo_por_sessao = listar_payloads_governanca(
        db_path, tipo_payload_governanca="CICLO_LOOP", sessao_id=payload_ciclo["sessao_id"]
    )
    assert len(listagem_ciclo_por_sessao) >= 1, "CICLO_LOOP deveria aparecer na listagem filtrada por sessao_id"

    print("8.1. listar CICLO_LOOP por cliente_id/sessao_id (Sprint 8.2): OK")


def testar_contar_registros_repositorio_governanca(db_path, db_path_inexistente):
    contagem = contar_registros_repositorio_governanca(db_path)

    assert contagem["total_payloads"] >= 4
    assert contagem["por_tipo"]["REGISTRO_ACOMPANHAMENTO"] >= 1
    assert contagem["por_tipo"]["SNAPSHOT_STATUS"] >= 1
    assert contagem["por_tipo"]["ITEM_LOOP"] >= 1
    assert contagem["por_tipo"]["CICLO_LOOP"] >= 1

    contagem_inexistente = contar_registros_repositorio_governanca(db_path_inexistente)
    assert contagem_inexistente["total_payloads"] == 0
    assert len(contagem_inexistente["avisos"]) >= 1

    print("9. contar_registros_repositorio_governanca: OK")

    return contagem


def testar_validar_integridade_repositorio_governanca(db_path, db_path_vazio):
    resultado = validar_integridade_repositorio_governanca(db_path)
    assert resultado["valido"] is True
    assert resultado["total_payloads"] >= 4

    inicializar_schema_governanca(db_path_vazio)
    resultado_vazio = validar_integridade_repositorio_governanca(db_path_vazio)
    assert resultado_vazio["valido"] is True
    assert len(resultado_vazio["avisos"]) >= 1

    print("10. validar_integridade_repositorio_governanca: OK")

    return resultado


def testar_formatar_resumo_repositorio_governanca(contagem):
    linhas = formatar_resumo_repositorio_governanca(contagem)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Total de payloads:") for linha in linhas)
    assert any(linha.startswith("Registros de acompanhamento:") for linha in linhas)
    assert any(linha.startswith("Snapshots de status:") for linha in linhas)
    assert any(linha.startswith("Itens de loop:") for linha in linhas)
    assert any(linha.startswith("Ciclos de loop:") for linha in linhas)
    assert any(linha.startswith("Governanças integradas:") for linha in linhas)

    print("11. formatar_resumo_repositorio_governanca: OK")


def testar_formatar_validacao_repositorio_governanca(resultado_integridade):
    linhas = formatar_validacao_repositorio_governanca(resultado_integridade)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Repositório válido:") for linha in linhas)
    assert any(linha.startswith("Total de payloads:") for linha in linhas)
    assert any(linha.startswith("Payloads válidos:") for linha in linhas)
    assert any(linha.startswith("Payloads inválidos:") for linha in linhas)
    assert any(linha.startswith("Erros:") for linha in linhas)
    assert any(linha.startswith("Avisos:") for linha in linhas)

    print("12. formatar_validacao_repositorio_governanca: OK")


def testar_seguranca_arquitetural(db_path, payload_registro, contagem, resultado_integridade):
    textos = [
        json.dumps(payload_registro),
    ]
    textos.extend(formatar_resumo_repositorio_governanca(contagem))
    textos.extend(formatar_validacao_repositorio_governanca(resultado_integridade))

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    pasta_scratch = os.path.dirname(os.path.abspath(__file__))
    pasta_raiz = os.path.abspath(os.path.join(pasta_scratch, "..", ".."))

    for pasta in (
        pasta_scratch,
        pasta_raiz,
        os.path.join(pasta_raiz, "star_persistence"),
        os.path.join(pasta_raiz, "star_governance"),
    ):
        for nome_arquivo in os.listdir(pasta):
            for extensao in EXTENSOES_PERSISTENCIA_PROIBIDAS:
                if nome_arquivo.lower().endswith(extensao):
                    raise AssertionError(f"arquivo de persistencia funcional encontrado: {nome_arquivo}")

    assert not os.path.exists(db_path), "o banco de teste deveria ter sido removido com o TemporaryDirectory"

    print("13. seguranca arquitetural: OK")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho_banco = str(Path(tmpdir) / "governanca_teste.sqlite")
        caminho_banco_sem_schema = str(Path(tmpdir) / "governanca_sem_schema.sqlite")
        caminho_banco_vazio = str(Path(tmpdir) / "governanca_vazio.sqlite")
        caminho_banco_inexistente = str(Path(tmpdir) / "nao_existe" / "governanca_inexistente.sqlite")

        testar_normalizar_caminho_banco_governanca(caminho_banco)
        testar_inicializar_schema_governanca(caminho_banco)

        conexao_bruta = __import__("sqlite3").connect(caminho_banco_sem_schema)
        conexao_bruta.close()
        testar_verificar_schema_governanca(caminho_banco, caminho_banco_sem_schema)

        payloads_teste = _construir_payloads_governanca("1")

        testar_preparar_linha_payload_governanca(payloads_teste["payload_registro"])
        testar_salvar_payload_governanca(caminho_banco, payloads_teste["payload_registro"])
        testar_carregar_payload_governanca(caminho_banco, payloads_teste["payload_registro"])
        testar_listar_payloads_governanca(caminho_banco, payloads_teste["payload_registro"])
        testar_salvar_lote_payloads_governanca(caminho_banco, payloads_teste)
        testar_listar_ciclo_loop_por_cliente_sessao(caminho_banco, payloads_teste)

        contagem_teste = testar_contar_registros_repositorio_governanca(caminho_banco, caminho_banco_inexistente)
        resultado_integridade_teste = testar_validar_integridade_repositorio_governanca(
            caminho_banco, caminho_banco_vazio
        )

        testar_formatar_resumo_repositorio_governanca(contagem_teste)
        testar_formatar_validacao_repositorio_governanca(resultado_integridade_teste)

    testar_seguranca_arquitetural(
        caminho_banco, payloads_teste["payload_registro"], contagem_teste, resultado_integridade_teste
    )

    print("REPOSITORIO_LOCAL_GOVERNANCA_OK")
