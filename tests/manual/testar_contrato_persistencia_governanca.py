"""
Teste manual simples do Contrato de Persistencia da Governanca
(star_persistence/contrato_governanca.py). Executavel diretamente por
python, sem pytest. Nao usa IA, nao chama API externa, nao consome
token, nao salva nada em disco, nao cria banco de dados.

Uso:
    python tests/manual/testar_contrato_persistencia_governanca.py
"""

import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_governance.acompanhamento import criar_registro_acompanhamento
from star_governance.status_acompanhamento import criar_snapshot_status_acompanhamento
from star_governance.loop_semanal import criar_item_loop_governanca, criar_ciclo_loop_semanal

from star_persistence.contrato_governanca import (
    obter_dict_seguro_governanca,
    obter_lista_segura_contrato_governanca,
    normalizar_tipo_payload_governanca,
    criar_metadados_persistencia_governanca,
    extrair_identificadores_governanca,
    criar_snapshot_id_deterministico,
    criar_payload_registro_acompanhamento_persistivel,
    criar_payload_snapshot_status_persistivel,
    criar_payload_item_loop_persistivel,
    criar_payload_ciclo_loop_persistivel,
    criar_payload_governanca_integrada,
    validar_payload_governanca,
    validar_payloads_governanca,
    formatar_validacao_payload_governanca_texto,
    formatar_payload_governanca_resumo_texto,
)

TERMOS_FRASE_PROIBIDOS = (
    "salvo no banco",
    "persistido com sucesso",
    "tabela criada",
    "sqlite",
    ".db",
    ".json criado",
    "automaticamente",
    "executar tarefa",
    "criar tarefa",
    "enviar mensagem",
    "acionar agente",
    "causa raiz confirmada",
    "plano de acao",
    "recomendado",
    "deve fazer",
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


def testar_obter_dict_seguro_governanca():
    assert obter_dict_seguro_governanca({"a": 1}) == {"a": 1}
    assert obter_dict_seguro_governanca(None) == {}
    assert obter_dict_seguro_governanca([1, 2, 3]) == {}

    print("1. obter_dict_seguro_governanca: OK")


def testar_obter_lista_segura_contrato_governanca():
    assert obter_lista_segura_contrato_governanca(None) == []
    assert obter_lista_segura_contrato_governanca([1, 2]) == [1, 2]
    assert obter_lista_segura_contrato_governanca((1, 2)) == [1, 2]
    assert obter_lista_segura_contrato_governanca("texto") == ["texto"]

    print("2. obter_lista_segura_contrato_governanca: OK")


def testar_normalizar_tipo_payload_governanca():
    casos = [
        ("registro acompanhamento", "REGISTRO_ACOMPANHAMENTO"),
        ("snapshot status", "SNAPSHOT_STATUS"),
        ("item loop", "ITEM_LOOP"),
        ("ciclo loop", "CICLO_LOOP"),
        ("governança integrada", "GOVERNANCA_INTEGRADA"),
        ("desconhecido", "GOVERNANCA_INTEGRADA"),
    ]

    for entrada, esperado in casos:
        resultado = normalizar_tipo_payload_governanca(entrada)
        assert resultado == esperado, f"{entrada!r}: esperado {esperado}, obtido {resultado}"

    print("3. normalizar_tipo_payload_governanca: OK")


def testar_criar_metadados_persistencia_governanca():
    metadados = criar_metadados_persistencia_governanca()

    assert metadados["versao_contrato_persistencia_governanca"] == "7.2"
    assert metadados["persistido"] is False
    assert metadados["persistencia_habilitada"] is False
    assert metadados["criado_em"] != ""
    assert metadados["atualizado_em"] != ""

    json.dumps(metadados)

    achado = _termo_proibido_encontrado(json.dumps(metadados))
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    print("4. criar_metadados_persistencia_governanca: OK")


def testar_extrair_identificadores_governanca(payload_historico):
    registro = criar_registro_acompanhamento(
        payload_historico=payload_historico, status_acompanhamento="EM_ACOMPANHAMENTO",
        observacao_acompanhamento="Retorno registrado.",
    )
    snapshot = criar_snapshot_status_acompanhamento(payload_historico=payload_historico, registros=[registro])
    item_loop = criar_item_loop_governanca(payload_historico=payload_historico, registros_acompanhamento=[registro])
    ciclo_loop = criar_ciclo_loop_semanal(
        entradas=[{"payload_historico": payload_historico, "registros_acompanhamento": [registro]}],
        periodo_referencia="2026-W27",
    )

    registro_copia = copy.deepcopy(registro)
    snapshot_copia = copy.deepcopy(snapshot)
    item_loop_copia = copy.deepcopy(item_loop)
    ciclo_loop_copia = copy.deepcopy(ciclo_loop)

    identificadores = extrair_identificadores_governanca(
        registro_acompanhamento=registro, snapshot_status=snapshot, item_loop=item_loop, ciclo_loop=ciclo_loop
    )

    assert registro == registro_copia, "registro nao deveria ser alterado"
    assert snapshot == snapshot_copia, "snapshot nao deveria ser alterado"
    assert item_loop == item_loop_copia, "item_loop nao deveria ser alterado"
    assert ciclo_loop == ciclo_loop_copia, "ciclo_loop nao deveria ser alterado"

    assert identificadores["cliente_id"] == item_loop["cliente_id"]
    assert identificadores["sessao_id"] == item_loop["sessao_id"]
    assert identificadores["registro_id"] == registro["registro_id"]
    assert identificadores["snapshot_id"] != ""
    assert identificadores["item_loop_id"] == item_loop["item_loop_id"]
    assert identificadores["ciclo_id"] == ciclo_loop["ciclo_id"]
    assert identificadores["status_atual_acompanhamento"] == "EM_ACOMPANHAMENTO"
    assert identificadores["classificacao_loop"] == "REVISAO_DO_CICLO"

    print("5. extrair_identificadores_governanca: OK")

    return registro, snapshot, item_loop, ciclo_loop


def testar_criar_snapshot_id_deterministico(snapshot):
    id1 = criar_snapshot_id_deterministico(snapshot)
    id2 = criar_snapshot_id_deterministico(snapshot)
    id3 = criar_snapshot_id_deterministico(dict(snapshot, status_atual_acompanhamento="ENCERRADO"))

    snapshot_copia = copy.deepcopy(snapshot)

    assert id1 == id2
    assert id1 != id3
    assert id1 != ""
    assert snapshot == snapshot_copia, "snapshot original nao deveria ser alterado"

    print("6. criar_snapshot_id_deterministico: OK")


def testar_criar_payload_registro_acompanhamento_persistivel(registro):
    registro_copia = copy.deepcopy(registro)

    payload = criar_payload_registro_acompanhamento_persistivel(registro)

    assert registro == registro_copia, "registro original nao deveria ser alterado"
    assert payload["tipo_payload_governanca"] == "REGISTRO_ACOMPANHAMENTO"
    assert payload["versao_payload_governanca"] == "7.2"
    assert payload["registro_id"] == registro["registro_id"]
    assert payload["dados_registro"] == registro
    assert "metadados_persistencia" in payload

    json.dumps(payload)

    resultado = validar_payload_governanca(payload)
    assert resultado["valido"] is True

    print("7. criar_payload_registro_acompanhamento_persistivel: OK")

    return payload


def testar_criar_payload_snapshot_status_persistivel(snapshot):
    snapshot_copia = copy.deepcopy(snapshot)

    payload = criar_payload_snapshot_status_persistivel(snapshot)

    assert snapshot == snapshot_copia, "snapshot original nao deveria ser alterado"
    assert payload["tipo_payload_governanca"] == "SNAPSHOT_STATUS"
    assert payload["snapshot_id"] != ""
    assert payload["status_atual_acompanhamento"] == snapshot["status_atual_acompanhamento"]
    assert "dados_snapshot" in payload
    assert "metadados_persistencia" in payload

    json.dumps(payload)

    resultado = validar_payload_governanca(payload)
    assert resultado["valido"] is True

    print("8. criar_payload_snapshot_status_persistivel: OK")

    return payload


def testar_criar_payload_item_loop_persistivel(item_loop):
    item_loop_copia = copy.deepcopy(item_loop)

    payload = criar_payload_item_loop_persistivel(item_loop)

    assert item_loop == item_loop_copia, "item_loop original nao deveria ser alterado"
    assert payload["tipo_payload_governanca"] == "ITEM_LOOP"
    assert payload["item_loop_id"] == item_loop["item_loop_id"]
    assert payload["classificacao_loop"] == item_loop["classificacao_loop"]
    assert payload["entra_no_loop_ativo"] == item_loop["entra_no_loop_ativo"]
    assert "dados_item_loop" in payload
    assert "metadados_persistencia" in payload

    json.dumps(payload)

    resultado = validar_payload_governanca(payload)
    assert resultado["valido"] is True

    print("9. criar_payload_item_loop_persistivel: OK")

    return payload


def testar_criar_payload_ciclo_loop_persistivel(ciclo_loop):
    ciclo_loop_copia = copy.deepcopy(ciclo_loop)

    payload = criar_payload_ciclo_loop_persistivel(ciclo_loop)

    assert ciclo_loop == ciclo_loop_copia, "ciclo_loop original nao deveria ser alterado"
    assert payload["tipo_payload_governanca"] == "CICLO_LOOP"
    assert payload["ciclo_id"] == ciclo_loop["ciclo_id"]
    assert payload["tipo_ciclo"] == ciclo_loop["tipo_ciclo"]
    assert payload["total_itens"] == ciclo_loop["total_itens"]
    assert "dados_ciclo_loop" in payload
    assert "metadados_persistencia" in payload

    json.dumps(payload)

    resultado = validar_payload_governanca(payload)
    assert resultado["valido"] is True

    print("10. criar_payload_ciclo_loop_persistivel: OK")

    return payload


def testar_criar_payload_governanca_integrada(registro, snapshot, item_loop, ciclo_loop):
    registro_copia = copy.deepcopy(registro)
    snapshot_copia = copy.deepcopy(snapshot)
    item_loop_copia = copy.deepcopy(item_loop)
    ciclo_loop_copia = copy.deepcopy(ciclo_loop)

    payload = criar_payload_governanca_integrada(
        registro_acompanhamento=registro, snapshot_status=snapshot, item_loop=item_loop, ciclo_loop=ciclo_loop
    )

    assert registro == registro_copia, "registro nao deveria ser alterado"
    assert snapshot == snapshot_copia, "snapshot nao deveria ser alterado"
    assert item_loop == item_loop_copia, "item_loop nao deveria ser alterado"
    assert ciclo_loop == ciclo_loop_copia, "ciclo_loop nao deveria ser alterado"

    assert payload["tipo_payload_governanca"] == "GOVERNANCA_INTEGRADA"
    assert payload["governanca_id"] != ""
    assert payload["referencias"]["registro_id"] == registro["registro_id"]
    assert payload["referencias"]["snapshot_id"] != ""
    assert payload["referencias"]["item_loop_id"] == item_loop["item_loop_id"]
    assert payload["referencias"]["ciclo_id"] == ciclo_loop["ciclo_id"]

    json.dumps(payload)

    resultado = validar_payload_governanca(payload)
    assert resultado["valido"] is True

    print("11. criar_payload_governanca_integrada: OK")

    return payload


def testar_validar_payload_governanca(payload_valido):
    resultado_valido = validar_payload_governanca(payload_valido)
    assert resultado_valido["valido"] is True

    resultado_none = validar_payload_governanca(None)
    assert resultado_none["valido"] is False

    payload_tipo_invalido = dict(payload_valido, tipo_payload_governanca="TIPO_DESCONHECIDO")
    resultado_tipo_invalido = validar_payload_governanca(payload_tipo_invalido)
    assert resultado_tipo_invalido["valido"] is False

    payload_persistido = copy.deepcopy(payload_valido)
    payload_persistido["metadados_persistencia"]["persistido"] = True
    resultado_persistido = validar_payload_governanca(payload_persistido)
    assert resultado_persistido["valido"] is False

    payload_habilitado = copy.deepcopy(payload_valido)
    payload_habilitado["metadados_persistencia"]["persistencia_habilitada"] = True
    resultado_habilitado = validar_payload_governanca(payload_habilitado)
    assert resultado_habilitado["valido"] is False

    payload_sem_cliente = dict(payload_valido, cliente_id="")
    resultado_sem_cliente = validar_payload_governanca(payload_sem_cliente)
    assert resultado_sem_cliente["valido"] is True
    assert len(resultado_sem_cliente["avisos"]) >= 1

    payload_sem_sessao = dict(payload_valido, sessao_id="")
    resultado_sem_sessao = validar_payload_governanca(payload_sem_sessao)
    assert resultado_sem_sessao["valido"] is True
    assert len(resultado_sem_sessao["avisos"]) >= 1

    print("12. validar_payload_governanca: OK")


def testar_validar_payloads_governanca(payload_valido):
    resultado_lista = validar_payloads_governanca([payload_valido, payload_valido])
    assert resultado_lista["valido"] is True
    assert resultado_lista["total_payloads"] == 2
    assert resultado_lista["payloads_validos"] == 2
    assert resultado_lista["payloads_invalidos"] == 0

    resultado_vazio = validar_payloads_governanca([])
    assert resultado_vazio["valido"] is True
    assert len(resultado_vazio["avisos"]) >= 1

    payload_invalido = dict(payload_valido, tipo_payload_governanca="TIPO_DESCONHECIDO")
    resultado_misto = validar_payloads_governanca([payload_valido, payload_invalido])
    assert resultado_misto["valido"] is False
    assert resultado_misto["total_payloads"] == 2
    assert resultado_misto["payloads_validos"] == 1
    assert resultado_misto["payloads_invalidos"] == 1

    print("13. validar_payloads_governanca: OK")


def testar_formatar_validacao_payload_governanca_texto(payload_valido):
    resultado = validar_payload_governanca(payload_valido)
    linhas = formatar_validacao_payload_governanca_texto(resultado)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Payload válido:") for linha in linhas)
    assert any(linha.startswith("Erros:") for linha in linhas)
    assert any(linha.startswith("Avisos:") for linha in linhas)

    print("14. formatar_validacao_payload_governanca_texto: OK")


def testar_formatar_payload_governanca_resumo_texto(payload_valido):
    linhas = formatar_payload_governanca_resumo_texto(payload_valido)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Tipo de payload:") for linha in linhas)
    assert any(linha.startswith("Versão do payload:") for linha in linhas)
    assert any(linha.startswith("Persistido:") for linha in linhas)
    assert any(linha.startswith("Persistência habilitada:") for linha in linhas)

    print("15. formatar_payload_governanca_resumo_texto: OK")


def testar_seguranca_arquitetural(payload_governanca_integrada):
    import star_persistence.contrato_governanca as modulo_contrato_governanca

    textos = [
        json.dumps(payload_governanca_integrada),
    ]
    textos.extend(formatar_payload_governanca_resumo_texto(payload_governanca_integrada))

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    codigo_fonte = ""
    with open(modulo_contrato_governanca.__file__, "r", encoding="utf-8") as arquivo:
        codigo_fonte = arquivo.read()

    assert "import streamlit" not in codigo_fonte.lower()
    assert "import pandas" not in codigo_fonte.lower()
    assert "import sqlite3" not in codigo_fonte.lower()
    assert "import requests" not in codigo_fonte.lower()
    assert "openai" not in codigo_fonte.lower()
    assert "anthropic" not in codigo_fonte.lower()

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

    print("16. seguranca arquitetural: OK")


if __name__ == "__main__":
    payload_teste = _construir_payload_historico_simulado()

    testar_obter_dict_seguro_governanca()
    testar_obter_lista_segura_contrato_governanca()
    testar_normalizar_tipo_payload_governanca()
    testar_criar_metadados_persistencia_governanca()

    registro_teste, snapshot_teste, item_loop_teste, ciclo_loop_teste = testar_extrair_identificadores_governanca(
        payload_teste
    )
    testar_criar_snapshot_id_deterministico(snapshot_teste)

    payload_registro = testar_criar_payload_registro_acompanhamento_persistivel(registro_teste)
    payload_snapshot = testar_criar_payload_snapshot_status_persistivel(snapshot_teste)
    payload_item = testar_criar_payload_item_loop_persistivel(item_loop_teste)
    payload_ciclo = testar_criar_payload_ciclo_loop_persistivel(ciclo_loop_teste)
    payload_integrado = testar_criar_payload_governanca_integrada(
        registro_teste, snapshot_teste, item_loop_teste, ciclo_loop_teste
    )

    testar_validar_payload_governanca(payload_integrado)
    testar_validar_payloads_governanca(payload_integrado)
    testar_formatar_validacao_payload_governanca_texto(payload_integrado)
    testar_formatar_payload_governanca_resumo_texto(payload_integrado)
    testar_seguranca_arquitetural(payload_integrado)

    print("CONTRATO_PERSISTENCIA_GOVERNANCA_OK")
