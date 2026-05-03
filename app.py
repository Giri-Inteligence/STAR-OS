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
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 15px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    
    /* Centralização da Tabela de Análise */
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { 
        text-align: center !important; 
        vertical-align: middle !important; 
        font-size: 16px !important;
    }
    div[data-testid="stTable"] th { font-weight: bold !important; text-transform: uppercase; }

    /* Indicadores: 120px de altura */
    [data-testid="column"] .stTextInput input {
        height: 120px !important; 
        font-size: 18px !important;
        font-weight: bold !important;
        text-align: center !important;
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

# --- INTERFACE DE NAVEGAÇÃO ---
st.sidebar.markdown("## GIRI | ARCHITECTURE")
menu = st.sidebar.radio("CENTRO DE COMANDO", ["Dashboard Inicial", "Matriz STAR (Clientes)", "Desempenho (Vendedores)"])

if menu == "Desempenho (Vendedores)":
    st.title("GOVERNANÇA DE DESEMPENHO | STAR-OS")
    
    # Gerenciamento de Tempo
    hoje = datetime.now()
    p_dia = hoje.replace(day=1)
    if hoje.month == 12: u_dia = hoje.replace(day=31)
    else: u_dia = (hoje.replace(month=hoje.month+1, day=1) - pd.Timedelta(days=1))
    d_uteis_totais = get_working_days(p_dia, u_dia)
    d_uteis_hoje = get_working_days(p_dia, hoje)

    # CADASTRO DA EQUIPE
    st.sidebar.markdown("---")
    st.sidebar.subheader("👥 GESTÃO DE EQUIPE")
    lista_vendedores = st.sidebar.text_area("Liste os nomes (um por linha):", "JOÃO\nMARIA\nCARLOS").split('\n')
    vendedor_ativo = st.sidebar.selectbox("VENDEDOR EM ANÁLISE", [v.strip() for v in lista_vendedores if v.strip()])

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"### 1. MÉTRICAS DE: {vendedor_ativo.upper()}")
    
    col_t = st.columns(1)[0]
    col_t.metric("Dias Úteis (Mês / Hoje)", f"{d_uteis_totais} / {d_uteis_hoje}")
    
    st.write("Ajuste as metas e realizados para este consultor:")
    ind_list = []
    c1, c2, c3, c4, c5 = st.columns(5)
    sugestoes = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES COM VENDA", "ORÇAMENTOS GERADOS", "FATURAMENTO"]

    for i, col in enumerate([c1, c2, c3, c4, c5]):
        with col:
            # Chaves únicas baseadas no vendedor ativo para não misturar os dados
            n = st.text_input(f"Indicador {i+1}", value=sugestoes[i], key=f"n_{i}_{vendedor_ativo}")
            m = st.number_input(f"Meta {i+1}", min_value=0.0, step=1.0, format="%.0f", key=f"m_{i}_{vendedor_ativo}")
            r = st.number_input(f"Realizado {i+1}", min_value=0.0, step=1.0, format="%.0f", key=f"r_{i}_{vendedor_ativo}")
            ind_list.append({"NOME": n, "META": m, "REALIZADO": r})
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. ANÁLISE DE DESEMPENHO
    st.markdown(f"### 2. DIAGNÓSTICO DE PERFORMANCE: {vendedor_ativo.upper()}")
    resultados = []
    for item in ind_list:
        v_esperado = math.ceil((item["META"] / d_uteis_totais) * d_uteis_hoje)
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
