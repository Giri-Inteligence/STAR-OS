import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import math

# 1. DESIGN EXECUTIVO GIRI - CONTROLE DE LARGURA E MENU MINIMALISTA
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #001220 0%, #002d4a 100%); color: #ffffff; }
    
    /* REDUÇÃO DRÁSTICA DO MENU LATERAL */
    [data-testid="stSidebar"] {
        min-width: 220px !important;
        max-width: 220px !important;
    }
    
    .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 12px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* TABELA: AJUSTE PARA CABER TUDO SEM BARRA DE ROLAGEM */
    div[data-testid="stTable"] table { width: 100% !important; table-layout: fixed !important; }
    
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { 
        text-align: center !important; 
        vertical-align: middle !important; 
        font-size: 13px !important;
        padding: 8px 5px !important;
        white-space: nowrap !important;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Distribuição de larguras para evitar cortes */
    div[data-testid="stTable"] th:nth-child(1), div[data-testid="stTable"] td:nth-child(1) { width: 25% !important; text-align: left !important; } /* Indicador */
    div[data-testid="stTable"] th:nth-child(2), div[data-testid="stTable"] td:nth-child(2) { width: 12% !important; } /* Meta */
    div[data-testid="stTable"] th:nth-child(3), div[data-testid="stTable"] td:nth-child(3) { width: 12% !important; } /* Esperado */
    div[data-testid="stTable"] th:nth-child(4), div[data-testid="stTable"] td:nth-child(4) { width: 12% !important; } /* Realizado */
    div[data-testid="stTable"] th:nth-child(5), div[data-testid="stTable"] td:nth-child(5) { width: 12% !important; } /* Rota */
    div[data-testid="stTable"] th:nth-child(6), div[data-testid="stTable"] td:nth-child(6) { width: 12% !important; } /* Projeção */
    div[data-testid="stTable"] th:nth-child(7), div[data-testid="stTable"] td:nth-child(7) { width: 15% !important; } /* Status */

    div[data-testid="stTable"] th { font-weight: bold !important; border-bottom: 2px solid rgba(255,255,255,0.1) !important; }

    /* INPUTS COMPACTOS */
    .stTextInput input, .stNumberInput input {
        height: 35px !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        font-size: 13px !important;
    }
    
    /* BOTÃO VOLTAR PERSONALIZADO */
    .stButton button {
        width: 100% !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DA NAVEGAÇÃO ---
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = 'Dashboard'

# --- FUNÇÕES DE APOIO ---
def format_executivo(val):
    if pd.isna(val) or val == 0: return "0"
    return f"{int(val):,}".replace(",", ".")

def get_working_days(start_date, end_date):
    days = pd.date_range(start_date, end_date)
    return len(days[days.dayofweek < 5])

# --- LÓGICA DE NAVEGAÇÃO LATERAL (MENU MINIMALISTA) ---
with st.sidebar:
    st.markdown("## GIRI | ARCHITECTURE")
    st.markdown("---")
    if st.session_state.pagina_ativa != 'Dashboard':
        if st.button("⬅ VOLTAR PARA DASHBOARD"):
            st.session_state.pagina_ativa = 'Dashboard'
            st.rerun()
    
    if st.session_state.pagina_ativa == 'Desempenho':
        st.markdown("---")
        nomes_raw = st.text_area("EQUIPE:", "MÁRIO\nJOÃO\nCARLOS", height=100)
        equipe = [v.strip().upper() for v in nomes_raw.split('\n') if v.strip()]
        vendedor_selecionado = st.selectbox("CONSULTOR:", equipe)

# --- TELA: DASHBOARD INICIAL ---
if st.session_state.pagina_ativa == 'Dashboard':
    st.title("Giri Strategic Hub")
    st.markdown("### Selecione a ferramenta de governança:")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="main-card"><h4>📍 Matriz STAR</h4>Análise de carteira por cliente.</div>', unsafe_allow_html=True)
        if st.button("ACESSAR MATRIZ STAR"):
            st.session_state.pagina_ativa = 'Matriz'
            st.rerun()
    with c2:
        st.markdown('<div class="main-card"><h4>📊 Desempenho Individual</h4>Governança de ritmo e meta.</div>', unsafe_allow_html=True)
        if st.button("ACESSAR DESEMPENHO"):
            st.session_state.pagina_ativa = 'Desempenho'
            st.rerun()

# --- TELA: MATRIZ STAR ---
elif st.session_state.pagina_ativa == 'Matriz':
    st.title("Matriz STAR-OS | Carteira")
    st.info("Módulo de Clientes em desenvolvimento com base no seu padrão STAR.")

# --- TELA: DESEMPENHO INDIVIDUAL ---
elif st.session_state.pagina_ativa == 'Desempenho':
    st.title(f"GOVERNANÇA: {vendedor_selecionado}")
    
    hoje = datetime.now()
    p_dia = hoje.replace(day=1)
    if hoje.month == 12: u_dia = hoje.replace(day=31)
    else: u_dia = (hoje.replace(month=hoje.month+1, day=1) - pd.Timedelta(days=1))
    
    d_uteis_totais = get_working_days(p_dia, u_dia)
    d_uteis_hoje = get_working_days(p_dia, hoje)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.info(f"📅 Mês: {hoje.strftime('%m/%Y')} | Dias Úteis: {d_uteis_totais} (Hoje: {d_uteis_hoje})")
    
    indicadores = []
    cols = st.columns(5)
    default_inds = ["CLIENTES ATIVOS", "CLIENTES REATIVADOS", "NOVOS CLIENTES COM VENDA", "ORÇAMENTOS GERADOS", "FATURAMENTO"]

    for i, col in enumerate(cols):
        with col:
            n = st.text_input(f"Indicador {i+1}", value=default_inds[i], key=f"n_{i}_{vendedor_selecionado}")
            m = st.number_input(f"Meta", min_value=0.0, step=1.0, format="%.0f", key=f"m_{i}_{vendedor_selecionado}")
            r = st.number_input(f"Realizado", min_value=0.0, step=1.0, format="%.0f", key=f"r_{i}_{vendedor_selecionado}")
            indicadores.append({"NOME": n, "META": m, "REALIZADO": r})
    st.markdown('</div>', unsafe_allow_html=True)

    # DIAGNÓSTICO
    resultados = []
    for item in indicadores:
        v_esp = math.ceil((item["META"] / d_uteis_totais) * d_uteis_hoje) if d_uteis_totais > 0 else 0
        rota = (item["REALIZADO"] / v_esp) if v_esp > 0 else 0
        tend = math.ceil((item["REALIZADO"] / d_uteis_hoje) * d_uteis_totais) if d_uteis_hoje > 0 else 0
        status = "🟢 NO RITMO" if rota >= 1.0 else "🟡 ATENÇÃO" if rota >= 0.85 else "🚨 CRÍTICO"
        
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
