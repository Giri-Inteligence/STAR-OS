import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter

st.set_page_config(page_title="Giri | Sistema STAR", layout="wide")

def engine_star(lp, cp):
    try:
        lp_v, cp_v = float(lp), float(cp)
    except:
        lp_v, cp_v = 0.0, 0.0

    txt_ina = (
        "OBJETIVO: Diagnóstico de causa\n"
        "PRÉ-CONTATO: Revisar último pedido. Identificar o que parou de ser comprado e em que momento.\n"
        "CONTATO: Contato de diagnóstico. Entender o motivo da inatividade sem pressão de venda.\n"
        "ORIENTAÇÃO: Não ofertar produto na primeira interação. Primeiro entender o que aconteceu. "
        "Registrar motivo antes de qualquer ação de reconquista."
    )
    txt_q_ac = (
        "OBJETIVO: Recuperação emergencial\n"
        "PRÉ-CONTATO: Revisar histórico completo do cliente. Identificar exatamente quais produtos caíram, "
        "em que momento e qual era o volume anterior. Calcular o gap entre a média histórica e o momento atual.\n"
        "CONTATO: Priorizar visita presencial ou ligação direta — não mensagem. Abrir diagnóstico sem pressão. "
        "Entender se houve mudança interna no cliente, problema de relacionamento ou entrada de concorrente.\n"
        "ORIENTAÇÃO: Este cliente está em risco de perda. O objetivo da primeira interação não é vender — é entender. "
        "Registrar causa com precisão. Escalar para o gestor se o motivo indicar risco de ruptura definitiva."
    )
    txt_q = (
        "OBJETIVO: Estabilização\n"
        "PRÉ-CONTATO: Revisar histórico de mix. Identificar quais produtos reduziram ou desapareceram nos últimos 3 meses.\n"
        "CONTATO: Diagnosticar contexto atual do cliente. Investigar se houve mudança operacional, financeira ou troca de fornecedor.\n"
        "ORIENTAÇÃO: Registrar causa identificada. Se houver abertura, propor recomposição de mix com base no histórico anterior."
    )
    txt_est = (
        "OBJETIVO: Blindagem e crescimento incremental\n"
        "PRÉ-CONTATO: Revisar mix atual. Mapear categorias que o cliente não compra mas que são compatíveis com seu perfil.\n"
        "CONTATO: Manter frequência de relacionamento. Explorar oportunidade de expansão de mix.\n"
        "ORIENTAÇÃO: Cliente estável não é cliente seguro. Monitorar frequência de pedidos e introduzir novos itens gradualmente."
    )
    txt_cre = (
        "OBJETIVO: Consolidação\n"
        "PRÉ-CONTATO: Identificar o driver do crescimento. Avaliar se é sazonalidade ou mudança estrutural no cliente.\n"
        "CONTATO: Reforçar relacionamento. Garantir abastecimento e antecipar demanda dos próximos períodos.\n"
        "ORIENTAÇÃO: Proteger o cliente. Momento de crescimento é o de maior risco de abordagem pelo concorrente."
    )
    txt_cre_ac = (
        "OBJETIVO: Consolidação e proteção\n"
        "PRÉ-CONTATO: Identificar quais produtos puxaram o crescimento. Avaliar se o cliente tem capacidade de sustentar "
        "esse volume ou se é pontual. Verificar se há mix ainda não explorado.\n"
        "CONTATO: Reforçar presença. Garantir que o abastecimento está adequado ao novo patamar de compra. Antecipar pedidos futuros.\n"
        "ORIENTAÇÃO: Crescimento acentuado atrai concorrência. Este é o momento de maior risco de abordagem externa. "
        "Aumentar frequência de contato e solidificar o relacionamento antes que o concorrente perceba a oportunidade."
    )

    if cp_v <= 0:
        return "INATIVO", 0, txt_ina
    if lp_v <= 0:
        return "ESTÁVEL", int(cp_v * 1.05), txt_est
    if cp_v < (lp_v * 0.85):
        return "QUEDA ACENTUADA", int(lp_v), txt_q_ac
    if cp_v < (lp_v * 0.98):
        return "QUEDA", int(lp_v), txt_q
    if cp_v > (lp_v * 1.20):
        return "CRESCIMENTO ACENTUADO", int(cp_v * 1.05), txt_cre_ac
    if cp_v > (lp_v * 1.05):
        return "CRESCIMENTO", int(cp_v * 1.05), txt_cre
    return "ESTÁVEL", int(lp_v * 1.05), txt_est


def gerar_excel(df_raw, final_ordem, clie_col, vend_col, meses_col):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_raw[final_ordem].to_excel(writer, index=False, sheet_name='STAR')
        wb = writer.book
        ws = writer.sheets['STAR']

        hdr = wb.add_format({
            'bold': True, 'bg_color': '#002060', 'font_color': '#FFFFFF',
            'border': 1, 'align': 'center', 'valign': 'vcenter',
            'text
