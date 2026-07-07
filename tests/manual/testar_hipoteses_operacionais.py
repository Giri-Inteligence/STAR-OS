"""
Teste manual simples das Hipoteses Operacionais por Status
(star_intelligence/hipoteses.py). Executavel diretamente por python,
sem pytest. Nao usa IA, nao chama API externa, nao consome token.

Uso:
    python tests/manual/testar_hipoteses_operacionais.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_intelligence.hipoteses import (
    gerar_hipoteses_por_status,
    gerar_hipoteses_por_sinais,
    gerar_perguntas_validacao,
    gerar_alertas_investigacao,
    gerar_hipoteses_cliente,
    formatar_hipoteses_texto,
)

COMANDOS_PROIBIDOS = ("ligue", "visite", "ofereça", "oferece", "execute")


def testar_gerar_hipoteses_por_status():
    casos = [
        "INATIVO",
        "QUEDA ACENTUADA",
        "QUEDA",
        "ESTAVEL",
        "CRESCIMENTO",
        "CRESCIMENTO ACENTUADO",
    ]

    for status in casos:
        hipoteses = gerar_hipoteses_por_status(pd.Series({"STATUS": status}))
        assert len(hipoteses) > 0, f"{status}: hipoteses vazias"
        assert all(isinstance(h, str) for h in hipoteses)

    print("gerar_hipoteses_por_status: OK")


def testar_gerar_hipoteses_por_sinais():
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

    hipoteses = gerar_hipoteses_por_sinais(row)
    texto = " ".join(hipoteses).lower()

    assert "risco relevante de receita" in texto
    assert "longo per" in texto
    assert "deterioração forte" in texto or "deterioracao forte" in texto
    assert "muito abaixo da média de longo prazo" in texto or "muito abaixo da media de longo prazo" in texto
    assert "preservação de receita" in texto or "preservacao de receita" in texto

    print("gerar_hipoteses_por_sinais: OK")


def testar_gerar_perguntas_validacao():
    casos = [
        ({"STATUS": "INATIVO"}, "concorrente"),
        ({"STATUS": "QUEDA"}, "volume"),
        ({"STATUS": "ESTAVEL", "EROSAO STAR": 6}, "estabilidade"),
        ({"STATUS": "CRESCIMENTO"}, "recorrente"),
    ]

    for dados, palavra_esperada in casos:
        perguntas = gerar_perguntas_validacao(pd.Series(dados))
        assert len(perguntas) > 0
        assert any(palavra_esperada in p.lower() for p in perguntas), (
            f"{dados}: nao encontrou {palavra_esperada!r} em {perguntas}"
        )

    print("gerar_perguntas_validacao: OK")


def testar_gerar_alertas_investigacao():
    alertas_curva_a_queda = gerar_alertas_investigacao(pd.Series({"CURVA": "A", "STATUS": "QUEDA"}))
    assert any("governança" in a.lower() or "governanca" in a.lower() for a in alertas_curva_a_queda)

    alertas_inativo = gerar_alertas_investigacao(pd.Series({"STATUS": "INATIVO"}))
    assert any("desaparecer" in a.lower() for a in alertas_inativo)

    alertas_erosao = gerar_alertas_investigacao(pd.Series({"EROSAO STAR": 8}))
    assert any("validação de causa" in a.lower() or "validacao de causa" in a.lower() for a in alertas_erosao)

    alertas_crescimento = gerar_alertas_investigacao(pd.Series({"STATUS": "CRESCIMENTO ACENTUADO"}))
    assert any("cautela" in a.lower() for a in alertas_crescimento)

    print("gerar_alertas_investigacao: OK")


def testar_gerar_hipoteses_cliente():
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

    pacote = gerar_hipoteses_cliente(row)

    assert len(pacote["hipoteses_status"]) > 0
    assert len(pacote["hipoteses_sinais"]) > 0
    assert len(pacote["perguntas_validacao"]) > 0
    assert len(pacote["alertas_investigacao"]) > 0
    assert pacote["resumo_hipotese"] != ""

    texto_completo = " ".join(
        pacote["hipoteses_status"] + pacote["hipoteses_sinais"] + pacote["perguntas_validacao"]
        + pacote["alertas_investigacao"] + [pacote["resumo_hipotese"]]
    ).lower()

    for comando in COMANDOS_PROIBIDOS:
        assert comando not in texto_completo, f"comando de acao encontrado: {comando!r}"

    print("gerar_hipoteses_cliente: OK")

    return pacote


def testar_formatar_hipoteses_texto(pacote):
    linhas = formatar_hipoteses_texto(pacote)

    assert isinstance(linhas, list)
    assert all(isinstance(linha, str) for linha in linhas)
    assert len(linhas) > 0

    print("formatar_hipoteses_texto: OK")


if __name__ == "__main__":
    testar_gerar_hipoteses_por_status()
    testar_gerar_hipoteses_por_sinais()
    testar_gerar_perguntas_validacao()
    testar_gerar_alertas_investigacao()
    pacote_teste = testar_gerar_hipoteses_cliente()
    testar_formatar_hipoteses_texto(pacote_teste)
    print("HIPOTESES_OPERACIONAIS_OK")
