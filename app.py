import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import math

# 1. DESIGN EXECUTIVO GIRI
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001220 0%, #002d4a 100%); color: #ffffff; }
    [data-testid="stSidebar"] { min-width: 220px !important; max-width: 220px !important; }
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 12px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.5px; }
    
    div[data-testid="stTable"] table { width: 100% !important; table-layout: fixed !important; }
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { 
        text-align: center !important; 
        vertical-align: middle !important; 
        font-size: 13px !important;
        padding: 10px 5px !important;
        white-space: nowrap !important;
    }
    div[data-testid="stTable"] th:nth-child(1), div[data-testid="stTable"] td:nth-child(1) { width: 25% !important; text-align: left !important; }
    div[data-testid="stTable"] th:nth-child(7), div[data-testid="stTable"] td:nth-child(7) { width: 15% !important; }
    div[data-testid="stTable"] th { font-weight: bold !important; border-bottom: 2px solid rgba(255,255,255,0.1) !important; }

    .stTextInput input, .stNumberInput input { height: 35px !important; font-size: 13px !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def format_executivo(val):
    if pd.isna(val) or val == 0: return "0"
    return f"{int(val):,}".replace(",", ".")

def get_working_days(start_date, end_date):
    days = pd.date_range(start_date, end_date)
    return len(days[days.dayofweek < 5])

# --- INICIALIZAÇÃO ---
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = 'Dashboard'

# --- NAVEGAÇÃO LATERAL ---
with st.sidebar:
    st.markdown("## GIRI | ARCHITECTURE")
    if st.session_state.pagina_ativa != 'Dashboard':
        if st.button("⬅ VOLTAR PARA DASHBOARD"):
            st.session_state.pagina_ativa = 'Dashboard'
            st.rerun()
    
    if st.session_state.pagina_ativa == 'Desempenho':
        st.markdown("---")
        nomes_raw = st.text_area("EQUIPE:", "JOÃO\nCARLOS\nMARIA", height=100)
        equipe = [v.strip().upper() for v in nomes_raw.split('\n') if v.strip()]
        vendedor_selecionado = st.selectbox("CONSULTOR:", equipe)

# --- LÓGICA DE TEMPO ---
hoje = datetime.now()
primeiro_dia = hoje.replace(day=1)
# Cálculo do último dia do mês corrente
if hoje.month == 12:
    ultimo_dia = hoje.replace(year=hoje.year + 1, month=1, day=1) - pd.Timedelta(days=1)
else:
    ultimo_dia = hoje.replace(month=hoje.month + 1, day=1) - pd.Timedelta(days=1)

d_uteis_totais = get_working_days(primeiro_dia, ultimo_dia)
d_uteis_transcorridos = get_working_days(primeiro_dia, hoje)

# Ajuste: Se hoje for dia útil, a meta "esperada" é até ontem (dia útil anterior)
if hoje.weekday() < 5:
    d_uteis_transcorridos = max(0, d_uteis_transcorridos - 1)
# Se hoje for sábado (5) ou domingo (6), d_uteis_transcorridos já reflete os dias úteis passados corretamente.

# --- TELAS ---
if st.session_state.pagina_ativa == 'Dashboard':
    st.title("Giri Strategic Hub")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="main-card"><h4>📍 Matriz STAR</h4></div>', unsafe_allow_html=True)
        if st.button("ACESSAR MATRIZ STAR"): st.session_state.pagina_ativa = 'Matriz'; st.rerun()
    with c2:
        st.markdown('<div class="main-card"><h4>📊 Desempenho</h4></div>', unsafe_allow_html=True)
        if st.button("ACESSAR DESEMPENHO"): st.session_state.pagina_ativa = 'Desempenho'; st.rerun()

elif st.session_state.pagina_ativa == 'Desempenho':
    st.title(f"GOVERNANÇA: {vendedor_selecionado}")
    st.markdown(f'<div class="main-card">📅 Meta baseada em **{d_uteis_transcorridos}** dias úteis transcorridos de **{d_uteis_totais}**.</div>', unsafe_allow_html=True)
    
    cols = st.columns(5)
    ind_list = []
    sugestoes = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES COM VENDA", "ORÇAMENTOS GERADOS", "FATURAMENTO"]

    for i, col in enumerate(cols):
        with col:
            n = st.text_input(f"Indicador {i+1}", value=sugestoes[i], key=f"n_{i}_{vendedor_selecionado}")
            m = st.number_input(f"Meta", min_value=0.0, step=1.0, format="%.0f", key=f"m_{i}_{vendedor_selecionado}")
            r = st.number_input(f"Realizado", min_value=0.0, step=1.0, format="%.0f", key=f"r_{i}_{vendedor_selecionado}")
            ind_list.append({"NOME": n, "META": m, "REALIZADO": r})

    # TABELA DE DIAGNÓSTICO
    resultados = []
    for item in ind_list:
        v_esp = math.ceil((item["META"] / d_uteis_totais) * d_uteis_transcorridos) if d_uteis_totais > 0 else 0
        rota = (item["REALIZADO"] / v_esp) if v_esp > 0 else (1.0 if item["REALIZADO"] > 0 else 0.0)
        tend = math.ceil((item["REALIZADO"] / d_uteis_transcorridos) * d_uteis_totais) if d_uteis_transcorridos > 0 else item["REALIZADO"]
        
        status = "🟢 NO RITMO" if (v_esp == 0) or rota >= 1.0 else "🟡 ATENÇÃO" if rota >= 0.85 else "🚨 CRÍTICO"
        
        resultados.append({
            "INDICADOR": item["NOME"].upper(),
            "META MENSAL": format_executivo(item["META"]),
            "ESPERADO HOJE": format_executivo(v_esp),
            "REALIZADO": format_executivo(item["REALIZADO"]),
            "EFICIÊNCIA (ROTA)": f"{round(rota * 100, 1)}%",
            "PROJEÇÃO FINAL": format_executivo(tend),
            "STATUS": status
        })
    st.table(pd.DataFrame(resultados))
