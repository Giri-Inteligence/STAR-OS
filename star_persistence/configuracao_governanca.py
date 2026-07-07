"""
star_persistence.configuracao_governanca

Modulo determinístico de configuracao de caminho do banco SQLite de
Governança. Usa apenas biblioteca padrao (os, pathlib). Nao abre
conexao, nao cria banco, nao cria diretorio automaticamente, nao
importa Streamlit.
"""

import os
from pathlib import Path

VARIAVEL_AMBIENTE_GOVERNANCA_DB = "STAR_OS_GOVERNANCA_DB"


def normalizar_caminho_governanca(caminho=None):
    if not caminho:
        return None

    return Path(caminho).expanduser()


def obter_caminho_padrao_banco_governanca():
    return Path.home() / ".star_os" / "governanca.sqlite"


def obter_caminho_banco_governanca():
    caminho_env = os.environ.get(VARIAVEL_AMBIENTE_GOVERNANCA_DB, "")

    if caminho_env:
        return normalizar_caminho_governanca(caminho_env)

    return obter_caminho_padrao_banco_governanca()


def gerar_resumo_configuracao_governanca():
    caminho_env = os.environ.get(VARIAVEL_AMBIENTE_GOVERNANCA_DB, "")
    caminho_banco = obter_caminho_banco_governanca()

    return {
        "variavel_ambiente": VARIAVEL_AMBIENTE_GOVERNANCA_DB,
        "usa_variavel_ambiente": bool(caminho_env),
        "caminho_banco_governanca": str(caminho_banco),
        "diretorio_existe": caminho_banco.parent.exists(),
        "arquivo_existe": caminho_banco.exists(),
        "observacao": "Esta configuracao nao cria banco nem diretorio — o banco so e criado por acao explicita de salvamento.",
    }


def formatar_configuracao_governanca_texto(resumo=None):
    resumo = resumo or {}

    return [
        f"Banco de governança: {resumo.get('caminho_banco_governanca', '')}",
        f"Diretório existe: {'SIM' if resumo.get('diretorio_existe') else 'NAO'}",
        f"Arquivo existe: {'SIM' if resumo.get('arquivo_existe') else 'NAO'}",
        "Persistência automática: NAO",
    ]
