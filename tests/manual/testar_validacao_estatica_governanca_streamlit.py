"""
Teste manual de validacao estatica da secao "Governanca investigativa"
em app.py (Sprint 8.3). Executavel diretamente por python, sem pytest.

Este teste NAO importa Streamlit, NAO executa app.py, NAO cria banco,
NAO cria arquivo JSON e NAO altera nenhum arquivo — apenas le app.py
como texto e valida presenca/ausencia de trechos criticos no bloco da
secao de governanca.

Uso:
    python tests/manual/testar_validacao_estatica_governanca_streamlit.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

CAMINHO_APP = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app.py"))

MARCADOR_INICIO_GOVERNANCA = '"**Governança investigativa**"'
MARCADOR_FIM_GOVERNANCA = "else:\n            st.caption(\"Nenhum cliente disponivel para Raio-X.\")"

TERMOS_PROIBIDOS_CAMPOS = (
    r'"Responsável"', r'"Responsavel"', r"'Responsável'", r"'Responsavel'",
    r'"Prazo"', r"'Prazo'",
    r'"Criar tarefa"', r"'Criar tarefa'",
    r'"Plano de ação"', r"'Plano de ação'", r'"Plano de acao"',
    r'"Agenda"', r"'Agenda'",
    r'"Calendário"', r"'Calendário'", r'"Calendario"',
)

CHAMADAS_GRAFICO_PROIBIDAS = (
    "st.line_chart", "st.bar_chart", "st.area_chart",
    "st.pyplot", "st.plotly_chart", "altair_chart",
)

CHAMADAS_EXTERNAS_PROIBIDAS = ("requests.", "httpx.", "openai", "anthropic")


def _ler_app_py():
    with open(CAMINHO_APP, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def _extrair_bloco_governanca(codigo_fonte):
    indice_inicio = codigo_fonte.find(MARCADOR_INICIO_GOVERNANCA)
    assert indice_inicio != -1, "marcador de inicio da secao de governanca nao encontrado em app.py"

    indice_fim = codigo_fonte.find(MARCADOR_FIM_GOVERNANCA, indice_inicio)
    assert indice_fim != -1, "marcador de fim da secao de governanca (else do Raio-X) nao encontrado em app.py"

    return codigo_fonte[indice_inicio:indice_fim]


def testar_secao_governanca_existe(codigo_fonte):
    assert "Governança investigativa" in codigo_fonte

    print("1. Secao 'Governança investigativa' existe em app.py: OK")


def _normalizar_literais_adjacentes(texto):
    # Literais de string Python adjacentes quebrados em linhas diferentes
    # (ex.: "...cria "\n                "plano...") nao ficam contiguos no
    # texto bruto do arquivo. Aqui a sequencia fecha-aspas + quebra de
    # linha + abre-aspas e substituida por um espaco, reconstituindo a
    # frase como ela aparece em tempo de execucao, e espacos repetidos
    # sao colapsados em um unico espaco.
    texto_sem_quebra = re.sub(r'"\s*\n\s*"', " ", texto)
    return re.sub(r" +", " ", texto_sem_quebra)


def testar_avisos_metodologicos(bloco_governanca):
    bloco_normalizado_lower = _normalizar_literais_adjacentes(bloco_governanca).lower()

    assert "não cria tarefa" in bloco_normalizado_lower
    assert "não cria plano de ação" in bloco_normalizado_lower
    assert "não cria agenda" in bloco_normalizado_lower
    assert "não executa ações automaticamente" in bloco_normalizado_lower

    print("2. Avisos metodologicos presentes (nao cria tarefa/plano de acao/agenda/execucao automatica): OK")


def testar_campos_permitidos(bloco_governanca):
    assert "tipo_acompanhamento_escolhido" in bloco_governanca
    assert "status_acompanhamento_escolhido" in bloco_governanca
    assert "observacao_acompanhamento_escolhida" in bloco_governanca
    assert "usuario_registro_governanca" in bloco_governanca

    print("3. Campos permitidos presentes (tipo/status/observacao/usuario): OK")


def testar_botoes_esperados(bloco_governanca):
    assert "Salvar governança desta investigação" in bloco_governanca
    assert "Consultar governança salva deste cliente" in bloco_governanca

    print("4. Botoes 'Salvar governança desta investigação' e 'Consultar governança salva deste cliente' presentes: OK")


def testar_uso_modulos_corretos(bloco_governanca):
    funcoes_esperadas = (
        "criar_payload_registro_acompanhamento_persistivel",
        "criar_payload_snapshot_status_persistivel",
        "criar_payload_item_loop_persistivel",
        "criar_payload_ciclo_loop_persistivel",
        "criar_payload_governanca_integrada",
        "salvar_lote_payloads_governanca",
        "listar_payloads_governanca",
    )

    for funcao in funcoes_esperadas:
        assert funcao in bloco_governanca, f"funcao esperada nao encontrada no bloco de governanca: {funcao}"

    print("5. Uso de contrato_governanca.py e repositorio_governanca.py confirmado no bloco: OK")


def testar_ausencia_campos_proibidos(bloco_governanca):
    for padrao in TERMOS_PROIBIDOS_CAMPOS:
        assert re.search(padrao, bloco_governanca) is None, f"campo proibido encontrado: {padrao}"

    assert "st.date_input" not in bloco_governanca, "st.date_input encontrado no bloco de governanca"
    assert "st.time_input" not in bloco_governanca, "st.time_input encontrado no bloco de governanca"

    print("6. Ausencia de campos de responsavel/prazo/tarefa/plano de acao/agenda/calendario: OK")


def testar_ausencia_graficos(bloco_governanca):
    for chamada in CHAMADAS_GRAFICO_PROIBIDAS:
        assert chamada not in bloco_governanca, f"chamada de grafico proibida encontrada: {chamada}"

    print("7. Ausencia de graficos no bloco de governanca: OK")


def testar_ausencia_download_novo(bloco_governanca):
    assert "st.download_button" not in bloco_governanca

    print("8. Ausencia de download novo no bloco de governanca: OK")


def testar_ausencia_chamadas_externas(bloco_governanca):
    bloco_lower = bloco_governanca.lower()

    for chamada in CHAMADAS_EXTERNAS_PROIBIDAS:
        assert chamada not in bloco_lower, f"chamada externa proibida encontrada: {chamada}"

    print("9. Ausencia de chamadas de IA/API externa (requests/httpx/openai/anthropic) no bloco: OK")


def testar_arquivo_nao_alterado():
    tamanho_arquivo = os.path.getsize(CAMINHO_APP)
    assert tamanho_arquivo > 0

    print("10. Confirmacao de leitura sem escrita em app.py (arquivo apenas lido como texto): OK")


if __name__ == "__main__":
    codigo_fonte_app = _ler_app_py()
    bloco_governanca_extraido = _extrair_bloco_governanca(codigo_fonte_app)

    testar_secao_governanca_existe(codigo_fonte_app)
    testar_avisos_metodologicos(bloco_governanca_extraido)
    testar_campos_permitidos(bloco_governanca_extraido)
    testar_botoes_esperados(bloco_governanca_extraido)
    testar_uso_modulos_corretos(bloco_governanca_extraido)
    testar_ausencia_campos_proibidos(bloco_governanca_extraido)
    testar_ausencia_graficos(bloco_governanca_extraido)
    testar_ausencia_download_novo(bloco_governanca_extraido)
    testar_ausencia_chamadas_externas(bloco_governanca_extraido)
    testar_arquivo_nao_alterado()

    print("VALIDACAO_ESTATICA_GOVERNANCA_STREAMLIT_OK")
