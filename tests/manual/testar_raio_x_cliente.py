"""
Teste manual simples do Raio-X Operacional do Cliente
(star_intelligence/raio_x_cliente.py). Executavel diretamente por python,
sem pytest.

Uso:
    python tests/manual/testar_raio_x_cliente.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_intelligence.raio_x_cliente import (
    calcular_variacao_media,
    classificar_sinal_variacao,
    gerar_sinais_operacionais_cliente,
    gerar_leitura_operacional_cliente,
    gerar_raio_x_cliente,
    formatar_raio_x_texto,
)


def testar_calcular_variacao_media():
    casos = [
        (10000, 3000, -70.0),
        (10000, 12000, 20.0),
        (0, 0, None),
        (0, 1000, None),
    ]

    for media_lp, media_cp, esperado in casos:
        resultado = calcular_variacao_media(media_lp, media_cp)
        assert resultado == esperado, f"lp={media_lp} cp={media_cp}: esperado {esperado}, obtido {resultado}"

    print("calcular_variacao_media: OK")


def testar_classificar_sinal_variacao():
    casos = [
        (10000, 0, "CURTO PRAZO ZERADO"),
        (10000, 3000, "FORTE REDUCAO"),
        (10000, 7000, "REDUCAO"),
        (10000, 10000, "ESTABILIDADE RELATIVA"),
        (10000, 13000, "CRESCIMENTO"),
        (0, 0, "SEM HISTORICO DE COMPRA"),
        (0, 1000, "COMPRA RECENTE SEM BASE HISTORICA"),
    ]

    for media_lp, media_cp, esperado in casos:
        resultado = classificar_sinal_variacao(media_lp, media_cp)
        assert resultado == esperado, f"lp={media_lp} cp={media_cp}: esperado {esperado}, obtido {resultado}"

    print("classificar_sinal_variacao: OK")


def testar_gerar_sinais_operacionais_cliente():
    row = pd.Series({
        "CURVA": "A",
        "STATUS": "QUEDA ACENTUADA",
        "MESES_SEM_COMPRA": 6,
        "EROSAO STAR": 8,
        "MEDIA LP": 10000,
        "MEDIA CP": 3000,
        "NIVEL_PRIORIDADE": "P1 CRITICA",
    })

    sinais = gerar_sinais_operacionais_cliente(row)

    assert "Cliente de alta relevância na carteira." in sinais
    assert "Cliente em queda acentuada." in sinais
    assert "Cliente com meses sem compra." in sinais
    assert "Cliente com longo período sem compra." in sinais
    assert "Erosão STAR elevada." in sinais
    assert "Curto prazo abaixo do longo prazo." in sinais
    assert "Cliente em prioridade crítica." in sinais

    print("gerar_sinais_operacionais_cliente: OK")


def testar_gerar_leitura_operacional_cliente():
    casos = [
        {"STATUS": "INATIVO"},
        {"STATUS": "QUEDA ACENTUADA", "CURVA": "A"},
        {"STATUS": "ESTAVEL", "EROSAO STAR": 6},
        {"STATUS": "CRESCIMENTO"},
    ]

    for dados in casos:
        leitura = gerar_leitura_operacional_cliente(pd.Series(dados))
        assert isinstance(leitura, str) and leitura != "", f"{dados}: leitura vazia ou invalida"

    leitura_inativo = gerar_leitura_operacional_cliente(pd.Series({"STATUS": "INATIVO"}))
    assert "inativo" in leitura_inativo.lower()

    leitura_deterioracao = gerar_leitura_operacional_cliente(pd.Series({"STATUS": "QUEDA ACENTUADA", "CURVA": "A"}))
    assert "deterioração" in leitura_deterioracao.lower()

    leitura_erosao = gerar_leitura_operacional_cliente(pd.Series({"STATUS": "ESTAVEL", "EROSAO STAR": 6}))
    assert "erosão" in leitura_erosao.lower()

    leitura_crescimento = gerar_leitura_operacional_cliente(pd.Series({"STATUS": "CRESCIMENTO"}))
    assert "crescimento" in leitura_crescimento.lower()

    print("gerar_leitura_operacional_cliente: OK")


def testar_gerar_raio_x_cliente():
    row = pd.Series({
        "NOME DO CLIENTE": "Empresa Alfa Ltda",
        "VENDEDOR": "Joao",
        "CIDADE": "Curitiba",
        "CURVA": "A",
        "STATUS": "QUEDA ACENTUADA",
        "MEDIA LP": 10000.0,
        "MEDIA CP": 3000.0,
        "MESES_SEM_COMPRA": 6,
        "EROSAO STAR": 8,
        "META": 10500,
        "ACAO": "Reverter queda",
        "PONTUACAO_PRIORIDADE": 134.0,
        "NIVEL_PRIORIDADE": "P1 CRITICA",
        "TIPO_PRIORIDADE": "PRESERVACAO",
    })

    raio_x = gerar_raio_x_cliente(row, "NOME DO CLIENTE", "VENDEDOR", "CIDADE")

    assert raio_x["cliente"] == "Empresa Alfa Ltda"
    assert raio_x["vendedor"] == "Joao"
    assert raio_x["cidade"] == "Curitiba"
    assert raio_x["status"] == "QUEDA ACENTUADA"
    assert raio_x["variacao_media_percentual"] == -70.0
    assert len(raio_x["sinais_operacionais"]) > 0
    assert raio_x["leitura_operacional"] != ""

    print("gerar_raio_x_cliente: OK")


def testar_formatar_raio_x_texto():
    row = pd.Series({
        "NOME DO CLIENTE": "Empresa Beta Ltda",
        "VENDEDOR": "Maria",
        "CURVA": "B",
        "STATUS": "ESTAVEL",
        "MEDIA LP": 5000.0,
        "MEDIA CP": 4800.0,
    })

    raio_x = gerar_raio_x_cliente(row, "NOME DO CLIENTE", "VENDEDOR", None)
    linhas = formatar_raio_x_texto(raio_x)

    assert isinstance(linhas, list)
    assert all(isinstance(linha, str) for linha in linhas)
    assert len(linhas) > 0

    print("formatar_raio_x_texto: OK")


if __name__ == "__main__":
    testar_calcular_variacao_media()
    testar_classificar_sinal_variacao()
    testar_gerar_sinais_operacionais_cliente()
    testar_gerar_leitura_operacional_cliente()
    testar_gerar_raio_x_cliente()
    testar_formatar_raio_x_texto()
    print("RAIO_X_CLIENTE_OK")
