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

# --- MOTOR DE MAPEAMENTO SEMÂNTICO ---
def identificar_colunas(df):
    mapa = {'CLIENTE': None, 'VENDEDOR': None, 'CIDADE': None, 'MESES': []}
    syn_cliente = ['EMPRESA', 'CLIENTE', 'NOME', 'RAZAO', 'IDENTIFICAO']
    syn_vendedor = ['VENDEDOR', 'REP', 'CONSULTOR', 'RESPONSAVEL', 'AGENTE', 'PATRICIA', 'JEFERSON']
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
    if cp <= 0: return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn e Reconexão.\nAÇÃO: Reestabelecer contato sem viés de venda.\nORIENTAÇÃO: Identifique o motivo real da parada."
    if cp < (lp * 0.85): return "🚨 QUEDA ACENTUADA", lp, "OBJETIVO: Defesa de Share.\nAÇÃO: Investigar concorrência ou falha de serviço.\nORIENTAÇÃO: Foque no negócio dele e entenda onde ele perde margem."
    if cp < (lp * 0.98): return "🔴 QUEDA", lp, "OBJETIVO: Estabilização de Giro.\nAÇÃO: Ajuste de mix e frequência.\nORIENTAÇÃO: Sugira ajustes que ajudem o cliente a reduzir perdas."
    if cp > (lp * 1.05): return "🟢 CRESCIMENTO", int(cp * 1.05), "OBJETIVO: Expansão (Upsell).\nAÇÃO: Analisar mix de clientes similares.\nORIENTAÇÃO: Aproveite a tração para elevar o ticket médio."
    return "🔵 ESTÁVEL", int(lp * 1.05), "OBJETIVO: Blindagem.\nAÇÃO: Manutenção e rituais de gestão.\nORIENTAÇÃO: Confirme se os objetivos do cliente estão sendo atingidos."

# --- INTERFACE ---
with st.sidebar:
    st.markdown("## GIRI | GOVERNANÇA")
    lp_m = st.number_input("Meses Longo Prazo", value=12, min_value=1)
    cp_m = st.number_input("Meses Curto Prazo", value=3, min_value=1)

st.title("STAR-OS | MATRIZ DE DECISÃO TÁTICA")
up = st.file_uploader("Upload da Planilha (Caso Real)", type=['xlsx', 'csv'])

if up:
    df_raw = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
    mapa = identificar_colunas(df_raw)
    
    if not mapa['MESES']:
        st.error("Não identifiquei colunas de faturamento temporal. Verifique o cabeçalho.")
    else:
        df = df_raw.copy()
        # Limpeza: Converter colunas de meses para numérico
        for c in mapa['MESES']: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        
        # Identificação das Chaves de Governança
        chaves_base = [mapa['CLIENTE'] or df.columns[0]]
        with st.sidebar:
            st.subheader("CHAVES")
            dims_sel = [d for d in [mapa['VENDEDOR'], mapa['CIDADE']] if d and st.checkbox(d, key=f"c_{d}")]
        
        chaves_final = list(dict.fromkeys(chaves_base + dims_sel))
        df_ag = df.groupby(chaves_final, as_index=False)[mapa['MESES']].sum()
        
        # --- FILTRO INTELIGENTE DE MESES ATIVOS ---
        # No caso real da cliente, existem meses futuros com zero. 
        # Vamos considerar apenas meses que possuem algum faturamento global para o cálculo da média.
        col_com_dados = [c for c in mapa['MESES'] if df_ag[c].sum() > 0]
        
        # Cálculos STAR (Baseados apenas no que ocorreu)
        c_lp = col_com_dados[-min(lp_m, len(col_com_dados)):]
        c_cp = col_com_dados[-min(cp_m, len(col_com_dados)):]
        
        df_ag['TOTAL_LP'] = df_ag[c_lp].sum(axis=1).round(0)
        df_ag['MEDIA_LP'] = (df_ag['TOTAL_LP'] / len(c_lp)).round(0)
        df_ag['MEDIA_CP'] = (df_ag[c_cp].sum(axis=1) / len(c_cp)).round(0)
        
        # HIERARQUIA: ORDENAÇÃO DECRESCENTE POR VALOR ACUMULADO
        df_ag = df_ag.sort_values('TOTAL_LP', ascending=False).reset_index(drop=True)
        
        # CURVA ABC
        df_ag['CURVA'] = (df_ag['TOTAL_LP'].cumsum() / df_ag['TOTAL_LP'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
        
        res = df_ag.apply(lambda r: engine_star(r, r['MEDIA_LP'], r['MEDIA_CP']), axis=1)
        df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)

        # --- PREPARAÇÃO PARA EXIBIÇÃO ---
        df_view = df_ag.copy()
        # Blindagem de nomes duplicados
        df_view = df_view.loc[:, ~df_view.columns.duplicated()]
        
        # Formatação de nomes de colunas (datas para string limpa)
        nomes_meses_str = [str(c).split(' ')[0] if isinstance(c, (pd.Timestamp, datetime.date)) else str(c) for c in mapa['MESES']]
        rename_dict = dict(zip(mapa['MESES'], nomes_meses_str))
        df_view = df_view.rename(columns=rename_dict)

        ordem_view = ['CURVA'] + chaves_final + nomes_meses_str + ['TOTAL_LP', 'STATUS', 'META', 'AÇÃO']
        ordem_view = list(dict.fromkeys(ordem_view)) # Garante lista única
        
        st.subheader(f"Governança STAR: {len(df_ag)} Clientes Priorizados por Faturamento")
        st.dataframe(df_view[ordem_view], use_container_width=True)

        # EXPORTAÇÃO EXECUTIVA
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
            df_view[ordem_view].to_excel(wr, index=False, sheet_name='STAR')
            wb, ws = wr.book, wr.sheets['STAR']
            
            # CABEÇALHO BRANCO NO AZUL ESCURO (Giri Standard)
            h_f = wb.add_format({'bold':True, 'bg_color':'#002060', 'font_color':'#FFFFFF', 'border':1, 'align':'center', 'valign':'vcenter', 'text_wrap':True})
            b_f = wb.add_format({'valign':'vcenter', 'align':'left', 'border':1, 'border_color':'#D9D9D9', 'text_wrap':True})
            n_f = wb.add_format({'num_format':'#,##0', 'valign':'vcenter', 'align':'center', 'border':1})
            
            for i, col in enumerate(ordem_view):
                ws.write(0, i, col, h_f)
            
            ws.set_default_row(75)
            ws.set_column(1, 1, 45) # Empresa
            ws.set_column(len(ordem_view)-1, len(ordem_view)-1, 80) # Ação

        st.download_button("📥 EXPORTAR LAUDO DE GOVERNANÇA", output.getvalue(), "Matriz_STAR_Giri.xlsx")
