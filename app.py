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
    div[data-testid="stDownloadButton"] button { height: 42px !important; border-radius: 6px !important; border: 1px solid rgba(255, 255, 255, 0.3) !important; background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.03)) !important; color: #ffffff !important; font-weight: 800 !important; text-transform: uppercase !important; box-shadow: 3px 3px 10px rgba(0,0,0,0.4), inset 1px 1px 2px rgba(255,255,255,0.2) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE GOVERNANÇA STAR ---
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
            df_ag = df_ag.sort_values('TOTAL_ACUMULADO', ascending=False)
            df_ag['CURVA'] = (df_ag['TOTAL_ACUMULADO'].cumsum() / df_ag['TOTAL_ACUMULADO'].sum()).apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
            res = df_ag.apply(lambda r: engine_star(r, r['MEDIA_LP'], r['MEDIA_CP']), axis=1)
            df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)

            # --- DRILL-DOWN ---
            st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#ccc;margin-top:20px;margin-bottom:10px;">🔬 DRILL-DOWN TÁTICO</div>', unsafe_allow_html=True)
            repres = df_ag.groupby(dim_p)['TOTAL_ACUMULADO'].sum().sort_values(ascending=False).index.tolist()
            opcoes = ["TODOS OS SEGMENTOS"] + repres
            if 'mem_f' not in st.session_state: st.session_state.mem_f = "TODOS OS SEGMENTOS"
            c_f, c_ex = st.columns([3, 2])
            with c_f:
                f_sel = st.selectbox("X", opcoes, index=opcoes.index(st.session_state.mem_f) if st.session_state.mem_f in opcoes else 0, label_visibility="collapsed", key="sel_f")
                st.session_state.mem_f = f_sel
            df_exib = df_ag[df_ag[dim_p] == f_sel].copy() if f_sel != "TODOS OS SEGMENTOS" else df_ag.copy()
            cols_v = list(dict.fromkeys(['CURVA', 'EMPRESA'] + dims_sel + col_m + ['TOTAL_ACUMULADO', 'STATUS', 'META', 'AÇÃO']))
            
            with c_ex:
                out = BytesIO()
                with pd.ExcelWriter(out, engine='xlsxwriter') as wr:
                    df_exib[cols_v].to_excel(wr, index=False, sheet_name='STAR')
                    wb, ws = wr.book, wr.sheets['STAR']
                    
                    # CORREÇÃO DEFINITIVA DO CABEÇALHO: FONTE BRANCA (#FFFFFF) NO AZUL ESCURO
                    h_fmt = wb.add_format({
                        'bold': True, 
                        'font_color': '#FFFFFF', 
                        'bg_color': '#002060', 
                        'border': 1, 
                        'border_color': '#FFFFFF', 
                        'align': 'center', 
                        'valign': 'vcenter', 
                        'text_wrap': True
                    })
                    
                    b_fmt = wb.add_format({'valign': 'vcenter', 'align': 'left', 'border': 1, 'border_color': '#D9D9D9', 'text_wrap': True})
                    num_fmt = wb.add_format({'num_format': '#,##0', 'valign': 'vcenter', 'align': 'center', 'border': 1, 'border_color': '#D9D9D9'})
                    bold_lbl = wb.add_format({'bold': True, 'valign': 'vcenter', 'text_wrap': True})
                    f_q = wb.add_format({'font_color': '#FF0000', 'bold': 1, 'valign': 'vcenter', 'border': 1, 'border_color': '#D9D9D9'})
                    f_q_ac = wb.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'bold': 1, 'valign': 'vcenter', 'border': 1})
                    f_c = wb.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100', 'bold': 1, 'valign': 'vcenter', 'border': 1})
                    f_e = wb.add_format({'bg_color': '#DDEBF7', 'font_color': '#0070C0', 'bold': 1, 'valign': 'vcenter', 'border': 1})

                    for i, v in enumerate(cols_v): ws.write(0, i, v, h_fmt)
                    st_idx, ac_idx = cols_v.index('STATUS'), cols_v.index('AÇÃO')
                    for r_idx, (idx, row) in enumerate(df_exib.iterrows()):
                        s_v, t_fmt = str(row['STATUS']), b_fmt
                        if "QUEDA ACENTUADA" in s_v: t_fmt = f_q_ac
                        elif "🔴 QUEDA" in s_v: t_fmt = f_q
                        elif "CRESCIMENTO" in s_v: t_fmt = f_c
                        elif "ESTÁVEL" in s_v: t_fmt = f_e
                        for c_idx, c_n in enumerate(cols_v):
                            val = row[c_n]
                            if c_idx == st_idx: ws.write(r_idx+1, c_idx, val, t_fmt)
                            elif c_idx == ac_idx:
                                parts = str(val).split('\n')
                                rich = []
                                for p in parts:
                                    if ':' in p:
                                        lbl, cont = p.split(':', 1)
                                        rich.extend([bold_lbl, lbl + ':', b_fmt, cont + '\n'])
                                if rich: ws.write_rich_string(r_idx+1, ac_idx, *rich, b_fmt)
                                else: ws.write(r_idx+1, c_idx, val, b_fmt)
                            elif isinstance(val, (int, float)): ws.write(r_idx+1, c_idx, int(val), num_fmt)
                            else: ws.write(r_idx+1, c_idx, val, b_fmt)
                    ws.set_column(0, 0, 10); ws.set_column(1, 1, 50); ws.set_column(ac_idx, ac_idx, 80); ws.set_default_row(75)
                st.download_button(f"📥 EXPORTAR {f_sel.upper()}", out.getvalue(), f"Matriz_STAR_{f_sel}.xlsx")

            st.dataframe(df_exib[cols_v].style.format({c: format_br for c in col_m + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)

elif st.session_state.pagina_ativa == 'Dashboard':
    st.markdown('<h1 class="title-center">GIRI | ARCHITECTURE</h1>', unsafe_allow_html=True)
    if st.button("ACESSAR MATRIZ STAR", use_container_width=True): st.session_state.pagina_ativa = 'Matriz'; st.rerun()
