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
    
    /* Centralização da Tabela de Desempenho */
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { 
        text-align: center !important; 
        vertical-align: middle !important; 
        font-size: 16px !important;
    }

    /* ALTURA DE 240PX EXCLUSIVA PARA OS TÍTULOS DOS INDICADORES */
    [data-testid="column"] .stTextInput input {
        height: 240px !important; 
        font-size: 20px !important;
        font-weight: bold !important;
        text-align: center !important;
        white-space: normal !important;
        word-break: break-word !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1.4 !important;
        padding: 20px !important;
    }

    /* MANUTENÇÃO DA ALTURA PADRÃO PARA O NOME DO VENDEDOR */
    .main-card > div > div > .stTextInput input {
        height: 45px !important;
        text-align: left !important;
        font-size: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def format_executivo(val):
    if pd.isna(val) or val == 0: return "-"
    return f"{int(val):,}".replace(",", ".")

def get_working_days(start_date, end_date):
    days = pd.date_range(start_date, end_date)
    return len(days[days.dayofweek < 5])

# --- INTERFACE DE NAVEGAÇÃO ---
st.sidebar.markdown("## GIRI | ARCHITECTURE")
menu = st.sidebar.radio("CENTRO DE COMANDO", ["Dashboard Inicial", "Matriz STAR (Clientes)", "Desempenho (Vendedores)"])

if menu == "Dashboard Inicial":
    st.title("Giri Strategic Hub")
    st.markdown("### Escolha a ferramenta de governança:")
    c1, c2 = st.columns(2)
    with c1: st.markdown('<div class="main-card"><h4>📍 Matriz STAR</h4>Análise de faturamento por cliente.</div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="main-card"><h4>📊 Desempenho</h4>Governança de ritmo individual.</div>', unsafe_allow_html=True)

elif menu == "Matriz STAR (Clientes)":
    st.title("Matriz STAR-OS | Gestão de Carteira")
    st.info("Módulo de Clientes Ativo.")

elif menu == "Desempenho (Vendedores)":
    st.title("GOVERNANÇA DE DESEMPENHO | STAR-OS")
    
    hoje = datetime.now()
    primeiro_dia = hoje.replace(day=1)
    if hoje.month == 12: ultimo_dia = hoje.replace(day=31)
    else: ultimo_dia = (hoje.replace(month=hoje.month+1, day=1) - pd.Timedelta(days=1))
    
    d_uteis_totais = get_working_days(primeiro_dia, ultimo_dia)
    d_uteis_hoje = get_working_days(primeiro_dia, hoje)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 1. CONFIGURAÇÃO DA RÉGUA COMERCIAL")
    
    vendedor_nome = st.text_input("Nome do Vendedor", placeholder="Digite o nome do consultor...")
    st.metric("Dias Úteis (Mês / Hoje)", f"{d_uteis_totais} / {d_uteis_hoje}")
    
    st.write("Defina os 5 indicadores estratégicos e suas metas:")
    ind_list = []
    
    c1, c2, c3, c4, c5 = st.columns(5)
    cols_ind = [c1, c2, c3, c4, c5]
    sugestoes = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES COM VENDA", "ORÇAMENTOS GERADOS", "FATURAMENTO"]

    for i, col in enumerate(cols_ind):
        with col:
            nome_i = st.text_input(f"Indicador {i+1}", value=sugestoes[i], key=f"n_{i}")
            meta_i = st.number_input(f"Meta {i+1}", min_value=0.0, step=1.0, format="%.0f", key=f"m_{i}")
            real_i = st.number_input(f"Realizado {i+1}", min_value=0.0, step=1.0, format="%.0f", key=f"r_{i}")
            ind_list.append({"NOME": nome_i, "META": meta_i, "REALIZADO": real_i})
    st.markdown('</div>', unsafe_allow_html=True)

    if vendedor_nome:
        st.markdown(f"### 2. ANÁLISE DE DESEMPENHO: {vendedor_nome.upper()}")
        resultados = []
        for item in ind_list:
            v_esperado = math.ceil((item["META"] / d_uteis_totais) * d_uteis_hoje)
            rota_raw = (item["REALIZADO"] / v_esperado) if v_esperado > 0 else 0
            tendencia = math.ceil((item["REALIZADO"] / d_uteis_hoje) * d_uteis_totais) if d_uteis_hoje > 0 else 0
            
            status = "🟢 NO RITMO" if rota_raw >= 1.0 else "🟡 ATENÇÃO" if rota_raw >= 0.85 else "🚨 CRÍTICO"
            
            resultados.append({
                "INDICADOR": item["NOME"].upper(),
                "META MENSAL": format_executivo(item["META"]),
                "ESPERADO HOJE": format_executivo(v_esperado),
                "REALIZADO": format_executivo(item["REALIZADO"]),
                "ROTA": f"{round(rota_raw * 100, 1)}%",
                "TENDÊNCIA": format_executivo(tendencia),
                "STATUS": status
            })
        
        st.table(pd.DataFrame(resultados))
