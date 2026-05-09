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
    div[data-testid="stDataFrame"] td { white-space: pre-wrap !important; vertical-align: middle !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE INTELIGÊNCIA DE MAPEAMENTO REFORÇADO ---
def identificar_colunas(df):
    mapeamento = {'CLIENTE': None, 'VENDEDOR': None, 'CIDADE': None, 'MESES': []}
    
    syn_cliente = ['EMPRESA', 'CLIENTE', 'NOME', 'RAZAO', 'IDENTIFICAO']
    syn_vendedor = ['VENDEDOR', 'REP', 'CONSULTOR', 'RESPONSAVEL', 'AGENTE']
    syn_cidade = ['CIDADE', 'MUNICIPIO', 'LOCALIDADE', 'UF', 'REGIAO']
    
    # Lista de meses para busca textual
    meses_pt = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']

    for col in df.columns:
        c_str = str(col).strip().upper()
        
        # 1. Identifica se a coluna é uma Data (mesmo que o pandas tenha lido como datetime)
        is_date = False
        if isinstance(col, (pd.Timestamp, datetime.date)):
            is_date = True
        elif any(m in c_str for m in meses_pt):
            is_date = True
        elif re.search(r"\d{1,2}[/-]\d{2,4}", c_str):
            is_date = True
            
        if is_date and 'TOTAL' not in c_str:
            mapeamento['MESES'].append(col)
        elif any(s in c_str for s in syn_cliente) and not mapeamento['CLIENTE']:
            mapeamento['CLIENTE'] = col
        elif any(s in c_str for s in syn_vendedor) and not mapeamento['VENDEDOR']:
            mapeamento['VENDEDOR'] = col
        elif any(s in c_str for s in syn_cidade) and not mapeamento['CIDADE']:
            mapeamento['CIDADE'] = col
            
    return mapeamento

def engine_star(row, lp, cp):
    if cp <= 0: 
        return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn.\nAÇÃO: Reconexão estratégica.\nORIENTAÇÃO: Identifique o motivo real da parada."
    if cp < (lp * 0.85):
        return "🚨 QUEDA ACENTUADA", lp, "OBJETIVO: Defesa de Share.\nAÇÃO: Investigar concorrência ou falha de serviço.\nORIENTAÇÃO: Entenda onde ele perde margem."
    if cp < (lp * 0.98): 
        return "🔴 QUEDA", lp, "OBJETIVO: Estabilização.\nAÇÃO: Ajuste de mix e frequência.\nORIENTAÇÃO: Recupere o giro histórico."
    if cp > (lp * 1.05): 
        return "🟢 CRESCIMENTO", int(cp * 1.05), "OBJETIVO: Expansão (Upsell).\nAÇÃO: Ofertar itens complementares.\nORIENTAÇÃO: Aproveite a tração para elevar o ticket."
    return "🔵 ESTÁVEL", int(lp * 1.05), "OBJETIVO: Blindagem.\nAÇÃO: Manutenção e rituais.\nORIENTAÇÃO: Garanta a recorrência."

# --- INTERFACE ---
with st.sidebar:
    st.markdown("## GIRI | GOVERNANÇA")
    lp_meses = st.number_input("Meses Longo Prazo", value=12, min_value=1)
    cp_meses = st.number_input("Meses Curto Prazo", value=3, min_value=1)

st.title("STAR-OS | MATRIZ DE DECISÃO TÁTICA")

up = st.file_uploader("Upload da Planilha", type=['xlsx', 'csv'])

if up:
    import datetime
    df_raw = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
    mapa = identificar_colunas(df_raw)
    
    if not mapa['MESES']:
        st.error(f"Não identifiquei colunas de data. Colunas lidas: {list(df_raw.columns)[:5]}...")
    else:
        df = df_raw.copy()
        # Converte valores para numérico e limpa nomes de colunas para o processamento
        for c in mapa['MESES']: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        
        chaves = [c for c in [mapa['CLIENTE'], mapa['VENDEDOR'], mapa['CIDADE']] if c]
        if not chaves: chaves = [df.columns[0]] # Fallback para a primeira coluna
            
        df_ag = df.groupby(chaves, as_index=False)[mapa['MESES']].sum()
        
        # Lógica de Médias
        col_lp = mapa['MESES'][-lp_meses:]
        col_cp = mapa['MESES'][-cp_meses:]
        
        df_ag['TOTAL_LP'] = df_ag[col_lp].sum(axis=1).round(0)
        df_ag['MEDIA_LP'] = (df_ag['TOTAL_LP'] / len(col_lp)).round(0)
        df_ag['MEDIA_CP'] = (df_ag[col_cp].sum(axis=1) / len(col_cp)).round(0)
        
        # Ordenação Decrescente por Faturamento LP
        df_ag = df_ag.sort_values('TOTAL_LP', ascending=False).reset_index(drop=True)
        
        # Curva ABC
        df_ag['CURVA'] = (df_ag['TOTAL_LP'].cumsum() / df_ag['TOTAL_LP'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
        
        res = df_ag.apply(lambda r: engine_star(r, r['MEDIA_LP'], r['MEDIA_CP']), axis=1)
        df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)
        
        # Preparação de colunas para exibição amigável (converte datas para string se necessário)
        df_exibir = df_ag.copy()
        nomes_meses_str = [str(c).split(' ')[0] if isinstance(c, (pd.Timestamp, datetime.date)) else str(c) for c in mapa['MESES']]
        df_exibir.columns = list(df_ag.columns[:len(df_ag.columns)-len(mapa['MESES'])-6]) + chaves + nomes_meses_str + ['TOTAL_LP', 'MEDIA_LP', 'MEDIA_CP', 'STATUS', 'META', 'AÇÃO']
        
        cols_final = ['CURVA'] + chaves + nomes_meses_str + ['TOTAL_LP', 'STATUS', 'META', 'AÇÃO']
        
        st.subheader(f"Governança STAR: {len(df_ag)} registros ordenados por faturamento total.")
        st.dataframe(df_exibir[cols_final], use_container_width=True)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
            df_exibir[cols_final].to_excel(wr, index=False, sheet_name='MATRIZ_STAR')
            wb, ws = wr.book, wr.sheets['MATRIZ_STAR']
            header = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'white', 'border':1, 'align':'center', 'valign':'vcenter'})
            for i, col in enumerate(cols_final): ws.write(0, i, col, header)
            ws.set_default_row(70)

        st.download_button("📥 EXPORTAR PLANO STAR", output.getvalue(), "Plano_STAR_Giri.xlsx")
