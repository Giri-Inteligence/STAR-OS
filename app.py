import streamlit as st
import pandas as pd
import numpy as np
import re
from io import BytesIO
import xlsxwriter

# 1. DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); color: #ffffff; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    .stDownloadButton > button { 
        width: 100%; height: 4em; background-color: #002060; color: white; 
        font-weight: bold; border: 2px solid #ffffff; border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

def engine_star(lp, cp):
    try: lp_v, cp_v = float(lp), float(cp)
    except: lp_v, cp_v = 0.0, 0.0
    
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

st.title("GIRI | STAR-OS")
uploaded_file = st.file_uploader("Upload da Planilha Base", type=['xlsx', 'csv'])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    
    # Detecção de Colunas
    cols = df_raw.columns.tolist()
    meses_col = [c for c in cols if any(m in c for m in ("JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"))]
    clie_col = next((c for c in cols if "CLIENTE" in c or "NOME" in c or "RAZAO" in c), cols[0])
    vend_col = next((c for c in cols if "VENDEDOR" in c or "REP" in c), cols[1])

    # Tratamento Numérico
    for c in meses_col: df_raw[c] = pd.to_numeric(df_raw[c], errors='coerce').fillna(0)
    
    # Processamento STAR
    df_raw['TOTAL LP'] = df_raw[meses_col].sum(axis=1).astype(int)
    df_raw['MÉDIA LP'] = (df_raw[meses_col].mean(axis=1)).astype(int)
    df_raw['MÉDIA CP'] = (df_raw[meses_col[-3:]].mean(axis=1)).astype(int)
    df_raw = df_raw.sort_values('TOTAL LP', ascending=False).reset_index(drop=True)
    df_raw['CURVA'] = (df_raw['TOTAL LP'].cumsum() / df_raw['TOTAL LP'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
    
    res = df_raw.apply(lambda r: engine_star(r['MÉDIA LP'], r['MÉDIA CP']), axis=1)
    df_raw['STATUS'], df_raw['META'], df_raw['AÇÃO'] = zip(*res)
    
    final_ordem = ['CURVA', clie_col, vend_col] + meses_col + ['TOTAL LP', 'MÉDIA LP', 'MÉDIA CP', 'STATUS', 'META', 'AÇÃO']

    # GERAÇÃO DO ARQUIVO
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_raw[final_ordem].to_excel(writer, index=False, sheet_name='STAR')
        workbook = writer.book
        worksheet = writer.sheets['STAR']
        
        # Formatos Hardcoded
        fmt_header = workbook.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'#FFFFFF', 'border':1, 'align':'center', 'valign':'vcenter', 'text_wrap':True})
        fmt_text = workbook.add_format({'valign':'top', 'align':'left', 'border':1, 'text_wrap':True})
        fmt_num = workbook.add_format({'num_format':'#,##0', 'valign':'top', 'align':'center', 'border':1})
        fmt_total = workbook.add_format({'num_format':'#,##0', 'bg_color':'#F2F2F2', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        
        # Status Colorizados
        fmt_qa = workbook.add_format({'bg_color':'#FFC7CE', 'font_color':'#9C0006', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        fmt_q = workbook.add_format({'font_color':'#9C0006', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        fmt_c = workbook.add_format({'font_color':'#006100', 'bold':True, 'valign':'top', 'align':'center', 'border':1})
        fmt_e = workbook.add_format({'font_color':'#0070C0', 'bold':True, 'valign':'top', 'align':'center', 'border':1})

        # Geometria
        worksheet.set_default_row(170)
        worksheet.set_row(0, 45)
        
        for i, col in enumerate(final_ordem):
            worksheet.write(0, i, col, fmt_header)
            if col == 'AÇÃO': worksheet.set_column(i, i, 100, fmt_text)
            elif col == 'STATUS': worksheet.set_column(i, i, 24)
            elif col == 'TOTAL LP': worksheet.set_column(i, i, 11)
            else: worksheet.set_column(i, i, 10)

        # Preenchimento de Dados
        for row_num, row_data in enumerate(df_raw[final_ordem].values):
            for col_num, val in enumerate(row_data):
                col_name = final_ordem[col_num]
                if col_name == 'STATUS':
                    f = fmt_num
                    if "QUEDA ACENTUADA" in str(val): f = fmt_qa
                    elif "QUEDA" in str(val): f = fmt_q
                    elif "CRESCIMENTO" in str(val): f = fmt_c
                    elif "ESTÁVEL" in str(val): f = fmt_e
                    worksheet.write_string(row_num + 1, col_num, str(val), f)
                elif col_name == 'TOTAL LP':
                    worksheet.write_number(row_num + 1, col_num, int(val), fmt_total)
                elif col_name in ('MÉDIA LP', 'MÉDIA CP', 'META') or col_name in meses_col:
                    worksheet.write_number(row_num + 1, col_num, int(val), fmt_num)
                else:
                    worksheet.write_string(row_num + 1, col_num, str(val), fmt_text)

    st.success("Plan
