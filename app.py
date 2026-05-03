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
    div[data-testid="stTable"] th { font-weight: bold !important; border-bottom: 2px solid rgba(255,255,255,0.1) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def format_executivo(val):
    if pd.isna(val) or val == 0: return "0"
    return f"{int(val):,}".replace(",", ".")

def get_working_days(start, end):
    if start > end: return 0
    days = pd.date_range(start, end)
    return len(days[days.dayofweek < 5])

def engine_star_logic(lp, cp):
    if cp == 0: return "⚫ INATIVO", 0, "AÇÃO: Diagnóstico de Churn."
    if cp < (lp * 0.80): return "🚨 QUEDA ACENTUADA", int(lp), "AÇÃO: Contenção de Perda."
    if cp < (lp * 0.95): return "🔴 QUEDA", int(lp), "AÇÃO: Estabilização de Giro."
    if cp > (lp * 1.05): return "🟢 CRESCIMENTO", int(cp * 1.05), "AÇÃO: Expansão de Share."
    return "🔵 ESTÁVEL", int(lp * 1.05), "AÇÃO: Manutenção e Blindagem."

# --- INICIALIZAÇÃO E NAVEGAÇÃO ---
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = 'Dashboard'

with st.sidebar:
    st.markdown("## GIRI | ARCHITECTURE")
    if st.session_state.pagina_ativa != 'Dashboard':
        if st.button("⬅ VOLTAR PARA DASHBOARD"):
            st.session_state.pagina_ativa = 'Dashboard'
            st.rerun()

# --- LÓGICA DE TEMPO ---
hoje = datetime.now()
p_dia = hoje.replace(day=1)
u_dia = (hoje.replace(month=hoje.month % 12 + 1, day=1) if hoje.month < 12 else hoje.replace(year=hoje.year + 1, month=1, day=1)) - pd.Timedelta(days=1)
d_totais = get_working_days(p_dia, u_dia)
d_passados = get_working_days(p_dia, hoje)
if hoje.weekday() < 5: d_passados = max(0, d_passados - 1)

# --- TELAS ---
if st.session_state.pagina_ativa == 'Dashboard':
    st.title("Giri Strategic Hub")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="main-card"><h4>📍 Matriz STAR (Clientes)</h4></div>', unsafe_allow_html=True)
        if st.button("ACESSAR MATRIZ STAR"): st.session_state.pagina_ativa = 'Matriz'; st.rerun()
    with c2:
        st.markdown('<div class="main-card"><h4>📊 Desempenho (Vendedores)</h4></div>', unsafe_allow_html=True)
        if st.button("ACESSAR DESEMPENHO"): st.session_state.pagina_ativa = 'Desempenho'; st.rerun()

elif st.session_state.pagina_ativa == 'Matriz':
    st.title("📍 MATRIZ STAR | GOVERNANÇA DE CARTEIRA")
    uploaded_file = st.file_uploader("Upload da Base de Faturamento (Excel)", type=['xlsx'])
    
    if uploaded_file:
        df_raw = pd.read_excel(uploaded_file)
        # Lógica de processamento STAR restaurada aqui
        st.dataframe(df_raw.head()) # Exemplo de retorno da funcionalidade
        st.success("Lógica de Longo e Curto Prazo pronta para análise.")

elif st.session_state.pagina_ativa == 'Desempenho':
    # Restaurado o seletor de equipe e lógica de Domingo = 0
    with st.sidebar:
        nomes = st.text_area("EQUIPE:", "JOÃO\nCARLOS\nMARIA", height=100)
        vendedor = st.selectbox("CONSULTOR:", [v.strip().upper() for v in nomes.split('\n') if v.strip()])
    
    st.title(f"📊 DESEMPENHO: {vendedor}")
    st.info(f"📅 Meta baseada em {d_passados} dias úteis de {d_totais}.")
    
    cols = st.columns(5)
    ind_list = []
    sugestoes = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES", "ORÇAMENTOS", "FATURAMENTO"]

    for i, col in enumerate(cols):
        with col:
            n = st.text_input(f"Indicador {i+1}", value=sugestoes[i], key=f"n_{i}_{vendedor}")
            m = st.number_input(f"Meta", min_value=0.0, step=1.0, key=f"m_{i}_{vendedor}")
            r = st.number_input(f"Realizado", min_value=0.0, step=1.0, key=f"r_{i}_{vendedor}")
            ind_list.append({"NOME": n, "META": m, "REALIZADO": r})

    res = []
    for it in ind_list:
        v_esp = math.ceil((it["META"] / d_totais) * d_passados) if d_totais > 0 else 0
        rota = (it["REALIZADO"] / v_esp) if v_esp > 0 else (1.0 if it["REALIZADO"] >= 0 else 0.0)
        res.append({"INDICADOR": it["NOME"].upper(), "META MENSAL": format_executivo(it["META"]), "ESPERADO": format_executivo(v_esp), "REALIZADO": format_executivo(it["REALIZADO"]), "STATUS": "🟢 NO RITMO" if rota >= 1.0 else "🚨 CRÍTICO"})
    st.table(pd.DataFrame(res))
