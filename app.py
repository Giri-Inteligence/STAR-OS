import streamlit as st
import pandas as pd
import numpy as np
import re
import datetime
from io import BytesIO
import xlsxwriter

# 1. DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); color: #ffffff; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    div[data-testid="stDataFrame"] td { white-space: pre-wrap !important; vertical-align: middle !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE MAPEAMENTO ---
def identificar_colunas(df):
    mapa = {'CLIENTE': None, 'VENDEDOR': None, 'CIDADE': None, 'MESES': []}
    syn_cliente = ['EMPRESA', 'CLIENTE', 'NOME', 'RAZAO', 'IDENTIFICAO']
    syn_vendedor = ['VENDEDOR', 'REP', 'CONSULTOR', 'RESPONSAVEL', 'AGENTE']
    syn_cidade = ['CIDADE', 'MUNICIPIO', 'LOCALIDADE', 'UF', 'REGIAO']
    meses_pt = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']

    for col in df.columns:
        c_str = str(col).strip().upper()
        is_date = False
        if isinstance(col, (pd.Timestamp, datetime.date)): is_date = True
        elif any(m in c_str for m in meses_pt): is_date = True
        elif re.search(r"\d{1,2}[/-]\d{2,4}", c_str): is_date = True
            
        if is_date and 'TOTAL' not in c_str: mapa['MESES'].append(col)
        elif any(s in c_str for s in syn_cliente) and not mapa['CLIENTE']: mapa['CLIENTE'] = col
        elif any(s in c_str for s in syn_vendedor) and not mapa['VENDEDOR']: mapa['VENDEDOR'] = col
        elif any(s in c_str for s in syn_cidade) and not mapa['CIDADE']: mapa['CIDADE'] = col
    return mapa

def engine_star(row, lp, cp):
    if cp <= 0: return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn.\nAÇÃO: Reconexão estratégica.\nORIENTAÇÃO: Identifique o motivo real da parada."
    if cp < (lp * 0.85): return "🚨 QUEDA ACENTUADA", lp, "OBJETIVO: Defesa de Share.\nAÇÃO: Investigar concorrência ou falha de serviço.\nORIENTAÇÃO: Entenda onde ele perde margem."
    if cp < (lp * 0.98): return "🔴 QUEDA", lp, "OBJETIVO: Estabilização.\nAÇÃO: Ajuste de mix e frequência.\nORIENTAÇÃO: Recupere o giro histórico."
    if cp > (lp * 1.05): return "🟢 CRESCIMENTO", int(cp * 1.05), "OBJETIVO: Expansão (Upsell).\nAÇÃO: Ofertar itens complementares.\nORIENTAÇÃO: Aproveite a tração para elevar o ticket."
    return "🔵 ESTÁVEL", int(lp * 1.05), "OBJETIVO: Blindagem.\nAÇÃO: Manutenção e rituais.\nORIENTAÇÃO: Garanta a recorrência."

# --- INTERFACE ---
with st.sidebar:
    st.markdown("## GIRI | GOVERNANÇA")
    lp_m = st.number_input("Meses Longo Prazo", value=12, min_value=1)
    cp_m = st.number_input("Meses Curto Prazo", value=3, min_value=1)

st.title("STAR-OS | MATRIZ DE DECISÃO TÁTICA")
up = st.file_uploader("Upload da Planilha", type=['xlsx', 'csv'])

if up:
    df_raw = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
    mapa = identificar_colunas(df_raw)
    
    if not mapa['MESES']:
        st.error("Não identifiquei colunas de data. Verifique o cabeçalho.")
    else:
        df = df_raw.copy()
        for c in mapa['MESES']: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        
        chaves = [c for c in [mapa['CLIENTE'], mapa['VENDEDOR'], mapa['CIDADE']] if c]
        with st.sidebar:
            st.subheader("CHAVES")
            dims_sel = [d for d in [mapa['VENDEDOR'], mapa['CIDADE']] if d and st.checkbox(d, key=f"c_{d}")]
        
        chaves_final = list(dict.fromkeys([mapa['CLIENTE'] or df.columns[0]] + dims_sel))
        df_ag = df.groupby(chaves_final, as_index=False)[mapa['MESES']].sum()
        
        # Cálculos STAR
        c_lp, c_cp = mapa['MESES'][-lp_m:], mapa['MESES'][-cp_m:]
        df_ag['TOTAL_LP'] = df_ag[c_lp].sum(axis=1).round(0)
        df_ag['MEDIA_LP'] = (df_ag['TOTAL_LP'] / len(c_lp)).round(0)
        df_ag['MEDIA_CP'] = (df_ag[c_cp].sum(axis=1) / len(c_cp)).round(0)
        
        df_ag = df_ag.sort_values('TOTAL_LP', ascending=False).reset_index(drop=True)
        df_ag['CURVA'] = (df_ag['TOTAL_LP'].cumsum() / df_ag['TOTAL_LP'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
        
        res = df_ag.apply(lambda r: engine_star(r, r['MEDIA_LP'], r['MEDIA_CP']), axis=1)
        df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)

        # Formatação das colunas de data para visualização
        nomes_meses_limpos = [str(c).split(' ')[0] if isinstance(c, (pd.Timestamp, datetime.date)) else str(c) for c in mapa['MESES']]
        
        # RECONSTRUÇÃO SEGURA DA EXIBIÇÃO (Resolve o ValueError)
        df_view = df_ag.copy()
        # Mapeia colunas antigas para novas apenas para os meses
        rename_dict = dict(zip(mapa['MESES'], nomes_meses_limpos))
        df_view = df_view.rename(columns=rename_dict)
        
        ordem_view = ['CURVA'] + chaves_final + nomes_meses_limpos + ['TOTAL_LP', 'STATUS', 'META', 'AÇÃO']
        
        st.subheader(f"Governança STAR: {len(df_ag)} Clientes em Ordem Decrescente")
        st.dataframe(df_view[ordem_view], use_container_width=True)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
            df_view[ordem_view].to_excel(wr, index=False, sheet_name='STAR')
            wb, ws = wr.book, wr.sheets['STAR']
            h_f = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'#FFFFFF', 'border':1, 'align':'center', 'valign':'vcenter'})
            for i, col in enumerate(ordem_view): ws.write(0, i, col, h_f)
            ws.set_default_row(70)
            ws.set_column(1, 1, 40) # Empresa
            ws.set_column(len(ordem_view)-1, len(ordem_view)-1, 70) # Ação

        st.download_button("📥 EXPORTAR PLANO STAR", output.getvalue(), "Giri_Plano_STAR.xlsx")
