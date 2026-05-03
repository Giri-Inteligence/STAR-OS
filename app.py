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
    
    /* Centralização da Tabela */
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { 
        text-align: center !important; 
        vertical-align: middle !important; 
    }

    /* AMPLIAÇÃO DOS RETÂNGULOS DOS INDICADORES */
    /* Criamos uma classe específica para garantir que apenas estes campos sejam afetados */
    div.stTextInput > div > div > input {
        text-align: center !important;
        font-weight: bold !important;
    }

    /* Alvo: Inputs de texto dentro das colunas de indicadores */
    [data-testid="column"] .stTextInput input {
        height: 120px !important; /* Altura máxima para 3 linhas de texto */
        font-size: 16px !important;
        line-height: 1.3 !important;
        white-space: normal !important;
        word-break: break-word !important;
        padding: 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Reset para o Nome do Vendedor (fora das colunas) */
    .main-card > div > div > .stTextInput input {
        height: 45px !important;
        text-align: left !important;
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

# --- INTERFACE ---
st.sidebar.markdown("## GIRI | ARCHITECTURE")
menu = st.sidebar.radio("CENTRO DE COMANDO", ["Dashboard Inicial", "Matriz STAR (Clientes)", "Desempenho (Vendedores)"])

if menu == "Desempenho (Vendedores)":
    st.title("GOVERNANÇA DE DESEMPENHO | STAR-OS")
    
    hoje = datetime.now()
    d_totais = get_working_days(hoje.replace(day=1), hoje) # Exemplo simplificado
    d_hoje = get_working_days(hoje.replace(day=1), hoje)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 1. CONFIGURAÇÃO DA RÉGUA COMERCIAL")
    
    # Campo Vendedor (Padrão)
    vendedor_nome = st.text_input("Nome do Vendedor", placeholder="Digite o nome...")
    
    st.write("Defina os 5 indicadores estratégicos:")
    ind_list = []
    cols = st.columns(5)
    sugestoes = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES COM VENDA", "ORÇAMENTOS GERADOS", "FATURAMENTO"]

    for i, col in enumerate(cols):
        with col:
            # Inputs com altura de 120px via CSS
            nome_i = st.text_input(f"Indicador {i+1}", value=sugestoes[i], key=f"n_{i}")
            meta_i = st.number_input(f"Meta {i+1}", min_value=0.0, step=1.0, format="%.0f", key=f"m_{i}")
            real_i = st.number_input(f"Realizado {i+1}", min_value=0.0, step=1.0, format="%.0f", key=f"r_{i}")
            ind_list.append({"NOME": nome_i, "META": meta_i, "REALIZADO": real_i})
    st.markdown('</div>', unsafe_allow_html=True)

    if vendedor_nome:
        st.markdown(f"### 2. ANÁLISE DE DESEMPENHO: {vendedor_nome.upper()}")
        # ... lógica de cálculo permanece ...
        res_list = []
        for it in ind_list:
            esp = math.ceil((it["META"] / 21) * 1) # Exemplo estático para visualização
            rot = (it["REALIZADO"] / esp) if esp > 0 else 0
            res_list.append({
                "INDICADOR": it["NOME"].upper(),
                "META MENSAL": format_executivo(it["META"]),
                "ESPERADO HOJE": format_executivo(esp),
                "REALIZADO": format_executivo(it["REALIZADO"]),
                "ROTA": f"{round(rot * 100, 1)}%",
                "STATUS": "🟢" if rot >= 1 else "🚨"
            })
        st.table(pd.DataFrame(res_list))
