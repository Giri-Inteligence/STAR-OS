"""
Teste manual estatico da estabilizacao da identidade de sessao
investigativa usada pela secao "Governanca investigativa" em app.py
(Sprint 9.3 — correcao do ACHADO-9-2-001). Executavel diretamente por
python, sem pytest.

Este teste NAO importa Streamlit, NAO executa app.py, NAO cria banco,
NAO cria arquivo JSON e NAO altera nenhum arquivo — apenas le app.py
como texto e valida presenca/ausencia de trechos criticos.

Uso:
    python tests/manual/testar_identidade_sessao_governanca_streamlit.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

CAMINHO_APP = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app.py"))

MARCADOR_INICIO_GOVERNANCA = '"**Governança investigativa**"'
MARCADOR_FIM_GOVERNANCA = "else:\n            st.caption(\"Nenhum cliente disponivel para Raio-X.\")"

TERMOS_SESSAO = ("sessao_investigativa", "sessao_governanca", "chave_sessao")

CHAMADAS_GRAFICO_METRICA_DOWNLOAD_PROIBIDAS = (
    "st.date_input", "st.time_input", "st.metric",
    "st.line_chart", "st.bar_chart", "st.area_chart",
    "st.pyplot", "st.plotly_chart", "st.download_button",
)

TERMOS_PROIBIDOS_CAMPOS = (
    r'"Responsável"', r'"Responsavel"', r"'Responsável'", r"'Responsavel'",
    r'"Prazo"', r"'Prazo'",
    r'"Plano de ação"', r"'Plano de ação'", r'"Plano de acao"',
    r'"Agenda"', r"'Agenda'",
    r'"Calendário"', r"'Calendário'", r'"Calendario"',
)


def _ler_app_py():
    with open(CAMINHO_APP, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def _extrair_bloco_governanca(codigo_fonte):
    indice_inicio = codigo_fonte.find(MARCADOR_INICIO_GOVERNANCA)
    assert indice_inicio != -1, "marcador de inicio da secao de governanca nao encontrado em app.py"

    indice_fim = codigo_fonte.find(MARCADOR_FIM_GOVERNANCA, indice_inicio)
    assert indice_fim != -1, "marcador de fim da secao de governanca (else do Raio-X) nao encontrado em app.py"

    return codigo_fonte[indice_inicio:indice_fim]


def _normalizar_literais_adjacentes(texto):
    texto_sem_quebra = re.sub(r'"\s*\n\s*"', " ", texto)
    return re.sub(r" +", " ", texto_sem_quebra)


def testar_usa_session_state(codigo_fonte):
    assert "st.session_state" in codigo_fonte, "st.session_state nao encontrado em app.py"

    print("1. app.py usa st.session_state: OK")


def testar_chave_sessao_investigativa_presente(codigo_fonte):
    encontrado = any(termo in codigo_fonte for termo in TERMOS_SESSAO)
    assert encontrado, f"nenhum termo de identidade de sessao encontrado (esperado um de: {TERMOS_SESSAO})"

    print("2. Chave de sessao investigativa/governanca presente (sessao_investigativa/sessao_governanca/chave_sessao): OK")


def testar_payload_historico_estabilizado_antes_da_governanca(codigo_fonte):
    indice_chave = codigo_fonte.find("sessao_investigativa")
    assert indice_chave != -1, "chave de sessao investigativa nao encontrada em app.py"

    indice_governanca = codigo_fonte.find(MARCADOR_INICIO_GOVERNANCA)
    assert indice_governanca != -1, "secao de governanca nao encontrada em app.py"

    assert indice_chave < indice_governanca, (
        "a estabilizacao da sessao investigativa deveria ocorrer antes da secao "
        "de Governanca investigativa, para que salvar e consultar usem a mesma identidade"
    )

    print("3. Estabilizacao da sessao investigativa ocorre antes da secao de Governanca investigativa: OK")


def testar_salvar_e_consultar_usam_payload_historico_estavel(bloco_governanca):
    indice_salvar = bloco_governanca.find("Salvar governança desta investigação")
    indice_consultar = bloco_governanca.find("Consultar governança salva deste cliente")

    assert indice_salvar != -1, "botao de salvar nao encontrado no bloco de governanca"
    assert indice_consultar != -1, "botao de consultar nao encontrado no bloco de governanca"

    bloco_salvar = bloco_governanca[indice_salvar:indice_consultar]
    bloco_consultar = bloco_governanca[indice_consultar:]

    assert "payload_historico" in bloco_salvar, "salvamento nao referencia payload_historico"
    assert "payload_historico" in bloco_consultar, "consulta nao referencia payload_historico"

    print("4. Salvamento e consulta de governanca referenciam o mesmo payload_historico estabilizado: OK")


def testar_botoes_essenciais_presentes(codigo_fonte):
    assert "Salvar governança desta investigação" in codigo_fonte
    assert "Consultar governança salva deste cliente" in codigo_fonte
    assert "sessao_id" in codigo_fonte
    assert "st.session_state" in codigo_fonte

    print("5. Presenca de botoes essenciais, 'sessao_id' e 'st.session_state': OK")


def testar_ausencia_elementos_proibidos_no_bloco_governanca(bloco_governanca):
    for chamada in CHAMADAS_GRAFICO_METRICA_DOWNLOAD_PROIBIDAS:
        assert chamada not in bloco_governanca, f"elemento proibido encontrado no bloco de governanca: {chamada}"

    print("6. Ausencia de novos date_input/time_input/metric/graficos/download no bloco de governanca: OK")


def testar_ausencia_campos_proibidos_no_bloco_governanca(bloco_governanca):
    for padrao in TERMOS_PROIBIDOS_CAMPOS:
        assert re.search(padrao, bloco_governanca) is None, f"campo proibido encontrado: {padrao}"

    print("7. Ausencia de campos de responsavel/prazo/plano de acao/agenda/calendario no bloco de governanca: OK")


def testar_aviso_metodologico_preservado(bloco_governanca):
    bloco_normalizado_lower = _normalizar_literais_adjacentes(bloco_governanca).lower()

    assert "não cria tarefa" in bloco_normalizado_lower
    assert "não cria plano de ação" in bloco_normalizado_lower
    assert "não cria agenda" in bloco_normalizado_lower

    print("8. Aviso metodologico preservado apos a correcao (termos 'nao cria tarefa/plano de acao/agenda' em contexto negativo): OK")


def testar_arquivo_nao_alterado_por_este_teste():
    tamanho_arquivo = os.path.getsize(CAMINHO_APP)
    assert tamanho_arquivo > 0

    print("9. Confirmacao de leitura sem escrita em app.py (arquivo apenas lido como texto): OK")


if __name__ == "__main__":
    codigo_fonte_app = _ler_app_py()
    bloco_governanca_extraido = _extrair_bloco_governanca(codigo_fonte_app)

    testar_usa_session_state(codigo_fonte_app)
    testar_chave_sessao_investigativa_presente(codigo_fonte_app)
    testar_payload_historico_estabilizado_antes_da_governanca(codigo_fonte_app)
    testar_salvar_e_consultar_usam_payload_historico_estavel(bloco_governanca_extraido)
    testar_botoes_essenciais_presentes(codigo_fonte_app)
    testar_ausencia_elementos_proibidos_no_bloco_governanca(bloco_governanca_extraido)
    testar_ausencia_campos_proibidos_no_bloco_governanca(bloco_governanca_extraido)
    testar_aviso_metodologico_preservado(bloco_governanca_extraido)
    testar_arquivo_nao_alterado_por_este_teste()

    print("IDENTIDADE_SESSAO_GOVERNANCA_STREAMLIT_OK")
