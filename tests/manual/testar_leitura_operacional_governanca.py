"""
Teste manual simples da Leitura Operacional da Governanca sem Tarefas
(star_governance/leitura_operacional.py). Executavel diretamente por
python, sem pytest. Nao usa IA, nao chama API externa, nao consome
token, nao salva nada em disco, nao cria banco de dados.

Uso:
    python tests/manual/testar_leitura_operacional_governanca.py
"""

import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_governance.leitura_operacional import (
    obter_dict_seguro_leitura,
    obter_lista_segura_leitura,
    normalizar_tipo_payload_leitura,
    extrair_payload_de_linha_repositorio,
    extrair_identidade_leitura,
    extrair_status_leitura,
    extrair_classificacao_loop_leitura,
    criar_item_leitura_operacional,
    gerar_resumo_quantitativo_leitura,
    gerar_sintese_operacional_governanca,
    gerar_leitura_operacional_governanca,
    formatar_item_leitura_operacional_texto,
    formatar_leitura_operacional_governanca_texto,
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
    "recomendamos",
    "deve fazer",
    "faca",
)
TERMOS_PALAVRA_PROIBIDOS = (r"\btoken\b",)


def _termo_proibido_encontrado(texto):
    texto_lower = texto.lower()

    for termo in TERMOS_FRASE_PROIBIDOS:
        if termo in texto_lower:
            return termo

    for padrao in TERMOS_PALAVRA_PROIBIDOS:
        if re.search(padrao, texto_lower):
            return padrao

    return None


def _payload_registro_acompanhamento():
    return {
        "tipo_payload_governanca": "REGISTRO_ACOMPANHAMENTO",
        "versao_payload_governanca": "7.2",
        "registro_id": "REGISTRO_TESTE_1",
        "cliente_id": "CLIENTE_TESTE_1",
        "sessao_id": "SESSAO_TESTE_1",
        "nome_cliente": "Empresa Alfa",
        "dados_registro": {"status_acompanhamento": "EM_ACOMPANHAMENTO"},
        "metadados_persistencia": {"origem": "GOVERNANCA_MANUAL", "criado_em": "2026-01-01T00:00:00+00:00"},
    }


def _payload_snapshot_status():
    return {
        "tipo_payload_governanca": "SNAPSHOT_STATUS",
        "versao_payload_governanca": "7.2",
        "snapshot_id": "SNAPSHOT_TESTE_1",
        "cliente_id": "CLIENTE_TESTE_1",
        "sessao_id": "SESSAO_TESTE_1",
        "nome_cliente": "Empresa Alfa",
        "status_atual_acompanhamento": "AGUARDANDO_DECISAO",
        "dados_snapshot": {"status_atual_acompanhamento": "AGUARDANDO_DECISAO"},
        "metadados_persistencia": {"origem": "GOVERNANCA_MANUAL", "criado_em": "2026-01-01T00:00:00+00:00"},
    }


def _payload_item_loop():
    return {
        "tipo_payload_governanca": "ITEM_LOOP",
        "versao_payload_governanca": "7.2",
        "item_loop_id": "ITEM_TESTE_1",
        "cliente_id": "CLIENTE_TESTE_1",
        "sessao_id": "SESSAO_TESTE_1",
        "nome_cliente": "Empresa Alfa",
        "classificacao_loop": "REVISAO_DO_CICLO",
        "entra_no_loop_ativo": True,
        "dados_item_loop": {"status_atual_acompanhamento": "EM_ACOMPANHAMENTO", "classificacao_loop": "REVISAO_DO_CICLO"},
        "metadados_persistencia": {"origem": "GOVERNANCA_MANUAL", "criado_em": "2026-01-01T00:00:00+00:00"},
    }


def _payload_ciclo_loop_com_identidade():
    return {
        "tipo_payload_governanca": "CICLO_LOOP",
        "versao_payload_governanca": "7.2",
        "ciclo_id": "CICLO_TESTE_1",
        "cliente_id": "CLIENTE_TESTE_1",
        "sessao_id": "SESSAO_TESTE_1",
        "nome_cliente": "Empresa Alfa",
        "tipo_ciclo": "SEMANAL",
        "periodo_referencia": "2026-W01",
        "origem": "GOVERNANCA_MANUAL",
        "total_itens": 1,
        "dados_ciclo_loop": {"ciclo_id": "CICLO_TESTE_1", "itens": []},
        "metadados_persistencia": {"origem": "GOVERNANCA_MANUAL", "criado_em": "2026-01-01T00:00:00+00:00"},
    }


def _payload_ciclo_loop_sem_identidade():
    return {
        "tipo_payload_governanca": "CICLO_LOOP",
        "versao_payload_governanca": "7.2",
        "ciclo_id": "CICLO_TESTE_2",
        "cliente_id": "",
        "sessao_id": "",
        "nome_cliente": "",
        "tipo_ciclo": "SEMANAL",
        "periodo_referencia": "2026-W02",
        "origem": "",
        "total_itens": 0,
        "dados_ciclo_loop": {"ciclo_id": "CICLO_TESTE_2", "itens": []},
        "metadados_persistencia": {"origem": "", "criado_em": "2026-01-02T00:00:00+00:00"},
    }


def _payload_governanca_integrada():
    return {
        "tipo_payload_governanca": "GOVERNANCA_INTEGRADA",
        "versao_payload_governanca": "7.2",
        "governanca_id": "GOVERNANCA_TESTE_1",
        "cliente_id": "CLIENTE_TESTE_1",
        "sessao_id": "SESSAO_TESTE_1",
        "nome_cliente": "Empresa Alfa",
        "registro_acompanhamento": {"status_acompanhamento": "EM_ACOMPANHAMENTO"},
        "snapshot_status": {"status_atual_acompanhamento": "EM_ACOMPANHAMENTO"},
        "item_loop": {"classificacao_loop": "REVISAO_DO_CICLO"},
        "ciclo_loop": {},
        "referencias": {},
        "metadados_persistencia": {"origem": "GOVERNANCA_MANUAL", "criado_em": "2026-01-01T00:00:00+00:00"},
    }


def testar_payloads_vazios():
    resultado = gerar_leitura_operacional_governanca(None)

    assert resultado["valido"] is True
    assert resultado["total_payloads"] == 0
    assert len(resultado["avisos"]) >= 1
    assert resultado["sintese_operacional"]["leitura_sintetica"] == (
        "Nenhuma governança salva foi encontrada para a consulta atual."
    )

    resultado_lista_vazia = gerar_leitura_operacional_governanca([])
    assert resultado_lista_vazia["valido"] is True
    assert resultado_lista_vazia["total_payloads"] == 0

    print("1. Payloads vazios: OK")


def testar_payload_registro_acompanhamento():
    payload = _payload_registro_acompanhamento()
    payload_copia = copy.deepcopy(payload)

    item = criar_item_leitura_operacional(payload)

    assert payload == payload_copia, "payload nao deveria ser alterado"
    assert item["tipo_payload_governanca"] == "REGISTRO_ACOMPANHAMENTO"
    assert item["payload_id"] == "REGISTRO_TESTE_1"
    assert item["cliente_id"] == "CLIENTE_TESTE_1"
    assert item["sessao_id"] == "SESSAO_TESTE_1"
    assert item["status_acompanhamento"] == "EM_ACOMPANHAMENTO"
    assert item["leitura_curta"] == "Registro de acompanhamento encontrado."

    print("2. Payload REGISTRO_ACOMPANHAMENTO: OK")


def testar_payload_snapshot_status():
    payload = _payload_snapshot_status()

    item = criar_item_leitura_operacional(payload)

    assert item["tipo_payload_governanca"] == "SNAPSHOT_STATUS"
    assert item["payload_id"] == "SNAPSHOT_TESTE_1"
    assert item["status_acompanhamento"] == "AGUARDANDO_DECISAO"

    print("3. Payload SNAPSHOT_STATUS: OK")


def testar_payload_item_loop():
    payload = _payload_item_loop()

    item = criar_item_leitura_operacional(payload)

    assert item["tipo_payload_governanca"] == "ITEM_LOOP"
    assert item["payload_id"] == "ITEM_TESTE_1"
    assert item["classificacao_loop"] == "REVISAO_DO_CICLO"

    print("4. Payload ITEM_LOOP: OK")


def testar_payload_ciclo_loop_com_identidade():
    payload = _payload_ciclo_loop_com_identidade()

    item = criar_item_leitura_operacional(payload)

    assert item["tipo_payload_governanca"] == "CICLO_LOOP"
    assert item["payload_id"] == "CICLO_TESTE_1"
    assert item["cliente_id"] == "CLIENTE_TESTE_1"
    assert item["sessao_id"] == "SESSAO_TESTE_1"
    assert item["nome_cliente"] == "Empresa Alfa"
    assert item["avisos"] == []

    sintese = gerar_sintese_operacional_governanca([item])
    assert sintese["ciclo_loop_com_identidade"] is True

    print("5. Payload CICLO_LOOP com identidade: OK")


def testar_payload_ciclo_loop_sem_identidade():
    payload = _payload_ciclo_loop_sem_identidade()

    item = criar_item_leitura_operacional(payload)

    assert item["tipo_payload_governanca"] == "CICLO_LOOP"
    assert len(item["avisos"]) >= 1

    sintese = gerar_sintese_operacional_governanca([item])
    assert sintese["ciclo_loop_com_identidade"] is False
    assert sintese["consulta_completa_para_cliente_sessao"] is False

    print("6. Payload CICLO_LOOP sem identidade: OK")


def testar_payload_governanca_integrada():
    payload = _payload_governanca_integrada()

    item = criar_item_leitura_operacional(payload)

    assert item["tipo_payload_governanca"] == "GOVERNANCA_INTEGRADA"
    assert item["payload_id"] == "GOVERNANCA_TESTE_1"

    print("7. Payload GOVERNANCA_INTEGRADA: OK")


def testar_linha_do_repositorio():
    payload_original = _payload_item_loop()
    linha = {
        "tipo_payload_governanca": "ITEM_LOOP",
        "payload_id": "ITEM_TESTE_1",
        "cliente_id": "CLIENTE_TESTE_1",
        "sessao_id": "SESSAO_TESTE_1",
        "nome_cliente": "Empresa Alfa",
        "origem": "GOVERNANCA_MANUAL",
        "criado_em_repositorio": "2026-01-01T00:00:00+00:00",
        "payload": payload_original,
    }
    linha_copia = copy.deepcopy(linha)

    payload_extraido = extrair_payload_de_linha_repositorio(linha)
    item = criar_item_leitura_operacional(linha)

    assert linha == linha_copia, "linha original nao deveria ser alterada"
    assert payload_extraido == payload_original
    assert item["tipo_payload_governanca"] == "ITEM_LOOP"
    assert item["payload_id"] == "ITEM_TESTE_1"

    print("8. Linha retornada pelo repositorio (chave 'payload'): OK")


def testar_resumo_quantitativo():
    itens = [
        criar_item_leitura_operacional(_payload_registro_acompanhamento()),
        criar_item_leitura_operacional(_payload_snapshot_status()),
        criar_item_leitura_operacional(_payload_ciclo_loop_com_identidade()),
        criar_item_leitura_operacional(_payload_ciclo_loop_sem_identidade()),
    ]

    resumo = gerar_resumo_quantitativo_leitura(itens)

    assert resumo["total_payloads"] == 4
    assert resumo["por_tipo"]["REGISTRO_ACOMPANHAMENTO"] == 1
    assert resumo["por_tipo"]["SNAPSHOT_STATUS"] == 1
    assert resumo["por_tipo"]["CICLO_LOOP"] == 2
    assert resumo["com_cliente_id"] == 3
    assert resumo["sem_cliente_id"] == 1
    assert resumo["com_sessao_id"] == 3
    assert resumo["sem_sessao_id"] == 1

    print("9. Resumo quantitativo: OK")


def testar_formatacao_textual():
    itens_ou_linhas = [
        _payload_registro_acompanhamento(),
        _payload_ciclo_loop_com_identidade(),
    ]
    itens_ou_linhas_copia = copy.deepcopy(itens_ou_linhas)

    leitura = gerar_leitura_operacional_governanca(itens_ou_linhas)

    assert itens_ou_linhas == itens_ou_linhas_copia, "payloads originais nao deveriam ser alterados"

    linhas = formatar_leitura_operacional_governanca_texto(leitura)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Total de payloads") for linha in linhas)
    assert any(linha.startswith("CICLO_LOOP com identidade completa") for linha in linhas)
    assert any(linha.startswith("Consulta completa para cliente/sessão") for linha in linhas)

    texto_completo = " ".join(linhas).lower()
    assert "recomend" not in texto_completo
    assert "deve fazer" not in texto_completo

    linhas_item = formatar_item_leitura_operacional_texto(leitura["itens"][0])
    assert any(linha.startswith("Tipo:") for linha in linhas_item)
    assert any(linha.startswith("Payload ID:") for linha in linhas_item)
    assert any(linha.startswith("Leitura:") for linha in linhas_item)

    print("10. Formatação textual: OK")

    return leitura


def testar_seguranca_arquitetural(leitura):
    import star_governance.leitura_operacional as modulo_leitura

    textos = [json.dumps(leitura["sintese_operacional"])]
    textos.extend(formatar_leitura_operacional_governanca_texto(leitura))

    for item in leitura["itens"]:
        textos.extend(formatar_item_leitura_operacional_texto(item))

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    codigo_fonte = ""
    with open(modulo_leitura.__file__, "r", encoding="utf-8") as arquivo:
        codigo_fonte = arquivo.read()

    assert "import streamlit" not in codigo_fonte.lower()
    assert "import pandas" not in codigo_fonte.lower()
    assert "import sqlite3" not in codigo_fonte.lower()
    assert "import requests" not in codigo_fonte.lower()
    assert "openai" not in codigo_fonte.lower()
    assert "anthropic" not in codigo_fonte.lower()

    print("11. Segurança arquitetural: OK")


def testar_imutabilidade():
    payload_registro = _payload_registro_acompanhamento()
    payload_snapshot = _payload_snapshot_status()
    payload_ciclo = _payload_ciclo_loop_com_identidade()

    copia_registro = copy.deepcopy(payload_registro)
    copia_snapshot = copy.deepcopy(payload_snapshot)
    copia_ciclo = copy.deepcopy(payload_ciclo)

    gerar_leitura_operacional_governanca([payload_registro, payload_snapshot, payload_ciclo])

    assert payload_registro == copia_registro
    assert payload_snapshot == copia_snapshot
    assert payload_ciclo == copia_ciclo

    print("12. Imutabilidade dos payloads originais: OK")


if __name__ == "__main__":
    testar_payloads_vazios()
    testar_payload_registro_acompanhamento()
    testar_payload_snapshot_status()
    testar_payload_item_loop()
    testar_payload_ciclo_loop_com_identidade()
    testar_payload_ciclo_loop_sem_identidade()
    testar_payload_governanca_integrada()
    testar_linha_do_repositorio()
    testar_resumo_quantitativo()
    leitura_teste = testar_formatacao_textual()
    testar_seguranca_arquitetural(leitura_teste)
    testar_imutabilidade()

    print("LEITURA_OPERACIONAL_GOVERNANCA_OK")
