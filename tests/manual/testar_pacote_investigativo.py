"""
Teste manual simples do Pacote Investigativo do Cliente
(star_intelligence/pacote_investigativo.py). Executavel diretamente por
python, sem pytest. Nao usa IA, nao chama API externa, nao consome token,
nao usa banco de dados nem persistencia.

Uso:
    python tests/manual/testar_pacote_investigativo.py
"""

import copy
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_intelligence.pacote_investigativo import (
    obter_lista_segura,
    contar_itens_por_status,
    extrair_evidencias_registradas,
    classificar_maturidade_investigacao,
    gerar_pacote_investigativo_cliente,
    formatar_pacote_investigativo_texto,
    gerar_tabela_evidencias,
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


def testar_obter_lista_segura():
    assert obter_lista_segura(["a", "b"]) == ["a", "b"]
    assert obter_lista_segura(("a", "b")) == ["a", "b"]
    assert obter_lista_segura(None) == []
    assert obter_lista_segura("") == []
    assert obter_lista_segura("x") == ["x"]

    print("obter_lista_segura: OK")


def testar_contar_itens_por_status():
    itens = [
        {"status": "PENDENTE"},
        {"status": "CONFIRMADA"},
        {"status": "DESCARTADA"},
        {"status": "INCONCLUSIVA"},
        {"status": "ALGO_DESCONHECIDO"},
    ]

    contagem = contar_itens_por_status(itens)

    assert contagem == {"PENDENTE": 2, "CONFIRMADA": 1, "DESCARTADA": 1, "INCONCLUSIVA": 1}

    print("contar_itens_por_status: OK")


def testar_extrair_evidencias_registradas():
    itens = [
        {"id_item": "INV_001", "pergunta": "P1?", "status": "CONFIRMADA", "resposta": "sim", "evidencia": ""},
        {"id_item": "INV_002", "pergunta": "P2?", "status": "PENDENTE", "resposta": "", "evidencia": "doc"},
        {"id_item": "INV_003", "pergunta": "P3?", "status": "PENDENTE", "resposta": "", "evidencia": ""},
    ]

    evidencias = extrair_evidencias_registradas(itens)

    assert len(evidencias) == 2
    assert evidencias[0]["id_item"] == "INV_001"
    assert evidencias[0]["pergunta"] == "P1?"
    assert evidencias[0]["resposta"] == "sim"
    assert evidencias[1]["id_item"] == "INV_002"
    assert evidencias[1]["evidencia"] == "doc"

    print("extrair_evidencias_registradas: OK")


def testar_classificar_maturidade_investigacao():
    casos = [
        ({"total_itens": 0, "percentual_respondido": 0, "inconclusivas": 0}, "SEM INVESTIGACAO"),
        ({"total_itens": 5, "percentual_respondido": 0, "inconclusivas": 0}, "NAO INICIADA"),
        ({"total_itens": 5, "percentual_respondido": 30, "inconclusivas": 0}, "INICIAL"),
        ({"total_itens": 5, "percentual_respondido": 70, "inconclusivas": 0}, "PARCIAL"),
        ({"total_itens": 5, "percentual_respondido": 100, "inconclusivas": 1}, "CONSOLIDADA COM PENDENCIAS"),
        ({"total_itens": 5, "percentual_respondido": 100, "inconclusivas": 0}, "CONSOLIDADA"),
    ]

    for resumo, esperado in casos:
        resultado = classificar_maturidade_investigacao(resumo)
        assert resultado == esperado, f"{resumo}: esperado {esperado}, obtido {resultado}"

    print("classificar_maturidade_investigacao: OK")


def testar_gerar_pacote_investigativo_cliente():
    raio_x = {
        "cliente": "Empresa Alfa Ltda",
        "vendedor": "Joao",
        "cidade": "Curitiba",
        "curva": "A",
        "status": "QUEDA ACENTUADA",
        "nivel_prioridade": "P1 CRITICA",
        "tipo_prioridade": "PRESERVACAO",
        "leitura_operacional": "Cliente relevante com forte sinal de deterioração.",
    }
    pacote_hipoteses = {
        "resumo_hipotese": "Cliente com hipóteses de preservação de receita a investigar.",
        "hipoteses_status": ["Possível perda relevante de volume."],
        "hipoteses_sinais": ["Por ser curva A, a queda pode representar risco relevante de receita."],
        "perguntas_validacao": [
            "A queda ocorreu por volume, frequência ou mix?",
            "Existe concorrente atuando neste cliente?",
        ],
    }
    recomendacoes = {
        "VENDEDOR": {
            "papel": "VENDEDOR", "foco_operacional": "PRESERVACAO DE RECEITA",
            "recomendacoes": ["Verificar volume."], "observacoes": [],
        },
        "GESTOR": {
            "papel": "GESTOR", "foco_operacional": "PRESERVACAO DE RECEITA",
            "recomendacoes": ["Priorizar conta."], "observacoes": [],
        },
    }
    pacote_investigacao = {
        "cliente": "Empresa Alfa Ltda",
        "vendedor": "Joao",
        "cidade": "Curitiba",
        "itens": [
            {
                "id_item": "INV_001", "origem": "PERGUNTA_VALIDACAO",
                "pergunta": "A queda ocorreu por volume, frequência ou mix?",
                "status": "CONFIRMADA", "resposta": "Foi por volume", "evidencia": "Relatorio X",
            },
            {
                "id_item": "INV_002", "origem": "PERGUNTA_VALIDACAO",
                "pergunta": "Existe concorrente atuando neste cliente?",
                "status": "PENDENTE", "resposta": "", "evidencia": "",
            },
        ],
        "resumo": {
            "total_itens": 2, "pendentes": 1, "confirmadas": 1, "descartadas": 0, "inconclusivas": 0,
            "respondidas": 1, "percentual_respondido": 50.0, "status_geral": "EM ANDAMENTO",
        },
    }

    raio_x_copia = copy.deepcopy(raio_x)
    pacote_hipoteses_copia = copy.deepcopy(pacote_hipoteses)
    recomendacoes_copia = copy.deepcopy(recomendacoes)
    pacote_investigacao_copia = copy.deepcopy(pacote_investigacao)

    pacote = gerar_pacote_investigativo_cliente(raio_x, pacote_hipoteses, recomendacoes, pacote_investigacao)

    assert raio_x == raio_x_copia, "raio_x nao deveria ser alterado"
    assert pacote_hipoteses == pacote_hipoteses_copia, "pacote_hipoteses nao deveria ser alterado"
    assert recomendacoes == recomendacoes_copia, "recomendacoes nao deveria ser alterado"
    assert pacote_investigacao == pacote_investigacao_copia, "pacote_investigacao nao deveria ser alterado"

    assert pacote["cliente"] == "Empresa Alfa Ltda"
    assert pacote["vendedor"] == "Joao"
    assert pacote["cidade"] == "Curitiba"
    assert pacote["status_star"] == "QUEDA ACENTUADA"
    assert pacote["resumo_hipotese"] == "Cliente com hipóteses de preservação de receita a investigar."
    assert len(pacote["itens_investigativos"]) == 2
    assert pacote["resumo_investigacao"]["total_itens"] == 2
    assert pacote["contagem_status_investigativo"]["CONFIRMADA"] == 1
    assert len(pacote["evidencias_registradas"]) == 1
    assert pacote["maturidade_investigacao"] != ""
    assert pacote["leitura_consolidada"] != ""

    print("gerar_pacote_investigativo_cliente: OK")

    return pacote


def testar_formatar_pacote_investigativo_texto(pacote):
    linhas = formatar_pacote_investigativo_texto(pacote)

    assert isinstance(linhas, list)
    assert all(isinstance(linha, str) for linha in linhas)
    assert any("Empresa Alfa" in linha for linha in linhas)
    assert any("QUEDA ACENTUADA" in linha for linha in linhas)
    assert any(pacote["maturidade_investigacao"] in linha for linha in linhas)

    print("formatar_pacote_investigativo_texto: OK")


def testar_gerar_tabela_evidencias(pacote):
    tabela = gerar_tabela_evidencias(pacote)

    assert isinstance(tabela, list)
    assert len(tabela) == 1
    assert set(tabela[0].keys()) == {"ID", "Pergunta", "Status", "Resposta", "Evidência"}

    print("gerar_tabela_evidencias: OK")


def testar_seguranca_metodologica(pacote):
    textos = formatar_pacote_investigativo_texto(pacote)

    for item in pacote["itens_investigativos"]:
        textos.append(item["pergunta"])
        textos.append(item["resposta"])
        textos.append(item["evidencia"])

    for pacote_papel in pacote["recomendacoes"].values():
        textos.extend(pacote_papel.get("recomendacoes", []))
        textos.extend(pacote_papel.get("observacoes", []))

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    print("seguranca metodologica: OK")


if __name__ == "__main__":
    testar_obter_lista_segura()
    testar_contar_itens_por_status()
    testar_extrair_evidencias_registradas()
    testar_classificar_maturidade_investigacao()
    pacote_teste = testar_gerar_pacote_investigativo_cliente()
    testar_formatar_pacote_investigativo_texto(pacote_teste)
    testar_gerar_tabela_evidencias(pacote_teste)
    testar_seguranca_metodologica(pacote_teste)
    print("PACOTE_INVESTIGATIVO_OK")
