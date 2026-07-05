"""
Teste manual simples da Configuracao de Persistencia
(star_persistence/configuracao.py). Executavel diretamente por python,
sem pytest. Usa tempfile.TemporaryDirectory quando necessario. Nao usa
IA, nao chama API externa, nao consome token, nao cria banco permanente.

Uso:
    python tests/manual/testar_configuracao_persistencia.py
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from star_persistence.configuracao import (
    obter_caminho_db_historico,
    preparar_diretorio_db,
    caminho_db_esta_no_repositorio,
    validar_caminho_db_historico,
    formatar_validacao_caminho_db,
)

EXTENSOES_PERSISTENCIA_PROIBIDAS = (".db", ".sqlite", ".sqlite3", ".json")


def testar_obter_caminho_db_historico():
    valor_original = os.environ.pop("STAR_OS_HISTORICO_DB", None)

    try:
        caminho_padrao = obter_caminho_db_historico()
        assert isinstance(caminho_padrao, str) and caminho_padrao != ""
        assert not os.path.exists(caminho_padrao)

        with tempfile.TemporaryDirectory() as tmpdir:
            caminho_customizado = str(Path(tmpdir) / "customizado.sqlite")
            os.environ["STAR_OS_HISTORICO_DB"] = caminho_customizado

            caminho_obtido = obter_caminho_db_historico()
            assert caminho_obtido == caminho_customizado
    finally:
        os.environ.pop("STAR_OS_HISTORICO_DB", None)
        if valor_original is not None:
            os.environ["STAR_OS_HISTORICO_DB"] = valor_original

    print("1. obter_caminho_db_historico: OK")


def testar_preparar_diretorio_db():
    try:
        preparar_diretorio_db("")
        raise AssertionError("preparar_diretorio_db deveria levantar ValueError para db_path vazio")
    except ValueError:
        pass

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = str(Path(tmpdir) / "subpasta" / "historico.sqlite")

        diretorio_criado = preparar_diretorio_db(db_path)

        assert os.path.isdir(diretorio_criado)
        assert not os.path.exists(db_path), "preparar_diretorio_db nao deveria criar o arquivo do banco"

    print("2. preparar_diretorio_db: OK")


def testar_caminho_db_esta_no_repositorio():
    with tempfile.TemporaryDirectory() as tmpdir:
        raiz = Path(tmpdir)
        caminho_dentro = str(raiz / "subpasta" / "historico.sqlite")
        caminho_fora = str(Path(tempfile.gettempdir()) / "fora_da_raiz" / "historico.sqlite")

        assert caminho_db_esta_no_repositorio(caminho_dentro, raiz_repositorio=str(raiz)) is True
        assert caminho_db_esta_no_repositorio(caminho_fora, raiz_repositorio=str(raiz)) is False

    print("3. caminho_db_esta_no_repositorio: OK")


def testar_validar_caminho_db_historico():
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho_valido = str(Path(tmpdir) / "historico.sqlite")
        resultado_valido = validar_caminho_db_historico(caminho_valido)

        assert resultado_valido["valido"] is True
        assert resultado_valido["erros"] == []
        assert not os.path.exists(caminho_valido)

        caminho_extensao_incomum = str(Path(tmpdir) / "historico.dat")
        resultado_extensao = validar_caminho_db_historico(caminho_extensao_incomum)

        assert resultado_extensao["valido"] is True
        assert len(resultado_extensao["avisos"]) >= 1

        caminho_no_cwd = str(Path.cwd() / "dentro_do_repo.sqlite")
        resultado_dentro = validar_caminho_db_historico(caminho_no_cwd)

        assert resultado_dentro["valido"] is True
        assert len(resultado_dentro["avisos"]) >= 1
        assert not os.path.exists(caminho_no_cwd)

    print("4. validar_caminho_db_historico: OK")


def testar_formatar_validacao_caminho_db():
    resultado = validar_caminho_db_historico(str(Path(tempfile.gettempdir()) / "historico.sqlite"))
    linhas = formatar_validacao_caminho_db(resultado)

    assert isinstance(linhas, list)
    assert any("Caminho do banco" in linha for linha in linhas)
    assert any("Caminho válido" in linha for linha in linhas)

    print("5. formatar_validacao_caminho_db: OK")


def testar_seguranca_arquitetural():
    import star_persistence.configuracao as modulo_configuracao

    codigo_fonte = ""
    with open(modulo_configuracao.__file__, "r", encoding="utf-8") as arquivo:
        codigo_fonte = arquivo.read()

    assert "import streamlit" not in codigo_fonte.lower()
    assert "import pandas" not in codigo_fonte.lower()
    assert "import requests" not in codigo_fonte.lower()
    assert "openai" not in codigo_fonte.lower()
    assert "anthropic" not in codigo_fonte.lower()

    pasta_scratch = os.path.dirname(os.path.abspath(__file__))
    pasta_raiz = os.path.abspath(os.path.join(pasta_scratch, "..", ".."))

    for pasta in (pasta_scratch, pasta_raiz, os.path.join(pasta_raiz, "star_persistence")):
        for nome_arquivo in os.listdir(pasta):
            for extensao in EXTENSOES_PERSISTENCIA_PROIBIDAS:
                if nome_arquivo.lower().endswith(extensao):
                    raise AssertionError(f"arquivo de persistencia funcional encontrado: {nome_arquivo}")

    print("6. seguranca arquitetural: OK")


if __name__ == "__main__":
    testar_obter_caminho_db_historico()
    testar_preparar_diretorio_db()
    testar_caminho_db_esta_no_repositorio()
    testar_validar_caminho_db_historico()
    testar_formatar_validacao_caminho_db()
    testar_seguranca_arquitetural()
    print("CONFIGURACAO_PERSISTENCIA_OK")
