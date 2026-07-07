"""
Teste manual simples do Loop Semanal de Governança
(star_governance/loop_semanal.py). Executavel diretamente por python,
sem pytest. Nao usa IA, nao chama API externa, nao consome token, nao
salva nada em disco, nao cria banco de dados.

Uso:
    python tests/manual/testar_loop_semanal_governanca.py
"""

import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_governance.acompanhamento import criar_registro_acompanhamento
from star_governance.loop_semanal import (
    obter_classificacoes_loop_permitidas,
    obter_pesos_classificacao_loop,
    gerar_id_loop_deterministico,
    classificar_item_loop,
    gerar_leitura_item_loop,
    criar_item_loop_governanca,
    ordenar_itens_loop,
    gerar_resumo_loop_semanal,
    criar_ciclo_loop_semanal,
    validar_item_loop_governanca,
    validar_ciclo_loop_semanal,
    formatar_item_loop_texto,
    formatar_resumo_loop_texto,
    formatar_validacao_loop_texto,
)

TERMOS_FRASE_PROIBIDOS = (
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

CLASSIFICACOES_ESPERADAS = (
    "SEM_REGISTRO_OPERACIONAL", "REVISAO_DO_CICLO", "AGUARDANDO_EVIDENCIA",
    "AGUARDANDO_DECISAO", "DECISAO_REGISTRADA", "ENCERRADO", "SUSPENSO", "INCONSISTENTE",
)


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


def _snapshot_status_simulado(status_atual, total_registros=1, erros=None, transicoes_validas=True):
    return {
        "versao_snapshot_status_governanca": "6.3",
        "cliente_id": "CLIENTE_SIMULADO",
        "sessao_id": "SESSAO_SIMULADA",
        "nome_cliente": "Empresa Simulada",
        "status_star": "ALERTA",
        "status_conclusivo_geral": "PARCIAL",
        "status_atual_acompanhamento": status_atual,
        "registro_id_atual": "REGISTRO_SIMULADO",
        "total_registros": total_registros,
        "transicoes_validas": transicoes_validas,
        "erros": erros or [],
        "avisos": [],
        "status_permitidos_a_partir_do_atual": [],
    }


def testar_obter_classificacoes_loop_permitidas():
    classificacoes = obter_classificacoes_loop_permitidas()

    assert isinstance(classificacoes, list)
    for classificacao in CLASSIFICACOES_ESPERADAS:
        assert classificacao in classificacoes

    classificacoes.append("HACK")
    classificacoes_novas = obter_classificacoes_loop_permitidas()
    assert "HACK" not in classificacoes_novas

    print("1. obter_classificacoes_loop_permitidas: OK")


def testar_obter_pesos_classificacao_loop():
    pesos = obter_pesos_classificacao_loop()

    assert isinstance(pesos, dict)
    for classificacao in CLASSIFICACOES_ESPERADAS:
        assert classificacao in pesos

    assert pesos["INCONSISTENTE"] < pesos["ENCERRADO"]

    pesos["HACK"] = 99
    pesos_novos = obter_pesos_classificacao_loop()
    assert "HACK" not in pesos_novos

    print("2. obter_pesos_classificacao_loop: OK")


def testar_gerar_id_loop_deterministico():
    id1 = gerar_id_loop_deterministico("A", "B", "C")
    id2 = gerar_id_loop_deterministico("A", "B", "C")
    id3 = gerar_id_loop_deterministico("A", "B", "D")

    assert id1 == id2
    assert id1 != id3
    assert id1 != ""

    print("3. gerar_id_loop_deterministico: OK")


def testar_classificar_item_loop():
    casos = [
        (_snapshot_status_simulado("NAO_INICIADO", total_registros=0), "SEM_REGISTRO_OPERACIONAL"),
        (_snapshot_status_simulado("EM_ACOMPANHAMENTO"), "REVISAO_DO_CICLO"),
        (_snapshot_status_simulado("AGUARDANDO_EVIDENCIA"), "AGUARDANDO_EVIDENCIA"),
        (_snapshot_status_simulado("AGUARDANDO_DECISAO"), "AGUARDANDO_DECISAO"),
        (_snapshot_status_simulado("DECISAO_REGISTRADA"), "DECISAO_REGISTRADA"),
        (_snapshot_status_simulado("ENCERRADO"), "ENCERRADO"),
        (_snapshot_status_simulado("SUSPENSO"), "SUSPENSO"),
        (_snapshot_status_simulado("EM_ACOMPANHAMENTO", erros=["erro simulado"]), "INCONSISTENTE"),
    ]

    for snapshot, esperado in casos:
        resultado = classificar_item_loop(snapshot)
        assert resultado["classificacao_loop"] == esperado, f"esperado {esperado}, obtido {resultado}"

    resultado_encerrado = classificar_item_loop(_snapshot_status_simulado("ENCERRADO"))
    assert resultado_encerrado["entra_no_loop_ativo"] is False

    resultado_suspenso = classificar_item_loop(_snapshot_status_simulado("SUSPENSO"))
    assert resultado_suspenso["entra_no_loop_ativo"] is False

    print("4. classificar_item_loop: OK")


def testar_gerar_leitura_item_loop():
    for classificacao in CLASSIFICACOES_ESPERADAS:
        leitura = gerar_leitura_item_loop({"classificacao_loop": classificacao})

        assert isinstance(leitura, str) and leitura != ""

        achado = _termo_proibido_encontrado(leitura)
        assert achado is None, f"leitura de {classificacao} contem termo proibido: {achado!r}"

    print("5. gerar_leitura_item_loop: OK")


def testar_criar_item_loop_governanca():
    payload = _construir_payload_historico_simulado("A")
    payload_copia = copy.deepcopy(payload)

    registro = criar_registro_acompanhamento(
        payload_historico=payload, tipo_acompanhamento="OBSERVACAO",
        status_acompanhamento="EM_ACOMPANHAMENTO", observacao_acompanhamento="Retorno registrado.",
    )
    registros = [registro]
    registros_copia = copy.deepcopy(registros)

    item_loop = criar_item_loop_governanca(payload_historico=payload, registros_acompanhamento=registros)

    assert payload == payload_copia, "payload nao deveria ser alterado"
    assert registros == registros_copia, "registros nao deveriam ser alterados"
    assert item_loop["versao_item_loop_governanca"] == "6.4"
    assert item_loop["item_loop_id"] != ""
    assert item_loop["cliente_id"] == "CLIENTE_TESTEA"
    assert item_loop["sessao_id"] == "SESSAO_TESTEA"
    assert item_loop["status_atual_acompanhamento"] == "EM_ACOMPANHAMENTO"
    assert item_loop["classificacao_loop"] == "REVISAO_DO_CICLO"
    assert item_loop["leitura_status"] != ""
    assert item_loop["leitura_loop"] != ""
    assert isinstance(item_loop["snapshot_status"], dict)

    json.dumps(item_loop)

    print("6. criar_item_loop_governanca: OK")

    return payload, registros, item_loop


def testar_ordenar_itens_loop():
    itens = [
        {"classificacao_loop": "ENCERRADO", "nome_cliente": "Zeta", "sessao_id": "S1"},
        {"classificacao_loop": "INCONSISTENTE", "nome_cliente": "Alfa", "sessao_id": "S2"},
        {"classificacao_loop": "AGUARDANDO_DECISAO", "nome_cliente": "Beta", "sessao_id": "S3"},
    ]
    itens_copia = copy.deepcopy(itens)

    ordenados = ordenar_itens_loop(itens)

    assert itens == itens_copia, "lista original nao deveria ser alterada"
    assert ordenados[0]["classificacao_loop"] == "INCONSISTENTE"
    assert ordenados[-1]["classificacao_loop"] == "ENCERRADO"

    print("7. ordenar_itens_loop: OK")


def testar_gerar_resumo_loop_semanal():
    itens = [
        {"classificacao_loop": "REVISAO_DO_CICLO", "entra_no_loop_ativo": True},
        {"classificacao_loop": "AGUARDANDO_EVIDENCIA", "entra_no_loop_ativo": True},
        {"classificacao_loop": "ENCERRADO", "entra_no_loop_ativo": False},
    ]
    itens_copia = copy.deepcopy(itens)

    resumo = gerar_resumo_loop_semanal(itens)

    assert itens == itens_copia, "itens originais nao deveriam ser alterados"
    assert resumo["total_itens"] == 3
    assert resumo["itens_ativos_no_loop"] == 2
    assert resumo["revisao_do_ciclo"] == 1
    assert resumo["aguardando_evidencia"] == 1
    assert resumo["encerrado"] == 1

    print("8. gerar_resumo_loop_semanal: OK")


def testar_criar_ciclo_loop_semanal():
    payload_a = _construir_payload_historico_simulado("X")
    payload_b = _construir_payload_historico_simulado("Y")

    registro_a = criar_registro_acompanhamento(
        payload_historico=payload_a, status_acompanhamento="EM_ACOMPANHAMENTO",
        observacao_acompanhamento="Retorno A.",
    )
    registro_b = criar_registro_acompanhamento(
        payload_historico=payload_b, status_acompanhamento="AGUARDANDO_DECISAO",
        observacao_acompanhamento="Retorno B.",
    )

    entradas = [
        {"payload_historico": payload_a, "registros_acompanhamento": [registro_a]},
        {"payload_historico": payload_b, "registros_acompanhamento": [registro_b]},
    ]
    entradas_copia = copy.deepcopy(entradas)

    ciclo = criar_ciclo_loop_semanal(entradas=entradas, periodo_referencia="2026-W27")

    assert entradas == entradas_copia, "entradas originais nao deveriam ser alteradas"
    assert ciclo["versao_ciclo_loop_governanca"] == "6.4"
    assert ciclo["tipo_ciclo"] == "SEMANAL"
    assert ciclo["ciclo_id"] != ""
    assert ciclo["periodo_referencia"] == "2026-W27"
    assert ciclo["total_itens"] == 2
    assert len(ciclo["itens"]) == 2
    assert ciclo["resumo_loop"]["total_itens"] == 2

    json.dumps(ciclo)

    print("9. criar_ciclo_loop_semanal: OK")

    return ciclo


def testar_validar_item_loop_governanca(item_loop):
    resultado_valido = validar_item_loop_governanca(item_loop)
    assert resultado_valido["valido"] is True

    resultado_invalido = validar_item_loop_governanca({"algo": "errado"})
    assert resultado_invalido["valido"] is False
    assert len(resultado_invalido["erros"]) > 0

    item_classificacao_invalida = dict(item_loop, classificacao_loop="NAO_EXISTE")
    resultado_classificacao_invalida = validar_item_loop_governanca(item_classificacao_invalida)
    assert resultado_classificacao_invalida["valido"] is False

    item_inconsistente_sem_erros = dict(item_loop, classificacao_loop="INCONSISTENTE", erros=[])
    resultado_inconsistente = validar_item_loop_governanca(item_inconsistente_sem_erros)
    assert resultado_inconsistente["valido"] is True
    assert len(resultado_inconsistente["avisos"]) >= 1

    print("10. validar_item_loop_governanca: OK")


def testar_validar_ciclo_loop_semanal(ciclo):
    resultado_valido = validar_ciclo_loop_semanal(ciclo)
    assert resultado_valido["valido"] is True

    ciclo_vazio = criar_ciclo_loop_semanal(entradas=[], periodo_referencia="2026-W28")
    resultado_vazio = validar_ciclo_loop_semanal(ciclo_vazio)
    assert resultado_vazio["valido"] is True
    assert len(resultado_vazio["avisos"]) >= 1

    resultado_invalido = validar_ciclo_loop_semanal({"algo": "errado"})
    assert resultado_invalido["valido"] is False

    ciclo_total_divergente = dict(ciclo, total_itens=99)
    resultado_divergente = validar_ciclo_loop_semanal(ciclo_total_divergente)
    assert resultado_divergente["valido"] is False

    ciclo_item_invalido = dict(ciclo, itens=[{"algo": "errado"}])
    resultado_item_invalido = validar_ciclo_loop_semanal(ciclo_item_invalido)
    assert resultado_item_invalido["valido"] is False

    print("11. validar_ciclo_loop_semanal: OK")


def testar_formatar_item_loop_texto(item_loop):
    linhas = formatar_item_loop_texto(item_loop)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Cliente:") for linha in linhas)
    assert any(linha.startswith("Sessão:") for linha in linhas)
    assert any(linha.startswith("Classificação no loop:") for linha in linhas)
    assert any(linha.startswith("Entra no loop ativo:") for linha in linhas)

    print("12. formatar_item_loop_texto: OK")


def testar_formatar_resumo_loop_texto(ciclo):
    linhas = formatar_resumo_loop_texto(ciclo["resumo_loop"])

    assert isinstance(linhas, list)
    assert any(linha.startswith("Total de itens:") for linha in linhas)
    assert any(linha.startswith("Itens ativos no loop:") for linha in linhas)
    assert any(linha.startswith("Aguardando evidência:") for linha in linhas)
    assert any(linha.startswith("Aguardando decisão:") for linha in linhas)

    print("13. formatar_resumo_loop_texto: OK")


def testar_formatar_validacao_loop_texto(ciclo):
    resultado = validar_ciclo_loop_semanal(ciclo)
    linhas = formatar_validacao_loop_texto(resultado)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Ciclo válido:") for linha in linhas)
    assert any(linha.startswith("Total de itens:") for linha in linhas)
    assert any(linha.startswith("Erros:") for linha in linhas)
    assert any(linha.startswith("Avisos:") for linha in linhas)

    print("14. formatar_validacao_loop_texto: OK")


def testar_seguranca_arquitetural(item_loop, ciclo):
    import star_governance.loop_semanal as modulo_loop

    textos = [
        json.dumps(item_loop),
        json.dumps(ciclo),
        gerar_leitura_item_loop(item_loop),
    ]
    textos.extend(formatar_item_loop_texto(item_loop))
    textos.extend(formatar_resumo_loop_texto(ciclo["resumo_loop"]))

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    codigo_fonte = ""
    with open(modulo_loop.__file__, "r", encoding="utf-8") as arquivo:
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
        os.path.join(pasta_raiz, "star_governance"),
        os.path.join(pasta_raiz, "star_persistence"),
    ):
        for nome_arquivo in os.listdir(pasta):
            for extensao in EXTENSOES_PERSISTENCIA_PROIBIDAS:
                if nome_arquivo.lower().endswith(extensao):
                    raise AssertionError(f"arquivo de persistencia funcional encontrado: {nome_arquivo}")

    print("15. seguranca arquitetural: OK")


if __name__ == "__main__":
    testar_obter_classificacoes_loop_permitidas()
    testar_obter_pesos_classificacao_loop()
    testar_gerar_id_loop_deterministico()
    testar_classificar_item_loop()
    testar_gerar_leitura_item_loop()
    _, _, item_loop_teste = testar_criar_item_loop_governanca()
    testar_ordenar_itens_loop()
    testar_gerar_resumo_loop_semanal()
    ciclo_teste = testar_criar_ciclo_loop_semanal()
    testar_validar_item_loop_governanca(item_loop_teste)
    testar_validar_ciclo_loop_semanal(ciclo_teste)
    testar_formatar_item_loop_texto(item_loop_teste)
    testar_formatar_resumo_loop_texto(ciclo_teste)
    testar_formatar_validacao_loop_texto(ciclo_teste)
    testar_seguranca_arquitetural(item_loop_teste, ciclo_teste)

    print("LOOP_SEMANAL_GOVERNANCA_OK")
