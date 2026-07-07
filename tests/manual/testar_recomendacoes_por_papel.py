"""
Teste manual simples das Recomendacoes por Papel
(star_intelligence/recomendacoes.py). Executavel diretamente por python,
sem pytest. Nao usa IA, nao chama API externa, nao consome token.

Uso:
    python tests/manual/testar_recomendacoes_por_papel.py
"""

import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_intelligence.recomendacoes import (
    normalizar_papel,
    definir_foco_por_status,
    gerar_recomendacoes_por_papel,
    gerar_recomendacoes_multiplos_papeis,
    formatar_recomendacoes_texto,
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


def testar_normalizar_papel():
    casos = [
        ("vendedor", "VENDEDOR"),
        ("gestor", "GESTOR"),
        ("gerente", "GESTOR"),
        ("sócio", "SOCIO"),
        ("ceo", "SOCIO"),
        ("diretor", "SOCIO"),
        ("consultor", "CONSULTOR"),
        ("desconhecido", "CONSULTOR"),
    ]

    for entrada, esperado in casos:
        resultado = normalizar_papel(entrada)
        assert resultado == esperado, f"{entrada!r}: esperado {esperado}, obtido {resultado}"

    print("normalizar_papel: OK")


def testar_definir_foco_por_status():
    casos = [
        ({"STATUS": "INATIVO"}, "REATIVACAO"),
        ({"STATUS": "QUEDA"}, "PRESERVACAO DE RECEITA"),
        ({"STATUS": "QUEDA ACENTUADA"}, "PRESERVACAO DE RECEITA"),
        ({"STATUS": "ESTAVEL", "EROSAO STAR": 5}, "INVESTIGACAO DE EROSAO"),
        ({"STATUS": "ESTAVEL", "EROSAO STAR": 4}, "MONITORAMENTO"),
        ({"STATUS": "CRESCIMENTO"}, "EXPANSAO CONTROLADA"),
        ({"STATUS": "CRESCIMENTO ACENTUADO"}, "EXPANSAO CONTROLADA"),
    ]

    for dados, esperado in casos:
        resultado = definir_foco_por_status(pd.Series(dados))
        assert resultado == esperado, f"{dados}: esperado {esperado}, obtido {resultado}"

    print("definir_foco_por_status: OK")


def testar_gerar_recomendacoes_por_papel():
    row = pd.Series({
        "CURVA": "A",
        "STATUS": "QUEDA ACENTUADA",
        "MESES_SEM_COMPRA": 6,
        "EROSAO STAR": 8,
        "MEDIA LP": 10000,
        "MEDIA CP": 3000,
        "NIVEL_PRIORIDADE": "P1 CRITICA",
        "TIPO_PRIORIDADE": "PRESERVACAO",
    })

    for papel in ("VENDEDOR", "GESTOR", "SOCIO", "CONSULTOR"):
        pacote = gerar_recomendacoes_por_papel(row, papel)

        assert pacote["papel"] == papel
        assert pacote["foco_operacional"] != ""
        assert len(pacote["recomendacoes"]) > 0
        assert len(pacote["observacoes"]) > 0

        texto = " ".join(pacote["recomendacoes"]) + " " + " ".join(pacote["observacoes"])
        achado = _termo_proibido_encontrado(texto)
        assert achado is None, f"{papel}: termo proibido encontrado: {achado!r}"

    print("gerar_recomendacoes_por_papel: OK")

    return row


def testar_gerar_recomendacoes_multiplos_papeis(row):
    todos = gerar_recomendacoes_multiplos_papeis(row)

    for papel in ("VENDEDOR", "GESTOR", "SOCIO", "CONSULTOR"):
        assert papel in todos, f"{papel} ausente no resultado"
        assert len(todos[papel]["recomendacoes"]) > 0

    print("gerar_recomendacoes_multiplos_papeis: OK")

    return todos


def testar_formatar_recomendacoes_texto(row, todos):
    linhas_papel_unico = formatar_recomendacoes_texto(gerar_recomendacoes_por_papel(row, "VENDEDOR"))

    assert isinstance(linhas_papel_unico, list)
    assert all(isinstance(linha, str) for linha in linhas_papel_unico)
    assert any(linha.startswith("Papel:") for linha in linhas_papel_unico)
    assert any(linha.startswith("Foco operacional:") for linha in linhas_papel_unico)
    assert any(linha.startswith("Recomenda") for linha in linhas_papel_unico)

    linhas_todos = formatar_recomendacoes_texto(todos)
    assert len([linha for linha in linhas_todos if linha.startswith("Papel:")]) == 4

    print("formatar_recomendacoes_texto: OK")


def testar_seguranca_metodologica(todos):
    texto_completo = " ".join(
        " ".join(pacote["recomendacoes"]) + " " + " ".join(pacote["observacoes"])
        for pacote in todos.values()
    )

    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    print("seguranca metodologica: OK")


if __name__ == "__main__":
    testar_normalizar_papel()
    testar_definir_foco_por_status()
    linha_teste = testar_gerar_recomendacoes_por_papel()
    todos_papeis = testar_gerar_recomendacoes_multiplos_papeis(linha_teste)
    testar_formatar_recomendacoes_texto(linha_teste, todos_papeis)
    testar_seguranca_metodologica(todos_papeis)
    print("RECOMENDACOES_POR_PAPEL_OK")
