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
    .tool-card { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(20px); border-radius: 4px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.08); text-align: center; height: 110px; display: flex; flex-direction: column; justify-content: center; transition: all 0.3s ease; }
    .title-center { text-align: center; text-transform: uppercase; letter-spacing: 5px; margin-top: -45px; font-weight: 800; font-size: 1.8rem; }
    .subtitle-center { text-align: center; text-transform: uppercase; letter-spacing: 2px; color: rgba(255, 255, 255, 0.6); margin-bottom: 30px; font-size: 0.9rem; }
    .stSelectbox div[data-baseweb="select"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; border-radius: 4px !important; min-height: 42px !important; }
    div[data-testid="stDownloadButton"] button { height: 42px !important; border-radius: 6px !important; border: 1px solid rgba(255, 255, 255, 0.3) !important; background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.03)) !important; color: #ffffff !important; font-weight: 800 !important; text-transform: uppercase !important; box-shadow: 3px 3px 10px rgba(0,0,0,0.4), inset 1px 1px 2px rgba(255,255,255,0.2) !important; transition: all 0.2s ease-in-out !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES ---
def format_br(val):
    try:
        if pd.isna(val) or val == 0: return "0"
        return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

def engine_star(row, lp, cp):
    if cp == 0: return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn.\nAÇÃO: Reconexão estratégica.\nORIENTAÇÃO: Identifique o motivo da parada."
    if cp < (lp * 0.80): return "🚨 QUEDA ACENTUADA", lp, "OBJETIVO: Contenção de Perda.\nAÇÃO: Investigação de concorrência.\nORIENTAÇÃO: Defenda o share."
    if cp < (lp * 0.95): return "🔴 QUEDA", lp, "OBJETIVO: Estabilização.\nAÇÃO: Ajuste de mix.\nORIENTAÇÃO: Recupere o giro."
    if cp > (lp * 1.05): return "🟢 CRESCIMENTO", int(cp * 1.05), "OBJETIVO: Expansão.\nAÇÃO: Upsell tático.\nORIENTAÇÃO: Eleve o ticket médio."
    return "🔵 ESTÁVEL", int(lp * 1.05), "OBJETIVO: Blindagem.\nAÇÃO: Validação de satisfação.\nORIENTAÇÃO: Mantenha a recorrência."

# --- ESTADO E NAVEGAÇÃO ---
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = 'Dashboard'
with st.sidebar:
    st.markdown('<div class="sidebar-title">GIRI | ARCHITECTURE</div>', unsafe_allow_html=True)
    if st.session_state.pagina_ativa != 'Dashboard' and st.button("⬅ VOLTAR"): st.session_state.pagina_ativa = 'Dashboard'; st.rerun()
    if st.session_state.pagina_ativa == 'Matriz':
        lp_val = st.number_input("Longo Prazo (Meses)", value=15, min_value=1)
        cp_val = st.number_input("Curto Prazo (Meses)", value=3, min_value=1)

# --- TELA MATRIZ STAR ---
if st.session_state.pagina_ativa == 'Matriz':
    st.markdown('<div class="title-center">MATRIZ STAR</div>', unsafe_allow_html=True)
    up = st.file_uploader("Upload", type=['xlsx'], label_visibility="collapsed")
    if up:
        df_raw = pd.read_excel(up)
        df_raw.columns = [str(c).upper() for c in df_raw.columns]
        dim_reais = [c for c in df_raw.columns if any(f in c for f in ["VENDEDOR", "SEGMENTO", "CIDADE", "REGIAO", "UF"])]
        with st.sidebar:
            st.subheader("GOVERNANÇA")
            dims_sel = [d for d in dim_reais if st.checkbox(d, key=f"chk_{d}")]
        if dims_sel:
            dim_p = dims_sel[0]
            col_m = [c for c in df_raw.columns if any(m in c for m in ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ'])]
            for col in col_m: df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce').fillna(0)
            p_meses = col_m[-lp_val:]
            df_ag = df_raw.groupby(['EMPRESA'] + dims_sel)[col_m].sum().reset_index()
            df_ag['TOTAL_ACUMULADO'] = df_ag[p_meses].sum(axis=1).round(0)
            df_ag['MEDIA_LP'] = (df_ag[p_meses].sum(axis=1) / len(p_meses)).round(0)
            df_ag['MEDIA_CP'] = (df_ag[col_m[-cp_val:]].sum(axis=1) / cp_val).round(0)
            
            # Pareto e Curva ABC
            df_ag = df_ag.sort_values('TOTAL_ACUMULADO', ascending=False)
            df_ag['CUM'] = df_ag['TOTAL_ACUMULADO'].cumsum()
            df_ag['CURVA'] = (df_ag['CUM'] / df_ag['TOTAL_ACUMULADO'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
            
            res = df_ag.apply(lambda r: engine_star(r, r['MEDIA_LP'], r['MEDIA_CP']), axis=1)
            df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)
            
            # Drill-Down com Ordenação de Pareto na Lista
            st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#ccc;margin-top:20px;margin-bottom:10px;">🔬 DRILL-DOWN TÁTICO: ISOLAMENTO DE CARTEIRA</div>', unsafe_allow_html=True)
            list_ord = df_ag.groupby(dim_p)['TOTAL_ACUMULADO'].sum().sort_values(ascending=False).index.tolist()
            opcoes = ["TODOS OS SEGMENTOS"] + list_ord
            if 'mem_f' not in st.session_state: st.session_state.mem_f = "TODOS OS SEGMENTOS"
            c_f, c_ex = st.columns([3, 2])
            with c_f:
                f_sel = st.selectbox("X", opcoes, index=opcoes.index(st.session_state.mem_f) if st.session_state.mem_f in opcoes else 0, label_visibility="collapsed", key="sel_f")
                st.session_state.mem_f = f_sel
            
            df_exib = df_ag[df_ag[dim_p] == f_sel].copy() if f_sel != "TODOS OS SEGMENTOS" else df_ag.copy()
            
            # --- BLINDAGEM DE DUPLICIDADE ---
            # Removemos colunas auxiliares e garantimos nomes únicos para a visualização
            cols_limpas = ['CURVA', 'EMPRESA'] + dims_sel + col_m + ['TOTAL_ACUMULADO', 'STATUS', 'META', 'AÇÃO']
            # O truque tático: dict.fromkeys remove duplicatas mantendo a ordem
            cols_view = list(dict.fromkeys(cols_limpas)) 
            
            with c_ex:
                out = BytesIO()
                with pd.ExcelWriter(out, engine='xlsxwriter') as wr:
                    df_exib[cols_view].to_excel(wr, index=False, sheet_name='STAR')
                    wb, ws = wr.book, wr.sheets['STAR']
                    h_fmt = wb.add_format({'bold':1,'font_color':'#FFF','bg_color':'#002060','border':1,'border_color':'#FFF','align':'center','valign':'vcenter','text_wrap':1})
                    b_fmt = wb.add_format({'valign':'vcenter','align':'left','border':1,'border_color':'#D9D9D9'})
                    n_fmt = wb.add_format({'num_format':'#,##0','valign':'vcenter','align':'center','border':1})
                    for i, v in enumerate(cols_view): ws.write(0, i, v, h_fmt)
                    ws.set_column(0,0,8); ws.set_column(1,1,45); ws.set_column(len(cols_view)-1, len(cols_view)-1, 70)
                    ws.set_default_row(60)
                st.download_button(f"📥 EXPORTAR {f_sel.upper()}", out.getvalue(), f"Matriz_STAR_{f_sel}.xlsx")

            # Exibição na Tela sem centavos
            st.dataframe(df_exib[cols_view].style.format({c: format_br for c in col_m + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)

elif st.session_state.pagina_ativa == 'Dashboard':
    st.markdown('<h1 class="title-center">GIRI | STAR-OS</h1>', unsafe_allow_html=True)
    if st.button("ACESSAR MATRIZ STAR", use_container_width=True): st.session_state.pagina_ativa = 'Matriz'; st.rerun()
