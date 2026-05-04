import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import math
from io import BytesIO

# 1. DESIGN EXECUTIVO GIRI - ESTÉTICA UNIFICADA E ALTA PERFORMANCE
st.set_page_config(page_title="Giri Architecture Hub", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* FUNDO GRADIENTE RADIAL PROFUNDO */
    .stApp { background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); color: #ffffff; }
    header {visibility: hidden;}
    
    /* SIDEBAR EXECUTIVA */
    [data-testid="stSidebar"] { background-color: #000810 !important; border-right: 1px solid rgba(255, 255, 255, 0.1) !important; min-width: 240px !important; }
    .sidebar-title { margin-top: -30px; margin-bottom: 20px; letter-spacing: 2px; font-size: 1.1rem; font-weight: 800; color: white; text-transform: uppercase; }

    /* DASHBOARD CARDS */
    .tool-card { 
        background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(20px); border-radius: 4px; padding: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.08); text-align: center; height: 110px; display: flex; 
        flex-direction: column; justify-content: center; transition: all 0.3s ease;
    }
    .tool-card:hover { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.2); }
    h4 { text-transform: uppercase; letter-spacing: 1.5px; font-size: 0.9rem; margin-bottom: 8px; color: #ffffff; font-weight: 700; }
    .tool-card p { color: rgba(255, 255, 255, 0.4); font-size: 0.7rem; line-height: 1.2; margin: 0; }

    /* TITULOS CENTRALIZADOS E SUBIDA DE CONTEÚDO */
    .title-center { text-align: center; text-transform: uppercase; letter-spacing: 5px; margin-top: -45px; font-weight: 800; font-size: 1.8rem; }
    .vendedor-destaque { text-align: center; text-transform: uppercase; letter-spacing: 3px; color: #ffffff; margin-bottom: 5px; font-weight: 700; font-size: 1.4rem; }
    .subtitle-center { text-align: center; text-transform: uppercase; letter-spacing: 2px; color: rgba(255, 255, 255, 0.6); margin-bottom: 30px; font-size: 0.9rem; }

    /* INPUTS LIMPOS */
    .stTextInput input { height: 40px !important; text-align: center !important; background-color: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 4px !important; color: #ffffff !important; }
    
    /* GATILHO INVISÍVEL DASHBOARD */
    .btn-container .stButton button { background-color: transparent !important; border: none !important; color: transparent !important; height: 110px !important; width: 100% !important; position: absolute; top: -110px; z-index: 101; }

    /* TABELAS */
    div[data-testid="stTable"] table { width: 100% !important; }
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { text-align: center !important; vertical-align: middle !important; font-size: 13px !important; color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def format_br(val):
    if val == 0 or pd.isna(val): return "-"
    return f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")

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
    if cp == 0: return "⚫ INATIVO", 0, "AÇÃO: Diagnóstico de Churn. Identifique o motivo real da parada."
    if cp < (lp * 0.80): return "🚨 QUEDA ACENTUADA", lp, "AÇÃO: Defesa de Share. Investigar concorrência ou falha."
    if cp < (lp * 0.95): return "🔴 QUEDA", lp, "AÇÃO: Estabilização. Identificar se é sazonal ou mix."
    if cp > (lp * 1.05): return "🟢 CRESCIMENTO", int(cp * 1.05), "AÇÃO: Expansão. Upsell e elevação de Ticket Médio."
    return "🔵 ESTÁVEL", int(lp * 1.05), "AÇÃO: Blindagem. Prevenir inércia e validar satisfação."

# --- LÓGICA TEMPORAL ---
hoje = datetime.now()
meses_br = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
d_totais = get_business_days(hoje.replace(day=1), (hoje.replace(month=hoje.month % 12 + 1, day=1) if hoje.month < 12 else hoje.replace(year=hoje.year + 1, month=1, day=1)) - pd.Timedelta(days=1))
d_passados = get_business_days(hoje.replace(day=1), hoje)
if hoje.weekday() < 5 and hoje.strftime('%Y-%m-%d') not in ['2026-05-01']: d_passados = max(0, d_passados - 1)

# --- NAVEGAÇÃO ---
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = 'Dashboard'

with st.sidebar:
    st.markdown('<div class="sidebar-title">GIRI | ARCHITECTURE</div>', unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state.pagina_ativa != 'Dashboard':
        if st.button("⬅ VOLTAR PARA DASHBOARD"):
            st.session_state.pagina_ativa = 'Dashboard'
            st.rerun()

# --- TELA 1: DASHBOARD ---
if st.session_state.pagina_ativa == 'Dashboard':
    st.markdown('<h1 class="title-center">Dashboard Estratégico</h1>', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        st.markdown('<div class="tool-card"><h4>MATRIZ STAR</h4><p>Diagnóstico de Carteira e Governança de Churn</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="btn-container">', unsafe_allow_html=True)
        if st.button("", key="btn_star"): st.session_state.pagina_ativa = 'Matriz'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<div class="tool-card"><h4>MATRIZ DE DESEMPENHO</h4><p>Gestão de Ritmo e Eficiência Individual</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="btn-container">', unsafe_allow_html=True)
        if st.button("", key="btn_des"): st.session_state.pagina_ativa = 'Desempenho'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- TELA 2: MATRIZ STAR ---
elif st.session_state.pagina_ativa == 'Matriz':
    st.markdown('<h1 class="title-center">STAR-OS | GOVERNANÇA</h1>', unsafe_allow_html=True)
    with st.sidebar:
        lp_val = st.number_input("Longo Prazo (Meses)", value=12, min_value=1)
        cp_val = st.number_input("Curto Prazo (Meses)", value=3, min_value=1)
    uploaded_file = st.file_uploader("Upload da Base de Faturamento", type=['xlsx'])
    if uploaded_file:
        df_raw = pd.read_excel(uploaded_file)
        df_raw.columns = [str(c).upper() for c in df_raw.columns]
        col_meses = [c for c in df_raw.columns if any(m in c for m in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'])]
        df_agrupado = df_raw.groupby(['EMPRESA', 'VENDEDOR'])[col_meses].sum().reset_index()
        df_agrupado['MEDIA_LP'] = (df_agrupado[col_meses[-(lp_val+cp_val):-cp_val]].sum(axis=1) / lp_val).round(0)
        df_agrupado['MEDIA_CP'] = (df_agrupado[col_meses[-cp_val:]].sum(axis=1) / cp_val).round(0)
        res_star = df_agrupado.apply(lambda row: engine_star(row, row['MEDIA_LP'], row['MEDIA_CP']), axis=1)
        df_agrupado['STATUS'], df_agrupado['META'], df_agrupado['AÇÃO'] = zip(*res_star)
        st.dataframe(df_agrupado.style.format({c: format_br for c in col_meses + ['MEDIA_LP', 'MEDIA_CP', 'META']}), use_container_width=True)

# --- TELA 3: DESEMPENHO ---
elif st.session_state.pagina_ativa == 'Desempenho':
    with st.sidebar:
        nomes = st.text_area("EQUIPE:", "JOÃO\nCARLOS\nMARIA", height=100)
        vendedor = st.selectbox("CONSULTOR:", [v.strip().upper() for v in nomes.split('\n') if v.strip()])
    st.markdown('<div class="title-center">MATRIZ DE DESEMPENHO</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="vendedor-destaque">{vendedor}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle-center">COMPETÊNCIA: {meses_br[hoje.month].upper()} / {hoje.year}</div>', unsafe_allow_html=True)
    st.info(f"📅 Meta baseada em **{d_passados}** dias úteis passados de **{d_totais}**.")
    cols_in = st.columns(5)
    ind_list = []
    sugestoes = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES", "ORÇAMENTOS", "FATURAMENTO"]
    for i, col in enumerate(cols_in):
        with col:
            st.text_input(f"Indicador {i+1}", value=sugestoes[i], key=f"n_{i}_{vendedor}")
            m_raw = st.text_input(f"Meta", value="", key=f"m_{i}_{vendedor}")
            r_raw = st.text_input(f"Realizado", value="", key=f"r_{i}_{vendedor}")
            ind_list.append({"NOME": sugestoes[i], "META": parse_int(m_raw), "REALIZADO": parse_int(r_raw)})
    res_des = []
    for it in ind_list:
        v_esp = math.ceil((it["META"] / d_totais) * d_passados) if d_totais > 0 else 0
        rota = (it["REALIZADO"] / v_esp) if v_esp > 0 else (1.0 if it["REALIZADO"] >= 0 else 0.0)
        status = "-" if it["META"] == 0 else ("🟢 NO RITMO" if (v_esp == 0) or rota >= 1.0 else "🚨 CRÍTICO")
        res_des.append({"INDICADOR": it["NOME"], "META MENSAL": format_br(it["META"]), "ESPERADO": format_br(v_esp), "REALIZADO": format_br(it["REALIZADO"]), "STATUS": status})
    st.table(pd.DataFrame(res_des))
