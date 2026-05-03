import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import math

# 1. DESIGN EXECUTIVO GIRI - REFINADO E COMPACTO
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001220 0%, #002d4a 100%); color: #ffffff; }
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 12px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* TABELA: CENTRALIZAÇÃO E AJUSTE DE LARGURA DA COLUNA STATUS */
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { 
        text-align: center !important; 
        vertical-align: middle !important; 
        font-size: 14px !important;
        padding: 10px !important;
        white-space: nowrap !important; /* Força linha única nas colunas numéricas */
    }
    
    /* Aumenta especificamente a largura da última coluna (Status) para caber em linha única */
    div[data-testid="stTable"] td:last-child, div[data-testid="stTable"] th:last-child {
        min-width: 200px !important;
        white-space: normal !important;
    }

    div[data-testid="stTable"] th { font-weight: bold !important; border-bottom: 2px solid rgba(255,255,255,0.1) !important; }

    /* INPUTS COMPACTOS: UMA LINHA APENAS */
    .stTextInput input, .stNumberInput input {
        height: 38px !important;
        text-align: center !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 6px !important;
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def format_executivo(val):
    if pd.isna(val) or val == 0: return "0"
    return f"{int(val):,}".replace(",", ".")

def get_working_days(start_date, end_date):
    days = pd.date_range(start_date, end_date)
    return len(days[days.dayofweek < 5])

# --- NAVEGAÇÃO ---
st.sidebar.markdown("## GIRI | ARCHITECTURE")
menu = st.sidebar.radio("CENTRO DE COMANDO", ["Dashboard Inicial", "Matriz STAR (Clientes)", "Desempenho (Vendedores)"])

if menu == "Desempenho (Vendedores)":
    st.title("GOVERNANÇA DE PERFORMANCE")
    
    hoje = datetime.now()
    p_dia = hoje.replace(day=1)
    if hoje.month == 12: u_dia = hoje.replace(day=31)
    else: u_dia = (hoje.replace(month=hoje.month+1, day=1) - pd.Timedelta(days=1))
    
    d_uteis_totais = get_working_days(p_dia, u_dia)
    d_uteis_hoje = get_working_days(p_dia, hoje)

    # PERSISTÊNCIA DE EQUIPE (SESSION STATE)
    st.sidebar.markdown("---")
    nomes_raw = st.sidebar.text_area("EQUIPE (UM POR LINHA):", "MÁRIO\nJOÃO\nCARLOS")
    equipe = [v.strip().upper() for v in nomes_raw.split('\n') if v.strip()]
    vendedor = st.sidebar.selectbox("SELECIONAR CONSULTOR", equipe)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"### CONFIGURAÇÃO: {vendedor}")
    st.info(f"📅 Mês: {hoje.strftime('%m/%Y')} | Dias Úteis: {d_uteis_totais} (Transcorridos: {d_uteis_hoje})")
    
    indicadores = []
    cols = st.columns(5)
    default_inds = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES", "ORÇAMENTOS", "FATURAMENTO"]

    for i, col in enumerate(cols):
        with col:
            # Inputs Compactos com chaves de sessão por vendedor
            n = st.text_input(f"Indicador {i+1}", value=default_inds[i], key=f"n_{i}_{vendedor}")
            m = st.number_input(f"Meta", min_value=0.0, step=1.0, format="%.0f", key=f"m_{i}_{vendedor}")
            r = st.number_input(f"Realizado", min_value=0.0, step=1.0, format="%.0f", key=f"r_{i}_{vendedor}")
            indicadores.append({"NOME": n, "META": m, "REALIZADO": r})
    st.markdown('</div>', unsafe_allow_html=True)

    # ANÁLISE DE DESEMPENHO
    st.markdown(f"### DIAGNÓSTICO DE PERFORMANCE: {vendedor}")
    resultados = []
    for item in indicadores:
        # Matemática STAR: Arredondamento para cima e Rota
        v_esperado = math.ceil((item["META"] / d_uteis_totais) * d_uteis_hoje) if d_uteis_totais > 0 else 0
        rota = (item["REALIZADO"] / v_esperado) if v_esperado > 0 else 0
        tendencia = math.ceil((item["REALIZADO"] / d_uteis_hoje) * d_uteis_totais) if d_uteis_hoje > 0 else 0
        
        status = "🟢 NO RITMO" if rota >= 1.0 else "🟡 ATENÇÃO" if rota >= 0.85 else "🚨 CRÍTICO"
        
        resultados.append({
            "INDICADOR": item["NOME"].upper(),
            "META MENSAL": format_executivo(item["META"]),
            "ESPERADO HOJE": format_executivo(v_esperado),
            "REALIZADO": format_executivo(item["REALIZADO"]),
            "EFICIÊNCIA (ROTA)": f"{round(rota * 100, 1)}%",
            "PROJEÇÃO FINAL": format_executivo(tendencia),
            "STATUS": status
        })
    
    st.table(pd.DataFrame(resultados))
