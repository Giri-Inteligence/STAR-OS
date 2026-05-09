import streamlit as st
import pandas as pd
import numpy as np
import re
from io import BytesIO
import xlsxwriter

# 1. AMBIENTE SEGURO (REMOÇÃO DE CSS CONFLITANTE)
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

def engine_star(lp, cp):
    try: lp_v, cp_v = float(lp), float(cp)
    except: lp_v, cp_v = 0.0, 0.0
    
    # MANUAL TÁTICO WILLIAM BERTO (PRESERVADO INTEGRALMENTE)
    txt_ina = "OBJETIVO: Diagnóstico de causa\nPRÉ-CONTATO: Revisar último pedido. Identificar o que parou de ser comprado e em que momento.\nCONTATO: Contato de diagnóstico. Entender o motivo da inatividade sem pressão de venda.\nORIENTAÇÃO: Não ofertar produto na primeira interação. Primeiro entender o que aconteceu. Registrar motivo antes de qualquer ação de reconquista."
    txt_q_ac = "OBJETIVO: Recuperação emergencial\nPRÉ-CONTATO: Revisar histórico completo do cliente. Identificar exatamente quais produtos caíram, em que momento e qual era o volume anterior. Calcular o gap entre a média histórica e o momento atual.\nCONTATO: Priorizar visita presencial ou ligação direta — não mensagem. Abrir diagnóstico sem pressão. Entender se houve mudança interna no cliente, problema de relacionamento ou entrada de concorrente.\nORIENTAÇÃO: Este cliente está em risco de perda. O objetivo da primeira interação não é vender — é entender. Registrar causa com precisão. Escalar para o gestor se o motivo indicar risco de ruptura definitiva."
    txt_q = "OBJETIVO: Estabilização\nPRÉ-CONTATO: Revisar histórico de mix. Identificar quais produtos reduziram ou desapareceram nos últimos 3 meses.\nCONTATO: Diagnosticar contexto atual do cliente. Investigar se houve mudança operacional, financeira ou troca de fornecedor.\nORIENTAÇÃO: Registrar causa identificada. Se houver abertura, propor recomposição de mix com base no histórico anterior."
    txt_est = "OBJETIVO: Blindagem e crescimento incremental\nPRÉ-CONTATO: Revisar mix atual. Mapear categorias que o cliente não compra mas que são compatíveis com seu perfil.\nCONTATO: Manter frequência de relacionamento. Explorar oportunidade de expansão de mix.\nORIENTAÇÃO: Cliente estável não é cliente seguro. Monitorar frequência de pedidos e introduzir novos itens gradualmente."
    txt_cre = "OBJETIVO: Consolidação\nPRÉ-CONTATO: Identificar o driver do crescimento. Avaliar se é sazonalidade ou mudança estrutural no cliente.\nCONTATO: Reforçar relacionamento. Garantir abastecimento e antecipar demanda dos próximos períodos.\nORIENTAÇÃO: Proteger o cliente. Momento de crescimento é o de maior risco de abordagem pelo concorrente."
    txt_cre_ac = "OBJETIVO: Consolidação e proteção\nPRÉ-CONTATO: Identificar quais produtos puxaram o crescimento. Avaliar se o cliente tem capacidade de sustentar esse volume ou se é pontual. Verificar se há mix ainda não explorado.\nCONTATO: Reforçar presença. Garantir que o abastecimento está adequado ao novo patamar de compra. Antecipar pedidos futuros.\nORIENTAÇÃO: Crescimento acentuado atrai concorrência. Este é o momento de maior risco de abordagem externa. Aumentar frequência de contato e solidificar o relacionamento antes que o concorrente perceba a oportunidade."

    if cp_v <= 0: return "⚫ INATIVO", 0, txt_ina
    if lp_v <= 0: return "🔵 ESTÁVEL", int(cp_v * 1.05), txt_est
    if cp_v < (lp_v * 0.85): return "🚨 QUEDA ACENTUADA", int(lp_v), txt_q_ac
    if cp_v < (lp_v * 0.98): return "🔴 QUEDA", int(lp_v), txt_q
    if cp_v > (lp_v * 1.20): return "🚀 CRESCIMENTO ACENTUADO", int(cp_v * 1.05), txt_cre_ac
    if cp_v > (lp_v * 1.05): return "🟢 CRESCIMENTO", int(cp_v * 1.05), txt_cre
    return "🔵 ESTÁVEL", int(lp_v * 1.05), txt_est

st.header("GIRI | SISTEMA DE GOVERNANÇA STAR")
uploaded_file = st.file_uploader("Upload da Base (XLSX ou CSV)", type=['xlsx', 'csv'])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    
    cols = df_raw.columns.tolist()
    meses_col = [c for c in cols if any(m in c for m in ("JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"))]
    clie_col = next((c for c in cols if "CLIENTE" in c or "NOME" in c or "RAZAO" in c), cols[0])
    vend_col = next((c for c in cols if "VENDEDOR" in c or "REP" in c), cols[1])

    for c in meses_col: df_raw[c] = pd.to_numeric(df_raw[c], errors='coerce').fillna(0)
    
    df_raw['TOTAL LP'] = df_raw[meses_col].sum(axis=1).astype(int)
    df_raw['MÉDIA LP'] = (df_raw[meses_col].mean(axis=1)).astype(int)
    df_raw['MÉDIA CP'] = (df_raw[meses_col[-3:]].mean(axis=1)).astype(int)
    df_raw = df_raw.sort_values('TOTAL LP', ascending=False).reset_index(drop=True)
    df_raw['CURVA'] = (df_raw['TOTAL LP'].cumsum() / df_raw['TOTAL LP'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
    
    res = df_raw.apply(lambda r: engine_star(r['MÉDIA LP'], r['MÉDIA CP']), axis=1)
    df_raw['STATUS'], df_raw['META'], df_raw['AÇÃO'] = zip(*res)
    
    final_ordem = ['CURVA', clie_col, vend_col] + meses_col + ['TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'STATUS', 'META', 'AÇÃO']

    # --- MOTOR DE EXCEL HARDCODED ---
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_raw[final_ordem].to_excel(writer, index=False, sheet_name='STAR')
        wb = writer.book
        ws = writer.sheets['STAR']
        
        # FORMATOS
        h_f = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'#FFFFFF', 'border':1, 'align':'center', 'valign':'vcenter', 'text_wrap':True})
        txt_f = wb.add_format({'valign':'top', 'align':'left', 'border':1, 'text_wrap':True})
        num_f = wb.add_format({'num_format':'#,##0', 'valign':'top', 'align':'center', 'border':1})
        
        # TRAVA VISUAL: TOTAL LP (CINZA + NEGRITO)
        total_f = wb.add_format({'num_format':'#,##0', 'bg_color':'#F2F2F2', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        
        # STATUS COLORIZADOS
        st_qa = wb.add_format({'bg_color':'#FFC7CE', 'font_color':'#9C0006', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        st_q = wb.add_format({'font_color':'#9C0006', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        st_c = wb.add_format({'font_color':'#006100', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        st_e = wb.add_format({'font_color':'#0070C0', 'bold':True, 'valign':'top', 'align':'center', 'border':1})

        ws.set_default_row(170)
        ws.set_row(0, 45)
        
        for i, col in enumerate(final_ordem):
            ws.write(0, i, col, h_f)
            if col == 'AÇÃO': ws.set_column(i, i, 100, txt_f)
            elif col == 'STATUS': ws.set_column(i, i, 24)
            elif col == 'TOTAL LP': ws.set_column(i, i, 11)
            else: ws.set_column(i, i, 9)

        for r_idx, row in df_raw.iterrows():
            xl_r = r_idx + 1
            for c_idx, col_n in enumerate(final_ordem):
                val = row[col_n]
                if col_n == 'STATUS':
                    f = num_f
                    if "QUEDA ACENTUADA" in str(val): f = st_qa
                    elif "QUEDA" in str(val): f = st_q
                    elif "CRESCIMENTO" in str(val): f = st_c
                    elif "ESTÁVEL" in str(val): f = st_e
                    ws.write_string(xl_r, c_idx, str(val), f)
                elif col_n == 'TOTAL LP': ws.write_number(xl_r, c_idx, int(val), total_f)
                elif col_n in ('MÉDIA LP', 'MÉDIA CP', 'META') or col_n in meses_col: ws.write_number(xl_r, c_idx, int(val), num_f)
                else: ws.write_string(xl_r, c_idx, str(val), txt_f)

    # SAÍDA BLINDADA
    st.info("Planilha processada.")
    st.download_button(
        label="📥 BAIXAR MATRIZ STAR V145",
        data=buffer.getvalue(),
        file_name="Matriz_STAR_Giri.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
