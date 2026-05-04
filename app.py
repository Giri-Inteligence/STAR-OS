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

    .tool-card { 
        background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(20px); border-radius: 4px; padding: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.08); text-align: center; height: 110px; display: flex; 
        flex-direction: column; justify-content: center; transition: all 0.3s ease;
    }
    .tool-card:hover { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.2); }
    
    .title-center { text-align: center; text-transform: uppercase; letter-spacing: 5px; margin-top: -45px; font-weight: 800; font-size: 1.8rem; }
    .subtitle-center { text-align: center; text-transform: uppercase; letter-spacing: 2px; color: rgba(255, 255, 255, 0.6); margin-bottom: 30px; font-size: 0.9rem; }

    /* INPUTS E SELETORES */
    .stSelectbox div[data-baseweb="select"] { 
        background-color: rgba(255, 255, 255, 0.05) !important; 
        border: 1px solid rgba(255, 255, 255, 0.2) !important; 
        border-radius: 4px !important; 
        min-height: 42px !important;
    }

    /* BOTÃO DE EXPORTAÇÃO 3D (BISEL E SOMBRA) */
    div[data-testid="stDownloadButton"] button { 
        height: 42px !important; 
        border-radius: 6px !important; 
        border: 1px solid rgba(255, 255, 255, 0.3) !important; 
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.02)) !important;
        color: #ffffff !important; 
        font-weight: 800 !important; 
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        white-space: nowrap !important; 
        width: 100% !important; 
        box-shadow: 3px 3px 10px rgba(0,0,0,0.4), inset 1px 1px 2px rgba(255,255,255,0.2) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-testid="stDownloadButton"] button:hover { 
        background: linear-gradient(145deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05)) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0px 0px 15px rgba(255,255,255,0.15), inset 1px 1px 1px rgba(255,255,255,0.3) !important;
        transform: translateY(-1px);
    }
    div[data-testid="stDownloadButton"] button:active {
        box-shadow: inset 2px 2px 5px rgba(0,0,0,0.5) !important;
        transform: translateY(1px);
    }

    div[data-testid="stDataFrame"] td { white-space: pre-wrap !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES GLOBAIS ---
def format_br(val):
    try:
        if pd.isna(val) or val == 0: return "0"
        return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return val

def parse_int(val):
    try:
        limpo = str(val).replace(".", "").replace(",", "")
        return int(limpo) if limpo else 0
    except: return 0

def get_business_days(start, end):
    holidays = ['2026-01-01', '2026-05-01', '2026-09-07', '2026-10-12', '2026-11-02', '2026-11-15', '2026-12-25']
    days = pd.date_range(start, end)
    return len([d for d in days if d.weekday() < 5 and d.strftime('%Y-%m-%d') not in holidays])

def engine_star(row, lp, cp):
    if cp == 0: return "⚫ INATIVO", 0, "OBJETIVO: Diagnóstico de Churn e Reconexão."
    if cp < (lp * 0.80): return "🚨 QUEDA ACENTUADA", lp, "OBJETIVO: Contenção de Perda e Defesa de Share."
    if cp < (lp * 0.95): return "🔴 QUEDA", lp, "OBJETIVO: Estabilização de Giro."
    if cp > (lp * 1.05): return "🟢 CRESCIMENTO", int(cp * 1.05), "OBJETIVO: Expansão de Share e Upsell."
    return "🔵 ESTÁVEL", int(lp * 1.05), "OBJETIVO: Manutenção e Blindagem."

# --- LÓGICA TEMPORAL ---
hoje = datetime.now()
p_dia, u_dia = hoje.replace(day=1), (hoje.replace(month=hoje.month % 12 + 1, day=1) if hoje.month < 12 else hoje.replace(year=hoje.year + 1, month=1, day=1)) - pd.Timedelta(days=1)
d_totais, d_passados = get_business_days(p_dia, u_dia), max(0, get_business_days(p_dia, hoje) - 1)

# --- NAVEGAÇÃO ---
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = 'Dashboard'
with st.sidebar:
    st.markdown('<div class="sidebar-title">GIRI | ARCHITECTURE</div>', unsafe_allow_html=True)
    if st.session_state.pagina_ativa != 'Dashboard' and st.button("⬅ VOLTAR"):
        st.session_state.pagina_ativa = 'Dashboard'; st.rerun()
    if st.session_state.pagina_ativa == 'Matriz':
        lp_val = st.number_input("Longo Prazo (Meses)", value=12, min_value=1)
        cp_val = st.number_input("Curto Prazo (Meses)", value=3, min_value=1)

# --- TELA 1: DASHBOARD ---
if st.session_state.pagina_ativa == 'Dashboard':
    st.markdown('<h1 class="title-center">DASHBOARD ESTRATÉGICO</h1>', unsafe_allow_html=True)
    cols = st.columns(4)
    titulos = ["MATRIZ STAR", "MATRIZ DE DESEMPENHO", "ARQUITETURA", "PIPELINE"]
    paginas = ["Matriz", "Desempenho", "Dashboard", "Dashboard"]
    for i, t in enumerate(titulos):
        with cols[i]:
            st.markdown(f'<div class="tool-card"><h4>{t}</h4></div>', unsafe_allow_html=True)
            if st.button("Acessar", key=f"btn_{i}", use_container_width=True): 
                st.session_state.pagina_ativa = paginas[i]; st.rerun()

# --- TELA 2: MATRIZ STAR ---
elif st.session_state.pagina_ativa == 'Matriz':
    st.markdown('<div class="title-center">MATRIZ STAR</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Base", type=['xlsx'], label_visibility="collapsed")
    if uploaded_file:
        df_raw = pd.read_excel(uploaded_file)
        df_raw.columns = [str(c).upper() for c in df_raw.columns]
        focos = ["VENDEDOR", "SEGMENTO", "CIDADE", "REGIAO", "UF"]
        dimensoes_reais = [c for c in df_raw.columns if any(f in c for f in focos)]
        
        with st.sidebar:
            st.subheader("CHAVES")
            dims_selecionadas = [d for d in dimensoes_reais if st.checkbox(d, key=f"chk_{d}")]
            
        if dims_selecionadas:
            col_meses = [c for c in df_raw.columns if any(m in c for m in ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ'])]
            meses_ativos = col_meses[-lp_val:]
            df = df_raw.copy()
            for col in col_meses: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            chaves = ['EMPRESA'] + dims_selecionadas
            df_ag = df.groupby(chaves)[col_meses].sum().reset_index()
            df_ag['TOTAL_ACUMULADO'] = df_ag[meses_ativos].sum(axis=1).round(0)
            df_ag['MEDIA_LP'] = (df_ag[meses_ativos].sum(axis=1) / len(meses_ativos)).round(0)
            df_ag['MEDIA_CP'] = (df_ag[col_meses[-cp_val:]].sum(axis=1) / cp_val).round(0)
            
            res = df_ag.apply(lambda row: engine_star(row, row['MEDIA_LP'], row['MEDIA_CP']), axis=1)
            df_ag['STATUS'], df_ag['META'], df_ag['AÇÃO'] = zip(*res)
            df_final = df_ag.sort_values('TOTAL_ACUMULADO', ascending=False)
            
            # --- INFOGRÁFICOS ---
            dim_principal = dims_selecionadas[0]
            df_pareto = df_final.groupby(dim_principal)[['TOTAL_ACUMULADO','MEDIA_LP','MEDIA_CP']].sum().reset_index()
            df_pareto = df_pareto.sort_values('TOTAL_ACUMULADO', ascending=False)
            df_pareto['CUM_PCT'] = df_pareto['TOTAL_ACUMULADO'].cumsum() / df_pareto['TOTAL_ACUMULADO'].sum()
            
            resumo_dim = df_final.groupby([dim_principal, 'STATUS']).size().unstack(fill_value=0)
            df_p = df_pareto.merge(resumo_dim, on=dim_principal, how='left')
            
            html = '<div style="margin-bottom:30px;">'
            for _, row in df_p.head(5).iterrows(): # Exemplo Curva A
                tot = row.get('🟢 CRESCIMENTO',0) + row.get('🔵 ESTÁVEL',0) + row.get('🔴 QUEDA',0) + row.get('🚨 QUEDA ACENTUADA',0) + row.get('⚫ INATIVO',0)
                media_lp, media_cp = row['MEDIA_LP'], row['MEDIA_CP']
                tracao_pct = ((media_cp / media_lp) - 1) * 100 if media_lp > 0 else 0
                color = "#00E676" if tracao_pct > 0 else "#FF1744"
                
                # Cálculo de Blocos Ordenados
                status_data = [
                    {"n": "Cresc.", "p": round(row.get('🟢 CRESCIMENTO',0)/tot*100,1) if tot>0 else 0, "c": "#00E676"},
                    {"n": "Queda", "p": round((row.get('🔴 QUEDA',0)+row.get('🚨 QUEDA ACENTUADA',0))/tot*100,1) if tot>0 else 0, "c": "#FF1744"},
                    {"n": "Inat.", "p": round(row.get('⚫ INATIVO',0)/tot*100,1) if tot>0 else 0, "c": "#888"}
                ]
                status_data.sort(key=lambda x: x["p"], reverse=True)
                
                barra = "".join([f'<div style="width:{s["p"]}%;padding-right:5px;"><div style="height:6px;background:{s["c"]};border-radius:2px;"></div><div style="font-size:0.6rem;color:{s["c"]};font-weight:700;">{s["n"]} {s["p"]}%</div></div>' for s in status_data if s["p"] > 0])
                
                html += f"""<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:15px;margin-bottom:10px;">
<div style="display:flex;justify-content:space-between;"><b>{row[dim_principal]}</b><span style="font-size:0.7rem;color:#888;">{int(tot)} CONTAS</span></div>
<div style="display:flex;gap:20px;margin:10px 0;border-bottom:1px solid rgba(255,255,255,0.05);padding-bottom:10px;">
<div><small style="color:#888;">RECEITA</small><br>R$ {format_br(row['TOTAL_ACUMULADO'])}</div>
<div style="color:{color};">▲ {tracao_pct:.1f}%</div>
</div>
<div style="display:flex;">{barra}</div>
</div>"""
            st.markdown(html + "</div>", unsafe_allow_html=True)

            # --- DRILL DOWN COM BOTÃO 3D ---
            st.markdown('<div style="font-size:0.8rem;font-weight:700;color:#888;margin-bottom:10px;">ISOLAMENTO DE CARTEIRA</div>', unsafe_allow_html=True)
            col_f, col_ex = st.columns([3, 2])
            
            if 'mem_f' not in st.session_state: st.session_state.mem_f = "TODOS"
            opcoes = ["TODOS"] + list(df_final[dim_principal].unique())
            
            with col_f:
                f_sel = st.selectbox("X", opcoes, index=opcoes.index(st.session_state.mem_f) if st.session_state.mem_f in opcoes else 0, label_visibility="collapsed", key="sel_f")
                st.session_state.mem_f = f_sel
            
            df_exib = df_final[df_final[dim_principal] == f_sel] if f_sel != "TODOS" else df_final
            
            with col_ex:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_exib.to_excel(writer, index=False)
                st.download_button(f"📥 EXPORTAR {f_sel}", output.getvalue(), f"{f_sel}.xlsx")

            st.dataframe(df_exib.style.format({c: format_br for c in col_meses + ['TOTAL_ACUMULADO', 'MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)
