"""
star_persistence.configuracao

Modulo determinístico de configuracao de caminho do banco SQLite do
Historico Investigativo. Usa apenas biblioteca padrao (os, pathlib).
Nao abre conexao, nao cria banco, nao cria diretorio automaticamente,
nao importa Streamlit.
"""

import os
from pathlib import Path

EXTENSOES_VALIDAS_DB = (".sqlite", ".sqlite3", ".db")


def obter_caminho_db_historico():
    caminho_env = os.environ.get("STAR_OS_HISTORICO_DB", "")

    if caminho_env:
        return caminho_env

    return str(Path.home() / ".star_os" / "historico_investigativo.sqlite")


def preparar_diretorio_db(db_path):
    if not db_path:
        raise ValueError("db_path e obrigatorio para preparar o diretorio do repositorio local.")

    diretorio_pai = Path(db_path).parent
    diretorio_pai.mkdir(parents=True, exist_ok=True)

    return str(diretorio_pai)


def caminho_db_esta_no_repositorio(db_path, raiz_repositorio=None):
    if not db_path:
        return False

    try:
        raiz = Path(raiz_repositorio) if raiz_repositorio else Path.cwd()
        caminho_resolvido = Path(db_path).resolve()
        raiz_resolvida = raiz.resolve()

        return raiz_resolvida in caminho_resolvido.parents or caminho_resolvido == raiz_resolvida
    except Exception:
        return False


def validar_caminho_db_historico(db_path=None):
    db_path = db_path if db_path else obter_caminho_db_historico()

    resultado = {
        "valido": True,
        "db_path": str(db_path or ""),
        "avisos": [],
        "erros": [],
    }

    if not db_path:
        resultado["valido"] = False
        resultado["erros"].append("Caminho do banco esta vazio.")
        return resultado

    extensao = Path(db_path).suffix.lower()
    if extensao not in EXTENSOES_VALIDAS_DB:
        resultado["avisos"].append(
            f"Extensao incomum para banco SQLite: '{extensao or '(sem extensao)'}'."
        )

    if caminho_db_esta_no_repositorio(db_path):
        resultado["avisos"].append(
            "Banco configurado dentro do repositorio. Recomenda-se um caminho fora do projeto."
        )

    return resultado


def formatar_validacao_caminho_db(resultado):
    resultado = resultado or {}

    linhas = [
        f"Caminho do banco: {resultado.get('db_path', '')}",
        f"Caminho válido: {'SIM' if resultado.get('valido') else 'NAO'}",
        f"Avisos: {len(resultado.get('avisos') or [])}",
    ]

    for aviso in resultado.get("avisos") or []:
        linhas.append(f"Aviso: {aviso}")

    for erro in resultado.get("erros") or []:
        linhas.append(f"Erro: {erro}")

    return linhas
