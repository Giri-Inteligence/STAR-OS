import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import math

# 1. DESIGN EXECUTIVO GIRI
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
    .stTextInput input {
        height: 38px !important;
        text-align: center !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        font-size: 14px !important;
        color: #ffffff !important;
    }
    .title-center { text-align: center; text-transform: uppercase; letter-spacing: 5px; margin-top: 20px; font-weight: 800; font-size: 1.8rem; }
    .subtitle-center { text-align: center; text-transform: uppercase; letter-spacing: 2px; color: rgba(255, 255, 255, 0.6); margin-bottom: 40px; font-size: 1rem; }
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

def get_business_days(start, end):
    # Lista básica de feriados nacionais 2026 (Exemplo: 01/01, 01/05)
    holidays = ['2026-01-01', '2026-05-01', '2026-09-07', '2026-10-12', '2026-11-02', '2026-11-15', '2026-12-25']
    if start > end: return 0
    days = pd.date_range(start, end)
    # Filtra finais de semana E feriados
    business_days = [d for d in days if d.dayofweek < 5 and d.strftime('%Y-%m-%d') not in holidays]
    return len(business_days)

# --- LÓGICA DE TEMPO ---
hoje = datetime.now()
p_dia = hoje.replace(day=1)
u_dia = (hoje.replace(month=hoje.month % 12 + 1, day=1) if hoje.month < 12 else hoje.replace(year=hoje.year + 1, month=1, day=1)) - pd.Timedelta(days=1)

# Cálculo Rigoroso
d_totais = get_business_days(p_dia, u_dia)
d_passados = get_business_days(p_dia, hoje)

# Se hoje for um dia de trabalho em curso, subtraímos 1 para refletir dias ENCERRADOS
# Se hoje for final de semana ou feriado, d_passados já reflete corretamente os dias úteis passados
if hoje.dayofweek < 5 and hoje.strftime('%Y-%m-%d') not in ['2026-05-01']:
    d_passados = max(0, d_passados - 1)

# --- TELA DESEMPENHO ---
if st.session_state.get('pagina_ativa') == 'Desempenho':
    meses_br = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
    competencia = f"{meses_br[hoje.month]} / {hoje.year}"
    
    st.markdown(f'<div class="title-center">MATRIZ DE DESEMPENHO</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle-center">COMPETÊNCIA: {competencia.upper()}</div>', unsafe_allow_html=True)
    
    st.info(f"📅 Meta baseada em **{d_passados}** dias úteis passados de **{d_totais}**.")
    # ... Restante da lógica de inputs e tabela permanece idêntica ...
