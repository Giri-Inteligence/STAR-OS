"""
Teste manual simples do Registro de Acompanhamento Operacional
(star_governance/acompanhamento.py). Executavel diretamente por python,
sem pytest. Nao usa IA, nao chama API externa, nao consome token, nao
salva nada em disco, nao cria banco de dados.

Uso:
    python tests/manual/testar_acompanhamento_operacional.py
"""

import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_governance.acompanhamento import (
    obter_dict_seguro,
    obter_lista_segura_governanca,
    normalizar_status_acompanhamento,
    normalizar_tipo_acompanhamento,
    extrair_contexto_payload_historico,
    criar_registro_acompanhamento,
    validar_registro_acompanhamento,
    gerar_leitura_acompanhamento,
    gerar_pacote_acompanhamento_operacional,
    formatar_registro_acompanhamento_texto,
    formatar_validacao_acompanhamento_texto,
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
            {"item_id": "ITEM_2", "pergunta": "Ha concorrencia nova?"},
        ],
        "pacote_investigativo": {"pacote_id": "PACOTE_TESTE789"},
        "conclusao_investigativa": {
            "conclusao_id": "CONCLUSAO_TESTE000",
            "status_conclusivo_geral": "PARCIAL",
            "leitura_conclusao": "Aguardando mais evidencias",
        },
    }


def testar_obter_dict_seguro():
    assert obter_dict_seguro({"a": 1}) == {"a": 1}
    assert obter_dict_seguro(None) == {}
    assert obter_dict_seguro([1, 2, 3]) == {}

    print("1. obter_dict_seguro: OK")


def testar_obter_lista_segura_governanca():
    assert obter_lista_segura_governanca(None) == []
    assert obter_lista_segura_governanca([1, 2]) == [1, 2]
    assert obter_lista_segura_governanca((1, 2)) == [1, 2]
    assert obter_lista_segura_governanca("texto") == ["texto"]

    print("2. obter_lista_segura_governanca: OK")


def testar_normalizar_status_acompanhamento():
    casos = [
        ("nao iniciado", "NAO_INICIADO"),
        ("em acompanhamento", "EM_ACOMPANHAMENTO"),
        ("aguardando evidência", "AGUARDANDO_EVIDENCIA"),
        ("aguardando decisão", "AGUARDANDO_DECISAO"),
        ("decisão registrada", "DECISAO_REGISTRADA"),
        ("encerrado", "ENCERRADO"),
        ("suspenso", "SUSPENSO"),
        ("desconhecido", "NAO_INICIADO"),
    ]

    for entrada, esperado in casos:
        resultado = normalizar_status_acompanhamento(entrada)
        assert resultado == esperado, f"{entrada!r}: esperado {esperado}, obtido {resultado}"

    print("3. normalizar_status_acompanhamento: OK")


def testar_normalizar_tipo_acompanhamento():
    casos = [
        ("observação", "OBSERVACAO"),
        ("retorno", "RETORNO"),
        ("complemento evidência", "COMPLEMENTO_EVIDENCIA"),
        ("revisão", "REVISAO"),
        ("decisão operacional", "DECISAO_OPERACIONAL"),
        ("pendência investigativa", "PENDENCIA_INVESTIGATIVA"),
        ("desconhecido", "OBSERVACAO"),
    ]

    for entrada, esperado in casos:
        resultado = normalizar_tipo_acompanhamento(entrada)
        assert resultado == esperado, f"{entrada!r}: esperado {esperado}, obtido {resultado}"

    print("4. normalizar_tipo_acompanhamento: OK")


def testar_extrair_contexto_payload_historico():
    payload = _construir_payload_historico_simulado()
    payload_copia = copy.deepcopy(payload)

    contexto = extrair_contexto_payload_historico(payload)

    assert payload == payload_copia, "payload_historico nao deveria ser alterado"
    assert contexto["cliente_id"] == "CLIENTE_TESTE123"
    assert contexto["sessao_id"] == "SESSAO_TESTE456"
    assert contexto["nome_cliente"] == "Empresa Alfa Ltda"
    assert contexto["status_star"] == "ALERTA"
    assert contexto["status_conclusivo_geral"] == "PARCIAL"
    assert contexto["total_itens_investigativos"] == 2

    contexto_vazio = extrair_contexto_payload_historico(None)
    assert contexto_vazio["cliente_id"] == ""

    print("5. extrair_contexto_payload_historico: OK")

    return payload


def testar_criar_registro_acompanhamento(payload):
    payload_copia = copy.deepcopy(payload)

    registro = criar_registro_acompanhamento(
        payload_historico=payload,
        tipo_acompanhamento="observação",
        status_acompanhamento="em acompanhamento",
        observacao_acompanhamento="Retorno registrado pelo consultor.",
        evidencia_complementar="Print da conversa com o cliente.",
        decisao_operacional="",
        usuario_registro="consultor",
    )

    assert payload == payload_copia, "payload_historico nao deveria ser alterado"
    assert registro["registro_id"] != ""
    assert registro["cliente_id"] == "CLIENTE_TESTE123"
    assert registro["sessao_id"] == "SESSAO_TESTE456"
    assert registro["tipo_acompanhamento"] == "OBSERVACAO"
    assert registro["status_acompanhamento"] == "EM_ACOMPANHAMENTO"
    assert registro["observacao_acompanhamento"] == "Retorno registrado pelo consultor."
    assert registro["evidencia_complementar"] == "Print da conversa com o cliente."
    assert registro["decisao_operacional"] == ""
    assert registro["referencias"]["pacote_id"] == "PACOTE_TESTE789"
    assert registro["referencias"]["conclusao_id"] == "CONCLUSAO_TESTE000"
    assert registro["referencias"]["total_itens_investigativos"] == 2

    json.dumps(registro)

    print("6. criar_registro_acompanhamento: OK")

    return registro


def testar_validar_registro_acompanhamento(registro):
    resultado_valido = validar_registro_acompanhamento(registro)
    assert resultado_valido["valido"] is True
    assert resultado_valido["erros"] == []

    registro_sem_conteudo = dict(registro)
    registro_sem_conteudo["observacao_acompanhamento"] = ""
    registro_sem_conteudo["evidencia_complementar"] = ""
    registro_sem_conteudo["decisao_operacional"] = ""
    resultado_sem_conteudo = validar_registro_acompanhamento(registro_sem_conteudo)
    assert resultado_sem_conteudo["valido"] is True
    assert len(resultado_sem_conteudo["avisos"]) >= 1

    resultado_invalido = validar_registro_acompanhamento({"algo": "errado"})
    assert resultado_invalido["valido"] is False
    assert len(resultado_invalido["erros"]) > 0

    registro_decisao_registrada = dict(registro)
    registro_decisao_registrada["status_acompanhamento"] = "DECISAO_REGISTRADA"
    registro_decisao_registrada["decisao_operacional"] = ""
    resultado_decisao = validar_registro_acompanhamento(registro_decisao_registrada)
    assert resultado_decisao["valido"] is True
    assert any("DECISAO_REGISTRADA" in aviso for aviso in resultado_decisao["avisos"])

    registro_aguardando_evidencia = dict(registro)
    registro_aguardando_evidencia["status_acompanhamento"] = "AGUARDANDO_EVIDENCIA"
    registro_aguardando_evidencia["evidencia_complementar"] = ""
    resultado_evidencia = validar_registro_acompanhamento(registro_aguardando_evidencia)
    assert resultado_evidencia["valido"] is True
    assert any("AGUARDANDO_EVIDENCIA" in aviso for aviso in resultado_evidencia["avisos"])

    print("7. validar_registro_acompanhamento: OK")


def testar_gerar_leitura_acompanhamento():
    for status in (
        "NAO_INICIADO", "EM_ACOMPANHAMENTO", "AGUARDANDO_EVIDENCIA",
        "AGUARDANDO_DECISAO", "DECISAO_REGISTRADA", "ENCERRADO", "SUSPENSO",
    ):
        leitura = gerar_leitura_acompanhamento({"status_acompanhamento": status})

        assert isinstance(leitura, str) and leitura != ""

        achado = _termo_proibido_encontrado(leitura)
        assert achado is None, f"leitura de {status} contem termo proibido: {achado!r}"

    print("8. gerar_leitura_acompanhamento: OK")


def testar_gerar_pacote_acompanhamento_operacional(payload, registro):
    registros_simulados = [
        registro,
        dict(registro, registro_id="OUTRO_1", status_acompanhamento="AGUARDANDO_DECISAO"),
        dict(registro, registro_id="OUTRO_2", status_acompanhamento="ENCERRADO"),
    ]
    registros_copia = copy.deepcopy(registros_simulados)

    pacote = gerar_pacote_acompanhamento_operacional(payload_historico=payload, registros=registros_simulados)

    assert registros_simulados == registros_copia, "registros originais nao deveriam ser alterados"
    assert pacote["cliente_id"] == "CLIENTE_TESTE123"
    assert pacote["sessao_id"] == "SESSAO_TESTE456"
    assert pacote["total_registros"] == 3
    assert pacote["resumo_acompanhamento"]["em_acompanhamento"] == 1
    assert pacote["resumo_acompanhamento"]["aguardando_decisao"] == 1
    assert pacote["resumo_acompanhamento"]["encerrado"] == 1

    json.dumps(pacote)

    print("9. gerar_pacote_acompanhamento_operacional: OK")


def testar_formatar_registro_acompanhamento_texto(registro):
    linhas = formatar_registro_acompanhamento_texto(registro)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Cliente:") for linha in linhas)
    assert any(linha.startswith("Sessão:") for linha in linhas)
    assert any(linha.startswith("Tipo de acompanhamento:") for linha in linhas)
    assert any(linha.startswith("Status de acompanhamento:") for linha in linhas)

    print("10. formatar_registro_acompanhamento_texto: OK")


def testar_formatar_validacao_acompanhamento_texto(registro):
    resultado = validar_registro_acompanhamento(registro)
    linhas = formatar_validacao_acompanhamento_texto(resultado)

    assert isinstance(linhas, list)
    assert any("Registro válido" in linha for linha in linhas)

    print("11. formatar_validacao_acompanhamento_texto: OK")


def testar_seguranca_arquitetural(registro):
    import star_governance.acompanhamento as modulo_acompanhamento

    textos = [
        json.dumps(registro),
        gerar_leitura_acompanhamento(registro),
    ]
    textos.extend(formatar_registro_acompanhamento_texto(registro))

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    codigo_fonte = ""
    with open(modulo_acompanhamento.__file__, "r", encoding="utf-8") as arquivo:
        codigo_fonte = arquivo.read()

    assert "import streamlit" not in codigo_fonte.lower()
    assert "import pandas" not in codigo_fonte.lower()
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

    print("12. seguranca arquitetural: OK")


if __name__ == "__main__":
    testar_obter_dict_seguro()
    testar_obter_lista_segura_governanca()
    testar_normalizar_status_acompanhamento()
    testar_normalizar_tipo_acompanhamento()
    payload_teste = testar_extrair_contexto_payload_historico()
    registro_teste = testar_criar_registro_acompanhamento(payload_teste)
    testar_validar_registro_acompanhamento(registro_teste)
    testar_gerar_leitura_acompanhamento()
    testar_gerar_pacote_acompanhamento_operacional(payload_teste, registro_teste)
    testar_formatar_registro_acompanhamento_texto(registro_teste)
    testar_formatar_validacao_acompanhamento_texto(registro_teste)
    testar_seguranca_arquitetural(registro_teste)
    print("ACOMPANHAMENTO_OPERACIONAL_OK")
