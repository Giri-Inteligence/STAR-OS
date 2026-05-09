import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import math
from io import BytesIO
import xlsxwriter

# 1. DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Architecture Hub", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); color: #ffffff; }
    header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000810 !important; border-right: 1px solid rgba(255, 255, 255, 0.1) !important; min-width: 240px !important; }
    .sidebar-title { margin-top: -30px; margin-bottom: 20px; letter-spacing: 2px; font-size: 1.1rem; font-weight: 800; color: white; text-transform: uppercase; }
    .title-center { text-align: center; text-transform: uppercase; letter-spacing: 5px; margin-top: -45px; font-weight: 800; font-size: 1.8rem; }
    .subtitle-center { text-align: center; text-transform: uppercase; letter-spacing: 2px; color: rgba(255, 255, 255, 0.6); margin-bottom: 30px; font-size: 0.9rem; }
    
    .stSelectbox div[data-baseweb="select"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; border-radius: 4px !important; }
    div[data-testid="stDownloadButton"] button { 
        height: 42px !important; border-radius: 6px !important; border: 1px solid rgba(255, 255, 255, 0.3) !important; 
        background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.03)) !important;
        color: #ffffff !important; font-weight: 800 !important; text-transform: uppercase !important;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.4), inset 1px 1px 2px rgba(255,255,255,0.2) !important;
    }
    div[data-testid="stDownloadButton"] button:hover { box-shadow: 0px 0px 15px rgba(255,255,255,0.15), inset 1px 1px 1px rgba(255,255,255,0.3) !important; transform: translateY(-1px); }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE GOVERNANÇA ---
def format_br(val):
    try:
        if pd.isna(val) or val == 0: return "0"
        return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

def engine_star(row, lp, cp):
    if cp == 0: return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn e Reconexão.\nAÇÃO: Reestabelecer contato sem viés de venda.\nORIENTAÇÃO: Identifique o motivo real da parada."
    if cp < (lp * 0.80): return "🚨 QUEDA ACENTUADA", lp, "OBJETIVO: Contenção de Perda e Defesa de Share.\nAÇÃO: Investigar entrada de concorrência ou falha de serviço.\nORIENTAÇÃO: Foque no negócio dele e entenda onde perde margem."
    if cp < (lp * 0.95): return "🔴 QUEDA", lp, "OBJETIVO: Estabilização de Giro.\nAÇÃO: Identificar se a queda é sazonal ou substituição de mix.\nORIENTAÇÃO: Sugira ajustes que ajudem o cliente a reduzir perdas."
    if cp > (lp * 1.05): return "🟢 CRESCIMENTO", int(cp * 1.05), "OBJETIVO: Expansão de Share e Upsell.\nAÇÃO: Analisar mix de clientes similares e elevar Ticket Médio.\nORIENTAÇÃO: Recomende itens complementares."
    return "🔵 ESTÁVEL", int(lp * 1.05), "OBJETIVO: Manutenção e Blindagem.\nAÇÃO: Prevenir inércia e validar satisfação.\nORIENTAÇÃO: Confirme se os objetivos estão sendo atingidos."

# --- NAVEGAÇÃO ---
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = 'Matriz'
with st.sidebar:
    st.markdown('<div class="sidebar-title">GIRI | ARCHITECTURE</div>', unsafe_allow_html=True)
    lp_val = st.number_input("Longo Prazo (Meses)", value=15, min_value=1)
    cp_val = st.number_input("Curto Prazo (Meses)", value=3, min_value=1)

# --- TELA MATRIZ STAR ---
st.markdown('<div class="title-center">MATRIZ STAR</div>', unsafe_allow_html=True)
up = st.file_uploader("Upload da Base", type=['xlsx'], label_visibility="collapsed")

if up:
    df_raw = pd.read_excel(up)
    df_raw.columns = [str(c).strip().upper() for c in df_raw.columns]
    
    # Identificação inteligente de colunas
    cols = df_raw.columns.tolist()
    col_cliente = next((c for c in ["EMPRESA", "CLIENTE", "NOME", "RAZAO SOCIAL"] if c in cols), cols[0])
    focos = ["VENDEDOR", "SEGMENTO", "CIDADE", "REGIAO", "UF"]
    dim_reais = [c for c in cols if any(f in c for f in focos)]

    with st.sidebar:
        st.subheader("GOVERNANÇA")
        dims_sel = [d for d in dim_reais if st.checkbox(d, key=f"chk_{d}")]
    
    meses_ref = ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ']
    col_m = [c for c in cols if any(m in c for m in meses_ref) and 'TOTAL' not in c]

    if not col_m:
        st.warning("Aguardando detecção de colunas de faturamento (JAN, FEV...)")
    else:
        for col in col_m: df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce').fillna(0)
        chaves_ag = list(dict.fromkeys([col_cliente] + dims_sel))
        df_ag = df_raw.groupby(chaves_ag, as_index=False)[col_m].sum()
        
        p_meses = col_m[-lp_val:]
        df_ag['TOTAL_ACUMULADO'] = df_ag[p_meses].sum(axis=1).round(0)
        df_ag['MEDIA_LP'] = (df_ag[p_meses].sum(axis=1) / len(p_meses)).round(0)
        df_ag['MEDIA_CP'] = (df_ag[col_m[-cp_val:]].sum(axis=1) / cp_val).round(0)
        
        df_ag = df_ag.sort_values('TOTAL_ACUMULADO', ascending=False)
        df_ag['CURVA'] = (df_ag['TOTAL_ACUMULADO'].cumsum() / df_ag['TOTAL_ACUMULADO'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
        
        res = df_ag.apply(lambda r: engine_star(r, r['MEDIA_LP'], r['MEDIA_CP']), axis=1)
        df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)

        # --- BLOCO VISUAL (INFOGRÁFICOS) ---
        if dims_sel:
            dim_p = dims_sel[0]
            st.markdown('<div class="subtitle-center" style="text-align: left; margin-top: 30px;">ANÁLISE ESTRUTURAL DA CARTEIRA</div>', unsafe_allow_html=True)
            df_p = df_ag.groupby(dim_p)[['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP']].sum().reset_index().sort_values('TOTAL_ACUMULADO', ascending=False)
            res_stat = df_ag.groupby([dim_p, 'STATUS']).size().unstack(fill_value=0)
            df_p = df_p.merge(res_stat, on=dim_p, how='left')
            
            for _, row in df_p.head(5).iterrows():
                tot = row.get('🟢 CRESCIMENTO',0)+row.get('🔵 ESTÁVEL',0)+row.get('🔴 QUEDA',0)+row.get('🚨 QUEDA ACENTUADA',0)+row.get('⚫ INATIVO',0)
                html_bar = f'<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:20px;margin-bottom:12px;"><b>{row[dim_p]}</b> (R$ {format_br(row["TOTAL_ACUMULADO"])})</div>'
                st.markdown(html_bar, unsafe_allow_html=True)

        # --- DRILL-DOWN E EXPORTAÇÃO ---
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#ccc;margin-top:50px;">🔬 DRILL-DOWN TÁTICO</div>', unsafe_allow_html=True)
        opcoes = ["TODOS"] + df_ag[dims_sel[0]].unique().tolist() if dims_sel else ["TODOS"]
        f_sel = st.selectbox("Isolar Análise", opcoes, label_visibility="collapsed")
        
        df_exib = df_ag[df_ag[dims_sel[0]] == f_sel].copy() if f_sel != "TODOS" and dims_sel else df_ag.copy()
        cols_v = list(dict.fromkeys(['CURVA', col_cliente] + dims_sel + col_m + ['TOTAL_ACUMULADO', 'STATUS', 'META', 'AÇÃO']))

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as wr:
            df_exib[cols_v].to_excel(wr, index=False, sheet_name='STAR')
            wb, ws = wr.book, wr.sheets['STAR']
            h_f = wb.add_format({'bold':1,'font_color':'#FFFFFF','bg_color':'#002060','border':1,'border_color':'#FFFFFF','align':'center','valign':'vcenter','text_wrap':1})
            b_f = wb.add_format({'valign':'vcenter','align':'left','border':1,'border_color':'#D9D9D9','text_wrap':1})
            for i, v in enumerate(cols_v): ws.write(0, i, v, h_f)
            ws.set_column(1,1,50); ws.set_column(len(cols_v)-1, len(cols_v)-1, 80); ws.set_default_row(75)
        
        st.download_button(f"📥 EXPORTAR {f_sel}", output.getvalue(), f"Giri_STAR_{f_sel}.xlsx")
        st.dataframe(df_exib[cols_v].style.format({c: format_br for c in col_m + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)
