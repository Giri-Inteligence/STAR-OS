import streamlit as st
import pandas as pd
import xlsxwriter
from io import BytesIO

# CONFIGURAÇÃO DE DESIGN EXECUTIVO
st.set_page_config(page_title="Giri Strategic Hub", layout="wide")

# CSS PREMIUM: GRADIENTES NAVY E GLASSMORPHISM
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #001220 0%, #002d4a 100%);
        color: #ffffff;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .main-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
    }
    h1, h2, h3 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## GIRI | INTELLIGENCE")
    st.markdown("---")
    dim_vendedor = st.selectbox("👤 Vendedor", ["Nenhum"] + ["Detectar Automático"])
    dim_segmento = st.selectbox("🏢 Segmento", ["Nenhum"] + ["Detectar Automático"])
    st.markdown("---")
    lp_val = st.number_input("Meses Longo Prazo", value=12)
    cp_val = st.number_input("Meses Curto Prazo", value=3)

st.title("STAR-OS | ENGINE DE GOVERNANÇA")
st.markdown("#### Arquitetura de Sistemas Comerciais para Empresas em Crescimento")

st.markdown('<div class="main-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload da Planilha Bruta ou Consolidada", type=['xlsx', 'csv'])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
    cols = df.columns.tolist()
    
    # Filtro dinâmico de colunas de faturamento
    colunas_valor = [c for c in cols if any(m in c.upper() for m in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ', 'TOTAL'])]
    
    if colunas_valor:
        # BLINDAGEM DE DADOS: Conversão forçada para numérico para evitar TypeError
        for col in colunas_valor:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        st.info(f"Análise baseada em {len(colunas_valor)} períodos de faturamento.")
        
        # CÁLCULO SEGURO DAS MÉDIAS
        df['MEDIA_LP'] = df[colunas_valor].sum(axis=1, numeric_only=True) / lp_val
        df['MEDIA_CP'] = df[colunas_valor[-3:]].sum(axis=1, numeric_only=True) / cp_val
        
        def status_star(row):
            if row['MEDIA_CP'] == 0: return "🔴 INATIVO"
            if row['MEDIA_CP'] > (row['MEDIA_LP'] * 1.15): return "🟢 CRESCIMENTO"
            if row['MEDIA_CP'] < (row['MEDIA_LP'] * 0.85): return "🟡 QUEDA"
            return "🔵 ESTÁVEL"
        
        df['STATUS_STAR'] = df.apply(status_star, axis=1)

        # KPIs EXECUTIVOS
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Total Clientes", len(df))
        with c2: st.metric("Em Queda", len(df[df['STATUS_STAR'] == "🟡 QUEDA"]))
        with c3: st.metric("Inativos", len(df[df['STATUS_STAR'] == "🔴 INATIVO"]))

        st.markdown("---")
        st.subheader("Matriz de Governança")
        st.dataframe(df.style.format({"MEDIA_LP": "R$ {:.2f}", "MEDIA_CP": "R$ {:.2f}"}), use_container_width=True)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='DIAGNOSTICO_STAR')
        
        st.download_button("📥 BAIXAR RELATÓRIO ESTRUTURADO", output.getvalue(), "Relatorio_STAR_Giri.xlsx")
