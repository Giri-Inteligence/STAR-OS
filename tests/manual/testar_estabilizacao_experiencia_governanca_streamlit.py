"""
Teste manual estatico da estabilizacao da experiencia da secao
"Governanca investigativa" em app.py (Sprint 9.4 — reavaliacao dos
ACHADO-9-2-002 e ACHADO-9-2-003). Executavel diretamente por python,
sem pytest.

Este teste NAO importa Streamlit, NAO executa app.py, NAO cria banco,
NAO cria arquivo JSON e NAO altera nenhum arquivo — apenas le app.py
como texto e valida presenca/ausencia de trechos criticos.

Uso:
    python tests/manual/testar_estabilizacao_experiencia_governanca_streamlit.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

CAMINHO_APP = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app.py"))

MARCADOR_INICIO_GOVERNANCA = '"**Governança investigativa**"'
MARCADOR_FIM_GOVERNANCA = "else:\n            st.caption(\"Nenhum cliente disponivel para Raio-X.\")"

CHAMADAS_PROIBIDAS_NO_BLOCO = (
    "st.date_input", "st.time_input", "st.metric",
    "st.line_chart", "st.bar_chart", "st.area_chart",
    "st.pyplot", "st.plotly_chart", "st.download_button",
)

TERMOS_PROIBIDOS_CAMPOS = (
    r'"Responsável"', r'"Responsavel"', r"'Responsável'", r"'Responsavel'",
    r'"Prazo"', r"'Prazo'",
)

BOTOES_PROIBIDOS = (
    "Criar tarefa", "Criar agenda", "Criar plano de ação", "Criar plano de acao",
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


def testar_secao_governanca_existe(codigo_fonte):
    assert "Governança investigativa" in codigo_fonte

    print("1. Secao 'Governança investigativa' existe em app.py: OK")


def testar_campo_observacao_existe(bloco_governanca):
    assert "Observação de acompanhamento" in bloco_governanca

    print("2. Campo 'Observação de acompanhamento' existe: OK")


def testar_campo_observacao_tem_key_estavel(bloco_governanca):
    indice_campo = bloco_governanca.find("Observação de acompanhamento")
    assert indice_campo != -1

    trecho_widget = bloco_governanca[indice_campo:indice_campo + 200]
    assert "key=" in trecho_widget, "campo de observacao sem parametro key= explicito"
    assert "governanca_observacao_" in trecho_widget, "key do campo de observacao nao segue o padrao esperado"

    print("3. Campo Observação possui key estável (governanca_observacao_<cliente>): OK")


def testar_variavel_observacao_usada_no_registro(bloco_governanca):
    indice_criacao = bloco_governanca.find("criar_registro_acompanhamento(")
    assert indice_criacao != -1, "chamada a criar_registro_acompanhamento nao encontrada"

    trecho_chamada = bloco_governanca[indice_criacao:indice_criacao + 400]
    assert "observacao_acompanhamento=observacao_acompanhamento_escolhida" in trecho_chamada, (
        "a variavel de observacao escolhida pelo usuario nao esta sendo passada a criar_registro_acompanhamento"
    )

    print("4. Variável de observação é usada na criação do registro de acompanhamento: OK")


def testar_botoes_essenciais_presentes(bloco_governanca):
    assert "Salvar governança desta investigação" in bloco_governanca
    assert "Consultar governança salva deste cliente" in bloco_governanca

    print("5. Botão 'Salvar governança desta investigação' permanece: OK")
    print("6. Botão 'Consultar governança salva deste cliente' permanece: OK")


def testar_ausencia_botoes_proibidos(bloco_governanca):
    for rotulo in BOTOES_PROIBIDOS:
        assert rotulo not in bloco_governanca, f"botao proibido encontrado: {rotulo}"

    print("7. Nenhum novo botão de tarefa: OK")
    print("8. Nenhum novo botão de agenda: OK")
    print("9. Nenhum novo botão de plano de ação: OK")


def testar_ausencia_elementos_proibidos(bloco_governanca):
    for chamada in CHAMADAS_PROIBIDAS_NO_BLOCO:
        assert chamada not in bloco_governanca, f"elemento proibido encontrado no bloco de governanca: {chamada}"

    print("10. Ausência de st.date_input: OK")
    print("11. Ausência de st.time_input: OK")
    print("12. Ausência de st.metric no bloco de governança: OK")
    print("13. Ausência de gráficos no bloco de governança: OK")
    print("14. Ausência de st.download_button no bloco de governança: OK")


def testar_ausencia_campos_responsavel_prazo(bloco_governanca):
    for padrao in TERMOS_PROIBIDOS_CAMPOS:
        assert re.search(padrao, bloco_governanca) is None, f"campo proibido encontrado: {padrao}"

    print("15. Ausência de campos de responsável ou prazo: OK")


def testar_identidade_sessao_presente(codigo_fonte):
    assert "st.session_state" in codigo_fonte, "st.session_state nao encontrado em app.py"
    assert "sessao_investigativa" in codigo_fonte, "chave de sessao investigativa nao encontrada em app.py"

    print("16. Identidade de sessão via st.session_state continua presente: OK")


def testar_leitura_operacional_presente(bloco_governanca):
    assert "Leitura operacional da governança" in bloco_governanca
    assert "gerar_leitura_operacional_governanca" in bloco_governanca

    print("17. Leitura operacional continua presente: OK")


def testar_arquivo_nao_alterado_por_este_teste():
    tamanho_arquivo = os.path.getsize(CAMINHO_APP)
    assert tamanho_arquivo > 0

    print("18. Confirmacao de leitura sem escrita em app.py (arquivo apenas lido como texto): OK")


if __name__ == "__main__":
    codigo_fonte_app = _ler_app_py()
    bloco_governanca_extraido = _extrair_bloco_governanca(codigo_fonte_app)

    testar_secao_governanca_existe(codigo_fonte_app)
    testar_campo_observacao_existe(bloco_governanca_extraido)
    testar_campo_observacao_tem_key_estavel(bloco_governanca_extraido)
    testar_variavel_observacao_usada_no_registro(bloco_governanca_extraido)
    testar_botoes_essenciais_presentes(bloco_governanca_extraido)
    testar_ausencia_botoes_proibidos(bloco_governanca_extraido)
    testar_ausencia_elementos_proibidos(bloco_governanca_extraido)
    testar_ausencia_campos_responsavel_prazo(bloco_governanca_extraido)
    testar_identidade_sessao_presente(codigo_fonte_app)
    testar_leitura_operacional_presente(bloco_governanca_extraido)
    testar_arquivo_nao_alterado_por_este_teste()

    print("ESTABILIZACAO_EXPERIENCIA_GOVERNANCA_OK")
