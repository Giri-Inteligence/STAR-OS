"""
Teste manual simples do Motor de Investigacao Operacional
(star_intelligence/investigacao.py). Executavel diretamente por python,
sem pytest. Nao usa IA, nao chama API externa, nao consome token, nao usa
banco de dados nem persistencia.

Uso:
    python tests/manual/testar_investigacao_operacional.py
"""

import copy
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_intelligence.investigacao import (
    normalizar_status_investigacao,
    criar_item_investigacao,
    criar_itens_a_partir_perguntas,
    criar_pacote_investigacao,
    atualizar_item_investigacao,
    resumir_investigacao,
    gerar_leitura_investigacao,
    formatar_resumo_investigacao,
)

TERMOS_FRASE_PROIBIDOS = (
    "automaticamente",
    "executar tarefa",
    "criar tarefa",
    "enviar mensagem",
    "acionar agente",
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


def testar_normalizar_status_investigacao():
    casos = [
        ("pendente", "PENDENTE"),
        ("confirmada", "CONFIRMADA"),
        ("confirmado", "CONFIRMADA"),
        ("descartada", "DESCARTADA"),
        ("descartado", "DESCARTADA"),
        ("inconclusiva", "INCONCLUSIVA"),
        ("inconclusivo", "INCONCLUSIVA"),
        ("", "PENDENTE"),
        ("desconhecido", "PENDENTE"),
        (None, "PENDENTE"),
    ]

    for entrada, esperado in casos:
        resultado = normalizar_status_investigacao(entrada)
        assert resultado == esperado, f"{entrada!r}: esperado {esperado}, obtido {resultado}"

    print("normalizar_status_investigacao: OK")


def testar_criar_item_investigacao():
    item = criar_item_investigacao(
        "INV_001", "Pergunta teste?", status="confirmada", resposta="sim", evidencia="doc x"
    )

    assert isinstance(item, dict)
    assert item["id_item"] == "INV_001"
    assert item["pergunta"] == "Pergunta teste?"
    assert item["status"] == "CONFIRMADA"
    assert item["resposta"] == "sim"
    assert item["evidencia"] == "doc x"

    print("criar_item_investigacao: OK")


def testar_criar_itens_a_partir_perguntas():
    perguntas = [
        "Pergunta valida 1?",
        "Pergunta duplicada?",
        "",
        "Pergunta duplicada?",
        "Pergunta valida 2?",
    ]

    itens = criar_itens_a_partir_perguntas(perguntas)

    assert len(itens) == 3, f"esperado 3 itens, obtido {len(itens)}"
    assert itens[0]["id_item"] == "INV_001"
    assert itens[1]["id_item"] == "INV_002"
    assert itens[2]["id_item"] == "INV_003"
    assert all(item["status"] == "PENDENTE" for item in itens)

    print("criar_itens_a_partir_perguntas: OK")


def testar_criar_pacote_investigacao():
    pacote_hipoteses = {
        "perguntas_validacao": [
            "A queda ocorreu por volume, frequência ou mix?",
            "Existe concorrente atuando neste cliente?",
        ]
    }

    pacote = criar_pacote_investigacao(
        cliente="Empresa Alfa", vendedor="Joao", cidade="Curitiba", pacote_hipoteses=pacote_hipoteses
    )

    assert pacote["cliente"] == "Empresa Alfa"
    assert pacote["vendedor"] == "Joao"
    assert pacote["cidade"] == "Curitiba"
    assert len(pacote["itens"]) == 2
    assert "resumo" in pacote

    print("criar_pacote_investigacao: OK")

    return pacote


def testar_atualizar_item_investigacao(pacote):
    pacote_copia_original = copy.deepcopy(pacote)

    pacote_atualizado = atualizar_item_investigacao(
        pacote, "INV_001", status="confirmada", resposta="Foi por volume", evidencia="Relatorio X"
    )

    assert pacote == pacote_copia_original, "o pacote original nao deveria ser alterado"

    item_atualizado = next(item for item in pacote_atualizado["itens"] if item["id_item"] == "INV_001")
    assert item_atualizado["status"] == "CONFIRMADA"
    assert item_atualizado["resposta"] == "Foi por volume"
    assert item_atualizado["evidencia"] == "Relatorio X"

    # id inexistente nao deve gerar erro
    pacote_sem_erro = atualizar_item_investigacao(pacote, "INV_999", status="confirmada")
    assert isinstance(pacote_sem_erro, dict)

    print("atualizar_item_investigacao: OK")

    return pacote_atualizado


def testar_resumir_investigacao(pacote_atualizado):
    resumo = resumir_investigacao(pacote_atualizado)

    assert resumo["total_itens"] == 2
    assert resumo["pendentes"] == 1
    assert resumo["confirmadas"] == 1
    assert resumo["descartadas"] == 0
    assert resumo["inconclusivas"] == 0
    assert resumo["respondidas"] == 1
    assert resumo["percentual_respondido"] == 50.0
    assert resumo["status_geral"] == "EM ANDAMENTO"

    print("resumir_investigacao: OK")

    return resumo


def testar_gerar_leitura_investigacao(pacote_atualizado):
    leitura = gerar_leitura_investigacao(pacote_atualizado)

    assert isinstance(leitura, str) and leitura != ""
    assert _termo_proibido_encontrado(leitura) is None

    print("gerar_leitura_investigacao: OK")


def testar_formatar_resumo_investigacao(resumo):
    linhas = formatar_resumo_investigacao(resumo)

    assert isinstance(linhas, list)
    assert all(isinstance(linha, str) for linha in linhas)
    assert any("2" in linha for linha in linhas)
    assert any("EM ANDAMENTO" in linha for linha in linhas)

    print("formatar_resumo_investigacao: OK")


def testar_seguranca_metodologica(pacote_atualizado, resumo):
    textos = [gerar_leitura_investigacao(pacote_atualizado)] + formatar_resumo_investigacao(resumo)

    for item in pacote_atualizado["itens"]:
        textos.append(item["pergunta"])
        textos.append(item["resposta"])
        textos.append(item["evidencia"])

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    print("seguranca metodologica: OK")


if __name__ == "__main__":
    testar_normalizar_status_investigacao()
    testar_criar_item_investigacao()
    testar_criar_itens_a_partir_perguntas()
    pacote_teste = testar_criar_pacote_investigacao()
    pacote_atualizado_teste = testar_atualizar_item_investigacao(pacote_teste)
    resumo_teste = testar_resumir_investigacao(pacote_atualizado_teste)
    testar_gerar_leitura_investigacao(pacote_atualizado_teste)
    testar_formatar_resumo_investigacao(resumo_teste)
    testar_seguranca_metodologica(pacote_atualizado_teste, resumo_teste)
    print("INVESTIGACAO_OPERACIONAL_OK")
