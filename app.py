import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import math

# 1. DESIGN EXECUTIVO GIRI - ESTÉTICA DE ALTA PERFORMANCE
st.set_page_config(page_title="Giri Architecture Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #001f3f 0%, #000c18 60%, #00050a 100%); 
        color: #ffffff; 
    }
    header {visibility: hidden;}
    [data-testid="stSidebar"] { 
        background-color: rgba(0, 0, 0, 0.3) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        min-width: 220px !important;
    }
    
    /* INPUTS MINIMALISTAS EM BRANCO */
    .stTextInput input {
        height: 38px !important;
        text-align: center !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        font-size: 14px !important;
        color: #ffffff !important;
    }
    
    div[data-testid="stTable"] table { width: 100% !important; table-layout: fixed !important; }
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { 
        text-align: center !important; 
        vertical-align: middle !important; 
        font-size: 13px !important;
        padding: 12px 5px !important;
        white-space: nowrap !important;
    }
    div[data-testid="stTable"] th:nth-child(1), div[data-testid="stTable"] td:nth-child(1) { width: 25% !important; text-align: left !important; }
    div[data-testid="stTable"] th { font-weight: bold !important; border-bottom: 2px solid rgba(255,255,255,0.1) !important; }

    .title-center {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 5px;
        margin-top: 20px;
        margin-bottom: 10px;
        font-weight: 800;
        font-size: 1.8rem;
    }
    
    .subtitle-center {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: rgba(255, 255, 255, 0.6);
        margin-bottom: 40px;
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
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

def get_working_days(start, end):
    if start > end: return 0
    days = pd.date_range(start, end)
    return len(days[days.dayofweek < 5])

# --- INICIALIZAÇÃO NAVEGAÇÃO ---
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = 'Dashboard'

with st.sidebar:
    st.markdown("<br><br><h2 style='letter-spacing:2px; font-size:1rem;'>GIRI | ARCHITECTURE</h2>", unsafe_allow_html=True)
    if st.session_state.pagina_ativa != 'Dashboard':
        if st.button("⬅ VOLTAR PARA DASHBOARD"):
            st.session_state.pagina_ativa = 'Dashboard'
            st.rerun()

# --- LÓGICA DE TEMPO ---
hoje = datetime.now()
meses_br = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}
competencia_txt = f"{meses_br[hoje.month]} / {hoje.year}"

p_dia = hoje.replace(day=1)
u_dia = (hoje.replace(month=hoje.month % 12 + 1, day=1) if hoje.month < 12 else hoje.replace(year=hoje.year + 1, month=1, day=1)) - pd.Timedelta(days=1)
d_totais = get_working_days(p_dia, u_dia)
d_passados = get_working_days(p_dia, hoje)
if hoje.weekday() < 5: d_passados = max(0, d_passados - 1)

# --- TELA DESEMPENHO ---
if st.session_state.pagina_ativa == 'Desempenho':
    with st.sidebar:
        st.markdown("---")
        nomes = st.text_area("EQUIPE:", "JOÃO\nCARLOS\nMARIA", height=100)
        vendedor = st.selectbox("CONSULTOR:", [v.strip().upper() for v in nomes.split('\n') if v.strip()])
    
    st.markdown(f'<div class="title-center">MATRIZ DE DESEMPENHO: {vendedor}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle-center">COMPETÊNCIA: {competencia_txt.upper()}</div>', unsafe_allow_html=True)
    
    st.info(f"📅 Meta baseada em {d_passados} dias úteis passados de {d_totais}.")
    
    cols_in = st.columns(5)
    ind_list = []
    sugestoes = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES", "ORÇAMENTOS", "FATURAMENTO"]

    for i, col in enumerate(cols_in):
        with col:
            n = st.text_input(f"Indicador {i+1}", value=sugestoes[i], key=f"n_{i}_{vendedor}")
            m_raw = st.text_input(f"Meta", value="", key=f"m_{i}_{vendedor}")
            r_raw = st.text_input(f"Realizado", value="", key=f"r_{i}_{vendedor}")
            
            ind_list.append({
                "NOME": n, 
                "META": parse_int(m_raw), 
                "REALIZADO": parse_int(r_raw)
            })

    res = []
    for it in ind_list:
        v_esp = math.ceil((it["META"] / d_totais) * d_passados) if d_totais > 0 else 0
        rota = (it["REALIZADO"] / v_esp) if v_esp > 0 else (1.0 if it["REALIZADO"] >= 0 else 0.0)
        tend = math.ceil((it["REALIZADO"] / d_passados) * d_totais) if d_passados > 0 else it["REALIZADO"]
        
        status = "🟢 NO RITMO" if (v_esp == 0) or rota >= 1.0 else "🟡 ATENÇÃO" if rota >= 0.85 else "🚨 CRÍTICO"
        
        res.append({
            "INDICADOR": it["NOME"].upper(),
            "META MENSAL": format_br(it["META"]),
            "ESPERADO": format_br(v_esp),
            "REALIZADO": format_br(it["REALIZADO"]),
            "EFICIÊNCIA (ROTA)": f"{round(rota * 100, 1)}%",
            "PROJEÇÃO FINAL": format_br(tend),
            "STATUS": status
        })
    st.table(pd.DataFrame(res))
