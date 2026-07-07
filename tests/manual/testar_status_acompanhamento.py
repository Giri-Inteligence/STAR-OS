"""
Teste manual simples do Status de Acompanhamento da Investigação
(star_governance/status_acompanhamento.py). Executavel diretamente por
python, sem pytest. Nao usa IA, nao chama API externa, nao consome
token, nao salva nada em disco, nao cria banco de dados.

Uso:
    python tests/manual/testar_status_acompanhamento.py
"""

import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_governance.acompanhamento import criar_registro_acompanhamento
from star_governance.status_acompanhamento import (
    obter_status_acompanhamento_permitidos,
    obter_transicoes_status_permitidas,
    status_eh_final,
    status_exige_evidencia,
    status_exige_decisao,
    avaliar_transicao_status,
    sugerir_status_conceituais_permitidos,
    ordenar_registros_por_criado_em,
    obter_status_atual_acompanhamento,
    validar_consistencia_status_acompanhamento,
    criar_snapshot_status_acompanhamento,
    gerar_leitura_status_acompanhamento,
    formatar_snapshot_status_texto,
    formatar_validacao_status_texto,
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

STATUS_ESPERADOS = (
    "NAO_INICIADO", "EM_ACOMPANHAMENTO", "AGUARDANDO_EVIDENCIA",
    "AGUARDANDO_DECISAO", "DECISAO_REGISTRADA", "ENCERRADO", "SUSPENSO",
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


def _construir_payload_historico_simulado():
    return {
        "versao_contrato": "5.2",
        "cliente": {
            "cliente_id": "CLIENTE_TESTE123",
            "nome_cliente": "Empresa Alfa Ltda",
            "vendedor": "Joao",
            "cidade": "Curitiba",
        },
        "sessao": {"sessao_id": "SESSAO_TESTE456"},
        "snapshot_star": {"status_star": "ALERTA", "curva": "A"},
        "itens_investigativos": [
            {"item_id": "ITEM_1", "pergunta": "Houve reajuste de preco?"},
        ],
        "pacote_investigativo": {"pacote_id": "PACOTE_TESTE789"},
        "conclusao_investigativa": {
            "conclusao_id": "CONCLUSAO_TESTE000",
            "status_conclusivo_geral": "PARCIAL",
            "leitura_conclusao": "Aguardando mais evidencias",
        },
    }


def testar_obter_status_acompanhamento_permitidos():
    status_lista = obter_status_acompanhamento_permitidos()

    assert isinstance(status_lista, list)
    for status in STATUS_ESPERADOS:
        assert status in status_lista

    status_lista.append("HACK")
    status_lista_nova = obter_status_acompanhamento_permitidos()
    assert "HACK" not in status_lista_nova

    print("1. obter_status_acompanhamento_permitidos: OK")


def testar_obter_transicoes_status_permitidas():
    transicoes = obter_transicoes_status_permitidas()

    assert isinstance(transicoes, dict)
    for status in STATUS_ESPERADOS:
        assert status in transicoes

    transicoes["NAO_INICIADO"].append("HACK")
    transicoes_novas = obter_transicoes_status_permitidas()
    assert "HACK" not in transicoes_novas["NAO_INICIADO"]

    print("2. obter_transicoes_status_permitidas: OK")


def testar_status_eh_final():
    assert status_eh_final("ENCERRADO") is True
    assert status_eh_final("encerrado") is True
    assert status_eh_final("SUSPENSO") is False
    assert status_eh_final("EM_ACOMPANHAMENTO") is False

    print("3. status_eh_final: OK")


def testar_status_exige_evidencia():
    assert status_exige_evidencia("AGUARDANDO_EVIDENCIA") is True
    assert status_exige_evidencia("EM_ACOMPANHAMENTO") is False

    print("4. status_exige_evidencia: OK")


def testar_status_exige_decisao():
    assert status_exige_decisao("AGUARDANDO_DECISAO") is True
    assert status_exige_decisao("DECISAO_REGISTRADA") is True
    assert status_exige_decisao("EM_ACOMPANHAMENTO") is False

    print("5. status_exige_decisao: OK")


def testar_avaliar_transicao_status():
    resultado_inicio = avaliar_transicao_status("NAO_INICIADO", "EM_ACOMPANHAMENTO")
    assert resultado_inicio["permitida"] is True

    resultado_evidencia = avaliar_transicao_status("EM_ACOMPANHAMENTO", "AGUARDANDO_EVIDENCIA")
    assert resultado_evidencia["permitida"] is True
    assert len(resultado_evidencia["avisos"]) >= 1

    resultado_decisao = avaliar_transicao_status("AGUARDANDO_DECISAO", "DECISAO_REGISTRADA")
    assert resultado_decisao["permitida"] is True
    assert len(resultado_decisao["avisos"]) >= 1

    resultado_bloqueado = avaliar_transicao_status("ENCERRADO", "EM_ACOMPANHAMENTO")
    assert resultado_bloqueado["permitida"] is False

    resultado_reaberto = avaliar_transicao_status(
        "ENCERRADO", "EM_ACOMPANHAMENTO", contexto={"permitir_reabertura": True}
    )
    assert resultado_reaberto["permitida"] is True

    resultado_reaberto_bloqueado = avaliar_transicao_status(
        "ENCERRADO", "AGUARDANDO_DECISAO", contexto={"permitir_reabertura": True}
    )
    assert resultado_reaberto_bloqueado["permitida"] is False

    print("6. avaliar_transicao_status: OK")


def testar_sugerir_status_conceituais_permitidos():
    resultado_nao_iniciado = sugerir_status_conceituais_permitidos("NAO_INICIADO")
    assert "EM_ACOMPANHAMENTO" in resultado_nao_iniciado["status_permitidos"]

    resultado_encerrado = sugerir_status_conceituais_permitidos("ENCERRADO")
    assert resultado_encerrado["status_permitidos"] == ["ENCERRADO"]

    resultado_encerrado_reaberto = sugerir_status_conceituais_permitidos(
        "ENCERRADO", contexto={"permitir_reabertura": True}
    )
    assert "EM_ACOMPANHAMENTO" in resultado_encerrado_reaberto["status_permitidos"]
    assert "ENCERRADO" in resultado_encerrado_reaberto["status_permitidos"]

    texto_completo = json.dumps(resultado_nao_iniciado) + json.dumps(resultado_encerrado)
    assert "recomendado" not in texto_completo.lower()
    assert "deve fazer" not in texto_completo.lower()

    print("7. sugerir_status_conceituais_permitidos: OK")


def testar_ordenar_registros_por_criado_em():
    registros = [
        {"registro_id": "B", "criado_em": "2026-01-02T00:00:00+00:00"},
        {"registro_id": "A", "criado_em": "2026-01-01T00:00:00+00:00"},
        {"registro_id": "SEM_DATA"},
    ]
    registros_copia = copy.deepcopy(registros)

    ordenados = ordenar_registros_por_criado_em(registros)

    assert registros == registros_copia, "lista original nao deveria ser alterada"
    assert [registro["registro_id"] for registro in ordenados] == ["A", "B", "SEM_DATA"]

    print("8. ordenar_registros_por_criado_em: OK")


def testar_obter_status_atual_acompanhamento():
    resultado_vazio = obter_status_atual_acompanhamento([])
    assert resultado_vazio["status_atual"] == "NAO_INICIADO"

    registros = [
        {"registro_id": "A", "criado_em": "2026-01-01T00:00:00+00:00", "status_acompanhamento": "EM_ACOMPANHAMENTO"},
        {"registro_id": "B", "criado_em": "2026-01-02T00:00:00+00:00", "status_acompanhamento": "AGUARDANDO_DECISAO"},
    ]
    registros_copia = copy.deepcopy(registros)

    resultado = obter_status_atual_acompanhamento(registros)

    assert registros == registros_copia, "lista original nao deveria ser alterada"
    assert resultado["status_atual"] == "AGUARDANDO_DECISAO"
    assert resultado["registro_id_atual"] == "B"

    print("9. obter_status_atual_acompanhamento: OK")


def testar_validar_consistencia_status_acompanhamento(payload):
    resultado_vazio = validar_consistencia_status_acompanhamento([])
    assert resultado_vazio["valido"] is True
    assert len(resultado_vazio["avisos"]) >= 1

    registro_1 = criar_registro_acompanhamento(
        payload_historico=payload, tipo_acompanhamento="OBSERVACAO",
        status_acompanhamento="EM_ACOMPANHAMENTO", observacao_acompanhamento="Retorno inicial.",
        criado_em="2026-01-01T00:00:00+00:00",
    )
    registro_2 = criar_registro_acompanhamento(
        payload_historico=payload, tipo_acompanhamento="REVISAO",
        status_acompanhamento="AGUARDANDO_DECISAO", observacao_acompanhamento="Aguardando decisao.",
        criado_em="2026-01-02T00:00:00+00:00",
    )

    registros_validos = [registro_1, registro_2]
    registros_copia = copy.deepcopy(registros_validos)

    resultado_valido = validar_consistencia_status_acompanhamento(registros_validos)
    assert registros_validos == registros_copia, "registros originais nao deveriam ser alterados"
    assert resultado_valido["valido"] is True

    registro_3_invalido = dict(registro_2, status_acompanhamento="NAO_INICIADO",
                                criado_em="2026-01-03T00:00:00+00:00")
    registros_invalidos = [registro_1, registro_2, registro_3_invalido]

    resultado_invalido = validar_consistencia_status_acompanhamento(registros_invalidos)
    assert resultado_invalido["valido"] is False

    print("10. validar_consistencia_status_acompanhamento: OK")

    return registros_validos


def testar_criar_snapshot_status_acompanhamento(payload, registros):
    payload_copia = copy.deepcopy(payload)
    registros_copia = copy.deepcopy(registros)

    snapshot = criar_snapshot_status_acompanhamento(payload_historico=payload, registros=registros)

    assert payload == payload_copia, "payload nao deveria ser alterado"
    assert registros == registros_copia, "registros nao deveriam ser alterados"
    assert snapshot["versao_snapshot_status_governanca"] == "6.3"
    assert snapshot["cliente_id"] == "CLIENTE_TESTE123"
    assert snapshot["sessao_id"] == "SESSAO_TESTE456"
    assert snapshot["status_atual_acompanhamento"] == "AGUARDANDO_DECISAO"
    assert snapshot["total_registros"] == 2
    assert isinstance(snapshot["transicoes_validas"], bool)
    assert isinstance(snapshot["status_permitidos_a_partir_do_atual"], list)

    json.dumps(snapshot)

    print("11. criar_snapshot_status_acompanhamento: OK")

    return snapshot


def testar_gerar_leitura_status_acompanhamento():
    for status in STATUS_ESPERADOS:
        leitura = gerar_leitura_status_acompanhamento({"status_atual_acompanhamento": status})

        assert isinstance(leitura, str) and leitura != ""

        achado = _termo_proibido_encontrado(leitura)
        assert achado is None, f"leitura de {status} contem termo proibido: {achado!r}"

    print("12. gerar_leitura_status_acompanhamento: OK")


def testar_formatar_snapshot_status_texto(snapshot):
    linhas = formatar_snapshot_status_texto(snapshot)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Cliente:") for linha in linhas)
    assert any(linha.startswith("Sessão:") for linha in linhas)
    assert any(linha.startswith("Status atual do acompanhamento:") for linha in linhas)
    assert any(linha.startswith("Transições válidas:") for linha in linhas)

    print("13. formatar_snapshot_status_texto: OK")


def testar_formatar_validacao_status_texto(registros):
    resultado = validar_consistencia_status_acompanhamento(registros)
    linhas = formatar_validacao_status_texto(resultado)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Sequência válida:") for linha in linhas)
    assert any(linha.startswith("Total de registros:") for linha in linhas)
    assert any(linha.startswith("Transições avaliadas:") for linha in linhas)

    print("14. formatar_validacao_status_texto: OK")


def testar_seguranca_arquitetural(snapshot):
    import star_governance.status_acompanhamento as modulo_status

    textos = [
        json.dumps(snapshot),
        gerar_leitura_status_acompanhamento(snapshot),
    ]
    textos.extend(formatar_snapshot_status_texto(snapshot))

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    codigo_fonte = ""
    with open(modulo_status.__file__, "r", encoding="utf-8") as arquivo:
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
    payload_teste = _construir_payload_historico_simulado()

    testar_obter_status_acompanhamento_permitidos()
    testar_obter_transicoes_status_permitidas()
    testar_status_eh_final()
    testar_status_exige_evidencia()
    testar_status_exige_decisao()
    testar_avaliar_transicao_status()
    testar_sugerir_status_conceituais_permitidos()
    testar_ordenar_registros_por_criado_em()
    testar_obter_status_atual_acompanhamento()
    registros_teste = testar_validar_consistencia_status_acompanhamento(payload_teste)
    snapshot_teste = testar_criar_snapshot_status_acompanhamento(payload_teste, registros_teste)
    testar_gerar_leitura_status_acompanhamento()
    testar_formatar_snapshot_status_texto(snapshot_teste)
    testar_formatar_validacao_status_texto(registros_teste)
    testar_seguranca_arquitetural(snapshot_teste)

    print("STATUS_ACOMPANHAMENTO_OK")
