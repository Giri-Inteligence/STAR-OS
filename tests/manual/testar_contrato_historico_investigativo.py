"""
Teste manual simples do Contrato de Dados do Historico Investigativo
(star_persistence/contrato_historico.py). Executavel diretamente por
python, sem pytest. Nao usa IA, nao chama API externa, nao consome token,
nao salva nada em disco, nao cria banco de dados.

Uso:
    python tests/manual/testar_contrato_historico_investigativo.py
"""

import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pandas as pd

from star_persistence.contrato_historico import (
    limpar_valor_serializavel,
    garantir_json_serializavel,
    gerar_id_deterministico,
    gerar_timestamp_iso,
    normalizar_status_sessao,
    criar_cliente_investigado,
    criar_sessao_investigativa,
    criar_snapshot_star,
    criar_itens_investigativos_payload,
    criar_pacote_investigativo_payload,
    criar_conclusao_investigativa_payload,
    criar_metadados_execucao,
    criar_payload_historico_investigativo,
    validar_payload_historico,
    formatar_validacao_payload_texto,
)

TERMOS_FRASE_PROIBIDOS = (
    "automaticamente",
    "executar tarefa",
    "criar tarefa",
    "enviar mensagem",
    "acionar agente",
    "causa raiz confirmada",
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


def testar_limpar_valor_serializavel():
    class ObjetoDesconhecido:
        def __repr__(self):
            return "ObjetoDesconhecidoRepr"

    assert limpar_valor_serializavel(None) is None
    assert limpar_valor_serializavel("texto") == "texto"
    assert limpar_valor_serializavel(10) == 10
    assert limpar_valor_serializavel(10.5) == 10.5
    assert limpar_valor_serializavel(float("nan")) is None
    assert limpar_valor_serializavel(float("inf")) is None
    assert limpar_valor_serializavel(float("-inf")) is None
    assert limpar_valor_serializavel([1, float("nan"), "x"]) == [1, None, "x"]
    assert limpar_valor_serializavel((1, 2, 3)) == [1, 2, 3]
    assert limpar_valor_serializavel({1: "a", "b": 2}) == {"1": "a", "b": 2}
    assert limpar_valor_serializavel(ObjetoDesconhecido()) == "ObjetoDesconhecidoRepr"

    print("limpar_valor_serializavel: OK")


def testar_garantir_json_serializavel():
    payload_original = {"a": float("nan"), "b": [1, 2, float("inf")], "c": (1, 2)}
    payload_copia = copy.deepcopy(payload_original)

    limpo = garantir_json_serializavel(payload_original)

    assert payload_original == payload_copia, "o payload original nao deveria ser alterado"

    json.dumps(limpo)

    print("garantir_json_serializavel: OK")


def testar_gerar_id_deterministico():
    id1 = gerar_id_deterministico("cliente", ["Empresa Alfa", "Joao", "Curitiba"])
    id2 = gerar_id_deterministico("cliente", ["Empresa Alfa", "Joao", "Curitiba"])
    id3 = gerar_id_deterministico("cliente", ["Empresa Beta", "Maria", "Sao Paulo"])

    assert id1 == id2, "o mesmo input deveria gerar o mesmo ID"
    assert id1 != id3, "inputs diferentes deveriam gerar IDs diferentes"
    assert id1.startswith("CLIENTE_")
    assert len(id1.split("_")[-1]) == 12

    print("gerar_id_deterministico: OK")


def testar_gerar_timestamp_iso():
    timestamp_atual = gerar_timestamp_iso()
    assert isinstance(timestamp_atual, str) and timestamp_atual != ""

    timestamp_string = gerar_timestamp_iso("2025-01-01T00:00:00")
    assert timestamp_string == "2025-01-01T00:00:00"

    print("gerar_timestamp_iso: OK")


def testar_normalizar_status_sessao():
    casos = [
        ("aberta", "ABERTA"),
        ("em andamento", "EM_ANDAMENTO"),
        ("concluída", "CONCLUIDA"),
        ("arquivada", "ARQUIVADA"),
        ("desconhecido", "ABERTA"),
    ]

    for entrada, esperado in casos:
        resultado = normalizar_status_sessao(entrada)
        assert resultado == esperado, f"{entrada!r}: esperado {esperado}, obtido {resultado}"

    print("normalizar_status_sessao: OK")


def testar_criar_cliente_investigado():
    cliente = criar_cliente_investigado(nome_cliente="Empresa Alfa Ltda", vendedor="Joao", cidade="Curitiba")

    assert cliente["cliente_id"] != ""
    assert cliente["nome_cliente"] == "Empresa Alfa Ltda"
    assert cliente["vendedor"] == "Joao"
    assert cliente["cidade"] == "Curitiba"
    assert cliente["criado_em"] != ""
    assert cliente["atualizado_em"] != ""

    print("criar_cliente_investigado: OK")

    return cliente


def testar_criar_sessao_investigativa(cliente):
    sessao = criar_sessao_investigativa(cliente_id=cliente["cliente_id"], versao_modelo="5.2")

    assert sessao["sessao_id"] != ""
    assert sessao["cliente_id"] == cliente["cliente_id"]
    assert sessao["status_sessao"] == "ABERTA"
    assert sessao["versao_modelo"] == "5.2"

    print("criar_sessao_investigativa: OK")

    return sessao


def testar_criar_snapshot_star(sessao, cliente):
    linha_star = {
        "STATUS": "QUEDA ACENTUADA", "CURVA": "A", "MEDIA LP": 10000, "MEDIA CP": 3000,
        "MESES_SEM_COMPRA": 6, "EROSAO STAR": 8, "META": 10500, "ACAO": "Reverter queda",
    }

    snapshot_dict = criar_snapshot_star(linha_star, sessao_id=sessao["sessao_id"], cliente_id=cliente["cliente_id"])
    snapshot_series = criar_snapshot_star(
        pd.Series(linha_star), sessao_id=sessao["sessao_id"], cliente_id=cliente["cliente_id"]
    )

    for snapshot in (snapshot_dict, snapshot_series):
        assert snapshot["snapshot_id"] != ""
        assert snapshot["status_star"] == "QUEDA ACENTUADA"
        assert snapshot["curva"] == "A"
        assert snapshot["media_lp"] == 10000.0
        assert snapshot["media_cp"] == 3000.0

    print("criar_snapshot_star: OK")


def testar_criar_itens_investigativos_payload():
    itens = [
        {"id_item": "INV_001", "origem": "PERGUNTA_VALIDACAO", "pergunta": "A queda ocorreu por volume?",
         "status": "CONFIRMADA", "resposta": "Sim", "evidencia": "Relatorio X"},
        None,
        "invalido",
        {"id_item": "INV_002", "origem": "PERGUNTA_VALIDACAO", "pergunta": "Existe concorrente?",
         "status": "PENDENTE", "resposta": "", "evidencia": ""},
    ]

    payload_itens = criar_itens_investigativos_payload(itens, sessao_id="SESSAO_TESTE")

    assert isinstance(payload_itens, list)
    assert len(payload_itens) == 2
    assert payload_itens[0]["item_id"] != ""
    assert payload_itens[0]["pergunta"] == "A queda ocorreu por volume?"
    assert payload_itens[0]["status_investigativo"] == "CONFIRMADA"
    assert payload_itens[0]["resposta"] == "Sim"
    assert payload_itens[0]["evidencia_textual"] == "Relatorio X"

    print("criar_itens_investigativos_payload: OK")


def testar_criar_pacote_investigativo_payload():
    pacote_investigativo = {
        "status_star": "QUEDA ACENTUADA", "curva": "A", "nivel_prioridade": "P1 CRITICA",
        "tipo_prioridade": "PRESERVACAO", "resumo_hipotese": "resumo",
        "resumo_investigacao": {"total_itens": 2}, "maturidade_investigacao": "PARCIAL",
        "leitura_consolidada": "leitura",
    }

    pacote_payload = criar_pacote_investigativo_payload(
        pacote_investigativo, sessao_id="SESSAO_TESTE", cliente_id="CLIENTE_TESTE"
    )

    assert pacote_payload["pacote_id"] != ""
    assert pacote_payload["resumo_investigacao"] == {"total_itens": 2}
    assert pacote_payload["maturidade_investigacao"] == "PARCIAL"
    assert pacote_payload["leitura_consolidada"] == "leitura"

    print("criar_pacote_investigativo_payload: OK")

    return pacote_payload


def testar_criar_conclusao_investigativa_payload(pacote_payload):
    conclusao_investigativa = {
        "leitura_conclusao": "leitura conclusiva",
        "resumo_conclusao": {
            "status_conclusivo_geral": "CLASSIFICACAO PARCIAL",
            "hipoteses_confirmadas": 1, "hipoteses_descartadas": 1, "hipoteses_inconclusivas": 1,
            "pendentes_validacao": 1, "respostas_sem_classificacao": 1,
        },
    }

    conclusao_payload = criar_conclusao_investigativa_payload(
        conclusao_investigativa, pacote_id=pacote_payload["pacote_id"], sessao_id="SESSAO_TESTE"
    )

    assert conclusao_payload["conclusao_id"] != ""
    assert conclusao_payload["status_conclusivo_geral"] == "CLASSIFICACAO PARCIAL"
    assert conclusao_payload["hipoteses_confirmadas_count"] == 1
    assert conclusao_payload["hipoteses_descartadas_count"] == 1

    print("criar_conclusao_investigativa_payload: OK")


def testar_criar_metadados_execucao():
    metadados = criar_metadados_execucao(sessao_id="SESSAO_TESTE", arquivo_origem_nome="planilha.xlsx")

    assert metadados["execucao_id"] != ""
    assert metadados["arquivo_origem_nome"] == "planilha.xlsx"
    assert metadados["versao_modelo_persistencia"] == "5.2"

    print("criar_metadados_execucao: OK")


def testar_criar_payload_historico_investigativo():
    linha_star = {
        "STATUS": "QUEDA ACENTUADA", "CURVA": "A", "MEDIA LP": 10000, "MEDIA CP": 3000,
        "MESES_SEM_COMPRA": 6, "EROSAO STAR": 8, "META": 10500, "ACAO": "Reverter queda",
    }
    itens = [
        {"id_item": "INV_001", "origem": "PERGUNTA_VALIDACAO", "pergunta": "A queda ocorreu por volume?",
         "status": "CONFIRMADA", "resposta": "Sim", "evidencia": "Relatorio X"},
    ]
    pacote_investigativo = {
        "status_star": "QUEDA ACENTUADA", "curva": "A", "nivel_prioridade": "P1 CRITICA",
        "tipo_prioridade": "PRESERVACAO", "resumo_hipotese": "resumo",
        "resumo_investigacao": {"total_itens": 1}, "maturidade_investigacao": "PARCIAL",
        "leitura_consolidada": "leitura",
    }
    conclusao_investigativa = {
        "leitura_conclusao": "leitura conclusiva",
        "resumo_conclusao": {
            "status_conclusivo_geral": "CLASSIFICACAO PARCIAL",
            "hipoteses_confirmadas": 1, "hipoteses_descartadas": 0, "hipoteses_inconclusivas": 0,
            "pendentes_validacao": 0, "respostas_sem_classificacao": 0,
        },
    }

    linha_star_copia = copy.deepcopy(linha_star)
    itens_copia = copy.deepcopy(itens)
    pacote_copia = copy.deepcopy(pacote_investigativo)
    conclusao_copia = copy.deepcopy(conclusao_investigativa)

    arquivos_antes = set(os.listdir(os.path.dirname(os.path.abspath(__file__))))

    payload = criar_payload_historico_investigativo(
        nome_cliente="Empresa Alfa Ltda", vendedor="Joao", cidade="Curitiba",
        linha_star=linha_star, itens_investigativos=itens,
        pacote_investigativo=pacote_investigativo, conclusao_investigativa=conclusao_investigativa,
        arquivo_origem_nome="planilha.xlsx", usuario_responsavel="consultor",
    )

    arquivos_depois = set(os.listdir(os.path.dirname(os.path.abspath(__file__))))

    assert linha_star == linha_star_copia, "linha_star nao deveria ser alterada"
    assert itens == itens_copia, "itens nao deveriam ser alterados"
    assert pacote_investigativo == pacote_copia, "pacote_investigativo nao deveria ser alterado"
    assert conclusao_investigativa == conclusao_copia, "conclusao_investigativa nao deveria ser alterada"
    assert arquivos_antes == arquivos_depois, "nenhum arquivo deveria ser criado em disco"

    assert isinstance(payload, dict)

    for chave in (
        "versao_contrato", "cliente", "sessao", "snapshot_star", "itens_investigativos",
        "pacote_investigativo", "conclusao_investigativa", "metadados_execucao",
    ):
        assert chave in payload, f"{chave} ausente no payload"

    json.dumps(payload)

    print("criar_payload_historico_investigativo: OK")

    return payload


def testar_validar_payload_historico(payload):
    resultado_completo = validar_payload_historico(payload)
    assert resultado_completo["valido"] is True
    assert resultado_completo["erros"] == []

    payload_sem_itens = dict(payload)
    payload_sem_itens["itens_investigativos"] = []
    resultado_sem_itens = validar_payload_historico(payload_sem_itens)
    assert resultado_sem_itens["valido"] is True
    assert len(resultado_sem_itens["avisos"]) > 0

    resultado_invalido = validar_payload_historico({"algo": "errado"})
    assert resultado_invalido["valido"] is False
    assert len(resultado_invalido["erros"]) > 0

    print("validar_payload_historico: OK")

    return resultado_completo


def testar_formatar_validacao_payload_texto(resultado):
    linhas = formatar_validacao_payload_texto(resultado)

    assert isinstance(linhas, list)
    assert all(isinstance(linha, str) for linha in linhas)
    assert any("Payload" in linha for linha in linhas)

    print("formatar_validacao_payload_texto: OK")


def testar_seguranca_arquitetural(payload):
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

    for pasta in (pasta_scratch, pasta_raiz, os.path.join(pasta_raiz, "star_persistence")):
        for nome_arquivo in os.listdir(pasta):
            for extensao in EXTENSOES_PERSISTENCIA_PROIBIDAS:
                if nome_arquivo.lower().endswith(extensao):
                    raise AssertionError(f"arquivo de persistencia funcional encontrado: {nome_arquivo}")

    print("seguranca arquitetural: OK")


if __name__ == "__main__":
    testar_limpar_valor_serializavel()
    testar_garantir_json_serializavel()
    testar_gerar_id_deterministico()
    testar_gerar_timestamp_iso()
    testar_normalizar_status_sessao()
    cliente_teste = testar_criar_cliente_investigado()
    sessao_teste = testar_criar_sessao_investigativa(cliente_teste)
    testar_criar_snapshot_star(sessao_teste, cliente_teste)
    testar_criar_itens_investigativos_payload()
    pacote_payload_teste = testar_criar_pacote_investigativo_payload()
    testar_criar_conclusao_investigativa_payload(pacote_payload_teste)
    testar_criar_metadados_execucao()
    payload_teste = testar_criar_payload_historico_investigativo()
    resultado_teste = testar_validar_payload_historico(payload_teste)
    testar_formatar_validacao_payload_texto(resultado_teste)
    testar_seguranca_arquitetural(payload_teste)
    print("CONTRATO_HISTORICO_INVESTIGATIVO_OK")
