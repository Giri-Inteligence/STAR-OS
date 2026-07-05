"""
Teste manual simples da Configuracao de Governanca
(star_persistence/configuracao_governanca.py). Executavel diretamente
por python, sem pytest. Nao usa IA, nao chama API externa, nao consome
token, nao cria banco permanente.

Uso:
    python tests/manual/testar_configuracao_governanca.py
"""

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_persistence.configuracao_governanca import (
    normalizar_caminho_governanca,
    obter_caminho_padrao_banco_governanca,
    obter_caminho_banco_governanca,
    gerar_resumo_configuracao_governanca,
    formatar_configuracao_governanca_texto,
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
    "causa raiz confirmada",
    "recomendado",
    "deve fazer",
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


def testar_normalizar_caminho_governanca():
    assert normalizar_caminho_governanca(None) is None
    assert normalizar_caminho_governanca("") is None
    assert normalizar_caminho_governanca("C:/temp/governanca.sqlite") == Path("C:/temp/governanca.sqlite")
    assert normalizar_caminho_governanca(Path("C:/temp/governanca.sqlite")) == Path("C:/temp/governanca.sqlite")

    print("1. normalizar_caminho_governanca: OK")


def testar_obter_caminho_padrao_banco_governanca():
    caminho = obter_caminho_padrao_banco_governanca()

    assert isinstance(caminho, Path)
    assert caminho.name == "governanca.sqlite"
    assert caminho.parent.name == ".star_os"
    assert not caminho.exists()
    assert not caminho.parent.exists() or caminho.parent == Path.home() / ".star_os"

    print("2. obter_caminho_padrao_banco_governanca: OK")


def testar_obter_caminho_banco_governanca():
    valor_original = os.environ.pop("STAR_OS_GOVERNANCA_DB", None)

    try:
        caminho_padrao = obter_caminho_banco_governanca()
        assert caminho_padrao == obter_caminho_padrao_banco_governanca()
        assert not caminho_padrao.exists()

        os.environ["STAR_OS_GOVERNANCA_DB"] = "C:/temp/governanca_customizada.sqlite"
        caminho_customizado = obter_caminho_banco_governanca()
        assert caminho_customizado == Path("C:/temp/governanca_customizada.sqlite")
        assert not caminho_customizado.exists()
    finally:
        os.environ.pop("STAR_OS_GOVERNANCA_DB", None)
        if valor_original is not None:
            os.environ["STAR_OS_GOVERNANCA_DB"] = valor_original

    print("3. obter_caminho_banco_governanca: OK")


def testar_gerar_resumo_configuracao_governanca():
    resumo = gerar_resumo_configuracao_governanca()

    assert isinstance(resumo, dict)
    assert "variavel_ambiente" in resumo
    assert "caminho_banco_governanca" in resumo
    assert "diretorio_existe" in resumo
    assert "arquivo_existe" in resumo

    json.dumps(resumo)

    caminho_banco = Path(resumo["caminho_banco_governanca"])
    assert not caminho_banco.exists()

    print("4. gerar_resumo_configuracao_governanca: OK")

    return resumo


def testar_formatar_configuracao_governanca_texto(resumo):
    linhas = formatar_configuracao_governanca_texto(resumo)

    assert isinstance(linhas, list)
    assert any(linha.startswith("Banco de governança:") for linha in linhas)
    assert any(linha.startswith("Diretório existe:") for linha in linhas)
    assert any(linha.startswith("Arquivo existe:") for linha in linhas)
    assert any(linha.startswith("Persistência automática:") for linha in linhas)

    print("5. formatar_configuracao_governanca_texto: OK")


def testar_seguranca_arquitetural(resumo):
    import star_persistence.configuracao_governanca as modulo_configuracao_governanca

    textos = [json.dumps(resumo)]
    textos.extend(formatar_configuracao_governanca_texto(resumo))

    texto_completo = " ".join(textos)
    achado = _termo_proibido_encontrado(texto_completo)
    assert achado is None, f"termo proibido encontrado: {achado!r}"

    codigo_fonte = ""
    with open(modulo_configuracao_governanca.__file__, "r", encoding="utf-8") as arquivo:
        codigo_fonte = arquivo.read()

    assert "import streamlit" not in codigo_fonte.lower()
    assert "import pandas" not in codigo_fonte.lower()
    assert "import sqlite3" not in codigo_fonte.lower()
    assert "import requests" not in codigo_fonte.lower()
    assert "openai" not in codigo_fonte.lower()
    assert "anthropic" not in codigo_fonte.lower()

    print("6. seguranca arquitetural: OK")


if __name__ == "__main__":
    testar_normalizar_caminho_governanca()
    testar_obter_caminho_padrao_banco_governanca()
    testar_obter_caminho_banco_governanca()
    resumo_teste = testar_gerar_resumo_configuracao_governanca()
    testar_formatar_configuracao_governanca_texto(resumo_teste)
    testar_seguranca_arquitetural(resumo_teste)

    print("CONFIGURACAO_GOVERNANCA_OK")
