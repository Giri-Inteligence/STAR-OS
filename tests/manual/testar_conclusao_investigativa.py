"""
Teste manual simples da Classificacao de Conclusao Investigativa
(star_intelligence/conclusao_investigativa.py). Executavel diretamente por
python, sem pytest. Nao usa IA, nao chama API externa, nao consome token,
nao conclui causa raiz automaticamente.

Uso:
    python tests/manual/testar_conclusao_investigativa.py
"""

import copy
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_intelligence.conclusao_investigativa import (
    normalizar_classificacao_conclusiva,
    classificar_item_investigativo,
    classificar_itens_investigativos,
    resumir_conclusao_investigativa,
    gerar_leitura_conclusao_investigativa,
    gerar_conclusao_investigativa,
    formatar_conclusao_investigativa_texto,
    gerar_tabela_conclusao,
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


def _termo_proibido_encontrado(texto):
    texto_lower = texto.lower()

    for termo in TERMOS_FRASE_PROIBIDOS:
        if termo in texto_lower:
            return termo

    for padrao in TERMOS_PALAVRA_PROIBIDOS:
        if re.search(padrao, texto_lower):
            return padrao

    return None


def testar_normalizar_classificacao_conclusiva():
    casos = [
        ("confirmada", "HIPOTESE CONFIRMADA"),
        ("confirmado", "HIPOTESE CONFIRMADA"),
        ("descartada", "HIPOTESE DESCARTADA"),
        ("descartado", "HIPOTESE DESCARTADA"),
        ("inconclusiva", "HIPOTESE INCONCLUSIVA"),
        ("inconclusivo", "HIPOTESE INCONCLUSIVA"),
        ("pendente", "PENDENTE DE VALIDACAO"),
        ("resposta sem classificação", "RESPOSTA SEM CLASSIFICACAO"),
        ("", "PENDENTE DE VALIDACAO"),
        (None, "PENDENTE DE VALIDACAO"),
        ("desconhecido", "PENDENTE DE VALIDACAO"),
    ]

    for entrada, esperado in casos:
        resultado = normalizar_classificacao_conclusiva(entrada)
        assert resultado == esperado, f"{entrada!r}: esperado {esperado}, obtido {resultado}"

    print("normalizar_classificacao_conclusiva: OK")


def testar_classificar_item_investigativo():
    item_confirmada = {"id_item": "INV_001", "pergunta": "P1?", "status": "CONFIRMADA", "resposta": "sim", "evidencia": "doc"}
    item_copia = copy.deepcopy(item_confirmada)
    resultado = classificar_item_investigativo(item_confirmada)

    assert item_confirmada == item_copia, "o item original nao deveria ser alterado"
    assert resultado["classificacao_conclusiva"] == "HIPOTESE CONFIRMADA"
    assert resultado["tem_resposta"] is True
    assert resultado["tem_evidencia"] is True
    assert resultado["leitura_item"] != ""

    r_descartada = classificar_item_investigativo({"id_item": "INV_002", "pergunta": "P2?", "status": "DESCARTADA", "resposta": "", "evidencia": ""})
    assert r_descartada["classificacao_conclusiva"] == "HIPOTESE DESCARTADA"

    r_inconclusiva = classificar_item_investigativo({"id_item": "INV_003", "pergunta": "P3?", "status": "INCONCLUSIVA", "resposta": "", "evidencia": ""})
    assert r_inconclusiva["classificacao_conclusiva"] == "HIPOTESE INCONCLUSIVA"

    r_pendente_sem_resposta = classificar_item_investigativo({"id_item": "INV_004", "pergunta": "P4?", "status": "PENDENTE", "resposta": "", "evidencia": ""})
    assert r_pendente_sem_resposta["classificacao_conclusiva"] == "PENDENTE DE VALIDACAO"

    r_pendente_com_resposta = classificar_item_investigativo({"id_item": "INV_005", "pergunta": "P5?", "status": "PENDENTE", "resposta": "algo", "evidencia": ""})
    assert r_pendente_com_resposta["classificacao_conclusiva"] == "RESPOSTA SEM CLASSIFICACAO"

    r_desconhecido = classificar_item_investigativo({"id_item": "INV_006", "pergunta": "P6?", "status": "XYZ", "resposta": "", "evidencia": ""})
    assert r_desconhecido["status_investigativo"] == "PENDENTE"
    assert r_desconhecido["classificacao_conclusiva"] == "PENDENTE DE VALIDACAO"

    print("classificar_item_investigativo: OK")


def testar_classificar_itens_investigativos():
    itens = [
        {"id_item": "INV_001", "pergunta": "P1?", "status": "CONFIRMADA", "resposta": "sim", "evidencia": ""},
        None,
        "string invalida",
        {"id_item": "INV_002", "pergunta": "P2?", "status": "DESCARTADA", "resposta": "", "evidencia": ""},
    ]
    itens_copia = copy.deepcopy(itens)

    classificacoes = classificar_itens_investigativos(itens)

    assert itens == itens_copia, "a lista original nao deveria ser alterada"
    assert len(classificacoes) == 2

    print("classificar_itens_investigativos: OK")


def testar_resumir_conclusao_investigativa():
    classificacoes = [
        {"classificacao_conclusiva": "HIPOTESE CONFIRMADA", "tem_resposta": True, "tem_evidencia": False},
        {"classificacao_conclusiva": "HIPOTESE DESCARTADA", "tem_resposta": True, "tem_evidencia": False},
        {"classificacao_conclusiva": "HIPOTESE INCONCLUSIVA", "tem_resposta": True, "tem_evidencia": False},
        {"classificacao_conclusiva": "PENDENTE DE VALIDACAO", "tem_resposta": False, "tem_evidencia": False},
        {"classificacao_conclusiva": "RESPOSTA SEM CLASSIFICACAO", "tem_resposta": True, "tem_evidencia": True},
    ]

    resumo = resumir_conclusao_investigativa(classificacoes)

    assert resumo["total_itens"] == 5
    assert resumo["hipoteses_confirmadas"] == 1
    assert resumo["hipoteses_descartadas"] == 1
    assert resumo["hipoteses_inconclusivas"] == 1
    assert resumo["pendentes_validacao"] == 1
    assert resumo["respostas_sem_classificacao"] == 1
    assert resumo["percentual_classificado"] == 60.0
    assert resumo["status_conclusivo_geral"] == "CLASSIFICACAO PARCIAL"

    print("resumir_conclusao_investigativa: OK")

    return resumo


def testar_gerar_leitura_conclusao_investigativa(resumo):
    leitura = gerar_leitura_conclusao_investigativa(resumo)

    assert isinstance(leitura, str) and leitura != ""
    assert "causa" not in leitura.lower()
    assert _termo_proibido_encontrado(leitura) is None

    print("gerar_leitura_conclusao_investigativa: OK")


def testar_gerar_conclusao_investigativa():
    pacote_investigativo = {
        "cliente": "Empresa Alfa Ltda",
        "status_star": "QUEDA ACENTUADA",
        "nivel_prioridade": "P1 CRITICA",
        "tipo_prioridade": "PRESERVACAO",
        "itens_investigativos": [
            {"id_item": "INV_001", "pergunta": "A queda ocorreu por volume?", "status": "CONFIRMADA", "resposta": "Sim, volume caiu", "evidencia": "Relatorio X"},
            {"id_item": "INV_002", "pergunta": "Existe concorrente atuando?", "status": "DESCARTADA", "resposta": "Nao ha concorrente", "evidencia": ""},
            {"id_item": "INV_003", "pergunta": "Houve mudança de decisor?", "status": "INCONCLUSIVA", "resposta": "Nao sabemos", "evidencia": ""},
            {"id_item": "INV_004", "pergunta": "O vendedor manteve contato?", "status": "PENDENTE", "resposta": "", "evidencia": ""},
            {"id_item": "INV_005", "pergunta": "Qual evidência confirma a hipótese?", "status": "PENDENTE", "resposta": "Ainda apurando", "evidencia": ""},
        ],
    }
    pacote_copia = copy.deepcopy(pacote_investigativo)

    conclusao = gerar_conclusao_investigativa(pacote_investigativo)

    assert pacote_investigativo == pacote_copia, "o pacote original nao deveria ser alterado"
    assert conclusao["cliente"] == "Empresa Alfa Ltda"
    assert len(conclusao["resumo_conclusao"]) > 0
    assert conclusao["leitura_conclusao"] != ""
    assert len(conclusao["hipoteses_confirmadas"]) == 1
    assert len(conclusao["hipoteses_descartadas"]) == 1
    assert len(conclusao["hipoteses_inconclusivas"]) == 1
    assert len(conclusao["pendentes_validacao"]) == 1
    assert len(conclusao["respostas_sem_classificacao"]) == 1

    print("gerar_conclusao_investigativa: OK")

    return conclusao


def testar_formatar_conclusao_investigativa_texto(conclusao):
    linhas = formatar_conclusao_investigativa_texto(conclusao)

    assert isinstance(linhas, list)
    assert all(isinstance(linha, str) for linha in linhas)
    assert any("Empresa Alfa" in linha for linha in linhas)
    assert any(conclusao["resumo_conclusao"]["status_conclusivo_geral"] in linha for linha in linhas)
    assert any(conclusao["leitura_conclusao"] in linha for linha in linhas)

    print("formatar_conclusao_investigativa_texto: OK")


def testar_gerar_tabela_conclusao(conclusao):
    tabela = gerar_tabela_conclusao(conclusao)

    assert isinstance(tabela, list)
    assert len(tabela) == 5

    colunas_esperadas = {"ID", "Pergunta", "Status investigativo", "Classificação conclusiva", "Resposta", "Evidência", "Leitura do item"}
    assert set(tabela[0].keys()) == colunas_esperadas

    print("gerar_tabela_conclusao: OK")


def testar_seguranca_metodologica(conclusao):
    textos = formatar_conclusao_investigativa_texto(conclusao)

    for item in conclusao["classificacoes"]:
        textos.append(item["pergunta"])
        textos.append(item["resposta"])
        textos.append(item["evidencia"])
        textos.append(item["leitura_item"])

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    print("seguranca metodologica: OK")


if __name__ == "__main__":
    testar_normalizar_classificacao_conclusiva()
    testar_classificar_item_investigativo()
    testar_classificar_itens_investigativos()
    resumo_teste = testar_resumir_conclusao_investigativa()
    testar_gerar_leitura_conclusao_investigativa(resumo_teste)
    conclusao_teste = testar_gerar_conclusao_investigativa()
    testar_formatar_conclusao_investigativa_texto(conclusao_teste)
    testar_gerar_tabela_conclusao(conclusao_teste)
    testar_seguranca_metodologica(conclusao_teste)
    print("CONCLUSAO_INVESTIGATIVA_OK")
